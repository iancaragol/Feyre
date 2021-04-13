run: # For running Feyre in a Docker container
	@echo "\e[34m[#] Killing old docker processes\e[0m"
	@docker-compose rm -fs || exit 1

	@echo "\e[34m[#] Building docker container\e[0m"
	@docker-compose up --build -d || exit 1

	@echo "\e[32m[#] Feyre container is now running!\e[0m"

push-test: # Builds and pushes Feyre image to ACR (test)
	@az acr login -n feyre
	@docker build -t feyre.azurecr.io/feyre:test .
	@docker push feyre.azurecr.io/feyre:test

push-release: # Builds and pushes Feyre image to ACR (release)
	@az acr login -n feyre
	@docker build -t feyre.azurecr.io/feyre:latest .
	@docker push feyre.azurecr.io/feyre:latest