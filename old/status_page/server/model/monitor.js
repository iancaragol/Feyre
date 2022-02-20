const https = require("https");
const dayjs = require("dayjs");
const utc = require("dayjs/plugin/utc");
let timezone = require("dayjs/plugin/timezone");
dayjs.extend(utc);
dayjs.extend(timezone);
const axios = require("axios");
const { Prometheus } = require("../prometheus");
const { debug, UP, DOWN, PENDING, flipStatus, TimeLogger } = require("../../src/util");
const { tcping, ping, dnsResolve, checkCertificate, checkStatusCode, getTotalClientInRoom } = require("../util-server");
const { R } = require("redbean-node");
const { BeanModel } = require("redbean-node/dist/bean-model");
const { Notification } = require("../notification");
const { demoMode } = require("../server");
const version = require("../../package.json").version;
const apicache = require("../modules/apicache");

/**
 * status:
 *      0 = DOWN
 *      1 = UP
 *      2 = PENDING
 */
class Monitor extends BeanModel {

    /**
     * Return a object that ready to parse to JSON for public
     * Only show necessary data to public
     */
    async toPublicJSON() {
        return {
            id: this.id,
            name: this.name,
        };
    }

    /**
     * Return a object that ready to parse to JSON
     */
    async toJSON() {

        let notificationIDList = {};

        let list = await R.find("monitor_notification", " monitor_id = ? ", [
            this.id,
        ]);

        for (let bean of list) {
            notificationIDList[bean.notification_id] = true;
        }

        const tags = await R.getAll("SELECT mt.*, tag.name, tag.color FROM monitor_tag mt JOIN tag ON mt.tag_id = tag.id WHERE mt.monitor_id = ?", [this.id]);

        return {
            id: this.id,
            name: this.name,
            url: this.url,
            hostname: this.hostname,
            port: this.port,
            maxretries: this.maxretries,
            weight: this.weight,
            active: this.active,
            type: this.type,
            interval: this.interval,
            retryInterval: this.retryInterval,
            keyword: this.keyword,
            ignoreTls: this.getIgnoreTls(),
            upsideDown: this.isUpsideDown(),
            maxredirects: this.maxredirects,
            accepted_statuscodes: this.getAcceptedStatuscodes(),
            dns_resolve_type: this.dns_resolve_type,
            dns_resolve_server: this.dns_resolve_server,
            dns_last_result: this.dns_last_result,
            pushToken: this.pushToken,
            notificationIDList,
            tags: tags,
        };
    }

    /**
     * Parse to boolean
     * @returns {boolean}
     */
    getIgnoreTls() {
        return Boolean(this.ignoreTls);
    }

    /**
     * Parse to boolean
     * @returns {boolean}
     */
    isUpsideDown() {
        return Boolean(this.upsideDown);
    }

    getAcceptedStatuscodes() {
        return JSON.parse(this.accepted_statuscodes_json);
    }

