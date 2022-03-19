// Import SlashCommandBuild to handle slash commands
const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, MessageActionRow, MessageButton, IntegrationApplication } = require('discord.js');

// Import our common backend functions
const backend = require("./../common/backend");

// Import our embed color constants
const embedColors = require('./../common/embed_colors')

// Status codes that can be returned by the backend
let status_codes = [200, 500, 504]

// Button row for all initiative messages
const initButtons = new MessageActionRow()
    .addComponents(
        new MessageButton()
            .setCustomId('init_join')
            .setLabel('➕ Join')
            .setStyle('PRIMARY'),
        new MessageButton()
            .setCustomId('init_next')
            .setLabel('⚔️ Next')
            .setStyle('SUCCESS'),
        // new MessageButton()
        //     .setCustomId('init_refresh')
        //     .setLabel('Refresh')
        //     .setStyle('SECONDARY'),
        // new MessageButton()
        //     .setCustomId('init_leave')
        //     .setLabel('Leave')
        //     .setStyle('DANGER'),
    );

// Setup our HTTP library
const bent = require('bent');
const get = bent('GET', status_codes)
const put = bent('PUT', status_codes);
const patch = bent('PATCH', status_codes);
const del = bent('DELETE', status_codes);

// Export the module which handles the slash command
module.exports = {
    data: new SlashCommandBuilder()
        .setName('init') // The name of the Discord Slash command
        .setDescription('Roll for initiative! Keep track of your turn order') // The description of the Discord Slash command
        .addSubcommand(subcommand =>
            subcommand
                .setName('join')
                .setDescription('Join initiative')
                .addStringOption(option => option.setName('character').setDescription('Name of your character').setRequired(false))
                .addStringOption(option => option.setName('roll').setDescription('Dice expression or Initiative roll value').setRequired(false))
                .addIntegerOption(option => option.setName('count').setDescription('Number of characters to add to initiative').setRequired(false))
        )
        .addSubcommand(subcommand =>
            subcommand
                .setName('get')
                .setDescription('Gets the initiative tracker for this channel and reposts it.')
        )
        .addSubcommand(subcommand =>
            subcommand
                .setName('remove')
                .setDescription('Remove a character initiative')
                .addStringOption(option => option.setName('character').setDescription('Name of your character').setRequired(false))
        )
        .addSubcommand(subcommand =>
            subcommand
                .setName('reset')
                .setDescription('Creates a brand new tracker')
        ),

    async execute_init(type, user, guild, channel, character = null, roll = null, count = null, debug = false)
    {
        try
        {
            // Ex: /initiative?user=12345&guild=4&channel=4&character_name=Carol&initiative_expression=1d20
            string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`

            // If we are joining, and character and roll are provided then those
            // Values need to be included in the PUT Query
            if (type === 'join' && character && roll)
            {
                string_url += `&character_name=${encodeURIComponent(character)}&initiative_expression=${encodeURIComponent(roll)}`
            }
            if (type === 'remove' && character)
            {
                string_url += `&character_name=${encodeURIComponent(character)}`
            }

            // Creates the URL to call the backend
            url = await backend.create_url({path: string_url});

            let request;
            let response;

            // Get maes a GET request to return the initiative tracker without modification
            if (type === 'get')
            {
                request = await get(url);
                response = await request.json();
            }
            // Join makes a PUT request to add a character to the initiative tracker
            else if (type === 'join')
            {
                request = await put(url);
                response = await request.json();
            }
            // Next makes a PATCH request to increment the turn by one
            else if (type === 'next')
            {
                request = await patch(url);
                response = await request.json();
            }
            // Remove makes a DELETE request to delete the character
            else if (type === 'remove')
            {
                request = await del(url);
                response = await request.json();
            }
            else if (type === 'reset')
            {
                request = await del(url);
                request = await get(url);
                response = await request.json();
            }

            console.log(response)
            
            // Backend should respond with a 200 OK
            if (request.statusCode == 200)
            {
                responseEmbed = new MessageEmbed().setColor(embedColors.successEmbedColor)
                responseEmbed.setTitle("[                Initiative                 ]")
                turnOrderString = ""
                
                for (let i = 0; i < response.characters.length; i++)
                {
                    if (response.turn % response.characters.length == i)
                    {
                        turnOrderString += `**➤ ${response.characters[i].name} (${response.characters[i].initiative_value})**\n`
                    }
                    else
                    {
                        turnOrderString += `${response.characters[i].name} (${response.characters[i].initiative_value})\n`
                    }
                }

                responseEmbed.setDescription(
                    turnOrderString.trim()
                )

                responseEmbed.addField(
                    "Round: ", String(response.turn)
                )

                return responseEmbed;
            }
            // Oops! Internal server error
            else if (request.statusCode == 500)
            {
                error_string = "There should be some error handling here..."
                responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
                .addFields(
                    { name: "Oops! Something broke.", value: error_string }
                )

                return responseEmbed;
            }
            // If the status code is something else, we are outside of expected behaviour
            else
            {
                responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
                .addFields(
                    { name: "Unexpected Response", value: request.statusCode }
                )

                return responseEmbed;
            }            
        }
        catch (error)
        {
            console.log("Caught Unhandled Exception in INIT")
            console.log(error)
            if (debug)
            {
                responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
                .addFields(
                    { name: "Unhandled Exception", value: error.toString() }
                )

                return responseEmbed;
            }
        }
    },

    // Executes the command from message context
    async execute_message(content, user, guild)
    {
        responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
        .addFields(
            { name: "Not supported.", value: "Sorry, initiative tracking requires using slash (/) commands. See /help init for details!" }
        )
        
        return responseEmbed;
    },

    // Executes the command from an interaction (slash command) context
    async execute_interaction(interaction) {
        user = interaction.user.id
        guild = interaction.guild.id
        channel = interaction.channel.id

        roll = interaction.options.getString('roll')
        character = interaction.options.getString('character')
        count = interaction.options.getString('count')

        // JOIN and GET both return the INIT Tracker so they need buttons
        if (interaction.options.getSubcommand() === 'join') {
            var response = await this.execute_init('join', user, guild, channel, character, roll, count)
            return await interaction.reply({ embeds: [response],  components: [initButtons] })
        }
        else if (interaction.options.getSubcommand() === 'get') {
            var response = await this.execute_init('get', user, guild, channel, character, roll, count)
            return await interaction.reply({ embeds: [response], components: [initButtons] })
        }
        else if (interaction.options.getSubcommand() === 'remove') {
            var response = await this.execute_init('remove', user, guild, channel, character, roll, count)
            return await interaction.reply({ embeds: [response], components: [initButtons] })
        }
        else if (interaction.options.getSubcommand() === 'reset') {
            var response = await this.execute_init('reset', user, guild, channel, character, roll, count)
            return await interaction.reply({ embeds: [response], components: [initButtons] })
        }
    },

    // Handles interactions from button presses
    async execute_button(interaction) {
        user = interaction.user.id
        guild = interaction.guild.id
        channel = interaction.channel.id

        if (interaction.customId == 'init_next')
        {
            var response = await this.execute_init('next', user, guild, channel)
            return await interaction.update({ embeds: [response], components: [initButtons] })
        }
        else if (interaction.customId == 'init_join')
        {
            var response = await this.execute_init('join', user, guild, channel)
            return await interaction.update({ embeds: [response], components: [initButtons] })
        }
    }
};