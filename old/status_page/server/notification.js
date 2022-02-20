const { R } = require("redbean-node");
const Apprise = require("./notification-providers/apprise");
const Discord = require("./notification-providers/discord");
const Gotify = require("./notification-providers/gotify");
const Line = require("./notification-providers/line");
const LunaSea = require("./notification-providers/lunasea");
const Mattermost = require("./notification-providers/mattermost");
const Matrix = require("./notification-providers/matrix");
const Octopush = require("./notification-providers/octopush");
const PromoSMS = require("./notification-providers/promosms");
const Pushbullet = require("./notification-providers/pushbullet");
const Pushover = require("./notification-providers/pushover");
const Pushy = require("./notification-providers/pushy");
const RocketChat = require("./notification-providers/rocket-chat");
const Signal = require("./notification-providers/signal");
const Slack = require("./notification-providers/slack");
const SMTP = require("./notification-providers/smtp");
const Teams = require("./notification-providers/teams");
const Telegram = require("./notification-providers/telegram");
const Webhook = require("./notification-providers/webhook");
const Feishu = require("./notification-providers/feishu");

class Notification {

    providerList = {};

    static init() {
        console.log("Prepare Notification Providers");

        this.providerList = {};

        const list = [
            new Apprise(),
            new Discord(),
            new Teams(),
            new Gotify(),
            new Line(),
            new LunaSea(),
            new Feishu(),
            new Mattermost(),
            new Matrix(),
            new Octopush(),
            new PromoSMS(),
            new Pushbullet(),
            new Pushover(),
            new Pushy(),
            new RocketChat(),
            new Signal(),
            new Slack(),
            new SMTP(),
            new Telegram(),
            new Webhook(),
        ];

        for (let item of list) {
            if (! item.name) {
                throw new Error("Notification provider without name");
            }

            if (this.providerList[item.name]) {
                throw new Error("Duplicate notification provider name");
            }
            this.providerList[item.name] = item;
        }
    }

    /**
     *
     * @param notification : BeanModel
     * @param msg : string General Message
     * @param monitorJSON : object Monitor details (For Up/Down only)
     * @param heartbeatJSON : object Heartbeat details (For Up/Down only)
     * @returns {Promise<string>} Successful msg
     * Throw Error with fail msg
     */
    static async send(notification, msg, monitorJSON = null, heartbeatJSON = null) {
        if (this.providerList[notification.type]) {
            return this.providerList[notification.type].send(notification, msg, monitorJSON, heartbeatJSON);
        } else {
            throw new Error("Notification type is not supported");
        }
    }

    static async save(notification, notificationID, userID) {
        let bean

        if (notificationID) {
            bean = await R.findOne("notification", " id = ? AND user_id = ? ", [
                notificationID,
                userID,
            ])

            if (! bean) {
                throw new Error("notification not found")
            }

        } else {
            bean = R.dispense("notification")
        }

        bean.name = notification.name;
        bean.user_id = userID;
        bean.config = JSON.stringify(notification);
        bean.is_default = notification.isDefault || false;
        await R.store(bean)

        if (notification.applyExisting) {
            await applyNotificationEveryMonitor(bean.id, userID);
        }

        return bean;
    }

    static async delete(notificationID, userID) {
        let bean = await R.findOne("notification", " id = ? AND user_id = ? ", [
            notificationID,
            userID,
        ])

        if (! bean) {
            throw new Error("notification not found")
        }

        await R.trash(bean)
    }

    static checkApprise() {
        let commandExistsSync = require("command-exists").sync;
        let exists = commandExistsSync("apprise");
        return exists;
    }

}

async function applyNotificationEveryMonitor(notificationID, userID) {
    let monitors = await R.getAll("SELECT id FROM monitor WHERE user_id = ?", [
        userID
    ]);

    for (let i = 0; i < monitors.length; i++) {
        let checkNotification = await R.findOne("monitor_notification", " monitor_id = ? AND notification_id = ? ", [
            monitors[i].id,
            notificationID,
        ])

        if (! checkNotification) {
            let relation = R.dispense("monitor_notification");
            relation.monitor_id = monitors[i].id;
            relation.notification_id = notificationID;
            await R.store(relation)
        }
    }
}

module.exports = {
    Notification,
}