    start(io) {
        let previousBeat = null;
        let retries = 0;

        let prometheus = new Prometheus(this);

        const beat = async () => {

            // Expose here for prometheus update
            // undefined if not https
            let tlsInfo = undefined;

            if (! previousBeat) {
                previousBeat = await R.findOne("heartbeat", " monitor_id = ? ORDER BY time DESC", [
                    this.id,
                ]);
            }

            const isFirstBeat = !previousBeat;

            let bean = R.dispense("heartbeat");
            bean.monitor_id = this.id;
            bean.time = R.isoDateTime(dayjs.utc());
            bean.status = DOWN;

            if (this.isUpsideDown()) {
                bean.status = flipStatus(bean.status);
            }

            // Duration
            if (! isFirstBeat) {
                bean.duration = dayjs(bean.time).diff(dayjs(previousBeat.time), "second");
            } else {
                bean.duration = 0;
            }

            try {
                if (this.type === "http" || this.type === "keyword") {
                    // Do not do any queries/high loading things before the "bean.ping"
                    let startTime = dayjs().valueOf();

                    let res = await axios.get(this.url, {
                        timeout: this.interval * 1000 * 0.8,
                        headers: {
                            "Accept": "*/*",
                            "User-Agent": "Uptime-Kuma/" + version,
                        },
                        httpsAgent: new https.Agent({
                            maxCachedSessions: 0,      // Use Custom agent to disable session reuse (https://github.com/nodejs/node/issues/3940)
                            rejectUnauthorized: ! this.getIgnoreTls(),
                        }),
                        maxRedirects: this.maxredirects,
                        validateStatus: (status) => {
                            return checkStatusCode(status, this.getAcceptedStatuscodes());
                        },
                    });
                    bean.msg = `${res.status} - ${res.statusText}`;
                    bean.ping = dayjs().valueOf() - startTime;

                    // Check certificate if https is used
                    let certInfoStartTime = dayjs().valueOf();
                    if (this.getUrl()?.protocol === "https:") {
                        try {
                            tlsInfo = await this.updateTlsInfo(checkCertificate(res));
                        } catch (e) {
                            if (e.message !== "No TLS certificate in response") {
                                console.error(e.message);
                            }
                        }
                    }

                    if (process.env.TIMELOGGER === "1") {
                        debug("Cert Info Query Time: " + (dayjs().valueOf() - certInfoStartTime) + "ms");
                    }

                    if (this.type === "http") {
                        bean.status = UP;
                    } else {

                        let data = res.data;

                        // Convert to string for object/array
                        if (typeof data !== "string") {
                            data = JSON.stringify(data);
                        }

                        if (data.includes(this.keyword)) {
                            bean.msg += ", keyword is found";
                            bean.status = UP;
                        } else {
                            throw new Error(bean.msg + ", but keyword is not found");
                        }

                    }

                } else if (this.type === "port") {
                    bean.ping = await tcping(this.hostname, this.port);
                    bean.msg = "";
                    bean.status = UP;

                } else if (this.type === "ping") {
                    bean.ping = await ping(this.hostname);
                    bean.msg = "";
                    bean.status = UP;
                } else if (this.type === "dns") {
                    let startTime = dayjs().valueOf();
                    let dnsMessage = "";

                    let dnsRes = await dnsResolve(this.hostname, this.dns_resolve_server, this.dns_resolve_type);
                    bean.ping = dayjs().valueOf() - startTime;

                    if (this.dns_resolve_type == "A" || this.dns_resolve_type == "AAAA" || this.dns_resolve_type == "TXT") {
                        dnsMessage += "Records: ";
                        dnsMessage += dnsRes.join(" | ");
                    } else if (this.dns_resolve_type == "CNAME" || this.dns_resolve_type == "PTR") {
                        dnsMessage = dnsRes[0];
                    } else if (this.dns_resolve_type == "CAA") {
                        dnsMessage = dnsRes[0].issue;
                    } else if (this.dns_resolve_type == "MX") {
                        dnsRes.forEach(record => {
                            dnsMessage += `Hostname: ${record.exchange} - Priority: ${record.priority} | `;
                        });
                        dnsMessage = dnsMessage.slice(0, -2);
                    } else if (this.dns_resolve_type == "NS") {
                        dnsMessage += "Servers: ";
                        dnsMessage += dnsRes.join(" | ");
                    } else if (this.dns_resolve_type == "SOA") {
                        dnsMessage += `NS-Name: ${dnsRes.nsname} | Hostmaster: ${dnsRes.hostmaster} | Serial: ${dnsRes.serial} | Refresh: ${dnsRes.refresh} | Retry: ${dnsRes.retry} | Expire: ${dnsRes.expire} | MinTTL: ${dnsRes.minttl}`;
                    } else if (this.dns_resolve_type == "SRV") {
                        dnsRes.forEach(record => {
                            dnsMessage += `Name: ${record.name} | Port: ${record.port} | Priority: ${record.priority} | Weight: ${record.weight} | `;
                        });
                        dnsMessage = dnsMessage.slice(0, -2);
                    }

                    if (this.dnsLastResult !== dnsMessage) {
                        R.exec("UPDATE `monitor` SET dns_last_result = ? WHERE id = ? ", [
                            dnsMessage,
                            this.id
                        ]);
                    }

                    bean.msg = dnsMessage;
                    bean.status = UP;
                } else if (this.type === "push") {      // Type: Push
                    const time = R.isoDateTime(dayjs.utc().subtract(this.interval, "second"));

                    let heartbeatCount = await R.count("heartbeat", " monitor_id = ? AND time > ? ", [
                        this.id,
                        time
                    ]);

                    debug("heartbeatCount" + heartbeatCount + " " + time);

                    if (heartbeatCount <= 0) {
                        throw new Error("No heartbeat in the time window");
                    } else {
                        // No need to insert successful heartbeat for push type, so end here
                        retries = 0;
                        this.heartbeatInterval = setTimeout(beat, this.interval * 1000);
                        return;
                    }

                } else {
                    bean.msg = "Unknown Monitor Type";
                    bean.status = PENDING;
                }

                if (this.isUpsideDown()) {
                    bean.status = flipStatus(bean.status);

                    if (bean.status === DOWN) {
                        throw new Error("Flip UP to DOWN");
                    }
                }

                retries = 0;

            } catch (error) {

                bean.msg = error.message;

                // If UP come in here, it must be upside down mode
                // Just reset the retries
                if (this.isUpsideDown() && bean.status === UP) {
                    retries = 0;

                } else if ((this.maxretries > 0) && (retries < this.maxretries)) {
                    retries++;
                    bean.status = PENDING;
                }
            }

            let beatInterval = this.interval;

            // * ? -> ANY STATUS = important [isFirstBeat]
            // UP -> PENDING = not important
            // * UP -> DOWN = important
            // UP -> UP = not important
            // PENDING -> PENDING = not important
            // * PENDING -> DOWN = important
            // PENDING -> UP = not important
            // DOWN -> PENDING = this case not exists
            // DOWN -> DOWN = not important
            // * DOWN -> UP = important
            let isImportant = isFirstBeat ||
                (previousBeat.status === UP && bean.status === DOWN) ||
                (previousBeat.status === DOWN && bean.status === UP) ||
                (previousBeat.status === PENDING && bean.status === DOWN);

            // Mark as important if status changed, ignore pending pings,
            // Don't notify if disrupted changes to up
            if (isImportant) {
                bean.important = true;

                // Send only if the first beat is DOWN
                if (!isFirstBeat || bean.status === DOWN) {
                    let notificationList = await R.getAll("SELECT notification.* FROM notification, monitor_notification WHERE monitor_id = ? AND monitor_notification.notification_id = notification.id ", [
                        this.id,
                    ]);

                    let text;
                    if (bean.status === UP) {
                        text = "✅ Up";
                    } else {
                        text = "🔴 Down";
                    }

                    let msg = `[${this.name}] [${text}] ${bean.msg}`;

                    for (let notification of notificationList) {
                        try {
                            await Notification.send(JSON.parse(notification.config), msg, await this.toJSON(), bean.toJSON());
                        } catch (e) {
                            console.error("Cannot send notification to " + notification.name);
                            console.log(e);
                        }
                    }

                    // Clear Status Page Cache
                    apicache.clear();
                }

            } else {
                bean.important = false;
            }

            if (bean.status === UP) {
                console.info(`Monitor #${this.id} '${this.name}': Successful Response: ${bean.ping} ms | Interval: ${beatInterval} seconds | Type: ${this.type}`);
            } else if (bean.status === PENDING) {
                if (this.retryInterval > 0) {
                    beatInterval = this.retryInterval;
                }
                console.warn(`Monitor #${this.id} '${this.name}': Pending: ${bean.msg} | Max retries: ${this.maxretries} | Retry: ${retries} | Retry Interval: ${beatInterval} seconds | Type: ${this.type}`);
            } else {
                console.warn(`Monitor #${this.id} '${this.name}': Failing: ${bean.msg} | Interval: ${beatInterval} seconds | Type: ${this.type}`);
            }

            io.to(this.user_id).emit("heartbeat", bean.toJSON());
            Monitor.sendStats(io, this.id, this.user_id);

            await R.store(bean);
            prometheus.update(bean, tlsInfo);

            previousBeat = bean;

            if (! this.isStop) {

                if (demoMode) {
                    if (beatInterval < 20) {
                        console.log("beat interval too low, reset to 20s");
                        beatInterval = 20;
                    }
                }

                this.heartbeatInterval = setTimeout(beat, beatInterval * 1000);
            }

        };

        // Delay Push Type
        if (this.type === "push") {
            setTimeout(() => {
                beat();
            }, this.interval * 1000);
        } else {
            beat();
        }
    }

