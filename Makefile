run: # For running Feyre in a Docker container
	@echo "\e[34m[#] Killing old docker processes\e[0m"
	@docker-compose rm -fs || exit 1

	@echo "\e[34m[#] Building docker container\e[0m"
	@docker-compose up --build -d || exit 1

	@echo -e "\e[32m[#] Feyre container is now running!\e[0m"

register: # This just registers the dev environment
	@docker-compose run --rm frontend "register.js" && echo "\e[32m[#] Registered all slash commands in the src/frontend/commands folder!\e[0m"

push-azure:
	script/build-and-push-azure

build:
	@script/build

destroy:
	@script/destroy
