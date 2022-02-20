const NotificationProvider = require("./notification-provider");
const axios = require("axios");

class Pushover extends NotificationProvider {

    name = "pushover";

    async send(notification, msg, monitorJSON = null, heartbeatJSON = null) {
        let okMsg = "Sent Successfully.";
        let pushoverlink = "https://api.pushover.net/1/messages.json"

        try {
            if (heartbeatJSON == null) {
                let data = {
                    "message": "<b>Uptime Kuma Pushover testing successful.</b>",
                    "user": notification.pushoveruserkey,
                    "token": notification.pushoverapptoken,
                    "sound": notification.pushoversounds,
                    "priority": notification.pushoverpriority,
                    "title": notification.pushovertitle,
                    "retry": "30",
                    "expire": "3600",
                    "html": 1,
                }
                await axios.post(pushoverlink, data)
                return okMsg;
            }

            let data = {
                "message": "<b>Uptime Kuma Alert</b>\n\n<b>Message</b>:" + msg + "\n<b>Time (UTC)</b>:" + heartbeatJSON["time"],
                "user": notification.pushoveruserkey,
                "token": notification.pushoverapptoken,
                "sound": notification.pushoversounds,
                "priority": notification.pushoverpriority,
                "title": notification.pushovertitle,
                "retry": "30",
                "expire": "3600",
                "html": 1,
            }
            await axios.post(pushoverlink, data)
            return okMsg;
        } catch (error) {
            this.throwGeneralAxiosError(error)
        }

    }
}

module.exports = Pushover;
