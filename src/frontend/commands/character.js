// Import SlashCommandBuild to handle slash commands
const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed, MessageActionRow, MessageButton, IntegrationApplication } = require('discord.js');

// Import our common backend functions
const backend = require("./../common/backend");

// Import our embed color constants
const embedColors = require('./../common/embed_colors')

// Status codes that can be returned by the backend
let status_codes = [200, 500, 504]

// Setup our HTTP library
const bent = require('bent');
const get = bent('GET', status_codes)
const put = bent('PUT', status_codes);
const patch = bent('PATCH', status_codes);
const del = bent('DELETE', status_codes);

// Export the module which handles the slash command
module.exports = {
    data: new SlashCommandBuilder()
        .setName('character') // The name of the Discord Slash command
        .setDescription('Manage your characters for the initiative tracker') // The description of the Discord Slash command
        .addSubcommand(subcommand =>
            subcommand
                .setName('add')
                .setDescription('Create a new character')
                .addStringOption(option => option.setName('name').setDescription('Name of your character').setRequired(false))
                .addStringOption(option => option.setName('initiative').setDescription('Dice expression or Initiative roll value').setRequired(false))
        )
        .addSubcommand(subcommand =>
            subcommand
                .setName('remove')
                .setDescription('Remove a character from your list')
                .addIntegerOption(option => option.setName('id').setDescription('The id of the character you want to remove').setRequired(false))
        )
        .addSubcommand(subcommand =>
            subcommand
                .setName('list')
                .setDescription('Shows your character list')
        ),

    async execute_character(type, user, guild, channel, characterName = null, characterId = null, characterInit = null, debug = false, logger)
    {
        try
        {
            string_url = `/api/backendservice/character?user=${user}`

            logger.log({
                level: 'info',
                message: `[CHARACTER] Executing character operation. Type is ${type}`
            });

            // If we are joining, and character and roll are provided then those
            // Values need to be included in the PUT Query
            if (type === 'add' && characterName && characterInit)
            {
                string_url += `&character_name=${encodeURIComponent(characterName)}&initiative_expression=${encodeURIComponent(characterInit)}`
            }
            else if ((type === 'remove' || type === 'select') && characterId)
            {
                string_url += `&character_id=${encodeURIComponent(characterId)}`
            }

            // Creates the URL to call the backend
            url = await backend.create_url({path: string_url});

            logger.log({
                level: 'info',
                message: `[CHARACTER] Sending request to backend. Uri: ${url}`
            });

            let request;
            let response;

            // Get gets the list of all characters for that user
            if (type === 'list')
            {
                request = await get(url);
                response = await request.json();
            }
            // Join makes a PUT request to add a character
            else if (type === 'add')
            {
                request = await put(url);
                response = await request.json();
            }
            // Next makes a PATCH request to select a character by its ID
            else if (type === 'select')
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

            // Backend should respond with a 200 OK
            if (request.statusCode == 200)
            {
                logger.log({
                    level: 'info',
                    message: `[CHARACTER] Backend returned 200 OK. Constructing response embed.`
                });

                responseEmbed = new MessageEmbed().setColor(embedColors.successEmbedColor)
                responseEmbed.setTitle("[                            Your Characters                             ]")
                characterListString = "" // String that will be shown to users
                buttons = []

                buttonRow = new MessageActionRow()

                if (response.characters.length > 0) { // User has characters
                    for (let i = 0; i < response.characters.length; i++) {
                        var character = response.characters[i]

                        if (character.is_active)
                        {
                            characterListString += `**➤ ${character.id}. ${character.name} (${character.initiative_expression})**\n`
                        }
                        else
                        {
                            characterListString += `${character.id}. ${character.name} (${character.initiative_expression})\n`
                        }

                        buttonRow.addComponents(
                            new MessageButton()
                                .setCustomId(`character_${character.id}`)
                                .setLabel(`${character.id}`)
                                .setStyle('SECONDARY')
                        )

                        // On the 5th iteration we need to create a new button row!
                        // Unless its the last iteration, in which case we do not want to add an empty button
                        if (i == 4 && i + 1 != response.characters.length) 
                        {
                            buttons.push(buttonRow)
                            buttonRow = new MessageActionRow()
                        }
                    }

                    buttons.push(buttonRow)

                }
                else { // User has no created characters
                    characterListString = "**You don't have any characters!**\n\nSee /help character or https://docs.feyre.io/commands/#character for instructions on creating characters."
                }

                responseEmbed.setDescription(
                    characterListString.trim()
                )

                logger.log({
                    level: 'info',
                    message: `[CHARACTER] Finished constructing response embed.`
                });

                return [responseEmbed, buttons];
            }
            // Oops! Internal server error
            else if (request.statusCode == 500)
            {
                logger.log({
                    level: 'warn',
                    message: `[CHARACTER] Backend returned 500 INTERNAL SERVER ERROR.`
                });

                error_string = "There should be some error handling here...\nYou might have too many characters already created. The maximum is 9!"
                responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
                .addFields(
                    { name: "Oops! Something broke.", value: error_string }
                )

                    return [responseEmbed, []];
            }
            // If the status code is something else, we are outside of expected behaviour
            else
            {
                logger.log({
                    level: 'warn',
                    message: `[CHARACTER] Backend returned an unexpected response. Expression: ${expression}, StatusCode: ${request.statusCode}`
                });

                responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
                .addFields(
                    { name: "Unexpected Response", value: request.statusCode }
                )

                return [responseEmbed, []];
            }            
        }
        catch (error)
        {
            logger.log({
                level: 'error',
                message: `[CHARACTER] Encountered an exception in Character. Type: ${type}, User: ${user}, Stack Trace: ${error.stack}`
            });

            if (debug)
            {
                responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
                .addFields(
                    { name: "Unhandled Exception", value: error.toString() }
                )

                return [responseEmbed];
            }
            else {
                responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
                .addFields(
                    { name: "Oops!", value: "Something went wrong." }
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
            { name: "Not supported.", value: "Sorry, characters requires using slash (/) commands. See /help character for details!" }
        )
        
        return responseEmbed;
    },

    // Executes the command from an interaction (slash command) context
    async execute_interaction(interaction, logger) {
        user = interaction.user.id
        guild = 0
        
        if (interaction.guild)
        {
            guild = interaction.guild.id
        }

        channel = 0
        
        if (interaction.channel)
        {
            channel = interaction.channel.id
        }

        characterName = interaction.options.getString('name')
        characterId = interaction.options.getInteger('id')
        characterInit = interaction.options.getString('initiative')

        logger.log({
            level: 'info',
            message: `[CHARACTER] Received character interaction`
        });

        if (interaction.options.getSubcommand() === 'add') {
            var response = await this.execute_character('add', user, guild, channel, characterName, characterId, characterInit, false, logger)
        }
        else if (interaction.options.getSubcommand() === 'remove') {
            var response = await this.execute_character('remove', user, guild, channel, characterName, characterId, characterInit, false, logger)
        }
        else if (interaction.options.getSubcommand() === 'list') {
            var response = await this.execute_character('list', user, guild, channel, characterName, characterId, characterInit, false, logger)
        }

        // I feel like this is really bad, but we rollin' with it
        if (response.length == 2)
        {
            return await interaction.reply({ embeds: [response[0]], components: response[1] })
        }
        return await interaction.reply({ embeds: [response[0]]})
    },

    // Handles interactions from button presses
    async execute_button(interaction, logger) {
        user = interaction.user.id
        guild = interaction.guild.id
        channel = interaction.channel.id

        characterId = parseInt(interaction.customId.split('_')[1])

        logger.log({
            level: 'info',
            message: `[CHARACTER] Received character interaction via button`
        });

        var response = await this.execute_character('select', user, guild, channel, null, characterId, null, false, logger)
        return await interaction.update({ embeds: [response[0]], components: response[1] })
    }
};