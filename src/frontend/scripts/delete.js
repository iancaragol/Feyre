require('dotenv').config();

const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');

const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
const CLIENT_ID = BigInt(process.env.CLIENT_ID);
    
// This method is pretty ugly but it works
// Simply do a register
// Then copy the ID of the command you want to delete
// Put it here
// Then run this script like you would register
const commandToDelete = "952660384085577808"

const rest = new REST({ version: '9' }).setToken(DISCORD_TOKEN);

rest.get(Routes.applicationCommands(CLIENT_ID))
    .then(data => {
        const promises = [];
        for (const command of data) {
            if (command.id == commandToDelete)
            {
                console.log('Deleting the command!');
                const deleteUrl = `${Routes.applicationCommands(CLIENT_ID)}/${command.id}`;
                promises.push(rest.delete(deleteUrl));
                console.log('Deleted.');
            }
        }
        console.log('All done.');
        return Promise.all(promises);
});
