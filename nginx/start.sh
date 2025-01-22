#!/bin/sh
# Start nginx in foreground
nginx &
nginx_pid=$!

# Retry mechanism for missing services
max_retries=30  # Wait up to 30 seconds for services
retry_interval=1 # Check every 1 second

# Wait for services to be available
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

# Keep monitoring backend services
while true; do
    if ! curl -s service1-1:8199 >/dev/null 2>&1 && \
       ! curl -s service1-2:8199 >/dev/null 2>&1 && \
       ! curl -s service1-3:8199 >/dev/null 2>&1 && \
       ! curl -s service2:5000/system_info >/dev/null 2>&1; then
        echo "All services are down. Restarting Nginx..."
        kill $nginx_pid
        sleep 5  # Wait before restarting
        nginx &
        nginx_pid=$!
    fi
    sleep 5
done
