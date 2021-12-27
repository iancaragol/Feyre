// Import SlashCommandBuild to handle slash commands
const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

// Import our common backend functions
const backend = require("../common/backend");

// Status codes that can be returned by the backend
let status_codes = [200, 500, 504]

// Setup our HTTP library
const bent = require('bent');
const get = bent(status_codes);

// Export the module which handles the slash command
module.exports = {
    data: new SlashCommandBuilder()
        .setName('stats') // The name of the Discord Slash command
        .setDescription('Show command usage'),

    // The function to execute when the slash command is called (calls our backend)
    async execute(interaction) {
        user = interaction.user.id
        string_url = "/api/backendservice/stats?user=" + user
        
        url = await backend.create_url({path: string_url});
        let request = await get(url);
        let response = await request.json()

        if (request.statusCode == 200)
        {
            interaction.reply(response.message)
        }
        else if (request.statusCode == 500)
        {
            interaction.reply("Oops! Something went wrong.");
        }
    }
};