const dotenv = require('dotenv');
const { ShardingManager } = require('discord.js');

// Setup logger
// https://www.npmjs.com/package/winston
const winston = require('winston');
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    defaultMeta: { service: 'shardingmanager' },
    transports: [
      new winston.transports.File({ filename: 'logs/shardingmanager.log', level: 'info' }),
    ],
});

if (process.env.ENVIRONMENT !== 'production') {
    logger.add(new winston.transports.Console({
        format: winston.format.simple(),
    }));
}

// Load env vars
dotenv.config();
const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
const TOP_GG_TOKEN = process.env.TOP_GG_TOKEN;

const manager = new ShardingManager('./bot.js', { token: DISCORD_TOKEN });
const { AutoPoster } = require('topgg-autoposter')
const poster = AutoPoster(TOP_GG_TOKEN, manager)

manager.on('shardCreate', shard => logger.log({
        level: 'info',
        message: `Launched shard ${shard.id}`
    })
);

logger.log({
    level: 'info',
    message: `Spawning shard manager.`
})

manager.spawn();

logger.log({
    level: 'info',
    message: `Shard mamanger was spawned.`
})

// Send info t// optional
poster.on('posted', (stats) => { // ran when succesfully posted
    logger.log({
        level: 'warn',
        message: `Posted stats to Top.gg | ${stats.serverCount} servers`
    })
})