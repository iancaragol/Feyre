# This is the entry method for both Backend and Sync services
# Doing it this way allows us to have the common folder for shared classes
import backend_service.app
import sync_service.app
import public_service.app

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-s', '--service', type = str, help = "The service to start")
    args = parser.parse_args()

    service = args.service.lower()

    if service == "backend":
        print("[#] Starting Backend Service on this container")
        backend_service.app.main()
    elif service == "sync":
        print("[#] Starting Sync Service on this container")
        sync_service.app.main()
    elif service == "public":
        print("[#] Starting Public Stats on this container")
        public_service.app.main()