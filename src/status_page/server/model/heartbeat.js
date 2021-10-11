const dayjs = require("dayjs");
const utc = require("dayjs/plugin/utc");
let timezone = require("dayjs/plugin/timezone");
dayjs.extend(utc);
dayjs.extend(timezone);
const { BeanModel } = require("redbean-node/dist/bean-model");

/**
 * status:
 *      0 = DOWN
 *      1 = UP
 *      2 = PENDING
 */
class Heartbeat extends BeanModel {

    toPublicJSON() {
        return {
            status: this.status,
            time: this.time,
            msg: "",        // Hide for public
            ping: this.ping,
        };
    }

    toJSON() {
        return {
            monitorID: this.monitor_id,
            status: this.status,
            time: this.time,
            msg: this.msg,
            ping: this.ping,
            important: this.important,
            duration: this.duration,
        };
    }

}

module.exports = Heartbeat;
