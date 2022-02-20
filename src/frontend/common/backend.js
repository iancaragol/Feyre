// Common function to create a backend URL for the frontend to use
async function create_url({protocol = 'http', host = null, path = null, port = 5000}) {

    // Check that the path starts with a "/"
    if (path.startsWith('/') === false) {
        throw 'Path must start with a "/"';
    }

    // Get the hostname of the backend
    if (host !== null) {
        host = host;
    }
    else if (process.env.ENVIRONMENT == "prod" && host === null) {
        // If the environment is prod, use the "name" set via docker-compose
        host = "backend";
    }
    else if (process.env.ENVIRONMENT == "staging" && host === null) {
        // If the environment is staging, use the "name" set via docker-compose
        host = 'backend';
    }
    else if (process.env.ENVIRONMENT == "dev" && host === null) {
        // If the environment is dev, use the "name" set via docker-compose
        host = 'backend';
    }

    // Format the URL
    url = protocol + '://' + host + ':' + port + path;

    return url;

}

module.exports = { create_url };
