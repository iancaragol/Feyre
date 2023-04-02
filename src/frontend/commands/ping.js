// This function is useful for checking the frontend container health
// Import SlashCommandBuild to handle slash commands
const { SlashCommandBuilder } = require('@discordjs/builders');
const { EmbedBuilder } = require('discord.js');

// Import our embed color constants
const embedColors = require('./../common/embed_colors')

// Export the module which handles the slash command
module.exports = {
    data: new SlashCommandBuilder()
        .setName('ping') // The name of the Discord Slash command
        .setDescription('Returns pong'), // The description of the Discord Slash command

    // Executes the command from message context
    async execute_message(content, user, guild) {
        var responseEmbed = new EmbedBuilder().setColor(embedColors.successEmbedColor)
        responseEmbed.setTitle("pong")

        return responseEmbed
    },

    // Exucutes the command from an interaction (slash command) context
    async execute_interaction(interaction, logger) {
        var responseEmbed = new EmbedBuilder().setColor(embedColors.successEmbedColor)
        responseEmbed.setTitle("pong")

        interaction.reply({ embeds: [responseEmbed] });
    }
};
