// Import SlashCommandBuild to handle slash commands
const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

// Import our common backend functions
const backend = require("./../common/backend");

// Status codes that can be returned by the backend
let status_codes = [200, 500, 504]

// Setup our HTTP library
const bent = require('bent');
const get = bent(status_codes);

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

        // Make the request
        let request = await get(url);
        let response = await request.json()
        
        // Temporary, remove this before going to prod
        console.log(response);

        if (request.statusCode != 200)
        {
            error_string = expression + "\n" + response.exception_message
            responseEmbed = new MessageEmbed()
            .setColor('#FF0000')
            //.setDescription(`<@!${user}>`)
            .addFields(
                { name: "Invalid Dice Expression", value: error_string }
            )

            // Sends a reply to the Slash command which triggered this function
            interaction.reply({ embeds: [responseEmbed] });
        }

        // Todo (IAN)
        // Need to put this in a loop for multiple dice counts.
        // Or display it differently, probably just the totals.
        // Otherwise it will hit the max size of an embed and be hard to read
        total_field = "[ " + response.parent_result[0].total + " ]"
        expression_value = response.parent_result[0].expression + " -> " + response.parent_result[0].md_result

        // Need to play around with this, what is the best way of displaying a roll?
        responseEmbed = new MessageEmbed()
            .setColor('#00FFDE')
            //.setDescription(`<@!${user}>`)
            .addFields(
                { name: total_field, value: expression_value }
            )

        // Sends a reply to the Slash command which triggered this function
        interaction.reply({ embeds: [responseEmbed] });
    }
};