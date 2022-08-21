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

// API Endpoint for initiative

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

    async execute_init_get(user, guild, channel) {
        string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`
        url = await backend.create_url({path: string_url});

        request = await get(url);
        response = await request.json();

        return response
    },

    async execute_init_join(user, guild, channel, character, roll)
    {
        string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`
        string_url += `&character_name=${encodeURIComponent(character)}&initiative_expression=${encodeURIComponent(roll)}`
        url = await backend.create_url({path: string_url});

        request = await put(url);
        response = await request.json();

        return response
    },

    async execute_init_remove(user, guild, channel, character)
    {
        string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`
        string_url += `&character_name=${encodeURIComponent(character)}`
        url = await backend.create_url({path: string_url});

        request = await del(url);
        response = await request.json();

        return response
    },

    async execute_init_next(user, guild, channel)
    {
        string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`
        url = await backend.create_url({path: string_url});

        request = await patch(url);
        response = await request.json();

        return response
    },

    async execute_init_reset(user, guild, channel)
    {
        string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`
        url = await backend.create_url({path: string_url});

        request = await del(url);
        request = await get(url);
        response = await request.json();

        return response
    },

    async execute_init_message_update(guild, channel, messageId) {
        string_url = `/api/backendservice/initiative/update?guild=${guild}&channel=${channel}&messageId=${messageId}`
        url = await backend.create_url({path: string_url});

        request = await patch(url);
        response = await request.json();

        console.log("TEMP")
        console.log(response)

        return response
    },

    async create_init_embed(response)
    {
        // Backend should respond with a 200 OK
        if (request.statusCode == 200)
        {
            console.log(response)

            responseEmbed = new MessageEmbed().setColor(embedColors.successEmbedColor)
            responseEmbed.setTitle("[              Initiative              ]")
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
            error_string = "Something went wrong. See /help init for examples."
            responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
            .setTitle("Oops!")
            .setDescription(error_string)

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
    },

    // Executes the command from message context
    async execute_message(content, user, guild)
    {
        responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
        .setTitle("DMs are not supported")
        .setDescription("Sorry, initiative tracking requires using slash (/) commands. See /help init for details!")
        
        return responseEmbed;
    },

    // Executes the command from an interaction (slash command) context
    async execute_interaction(interaction) {
        user = interaction.user.id

        // If command was executed in DM context
        if (interaction.guild == null) {   
            response = new MessageEmbed().setColor(embedColors.errorEmbedColor)
            .setTitle("DMs are not supported")
            .setDescription("Sorry, the initiative tracker can not be used in Direct Messages. See /help init for details!")

            return await interaction.reply({ embeds: [response]})
        }

        guild = interaction.guild.id
        channel = interaction.channel.id

        roll = interaction.options.getString('roll')
        character = interaction.options.getString('character')
        count = interaction.options.getString('count')

        // JOIN and GET both return the INIT Tracker so they need buttons
        if (interaction.options.getSubcommand() === 'join') {
            // Make the request to the backend to get the tracker
            var response = await this.execute_init_join(user, guild, channel, character, roll, count)

            // Delete the old messsage
            if (response.message_id) {
                console.log("Delete reply ")
                console.log(response.message_id)
                //await interaction,channel.fetchMessage(response.message_id)
                //                         .then(msg => msg.delete());
                
                await interaction.webhook.deleteMessage(response.message_id)
            }

            responseEmbed = await this.create_init_embed(response)

            // Respond and update the initiative tracker with the message's id
            return await interaction.reply({ embeds: [responseEmbed],  components: [initButtons], fetchReply: true  })
                                    .then((reply) => this.execute_init_message_update(reply.guild.id, reply.channel.id, reply.id))
        }
        else if (interaction.options.getSubcommand() === 'get') {
            var response = await this.execute_init_get(user, guild, channel)
            responseEmbed = await this.create_init_embed(response)

            return await interaction.reply({ embeds: [responseEmbed], components: [initButtons] })
        }
        else if (interaction.options.getSubcommand() === 'remove') {
            var response = await this.execute_init_remove(user, guild, channel, character)
            responseEmbed = await this.create_init_embed(response)

            return await interaction.reply({ embeds: [responseEmbed], components: [initButtons] })
        }
        else if (interaction.options.getSubcommand() === 'reset') {
            var response = await this.execute_init_reset(user, guild, channel)
            responseEmbed = await this.create_init_embed(response)

            return await interaction.reply({ embeds: [responseEmbed], components: [initButtons] })
        }
    },

    // Handles interactions from button presses
    async execute_button(interaction) {
        user = interaction.user.id
        guild = interaction.guild.id
        channel = interaction.channel.id

        if (interaction.customId == 'init_next')
        {
            var response = await this.execute_init_next(user, guild, channel)
            responseEmbed = await this.create_init_embed(response)
            return await interaction.update({ embeds: [responseEmbed], components: [initButtons] })
        }
        else if (interaction.customId == 'init_join')
        {
            var response = await this.execute_init_join(user, guild, channel, null, null)
            responseEmbed = await this.create_init_embed(response)
            return await interaction.update({ embeds: [responseEmbed], components: [initButtons] })
        }
    }
};