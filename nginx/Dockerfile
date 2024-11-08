FROM nginx:alpine

RUN apk add apache2-utils

COPY nginx.conf /etc/nginx/nginx.conf

COPY html /usr/share/nginx/html

COPY htpasswd /etc/nginx/.htpasswd