# DON'T UPDATE TO alpine3.13, 1.14, see #41.
FROM node:14-alpine3.12
WORKDIR /app

# Install apprise, iputils for non-root ping, setpriv
RUN apk add --no-cache iputils setpriv dumb-init python3 py3-cryptography py3-pip py3-six py3-yaml py3-click py3-markdown py3-requests py3-requests-oauthlib && \
    pip3 --no-cache-dir install apprise && \
    rm -rf /root/.cache
