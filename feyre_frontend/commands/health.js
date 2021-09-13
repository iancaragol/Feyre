const { SlashCommandBuilder } = require('@discordjs/builders');
const bent = require('bent');
const getJSON = bent('json');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('health')
        .setDescription('Returns the healthcheck of the Feyre backend'),
    async execute(interaction) {
        let response = await getJSON('http://localhost:5000/api/backendservice/healthcheck/');
        interaction.reply({ content: `Status: ${response.message} - HTTP: ${response.status}` });
    }
};
