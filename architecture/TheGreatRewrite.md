# The Great Rewrite

## Why is this neccessary?
Feyre has been built using the discord.py library created by Rapptz. Going forward, this library will no longer be supported. I would like to thank Danny for all of his hard work. Without discord.py, Feyre would not exist. Through discord.py I was able to create something that is *actually used* and has a had positive impact on people's lives by helping them play D&D and other RPG games. 

https://gist.github.com/Rapptz/4a2f62751b9600a31a0d3c78100287f1

Discord is requiring all bots to move to the new slash command framework by April 2022. As of now, Feyre has no support for slash commands, and now that discord.py has been archived, another solution needs to be found. My views on this requirement match Rapptz's, and can be read in the link above.

## What will need to be done?

Feyre will be split into two services. The Frontend Service will be written in JavaScript using the discord.js library. Discord.js is by far the most used framework for Discord bots, and should continue to be supported for the foreseeable future. It would be very painful to completely rewrite Feyre in JS (especially since I have never used it) so all of the existing code will be turned into the Feyre Backend Service.

Feyre Frontend service will handle the interactions with discord (slash commands, buttons, etc...). For every command, it will make calls to the Backend Service using a REST API. The backend service will respond with a JSON object that will be parsed and formatted by the Frontend Service before being sent to the discord user.

There are many advantages to this approach. The BE service will be be more scalable and easier to maintain. Much of the code I have written for Feyre will be able to be reused with some minor refactoring (returning JSON objects). The FE service will be very simple and only handle making requests to the BE and parsing the response. This minimizes the amount of JS code that needs to be written. Yay!

## Phases

### Phase 1

In Phase 1, the goal will be to standup the Frontend and Backend Services in individual VMs. Phase 1 needs to be completed before April 2022.

There are three major work areas:

- Refactoring existing code to into a RESTful microservice
- Writing the Frontend Service using discord.js
- Migrating all existing data over to a single Mongo DB and creating the new infrastructure

### Phase 2

In Phase 2, the goal will be to improve the reliability and scalability of Feyre by moving the Backend Service into a Kubernetes cluster. This way Feyre will be able to handle lots of concurrent requests.
