#!/bin/sh

# Start nginx in background and get its process ID
nginx & # & makes it run in background
nginx_pid=$! # $! stores PID of last background process

# Keep monitoring other containers
while true; do
    # Check if any service1 or service2 containers are still running
    # >/dev/null -> Redirect output to nowhere
    # >/dev/null -> Redirect output to nowhere
    # 2>&1 -> Redirect stderr to stdout
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