// This is the main file for the frontend application
// Required Dependencies
const dotenv = require('dotenv');
const fs = require('fs');

// Load env vars
dotenv.config();
const DISCORD_TOKEN = process.env.DISCORD_TOKEN;

// Require the necessary discord.js classes
const { Client, Intents, Collection } = require('discord.js');

// Create a new client instance
const client = new Client({ intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.DIRECT_MESSAGES, Intents.FLAGS.GUILD_MESSAGES] });

// Load all commands from the commands folder
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

// Regex to remove <@!id>
const mentionRegex = RegExp('<@!.*>');

// Setup logger
// https://www.npmjs.com/package/winston
const winston = require('winston');
const { getSystemErrorMap } = require('util');
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    defaultMeta: { service: 'frontend' },
    transports: [
      new winston.transports.File({ filename: 'logs/frontend.log', level: 'warn' }),
    ],
    handleExceptions: true,
    exitOnError: false,
});

if (process.env.ENVIRONMENT !== 'production') {
    logger.add(new winston.transports.Console({
        format: winston.format.simple(),
    }));
}

// Creating a collection for commands in client
const commands = [];
client.commands = new Collection();
for (const file of commandFiles) {
    const command = require(`./commands/${file}`);
    commands.push(command.data.toJSON());
    client.commands.set(command.data.name, command);
}

// When the client is ready, run this code (only once)
client.once('ready', () => {
    client.user.setActivity('docs.feyre.io | /help');

	logger.log({
        level: 'warn',
        message: `Client is ready. Shard ID: ${client.shard.id}`
    });
});

// Log any errors that the shard hits
client.on('shardError', error => {
    logger.log({
        level: 'error',
        message: `Client encountered a shard error. Shard ID: ${client.shard.id}, Error Stack: ${error.stack}`
    });
});

// Log any unhandled promises, this can be encountered when there is an error talking to Discord API
process.on('unhandledRejection', error => {

    // This is a very common exception hit when interacting with the discord API
    // We just supress it
    if (String(error.message).includes("The reply to this interaction has already been sent"))
    {
        return;
    }

	logger.log({
        level: 'error',
        message: `Process encountered an unhandled promise rejection. Error Message: ${error.message}`
    });
});

// Login to Discord
logger.log({
    level: 'warn',
    message: `Client is logging into discord. Shard ID: ${client.shard.id}`
});

client.login(DISCORD_TOKEN);

logger.log({
    level: 'warn',
    message: `Client logged into discord. Shard ID: ${client.shard.id}`
});

// Reply to @bot messages
client.on('messageCreate', async message => {
    // Only respond to @bot from not another bot
    if (!message.mentions.has(client.user) || message.author.bot)
    {
        return;
    }

    logger.log({
        level: 'info',
        message: 'Got an @ message'
    });
    
    // Remove the @bot
    var content = message.content.replace(mentionRegex, '').trim()

    logger.log({
        level: 'info',
        message: '@ message content: ' + content
    });

    // There is probably some cool way to reduce all of these if statements
    // But leave it like this for now
    // TODO(IAN)
    // Determine what commands should support this functionality
    // Thinking just roll?
    if (content.startsWith("ping"))
    {
        logger.log({
            level: 'info',
            message: 'Executing ping operation'
        });

        const command = client.commands.get("ping")
        var response = await command.execute_message(content, message.author.id, message.guild.id)

        await message.channel.send({ embeds: [response]})
    }
    else if (content.startsWith("roll"))
    {
        logger.log({
            level: 'info',
            message: 'Executing roll operation'
        });

        content = content.slice(4).trim() // Remove the "roll"
        const command = client.commands.get("roll")
        var response = await command.execute_message(content, message.author.id, message.guild.id, logger)

        await message.channel.send({ embeds: [response]})
    }
    else if (content.startsWith("help"))
    {
        logger.log({
            level: 'info',
            message: 'Executing help operation'
        });

        const command = client.commands.get("help")
        content = content.slice(4).trim() // Remove the "help"
        var response = await command.execute_message(content, message.author.id, message.guild.id)

        // Slightly different response
        // Already has the {embeds}
        await message.channel.send(response)
    }   
});

// Reply to Slash Commands
client.on('interactionCreate', async interaction => {

    logger.log({
        level: 'info',
        message: 'Processing interaction: ' + interaction.commandName
    });

    if (!interaction.isCommand()) return;
    const command = client.commands.get(interaction.commandName);
    if (!command) return;

    try {
        if (interaction.commandName == "stats") { // With the stats interaction, we need to pass in a few properties from the client
            users = await client.shard.broadcastEval(c => c.guilds.cache.reduce((acc, guild) => acc + guild.memberCount, 0));
            usercount = users.reduce((acc, userSize) => acc + userSize, 0)
            guilds = await client.shard.fetchClientValues('guilds.cache.size')
            guildtotal = guilds.reduce((acc, guildsizes) => acc + guildsizes, 0)

            logger.log({
                level: 'info',
                message: `Processing stats interaction. User Count: ${usercount}, Guild Count: ${guildtotal}, Shard Count ${client.shard.count}`
            });

            await command.execute_interaction(interaction, guildtotal, usercount, client.shard.count, logger);
        }
        else {
            await command.execute_interaction(interaction, logger);
        }

        logger.log({
            level: 'info',
            message: 'Interaction executed successfully!'
        });
    } catch (error) {
        if (error) {
            logger.log({
                level: 'error',
                message: error.stack
            });
        }
        await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
    }
});

// Reply to Buttons
client.on('interactionCreate', async interaction => {
	if (!interaction.isButton()) return;

    logger.log({
        level: 'info',
        message: 'Processing button interaction: ' + interaction.customId
    });

	// console.log(interaction);
    // All buttons are labeled with command_button
    // Like this: init_join
    const command = client.commands.get(interaction.customId.split('_')[0]); 

    if(interaction.customId.startsWith('init') ||
       interaction.customId.startsWith('character'))
    {
        try {
            await command.execute_button(interaction, logger);
        }
        catch (error) {
            if (error) {
                logger.log({
                    level: 'error',
                    message: error.stack
                });
            }
        }
    }
});
