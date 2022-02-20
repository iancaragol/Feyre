const fs = require("fs");
const { R } = require("redbean-node");
const { setSetting, setting } = require("./util-server");
const { debug, sleep } = require("../src/util");
const dayjs = require("dayjs");
const knex = require("knex");

/**
 * Database & App Data Folder
 */
class Database {

    static templatePath = "./db/kuma.db";

    /**
     * Data Dir (Default: ./data)
     */
    static dataDir;

    /**
     * User Upload Dir (Default: ./data/upload)
     */
    static uploadDir;

    static path;

    /**
     * @type {boolean}
     */
    static patched = false;

    /**
     * For Backup only
     */
    static backupPath = null;

    /**
     * Add patch filename in key
     * Values:
     *      true: Add it regardless of order
     *      false: Do nothing
     *      { parents: []}: Need parents before add it
     */
    static patchList = {
        "patch-setting-value-type.sql": true,
        "patch-improve-performance.sql": true,
        "patch-2fa.sql": true,
        "patch-add-retry-interval-monitor.sql": true,
        "patch-incident-table.sql": true,
        "patch-group-table.sql": true,
        "patch-monitor-push_token.sql": true,
    }

    /**
     * The finally version should be 10 after merged tag feature
     * @deprecated Use patchList for any new feature
     */
    static latestVersion = 10;

    static noReject = true;

    static init(args) {
        // Data Directory (must be end with "/")
        Database.dataDir = process.env.DATA_DIR || args["data-dir"] || "./data/";
        Database.path = Database.dataDir + "kuma.db";
        if (! fs.existsSync(Database.dataDir)) {
            fs.mkdirSync(Database.dataDir, { recursive: true });
        }

        Database.uploadDir = Database.dataDir + "upload/";

        if (! fs.existsSync(Database.uploadDir)) {
            fs.mkdirSync(Database.uploadDir, { recursive: true });
        }

        console.log(`Data Dir: ${Database.dataDir}`);
    }

    static async connect() {
        const acquireConnectionTimeout = 120 * 1000;

        const Dialect = require("knex/lib/dialects/sqlite3/index.js");
        Dialect.prototype._driver = () => require("@louislam/sqlite3");

        const knexInstance = knex({
            client: Dialect,
            connection: {
                filename: Database.path,
                acquireConnectionTimeout: acquireConnectionTimeout,
            },
            useNullAsDefault: true,
            pool: {
                min: 1,
                max: 1,
                idleTimeoutMillis: 120 * 1000,
                propagateCreateError: false,
                acquireTimeoutMillis: acquireConnectionTimeout,
            }
        });

        R.setup(knexInstance);

        if (process.env.SQL_LOG === "1") {
            R.debug(true);
        }

        // Auto map the model to a bean object
        R.freeze(true);
        await R.autoloadModels("./server/model");

        await R.exec("PRAGMA foreign_keys = ON");
        // Change to WAL
        await R.exec("PRAGMA journal_mode = WAL");
        await R.exec("PRAGMA cache_size = -12000");

        console.log("SQLite config:");
        console.log(await R.getAll("PRAGMA journal_mode"));
        console.log(await R.getAll("PRAGMA cache_size"));
        console.log("SQLite Version: " + await R.getCell("SELECT sqlite_version()"));
    }

    static async patch() {
        let version = parseInt(await setting("database_version"));

        if (! version) {
            version = 0;
        }

        console.info("Your database version: " + version);
        console.info("Latest database version: " + this.latestVersion);

        if (version === this.latestVersion) {
            console.info("Database no need to patch");
        } else if (version > this.latestVersion) {
            console.info("Warning: Database version is newer than expected");
        } else {
            console.info("Database patch is needed");

            this.backup(version);

            // Try catch anything here, if gone wrong, restore the backup
            try {
                for (let i = version + 1; i <= this.latestVersion; i++) {
                    const sqlFile = `./db/patch${i}.sql`;
                    console.info(`Patching ${sqlFile}`);
                    await Database.importSQLFile(sqlFile);
                    console.info(`Patched ${sqlFile}`);
                    await setSetting("database_version", i);
                }
            } catch (ex) {
                await Database.close();

                console.error(ex);
                console.error("Start Uptime-Kuma failed due to patch db failed");
                console.error("Please submit the bug report if you still encounter the problem after restart: https://github.com/louislam/uptime-kuma/issues");

                this.restore();
                process.exit(1);
            }
        }

        await this.patch2();
    }

