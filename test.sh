#!/bin/bash

# Test script for Chat Assistant System

echo "🧪 Testing Chat Assistant System"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function
test_endpoint() {
    local name=$1
    local url=$2
    local expected=$3

    echo -n "Testing $name... "

    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)

    if [ "$response" = "$expected" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $response)"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC} (Expected $expected, got $response)"
        ((TESTS_FAILED++))
    fi
}

# Test if services are running
echo "1. Service Health Checks"
echo "------------------------"

test_endpoint "Backend Health" "http://localhost:8000/health" "200"
test_endpoint "Frontend Health" "http://localhost:8501/_stcore/health" "200"
test_endpoint "Backend API Docs" "http://localhost:8000/docs" "200"

echo ""
echo "2. API Endpoints"
echo "----------------"

# Test tools endpoint
echo -n "Testing tools list... "
tools_response=$(curl -s "http://localhost:8000/tools")
if echo "$tools_response" | grep -q "calculate"; then
    echo -e "${GREEN}✓ PASSED${NC} (Tools listed successfully)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (Tools not listed)"
    ((TESTS_FAILED++))
fi

echo ""
echo "3. Agent Functionality"
echo "----------------------"

# Test chat endpoint with streaming
echo -n "Testing chat endpoint... "
chat_response=$(curl -s -X POST "http://localhost:8000/chat" \
    -H "Content-Type: application/json" \
    -d '{"message": "What is 2 + 2?"}' \
    --max-time 30)

if [ -n "$chat_response" ]; then
    echo -e "${GREEN}✓ PASSED${NC} (Chat response received)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAILED${NC} (No response from chat)"
    ((TESTS_FAILED++))
fi

echo ""
echo "4. Docker Services"
echo "------------------"

# Check if containers are running
echo -n "Checking frontend container... "
if docker ps | grep -q "frontend"; then
    echo -e "${GREEN}✓ RUNNING${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ NOT RUNNING${NC}"
    ((TESTS_FAILED++))
fi

echo -n "Checking backend container... "
if docker ps | grep -q "backend"; then
    echo -e "${GREEN}✓ RUNNING${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ NOT RUNNING${NC}"
    ((TESTS_FAILED++))
fi

echo -n "Checking mcp-server container... "
if docker ps | grep -q "mcp-server"; then
    echo -e "${GREEN}✓ RUNNING${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ NOT RUNNING${NC}"
    ((TESTS_FAILED++))
fi

echo ""
echo "=================================="
echo "Test Results"
echo "=================================="
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Check the output above.${NC}"
    echo ""
    echo "Troubleshooting tips:"
    echo "1. Check if all services are running: docker compose ps"
    echo "2. View logs: docker compose logs"
    echo "3. Restart services: docker compose restart"
    exit 1
fi
