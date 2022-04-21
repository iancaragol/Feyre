// Import SlashCommandBuild to handle slash commands
const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

// Import our common backend functions
const backend = require("./../common/backend");

// Import our models
const help_embeds = require("./../common/help_embeds.js")

// Status codes that can be returned by the backend
let status_codes = [200, 500, 504]

// Setup our HTTP library
const bent = require('bent');
const get = bent(status_codes);

// Export the module which handles the slash command
module.exports = {
    data: new SlashCommandBuilder()
        .setName('help') // The name of the Discord Slash command
        .setDescription('How to use Feyre') // The description of the Discord Slash command
        .addStringOption(option =>
            option.setName('command')
                .setDescription('Command to learn more about')
                .setRequired(false),
        ),

    async execute_help(command, user, guild)
    {
        // Trim any whitespace

        // Here we notify the backend, just to keep track of the help count
        string_url = "/api/backendservice/help?user=" + user
        if (command)
        {
            command = command.trim()
            string_url = string_url + "&command=" + command
        }
        
        url = await backend.create_url({path: string_url});
        let request = await get(url);
        
        if (!command)
        {
            return { embeds: [help_embeds.helpEmbed], components: [help_embeds.helpRow] };
        }
        else if (command == 'roll')
        {
            return { embeds: [help_embeds.rollEmbed], components: [help_embeds.rollRow] };
        }
        else if (command == 'init')
        {
            return { embeds: [help_embeds.initEmbed], components: [help_embeds.initRow] };
        }
        else if (command == 'character')
        {
            return { embeds: [help_embeds.charEmbed], components: [help_embeds.charRow] };
        }
        else
        {
            return {embeds: [help_embeds.notfoundEmbed], components: [help_embeds.helpRow]};
        }
    },

    async execute_message(content, user, guild)
    {    
        return await this.execute_help(content, user, guild);
    },

    // The function to execute when the slash command is called (calls our backend)
    async execute_interaction(interaction) {
        command = interaction.options.getString('command')
        user = interaction.user.id
        guild = interaction.guild.id
        interaction.reply(await this.execute_help(command, user, guild));
    }
};