    stop() {
        clearTimeout(this.heartbeatInterval);
        this.isStop = true;
    }

    /**
     * Helper Method:
     * returns URL object for further usage
     * returns null if url is invalid
     * @returns {null|URL}
     */
    getUrl() {
        try {
            return new URL(this.url);
        } catch (_) {
            return null;
        }
    }

    /**
     * Store TLS info to database
     * @param checkCertificateResult
     * @returns {Promise<object>}
     */
    async updateTlsInfo(checkCertificateResult) {
        let tls_info_bean = await R.findOne("monitor_tls_info", "monitor_id = ?", [
            this.id,
        ]);
        if (tls_info_bean == null) {
            tls_info_bean = R.dispense("monitor_tls_info");
            tls_info_bean.monitor_id = this.id;
        }
        tls_info_bean.info_json = JSON.stringify(checkCertificateResult);
        await R.store(tls_info_bean);

        return checkCertificateResult;
    }

    static async sendStats(io, monitorID, userID) {
        const hasClients = getTotalClientInRoom(io, userID) > 0;

        if (hasClients) {
            await Monitor.sendAvgPing(24, io, monitorID, userID);
            await Monitor.sendUptime(24, io, monitorID, userID);
            await Monitor.sendUptime(24 * 30, io, monitorID, userID);
            await Monitor.sendCertInfo(io, monitorID, userID);
        } else {
            debug("No clients in the room, no need to send stats");
        }
    }

