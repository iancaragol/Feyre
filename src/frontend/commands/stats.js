// Import SlashCommandBuild to handle slash commands
const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

// Import our common backend functions
const backend = require("../common/backend");

// Import our embed color constants
const embedColors = require('./../common/embed_colors')

// Status codes that can be returned by the backend
let status_codes = [200, 500, 504]

// Setup our HTTP library
const bent = require('bent');
const get = bent(status_codes);

// Export the module which handles the slash command
module.exports = {
    data: new SlashCommandBuilder()
        .setName('stats') // The name of the Discord Slash command
        .setDescription('Show command usage')
        .addBooleanOption(option =>
            option.setName('all')
                .setDescription('More detailed stats information')
                .setRequired(false)),

    // The function to execute when the slash command is called (calls our backend)
    async execute_interaction(interaction, serverCount, userReach, logger) {
        logger.log({
            level: 'info',
            message: '[STATS] Executing Stats interaction'
        });

        all = interaction.options.getBoolean('all') || true
        user = interaction.user.id
        string_url = "/api/backendservice/stats?user=" + user + "&all=true" // Hardcode to true
        
        url = await backend.create_url({path: string_url});

        logger.log({
            level: 'info',
            message: '[STATS] Making request to backend using uri: ' + string_url
        });

        let request = await get(url);
        let response = await request.json()

        if (request.statusCode == 200)
        {
            logger.log({
                level: 'info',
                message: '[STATS] Backend returned 200 OK'
            });

            responseEmbed = new MessageEmbed().setColor(embedColors.successEmbedColor)
            responseEmbed.setTitle("Feyre - Statistics")
            
            var commandsBody = `**roll** - ${response.roll}
**init** - ${response.init}
**character** - ${response.char}

**stats** - ${response.stats}
**help** - ${response.help}`

            responseEmbed.addField(
                "Commands", commandsBody
            )

            var serverBody = `**Unique Users** - ${response.user_count}
**User Reach** - ${userReach}
**Servers** - ${serverCount}`

            responseEmbed.addField(
                "Servers", serverBody
            )

            interaction.reply({ embeds: [responseEmbed]})
        }
        else if (request.statusCode == 500)
        {
            logger.log({
                level: 'warn',
                message: '[STATS] Backend returned 500 INTERNAL SERVER ERROR'
            });

            responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
                .addFields(
                    { name: "Error", value: "Oops! Something went wrong." }
                )

            interaction.reply({ embeds: [responseEmbed]})
        }
    }
}; 