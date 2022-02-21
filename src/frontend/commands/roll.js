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
const get = bent(status_codes);

// Export the module which handles the slash command
module.exports = {
    data: new SlashCommandBuilder()
        .setName('roll') // The name of the Discord Slash command
        .setDescription('Roll any size/type of dice with modifiers!') // The description of the Discord Slash command
        .addStringOption(option =>
            option.setName('expression')
                .setDescription('The expression to roll. Ex: 1d20+5')
                .setRequired(true))
        .addBooleanOption(boolean =>
            boolean.setName('debug')
                .setDescription('Literally does nothing.')
                .setRequired(false),
        ),

    async execute_roll(expression, user, guild = 0, debug = false)
    {
        try
        {
            expression = encodeURIComponent(expression)
            string_url = "/api/backendservice/roll?user=" + user + "&expression=" + expression + "&verbose=false"

            // Creates the URL to call the backend
            url = await backend.create_url({path: string_url});

            // Make the request
            let request = await get(url);
            let response = await request.json()
            
            // Backend should respond with a 200 OK if the dice expression is valid
            if (request.statusCode == 200)
            {
                // Todo (IAN)
                // Need to put this in a loop for multiple dice counts.
                // Or display it differently, probably just the totals.
                // Otherwise it will hit the max size of an embed and be hard to read
                responseEmbed = new MessageEmbed().setColor(embedColors.successEmbedColor)

                if (response.parent_result.length > 1)
                {
                    for (let i = 0; i < response.parent_result.length; i++)
                    {
                        total_field = "🎲 -> " + response.parent_result[i].total
                        expression_value = response.parent_result[i].expression + " -> " + response.parent_result[i].md_result
                        responseEmbed.addFields(
                            { name: total_field, value: expression_value }
                        )
                    }
                }
                else
                {
                    total_field = "🎲 -> " + response.parent_result[0].total
                    expression_value = response.parent_result[0].expression + " -> " + response.parent_result[0].md_result
                
                    responseEmbed.addFields(
                        { name: total_field, value: expression_value }
                    )
                }
                
                return responseEmbed;
            }
            // If the backend could not parse the expression, we should get a 400 BAD REQUEST
            // For now we get a 500
            else if (request.statusCode == 500)
            {
                error_string = response.expression + "\n" + response.exception_message
                responseEmbed = new MessageEmbed().setColor(embedColors.errorEmbedColor)
                .addFields(
                    { name: "Invalid Dice Expression", value: error_string }
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
            console.log("Caught Unhandled Exception in ROLL")
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
        var expression = "1d20"
        var debug = false
    
        return await this.execute_roll(expression, user, guild, debug);
    },

    // Executes the command from an interaction (slash command) context
    async execute_interaction(interaction) {
        expression = interaction.options.getString('expression')
        debug = interaction.options.getString('debug')
        user = interaction.user.id
        guild = interaction.guild.id

        var response = await this.execute_roll(expression, user, guild, debug)
        return await interaction.reply({ embeds: [response]})
    }
};