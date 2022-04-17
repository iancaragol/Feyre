const dotenv = require('dotenv');
const { ShardingManager } = require('discord.js');

// Load env vars
dotenv.config();
const DISCORD_TOKEN = process.env.DISCORD_TOKEN;

const manager = new ShardingManager('./bot.js', { token: DISCORD_TOKEN });

manager.on('shardCreate', shard => console.log(`Launched shard ${shard.id}`));

manager.spawn();