#!/bin/sh
# Start nginx in foreground
nginx &
nginx_pid=$!

# Keep monitoring other containers
while true; do
    # Check if any service1 replicas or service2 are running
    if ! curl -s service1-1:8199 >/dev/null 2>&1 && \
       ! curl -s service1-2:8199 >/dev/null 2>&1 && \
       ! curl -s service1-3:8199 >/dev/null 2>&1 && \
       ! curl -s service2:5000/system_info >/dev/null 2>&1; then
        # All services are down, kill nginx process
        kill $nginx_pid
        exit 0
    fi
    sleep 1
done