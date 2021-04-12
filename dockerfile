FROM python:3.9.4-slim as build

WORKDIR /wheels

# pyodbc install and drivers
RUN apt-get update && apt-get install curl -y && apt-get install gnupg -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install msodbcsql17 -y
RUN apt-get install gcc -y && apt-get install g++ -y
RUN apt-get -y install unixodbc-dev

COPY requirements.txt /opt/feyre/requirements.txt
RUN pip3 wheel -r /opt/feyre/requirements.txt



FROM python:3.9.4-slim

# pyodbc install and drivers
RUN apt-get update && apt-get install curl -y && apt-get install gnupg -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install msodbcsql17 -y
RUN apt-get install gcc -y && apt-get install g++ -y
RUN apt-get -y install unixodbc-dev

# create nonroot user
RUN adduser nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
WORKDIR /home/app

COPY --from=build /wheels /wheels
COPY --chown=nonroot:nonroot requirements.txt /home/app/
RUN pip3 install -r requirements.txt -f /wheels \
  && rm -rf /wheels \
  && rm -rf /root/.cache/pip/* \
  && rm requirements.txt

# testing
RUN apt-get install iputils-ping redis -y

USER nonroot

# Feyre.py
COPY --chown=nonroot:nonroot . .

ENTRYPOINT [ "python" ]
