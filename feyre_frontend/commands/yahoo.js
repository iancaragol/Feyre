const { SlashCommandBuilder } = require('@discordjs/builders');

module.exports = {
    data: new SlashCommandBuilder()
        .setName('yahoo')
        .setDescription('Replies with yahoi'),
    async execute(interaction) {
        interaction.reply({ content: 'Yahoi!' });
    }
};