    /**
     * Call it from patch() only
     * @returns {Promise<void>}
     */
    static async patch2() {
        console.log("Database Patch 2.0 Process");
        let databasePatchedFiles = await setting("databasePatchedFiles");

        if (! databasePatchedFiles) {
            databasePatchedFiles = {};
        }

        debug("Patched files:");
        debug(databasePatchedFiles);

        try {
            for (let sqlFilename in this.patchList) {
                await this.patch2Recursion(sqlFilename, databasePatchedFiles);
            }

            if (this.patched) {
                console.log("Database Patched Successfully");
            }

        } catch (ex) {
            await Database.close();

            console.error(ex);
            console.error("Start Uptime-Kuma failed due to patch db failed");
            console.error("Please submit the bug report if you still encounter the problem after restart: https://github.com/louislam/uptime-kuma/issues");

            this.restore();

            process.exit(1);
        }

        await setSetting("databasePatchedFiles", databasePatchedFiles);
    }

    /**
     * Used it patch2() only
     * @param sqlFilename
     * @param databasePatchedFiles
     */
    static async patch2Recursion(sqlFilename, databasePatchedFiles) {
        let value = this.patchList[sqlFilename];

        if (! value) {
            console.log(sqlFilename + " skip");
            return;
        }

        // Check if patched
        if (! databasePatchedFiles[sqlFilename]) {
            console.log(sqlFilename + " is not patched");

            if (value.parents) {
                console.log(sqlFilename + " need parents");
                for (let parentSQLFilename of value.parents) {
                    await this.patch2Recursion(parentSQLFilename, databasePatchedFiles);
                }
            }

            this.backup(dayjs().format("YYYYMMDDHHmmss"));

            console.log(sqlFilename + " is patching");
            this.patched = true;
            await this.importSQLFile("./db/" + sqlFilename);
            databasePatchedFiles[sqlFilename] = true;
            console.log(sqlFilename + " is patched successfully");

        } else {
            debug(sqlFilename + " is already patched, skip");
        }
    }

    /**
     * Sadly, multi sql statements is not supported by many sqlite libraries, I have to implement it myself
     * @param filename
     * @returns {Promise<void>}
     */
    static async importSQLFile(filename) {

        await R.getCell("SELECT 1");

        let text = fs.readFileSync(filename).toString();

        // Remove all comments (--)
        let lines = text.split("\n");
        lines = lines.filter((line) => {
            return ! line.startsWith("--");
        });

        // Split statements by semicolon
        // Filter out empty line
        text = lines.join("\n");

        let statements = text.split(";")
            .map((statement) => {
                return statement.trim();
            })
            .filter((statement) => {
                return statement !== "";
            });

        for (let statement of statements) {
            await R.exec(statement);
        }
    }

    static getBetterSQLite3Database() {
        return R.knex.client.acquireConnection();
    }

    /**
     * Special handle, because tarn.js throw a promise reject that cannot be caught
     * @returns {Promise<void>}
     */
    static async close() {
        const listener = (reason, p) => {
            Database.noReject = false;
        };
        process.addListener("unhandledRejection", listener);

        console.log("Closing DB");

        while (true) {
            Database.noReject = true;
            await R.close();
            await sleep(2000);

            if (Database.noReject) {
                break;
            } else {
                console.log("Waiting to close the db");
            }
        }
        console.log("SQLite closed");

        process.removeListener("unhandledRejection", listener);
    }

    /**
     * One backup one time in this process.
     * Reset this.backupPath if you want to backup again
     * @param version
     */
    static backup(version) {
        if (! this.backupPath) {
            console.info("Backup the db");
            this.backupPath = this.dataDir + "kuma.db.bak" + version;
            fs.copyFileSync(Database.path, this.backupPath);

            const shmPath = Database.path + "-shm";
            if (fs.existsSync(shmPath)) {
                this.backupShmPath = shmPath + ".bak" + version;
                fs.copyFileSync(shmPath, this.backupShmPath);
            }

            const walPath = Database.path + "-wal";
            if (fs.existsSync(walPath)) {
                this.backupWalPath = walPath + ".bak" + version;
                fs.copyFileSync(walPath, this.backupWalPath);
            }
        }
    }

    /**
     *
     */
    static restore() {
        if (this.backupPath) {
            console.error("Patch db failed!!! Restoring the backup");

            const shmPath = Database.path + "-shm";
            const walPath = Database.path + "-wal";

            // Delete patch failed db
            try {
                if (fs.existsSync(Database.path)) {
                    fs.unlinkSync(Database.path);
                }

                if (fs.existsSync(shmPath)) {
                    fs.unlinkSync(shmPath);
                }

                if (fs.existsSync(walPath)) {
                    fs.unlinkSync(walPath);
                }
            } catch (e) {
                console.log("Restore failed, you may need to restore the backup manually");
                process.exit(1);
            }

            // Restore backup
            fs.copyFileSync(this.backupPath, Database.path);

            if (this.backupShmPath) {
                fs.copyFileSync(this.backupShmPath, shmPath);
            }

            if (this.backupWalPath) {
                fs.copyFileSync(this.backupWalPath, walPath);
            }

        } else {
            console.log("Nothing to restore");
        }
    }
}

module.exports = Database;
