# Developer Updates

**Have any questions? Reach out on the Feyre discord channel!**

---

## 4/16/22 - The Great Rewrite & Slash Commands

On 4/30/2022 Discord will be requiring all Verified bots to apply for the Message Content intent in order to read the content of messages. You can read more about this change here:

To summarize, most bots (including Feyre) rely on reading Message Content in order parse commands. For example, to parse a command like `!roll`, Feyre will look at all messages starting with an `!`, then if that `!` is followed by `roll`, it will treat the message as a roll command. Even though Feyre has been a verified bot for almost 3 years, it does not meet the strict requirements for the Message Content intent. This means that Feyre has no choice but to move to Slash Commands.

### What does this mean for Feyre?

All commands will use Slash commands going forward. This will definently take some getting used to!

Check how to use the new commands [here](commands.md)

### Why were so many commands removed?

In order to support Slash commands, and build a more reliable bot, I re-wrote Feyre completetly from scratch with reliability, performance, and observability in mind. This was a major effort and I focussed on creating a framework that would be easy to build upon.

Feyre's usage statistics show that two commands make up over 96% of commands used. I chose to focus on improving the top 2 used commands (rolls and initiative tracking) first. Other commands such as monster-manual and spellbook will be added back at a later date.

| Command      | % of total uses |
| -----------  | -----------     |
| roll         | 93              |
| init         | 5.6             |
| help         | .7%             |
| spell        | .3%             |
| deck of many | .2%             |
| everything else | .2%          |
