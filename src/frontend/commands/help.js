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

    // The function to execute when the slash command is called (calls our backend)
    async execute(interaction) {
        command = interaction.options.getString('command')

        // Here we notify the backend, but this should probably be a no-op.
        // It doesnt make a lot of sense to go all the way to the backend just to create an embed
        user = interaction.user.id
        string_url = "/api/backendservice/help?user=" + user
        if (command)
        {
            string_url = string_url + "&command=" + command
        }
        
        url = await backend.create_url({path: string_url});
        let request = await get(url);
        let response = await request.json()

        if (!command)
        {
            interaction.reply({ embeds: [help_embeds.helpEmbed], components: [help_embeds.helpRow] });
        }
        else if (command == 'roll')
        {
            interaction.reply({ embeds: [help_embeds.rollEmbed]});
        }
        else
        {
            // TODO: Improve this
            interaction.reply("Could not find that command!");
        }
        /*
        if (request.statusCode == 200)
        {
            interaction.reply(response.message)
        }
        else if (request.statusCode == 500)
        {
            interaction.reply({emve}");
        }
        */
    }
};