// Import SlashCommandBuild to handle slash commands
const { SlashCommandBuilder } = require('@discordjs/builders');
const { EmbedBuilder } = require('discord.js');

// Import our common backend functions
const backend = require("./../common/backend");

// Import our embed color constants
const embedColors = require('./../common/embed_colors')

// Setup our HTTP library
const bent = require('bent');
const getJSON = bent('json');

// Export the module which handles the slash command
module.exports = {
    data: new SlashCommandBuilder()
        .setName('health') // The name of the Discord Slash command
        .setDescription('Check backend service health'), // The description of the Discord Slash command

    // The function to execute when the slash command is called (calls our backend)
    async execute_interaction(interaction, logger) {
        // Creates the URL to call the backend
        user = interaction.user.id
        string_url = "/api/backendservice/healthcheck?user=" + user
        url = await backend.create_url({path: string_url});

        // Calls the backend with a GET request and returns the JSON response
        let response = await getJSON(url);

        // console.log(response);
        
        var backendstr = response.backend;
        var redisstr = `**Available:** ${response.redis.available}\n`;

        if (response.redis.available === true)
        {
            redisstr += `   **CPU**: ${response.redis.cpu.used_cpu}\n`;
            redisstr += `   **Memory:**\n`;
            redisstr += `->     Used: ${response.redis.memory.used_memory}\n`;
            redisstr += `->     Used RSS: ${response.redis.memory.used_memory_rss}\n`;
            redisstr += `->     Total: ${response.redis.memory.total_memory}\n`;
            redisstr += `   **Stats:**\n`;
            redisstr += `->     Commands Processed: ${response.redis.stats.total_commands_processed}\n`;
            redisstr += `->     Connections Received: ${response.redis.stats.total_connections_received}\n`;
        }

        responseEmbed = new EmbedBuilder()
        .setColor(embedColors.successEmbedColor)
        .addFields(
            { name: "Backend", value: backendstr },
            { name: "Redis", value: redisstr },
        );

        // Sends a reply to the Slash command which triggered this function
        interaction.reply({ embeds: [responseEmbed] });
    }
};