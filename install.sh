#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Social Media Sentiment Analysis Tool - Installation${NC}"
echo "======================================================"
echo

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3 &>/dev/null; then
    python_version=$(python3 --version)
    echo -e "${GREEN}Found ${python_version}${NC}"
else
    echo -e "${RED}Python 3 not found. Please install Python 3.7 or higher.${NC}"
    exit 1
fi

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
if command -v python3 -m venv &>/dev/null; then
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created successfully.${NC}"
else
    echo -e "${RED}Failed to create virtual environment. Please install venv module.${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}Virtual environment activated.${NC}"

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}Dependencies installed successfully.${NC}"

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    echo -e "\n${YELLOW}Creating .env file from example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env file created. Please edit it to add your LinkedIn credentials.${NC}"
fi

# Install the package in development mode
echo -e "\n${YELLOW}Installing package in development mode...${NC}"
pip install -e .
echo -e "${GREEN}Package installed in development mode.${NC}"

echo
echo -e "${GREEN}Installation complete!${NC}"
echo
echo "To use the tool, follow these steps:"
echo "1. Edit the .env file to add your LinkedIn credentials"
echo "2. Activate the virtual environment with 'source venv/bin/activate'"
echo "3. Run the tool with 'python src/main.py --company \"Company Name\"'"
echo
echo "For a quick test with mock data (no LinkedIn credentials needed):"
echo "python src/main.py --company \"Example Corp\" --use-mock-data"
echo 