    /**
     *
     * @param duration : int Hours
     */
    static async sendAvgPing(duration, io, monitorID, userID) {
        const timeLogger = new TimeLogger();

        let avgPing = parseInt(await R.getCell(`
            SELECT AVG(ping)
            FROM heartbeat
            WHERE time > DATETIME('now', ? || ' hours')
            AND ping IS NOT NULL
            AND monitor_id = ? `, [
            -duration,
            monitorID,
        ]));

        timeLogger.print(`[Monitor: ${monitorID}] avgPing`);

        io.to(userID).emit("avgPing", monitorID, avgPing);
    }

    static async sendCertInfo(io, monitorID, userID) {
        let tls_info = await R.findOne("monitor_tls_info", "monitor_id = ?", [
            monitorID,
        ]);
        if (tls_info != null) {
            io.to(userID).emit("certInfo", monitorID, tls_info.info_json);
        }
    }

    /**
     * Uptime with calculation
     * Calculation based on:
     * https://www.uptrends.com/support/kb/reporting/calculation-of-uptime-and-downtime
     * @param duration : int Hours
     */
    static async calcUptime(duration, monitorID) {
        const timeLogger = new TimeLogger();

        const startTime = R.isoDateTime(dayjs.utc().subtract(duration, "hour"));

        // Handle if heartbeat duration longer than the target duration
        // e.g. If the last beat's duration is bigger that the 24hrs window, it will use the duration between the (beat time - window margin) (THEN case in SQL)
        let result = await R.getRow(`
            SELECT
               -- SUM all duration, also trim off the beat out of time window
                SUM(
                    CASE
                        WHEN (JULIANDAY(\`time\`) - JULIANDAY(?)) * 86400 < duration
                        THEN (JULIANDAY(\`time\`) - JULIANDAY(?)) * 86400
                        ELSE duration
                    END
                ) AS total_duration,

               -- SUM all uptime duration, also trim off the beat out of time window
                SUM(
                    CASE
                        WHEN (status = 1)
                        THEN
                            CASE
                                WHEN (JULIANDAY(\`time\`) - JULIANDAY(?)) * 86400 < duration
                                    THEN (JULIANDAY(\`time\`) - JULIANDAY(?)) * 86400
                                ELSE duration
                            END
                        END
                ) AS uptime_duration
            FROM heartbeat
            WHERE time > ?
            AND monitor_id = ?
        `, [
            startTime, startTime, startTime, startTime, startTime,
            monitorID,
        ]);

        timeLogger.print(`[Monitor: ${monitorID}][${duration}] sendUptime`);

        let totalDuration = result.total_duration;
        let uptimeDuration = result.uptime_duration;
        let uptime = 0;

        if (totalDuration > 0) {
            uptime = uptimeDuration / totalDuration;
            if (uptime < 0) {
                uptime = 0;
            }

        } else {
            // Handle new monitor with only one beat, because the beat's duration = 0
            let status = parseInt(await R.getCell("SELECT `status` FROM heartbeat WHERE monitor_id = ?", [ monitorID ]));

            if (status === UP) {
                uptime = 1;
            }
        }

        return uptime;
    }

    /**
     * Send Uptime
     * @param duration : int Hours
     */
    static async sendUptime(duration, io, monitorID, userID) {
        const uptime = await this.calcUptime(duration, monitorID);
        io.to(userID).emit("uptime", monitorID, duration, uptime);
    }

}

module.exports = Monitor;
