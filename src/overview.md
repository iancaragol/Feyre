# Overview

### Permissions
https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=2147559488&scope=bot%20applications.commands

Staging bot:
https://discord.com/api/oauth2/authorize?client_id=505120997658329108&permissions=2147493952&scope=bot%20applications.commands

Dev bot:
https://discord.com/api/oauth2/authorize?client_id=896435492273393694&permissions=2147559488&scope=bot%20applications.commands


### Style Guide:
https://google.github.io/styleguide/pyguide.html

### Deployment

1. Clone the Feyre repro
2. Install dependencies (docker, docker-compose)
3. Update all environment files (backend.env, frontend.env, prometheus.env, redis-primary.env, redis-secondary.env)
4. Start containers (docker-compose up --build d)

### Regristration

If deploying a new command, then that command will need to be registered. Run the following to run register.js in the frontend container

`docker-compose run --rm frontend "register.js" && echo "\e[32m[#] Registered all slash commands in the src/frontend/commands folder!\e[0m"`

# Backend Service

## Controller

The controller receives the REST request, parses the arguments, and kicks off an operation. The operation result will be returned in the response body.

It is the duty of the controller to increment the command counter and add the user to the user set in redis.

## Operation

An operation is created and executed by the controller whenever a request is received. This is where the majority of the work is done. For example, the RollOperation parses a dice expression and evaluates it. It returns a RollOperatioModel.

## Model

The model is where any properties that are used by the operation are stored. The model should have a to_dict method which will be used to create the JSON response.

# Sync Service

Sync service runs in a separate docker container and periodically syncronizes the local Redis store with Azure Storage.

On service startup, Sync Service will download all data from the Azure Storage and recreate it in Redis UNLESS the data stored in Redis is more up-to-date. (Meaning the SyncService crashed, while BackendService continued writing to Redis)

Once per hour, sync service will take all of the data stored in Redis and mirror it in Azure Storage.

# Redis Models

#### key:updated_time
    All keys have an additional key called updated_time. This is the timestamp of the last update time for that key.
    So when SETTING a key, this value must be SET too.

    Ex:
        user_set:updated_time

#### user_set
    Set of all User IDs. All REST requests will have user=? in the query parameters. That value will ALWAYS be added to the users set

    Ex: [414560806764675074, 680486242424586250, 107624977066381312]

#### user_(user_id)
    Json object representing any of the user's personal data, such as characters, saved rolls, etc...

    Ex: user_107624977066381312 : 
    {
        characters = {
            
        }
    }
    
#### c_command
    Contains the counter for that specific command. Rather than having a c_command:updated_time we set c_:updated_time. Keeping track of the update time for each individual counter is not needed.

    Ex: c_roll

#### init_(channel_id)
    Not sure what this will look like yet.