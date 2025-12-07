#!/bin/bash
# Test script for the network monitoring backend API

echo "Testing Network Monitoring Tool Backend API"
echo "==========================================="
echo ""

BASE_URL="http://localhost:5000/api"

# Test health check
echo "1. Testing health check endpoint..."
curl -s "${BASE_URL}/health" | python3 -m json.tool
echo ""
echo ""

# Test user registration
echo "2. Testing user registration..."
REGISTER_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}')
echo "$REGISTER_RESPONSE" | python3 -m json.tool
echo ""

# Extract token
TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "Failed to get token, trying to login..."
  LOGIN_RESPONSE=$(curl -s -X POST "${BASE_URL}/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser","password":"testpass123"}')
  echo "$LOGIN_RESPONSE" | python3 -m json.tool
  TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)
fi

echo ""
echo "Token: ${TOKEN:0:20}..."
echo ""

# Test authenticated endpoints
if [ -n "$TOKEN" ]; then
  echo "3. Testing get current user..."
  curl -s "${BASE_URL}/auth/me" \
    -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
  echo ""
  echo ""

  echo "4. Testing add device..."
  curl -s -X POST "${BASE_URL}/devices" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"Test Router","ip_address":"192.168.1.1","device_type":"router"}' | python3 -m json.tool
  echo ""
  echo ""

  echo "5. Testing get devices..."
  curl -s "${BASE_URL}/devices" \
    -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
  echo ""
  echo ""

  echo "6. Testing network traffic monitoring..."
  curl -s "${BASE_URL}/monitoring/traffic" \
    -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
  echo ""
  echo ""

  echo "7. Testing system stats..."
  curl -s "${BASE_URL}/monitoring/system" \
    -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
  echo ""
  echo ""

  echo "8. Testing available protocols..."
  curl -s "${BASE_URL}/analysis/protocols" \
    -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
  echo ""
fi

echo "==========================================="
echo "Backend API tests completed!"
