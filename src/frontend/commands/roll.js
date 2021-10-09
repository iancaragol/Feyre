// Import SlashCommandBuild to handle slash commands
const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

// Import our common backend functions
const backend = require("./../common/backend");

// Setup our HTTP library
const bent = require('bent');
const getJSON = bent('json');

// Export the module which handles the slash command
module.exports = {
    data: new SlashCommandBuilder()
        .setName('roll') // The name of the Discord Slash command
        .setDescription('Rolls a dice expression') // The description of the Discord Slash command
        .addStringOption(option =>
            option.setName('expression')
                .setDescription('The expression to roll. Ex: 1d20+5')
                .setRequired(true)),

    // The function to execute when the slash command is called (calls our backend)
    async execute(interaction) {
        expression = interaction.options.getString('expression')
        user = interaction.user.id
        string_url = "/api/backendservice/roll/?user=" + user + "&expression=" + expression
        // Creates the URL to call the backend
        url = await backend.create_url({path: string_url});
        // Calls the backend with a GET request and returns the JSON response
        let response = await getJSON(url);

        // Temporary, remove this before going to prod
        console.log(response);

        // Need to play around with this, what is the best way of displaying a roll?
        responseEmbed = new MessageEmbed()
            .setColor('#544bcc')
            .addFields(
                { name: '**Result**', value: response.parent_result[0].total},
            )

        // Sends a reply to the Slash command which triggered this function
        interaction.reply({ embeds: [responseEmbed] });
    }
};