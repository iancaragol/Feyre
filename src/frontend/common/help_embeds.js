const { MessageEmbed, MessageActionRow, MessageButton } = require('discord.js');
const embedColors = require('./embed_colors')

var embedColor = embedColors.helpEmbedColor
var documentationUrl = "https://feyre.readthedocs.io/en/latest/"

// ================================================
//                      HELP
// ================================================
var helpEmbed = new MessageEmbed()
helpEmbed.setColor(embedColors.helpEmbedColor)
helpEmbed.setTitle("Feyre - Help")

var helpDescription = `All commands use **/** or **@Feyre**
 
To learn more about a command you can type **/help <command>**
**Ex: /help roll**`
helpEmbed.setDescription(helpDescription)

helpEmbed.setThumbnail("https://www.kindpng.com/picc/m/689-6892346_d20-png-transparent-png-download.png")

// Main body
var commandFieldBody = `**roll** - Roll complicated dice expressions

**stats** - Feyre usage statistics
**health** - Feyre service health`

helpEmbed.addField(
    "Commands", commandFieldBody
)

// Documentation button
var helpRow = new MessageActionRow()
helpRow.addComponents(
    new MessageButton()
    .setLabel('Documentation')
    .setStyle('LINK')
    .setURL(documentationUrl)
)

// ================================================
//                COMMAND NOT FOUND
// ================================================
var notfoundEmbed = new MessageEmbed()
notfoundEmbed.setColor(embedColors.errorEmbedColor)
notfoundEmbed.setTitle("Command not found")

var notfoundEmbedDescription = `I could not find that command. Try /help for a list of commands!`
notfoundEmbed.setDescription(notfoundEmbedDescription)

// ================================================
//                      ROLL
// ================================================
var rollEmbed = new MessageEmbed()
rollEmbed.setColor(embedColor)
rollEmbed.setTitle("roll")

var rollDescription = 
`/roll can be used to roll dice of any size with complicated expressions.

Dice are represented with the standard [# of dice]d[size of dice] format.

Ex:
/roll expression:4d6
/roll expression:(1d6+2)*2`

var skillCheckField =
`
**[<, >, >=, <=, =]**
Skill checks can be built into the dice expression using the < and > symbols.

    1d20 > 15 -> True if greater than 15, False otherwise`

var conditionalOperatorField = 
`    
**[t]**
You can add a condition using the letter 't'. Think of the letter 't' as 'then', if the condition on the left side is True, then the expression on the right side will be evaulated.

    1d20 > 15 t 2d6+3 -> If 1d20 is greater than 15 THEN roll 2d6+3`

var countOperatorField = 
`
**[c#]**
You can repeat a dice roll using the count operator, 'c' followed by a number. This needs to be put at the END of an expression, it will roll the expression independently count # of times.

    2d6+3c3 -> Roll 2d6+3 3 times`

var keepOperatorField = 
`
**[k#]**
When rolling multiple dice, you can use the keep operator, 'k' follwed by a number, to keep the highest number of dice.

    5d20k3 -> Roll 5d20 keep the highest 3

**[kl#]**
Keep Lowest, Not implemented yet, will be the inverse of keep`

var advantageOperatorField = 
`Not implemented yet, you can acheive this advantage with keep operator.

    2d20k1 -> Roll 2d20, keep the highest`

var explodeOperatorField = 
`**[e#]**
To explode dice, you can use the explode operator 'e' followed by a number. If the dice rolled is greater tan or equal to #, then it will explode (rolled again, added to the total).

    3d6e3 -> Roll 3d6, roll an extra d6 for each roll GREATER THAN OR EQUAL to 3

**[eo#]**
To explode *ON* a specific dice, you can use the explode ON operator 'eo' followed by a number. This will roll an additional dice ONLY IF the value is EQUAL to #.

    3d6eo3 -> Roll 3d6, roll an addional dice for each roll EQUAL to 3`
rollEmbed.setDescription(rollDescription)
rollEmbed.addField("Skill Checks", skillCheckField)
rollEmbed.addField("Conditional Operator - if then", conditionalOperatorField)
rollEmbed.addField("Count Operator", countOperatorField)
rollEmbed.addField("Keep / Drop Operator", keepOperatorField)
rollEmbed.addField("Advantage / Disadvantage", advantageOperatorField)
rollEmbed.addField("Explode Operator", explodeOperatorField)

module.exports = { helpEmbed, helpRow, notfoundEmbed, rollEmbed };