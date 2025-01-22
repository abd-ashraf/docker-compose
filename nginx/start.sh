#!/bin/sh
# Start Nginx in the background
nginx &
nginx_pid=$!

# Retry mechanism for missing services
max_retries=30  # Wait up to 30 seconds for services
retry_interval=1 # Check every 1 second

# Wait for services to be available before continuing
echo "Waiting for backend services to start..."
for i in $(seq 1 $max_retries); do
    if curl -s service1-1:8199 >/dev/null 2>&1 || \
       curl -s service1-2:8199 >/dev/null 2>&1 || \
       curl -s service1-3:8199 >/dev/null 2>&1 || \
       curl -s service2:5000/system_info >/dev/null 2>&1; then
        echo "Backend services are up!"
        break
    fi
    echo "Retry $i/$max_retries: Waiting for services..."
    sleep $retry_interval
done

# Monitor backend services
while true; do
    if ! curl -s service1-1:8199 >/dev/null 2>&1 && \
       ! curl -s service1-2:8199 >/dev/null 2>&1 && \
       ! curl -s service1-3:8199 >/dev/null 2>&1 && \
       ! curl -s service2:5000/system_info >/dev/null 2>&1; then
        echo "All services are down. Shutting down Nginx..."
        kill $nginx_pid
        wait $nginx_pid  # Ensure Nginx exits properly
        exit 0  # Graceful shutdown
    fi
    sleep 5
done
