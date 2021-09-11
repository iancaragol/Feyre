# Backend Service

## Controller

The controller receives the REST request, parses the arguments, and kicks off an operation. The operation result will be returned in the response body.

It is the duty of the controller to increment the command counter and add the user to the user set in redis.

## Operation

An operation is created and executed by the controller whenever a request is received. This is where the majority of the work is done. For example, the RollOperation parses a dice expression and evaluates it. It returns a RollOperatioModel.

## Model

The model is where any properties that are used by the operation are stored. The model should have a to_dict method which will be used to create the JSON response.

# Sync Service

Sync service runs in a seperate docker container and periodically syncronizes the local Redis store with the Mongo DB.

On service startup, Sync Service will download all data from the MongoDB and recreate it in Redis UNLESS the data stored in Redis is more up-to-date. (Meaning the SyncService crashed, while BackendService continued writing to Redis)

Once per hour, sync service will take all of the data stored in Redis and format it as JSON objects to be stored in the Mongo DB.

Currently the following is stored in redis:

Key: "users"
Type: set
Values: The user IDs of any users

Key: "command" (ex: roll)
Type: int
Values: The number of times this command has been used


### References:
https://livecodestream.dev/post/python-flask-api-starter-kit-and-project-layout/
https://github.com/bitnami/bitnami-docker-redis#configuration

### Style Guide:
https://google.github.io/styleguide/pyguide.html

#### Adding a new command

#### Step 1:
    Create the controller, model, and operations

#### Step 2:
    Add the new command to the StatsModel

#### Step 3:
    Register the new controller's blueprint in app.py

# Redis Models

#### user_set
    Set of all User IDs. All REST requests will have user=? in the query parameters. That value will ALWAYS be added to the users set

    Ex: [414560806764675074, 680486242424586250, 107624977066381312]

#### user_id
    Json object representing any of the user's personal data, such as characters, saved rolls, etc...

    Ex: user_107624977066381312 : 
    {
        characters = {
            
        }
    }