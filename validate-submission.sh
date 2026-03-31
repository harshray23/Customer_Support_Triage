#!/usr/bin/env bash

PING_URL="${1:-}"
REPO_DIR="${2:-.}"

echo "========================================"
echo "  OpenEnv Submission Validator"
echo "========================================"

echo ""
echo "Step 1: Checking HF Space..."

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H "Content-Type: application/json" \
  -d '{}' \
  "$PING_URL/reset")

if [ "$HTTP_CODE" = "200" ]; then
  echo "PASSED: HF Space is live"
else
  echo "FAILED: HF Space not responding"
  exit 1
fi

echo ""
echo "Step 2: Checking Dockerfile..."

if [ -f "$REPO_DIR/Dockerfile" ]; then
  echo "PASSED: Dockerfile exists"
else
  echo "FAILED: No Dockerfile found"
  exit 1
fi

echo ""
echo "Step 3: Running openenv validate..."

if ! command -v openenv &>/dev/null; then
  echo "FAILED: openenv not installed"
  exit 1
fi

openenv validate

echo ""
echo "========================================"
echo "ALL CHECKS PASSED ✅"
echo "READY TO SUBMIT 🚀"
echo "========================================"
