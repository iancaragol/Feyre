
## Controller

The controller receives the REST request, parses the arguments, and kicks off an operation. The operation result will be returned in the response body.

It is the duty of the controller to increment the command counter and add the user to the user set in redis.

## Operation

An operation is created and executed by the controller whenever a request is received. This is where the majority of the work is done. For example, the RollOperation parses a dice expression and evaluates it. It returns a RollOperatioModel.

## Model

The model is where any properties that are used by the operation are stored. The model should have a to_dict method which will be used to create the JSON response.

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