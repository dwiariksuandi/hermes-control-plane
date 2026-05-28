#!/bin/bash
set -e
echo "Initiating Hermes Phoenix Protocol..."

# Terminate any existing ghost processes
pkill -f uvicorn || true

# Wait for clean state
sleep 2

# Launch dashboard daemon
python3 /home/hiryu/.hermes/launch_dashboard.py

# Wait and verify server is up
for i in $(seq 1 5); do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/status 2>/dev/null || echo "000")
    if [ "$STATUS" = "200" ]; then
        echo "Hermes System Online. Mission Control Dashboard is LIVE."
        exit 0
    fi
    sleep 1
done

echo "ERROR: Server failed to respond after 5 seconds."
exit 1
