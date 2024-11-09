FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Create directory for pid file
RUN mkdir -p /var/run && \
    chmod -R 777 /var/run

COPY nginx.conf /etc/nginx/nginx.conf
COPY html /usr/share/nginx/html
COPY htpasswd /etc/nginx/.htpasswd
COPY start.sh /start.sh

RUN chmod +x /start.sh

CMD ["/start.sh"]