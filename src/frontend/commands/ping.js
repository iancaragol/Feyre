// This function is useful for checking the frontend container health
// Import SlashCommandBuild to handle slash commands
const { SlashCommandBuilder } = require('@discordjs/builders');

// Export the module which handles the slash command
module.exports = {
    data: new SlashCommandBuilder()
        .setName('ping') // The name of the Discord Slash command
        .setDescription('Returns pong'), // The description of the Discord Slash command

    // Executes the command from message context
    async execute_message(content) {
        return "pong"
    },

    // Exucutes the command from an interaction (slash command) context
    async execute_interaction(interaction) {
        // Sends a reply to the Slash command which triggered this function
        interaction.reply({ content: "pong" });
    }
};
