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
	console.log('Ready!');
});

// Login to Discord
client.login(DISCORD_TOKEN);

// Reply to @bot messages
client.on('messageCreate', async message => {
    // Only respond to @bot from not another bot
    if (!message.mentions.has(client.user) || message.author.bot)
    {
        return;
    }

    console.log("Got a message: ", message.content);
    var content = message.content.replace(mentionRegex, '').trim()
    console.log("New content: ", content);
    if (content.startsWith("ping"))
    {
        const command = client.commands.get("ping")
        await message.channel.send(await command.execute_message(content))
    }  
});

// Reply to Slash Commands
client.on('interactionCreate', async interaction => {

    console.log("Processing command:", interaction.commandName);
    if (!interaction.isCommand()) return;
    const command = client.commands.get(interaction.commandName);
    if (!command) return;

    try {
        await command.execute_interaction(interaction);
    } catch (error) {
        if (error) console.error(error);
        await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
    }
});
