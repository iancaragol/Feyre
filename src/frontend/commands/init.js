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

    async execute_init_get(user, guild, channel, logger) {
        string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`
        url = await backend.create_url({path: string_url});

        logger.log({
            level: 'info',
            message: `[INIT] Executing init join. Uri: ${url}`
        });

        request = await get(url);
        response = await request.json();

        return response
    },

    async execute_init_join(user, guild, channel, character, roll, logger)
    {
        string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`

        // If character is provided, but not roll, then default to 1d20
        if (character != null && roll == null)
        {
            roll = "1d20"
        }

        // Initiative API expects no character name or expression if it is going to fetch from the database.
        if (character != null && roll != null)
        {
            string_url += `&character_name=${encodeURIComponent(character)}&initiative_expression=${encodeURIComponent(roll)}`
        }

        url = await backend.create_url({path: string_url});

        logger.log({
            level: 'info',
            message: `[INIT] Executing init join. Uri: ${url}`
        });

        request = await put(url);
        response = await request.json();

        return response
    },

    async execute_init_remove(user, guild, channel, character, logger)
    {
        string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`
        string_url += `&character_name=${encodeURIComponent(character)}`
        url = await backend.create_url({path: string_url});

        logger.log({
            level: 'info',
            message: `[INIT] Executing init remove. Uri: ${url}`
        });

        request = await del(url);
        response = await request.json();

        return response
    },

    async execute_init_next(user, guild, channel, logger)
    {
        string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`
        url = await backend.create_url({path: string_url});

        logger.log({
            level: 'info',
            message: `[INIT] Executing init next. Uri: ${url}`
        });

        request = await patch(url);
        response = await request.json();

        return response
    },

    async execute_init_reset(user, guild, channel, logger)
    {
        string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`
        url = await backend.create_url({path: string_url});

        logger.log({
            level: 'info',
            message: `[INIT] Executing init reset. Uri: ${url}`
        });

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

    async create_init_embed(response, logger)
    {
        logger.log({
            level: 'info',
            message: `[INIT] Creating response embed.`
        });

        // Backend should respond with a 200 OK
        if (request.statusCode == 200)
        {
            logger.log({
                level: 'info',
                message: `[INIT] Response had status code 200 OK`
            });

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

            logger.log({
                level: 'info',
                message: `[INIT] Constructed response embed.`
            });

            return responseEmbed;
        }
        // Oops! Internal server error
        else if (request.statusCode == 500)
        {
            logger.log({
                level: 'warn',
                message: `[INIT] Response status code was 500 INTERNAL SERVER ERROR.`
            });

            error_string = "Something went wrong. See /help init for examples."
            responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
            .setTitle("Oops!")
            .setDescription(error_string)

            return responseEmbed;
        }
        // If the status code is something else, we are outside of expected behaviour
        else
        {
            logger.log({
                level: 'warn',
                message: `[INIT] Response status code was unexpected. StatusCode: ${request.statusCode}`
            });

            responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
            .addFields(
                { name: "Unexpected Response", value: request.statusCode }
            )

            return responseEmbed;
        }            
    },

    // Executes the command from message context
    async execute_message(content, user, guild, logger)
    {
        responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
        .setTitle("DMs are not supported")
        .setDescription("Sorry, initiative tracking requires using slash (/) commands. See /help init for details!")
        
        return responseEmbed;
    },

    // Executes the command from an interaction (slash command) context
    async execute_interaction(interaction, logger) {
        logger.log({
            level: 'info',
            message: '[INIT] Received initiative interaction'
        });

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
        count = interaction.options.getInteger('count')

        // TODO(IAN) Implement the count argument
        // Count is not supported right now...
        if (count != null) {
            logger.log({
                level: 'warn',
                message: '[INIT] Count is not supported yet'
            });

            response = new MessageEmbed().setColor(embedColors.errorEmbedColor)
            .setTitle("Count is not supported")
            .setDescription("Sorry, the count argument is not supported yet!")

            return await interaction.reply({ embeds: [response]})
        }

        // JOIN and GET both return the INIT Tracker so they need buttons
        if (interaction.options.getSubcommand() === 'join') {
            logger.log({
                level: 'info',
                message: '[INIT] Subcommand is join'
            });

            // Make the request to the backend to get the tracker
            var response = await this.execute_init_join(user, guild, channel, character, roll, logger)

            // Delete the old messsage
            if (response.message_id) {
                logger.log({
                    level: 'info',
                    message: `[INIT] Deleting old message. Message Id: ${response.message_id}`
                });
                
                await interaction.webhook.deleteMessage(response.message_id)
            }

            responseEmbed = await this.create_init_embed(response, logger)

            logger.log({
                level: 'info',
                message: '[INIT] Replying.'
            });

            // Respond and update the initiative tracker with the message's id
            return await interaction.reply({ embeds: [responseEmbed],  components: [initButtons], fetchReply: true  })
                                    .then((reply) => this.execute_init_message_update(reply.guild.id, reply.channel.id, reply.id))
        }
        else if (interaction.options.getSubcommand() === 'get') {
            logger.log({
                level: 'info',
                message: '[INIT] Subcommand is get'
            });

            var response = await this.execute_init_get(user, guild, channel, logger)
            responseEmbed = await this.create_init_embed(response, logger)

            logger.log({
                level: 'info',
                message: '[INIT] Replying.'
            });

            return await interaction.reply({ embeds: [responseEmbed], components: [initButtons] })
        }
        else if (interaction.options.getSubcommand() === 'remove') {
            logger.log({
                level: 'info',
                message: '[INIT] Subcommand is remove'
            });

            var response = await this.execute_init_remove(user, guild, channel, character, logger)
            responseEmbed = await this.create_init_embed(response, logger)

            return await interaction.reply({ embeds: [responseEmbed], components: [initButtons] })
        }
        else if (interaction.options.getSubcommand() === 'reset') {
            logger.log({
                level: 'info',
                message: '[INIT] Subcommand is reset'
            });

            var response = await this.execute_init_reset(user, guild, channel, logger)
            responseEmbed = await this.create_init_embed(response, logger)

            return await interaction.reply({ embeds: [responseEmbed], components: [initButtons] })
        }
    },

    // Handles interactions from button presses
    async execute_button(interaction, logger) {
        logger.log({
            level: 'info',
            message: '[INIT] Received init button interaction'
        });

        user = interaction.user.id
        guild = interaction.guild.id
        channel = interaction.channel.id

        if (interaction.customId == 'init_next')
        {
            logger.log({
                level: 'info',
                message: '[INIT] Button interaction is next'
            });

            var response = await this.execute_init_next(user, guild, channel, logger)
            responseEmbed = await this.create_init_embed(response, logger)

            logger.log({
                level: 'info',
                message: '[INIT] Updating embed message.'
            });
            return await interaction.update({ embeds: [responseEmbed], components: [initButtons] })
        }
        else if (interaction.customId == 'init_join')
        {
            logger.log({
                level: 'info',
                message: '[INIT] Button interaction is join.'
            });

            var response = await this.execute_init_join(user, guild, channel, null, null, logger)
            responseEmbed = await this.create_init_embed(response, logger)

            logger.log({
                level: 'info',
                message: '[INIT] Updating embed message.'
            });
            return await interaction.update({ embeds: [responseEmbed], components: [initButtons] })
        }
    }
};