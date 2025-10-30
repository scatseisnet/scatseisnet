#!/bin/bash
# Quick test script for scatseisnet

set -e

echo "=================================================="
echo "ScatSeisNet Test Suite"
echo "=================================================="
echo ""

# Check Python version
echo "Python version:"
python --version
echo ""

# Run tests with coverage
echo "Running tests with coverage..."
pytest tests/ -v --cov=scatseisnet --cov-report=term-missing --cov-report=html

echo ""
echo "=================================================="
echo "Test Summary"
echo "=================================================="
echo "✓ All tests passed!"
echo "✓ Coverage report generated in htmlcov/"
echo ""
echo "To view coverage report:"
echo "  open htmlcov/index.html"
echo ""
