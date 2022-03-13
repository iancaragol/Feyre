// Import SlashCommandBuild to handle slash commands
const { SlashCommandBuilder } = require('@discordjs/builders');
const { MessageEmbed } = require('discord.js');

// Import our common backend functions
const backend = require("./../common/backend");

// Import our embed color constants
const embedColors = require('./../common/embed_colors')

// Status codes that can be returned by the backend
let status_codes = [200, 500, 504]

// Setup our HTTP library
const bent = require('bent');
const { execute_interaction } = require('./stats');
const get = bent('GET', status_codes)
const put = bent('PUT', status_codes);

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
        ),

    async execute_init(type, user, guild, channel, character = null, roll = null, count = null, debug = false)
    {
        try
        {
            // Ex: /initiative?user=12345&guild=4&channel=4&character_name=Carol&initiative_expression=1d20
            string_url = `/api/backendservice/initiative?user=${user}&guild=${guild}&channel=${channel}`

            if (character && roll)
            {
                string_url += `&character_name=${encodeURIComponent(character)}&initiative_expression=${encodeURIComponent(roll)}`
            }

            // Creates the URL to call the backend
            url = await backend.create_url({path: string_url});

            let request;
            let response;

            if(type === 'get')
            {
                request = await get(url);
                response = await request.json();
            }
            else if(type === 'join')
            {
                request = await put(url);
                response = await request.json();
            }

            console.log(response)
            
            // Backend should respond with a 200 OK
            if (request.statusCode == 200)
            {
                responseEmbed = new MessageEmbed().setColor(embedColors.successEmbedColor)
                responseEmbed.setTitle("Initiative")
                responseEmbed.setDescription(`Round: ${response.turn + 1}`)
                turnOrderString = ""
                
                for (let i = 0; i < response.characters.length; i++)
                {
                    if (i + 1 % response.turn == 0)
                    {
                        turnOrderString += `**[ ${response.characters[i].name} ]**\n`
                    }
                    else
                    {
                        turnOrderString += `${response.characters[i].name}\n`
                    }
                }

                responseEmbed.addField(
                    "Turn Order", turnOrderString
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

        if (interaction.options.getSubcommand() === 'join') {
            var response = await this.execute_init('join', user, guild, channel, character, roll, count)
            return await interaction.reply({ embeds: [response]})
        }
        else if (interaction.options.getSubcommand() === 'get') {
            var response = await this.execute_init('get', user, guild, channel, character, roll, count)
            return await interaction.reply({ embeds: [response]})
        }
    }
};