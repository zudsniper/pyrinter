#!/bin/bash

echo "building pyrinter..."

# Update package list
sudo apt update -y

# Install required packages
sudo apt install -y libcups2-dev curl

# Check if Poetry is already installed
if ! command -v poetry &> /dev/null; then
  # Install Poetry
  curl -sSL https://install.python-poetry.org | python3 -
else
  echo "Poetry is already installed. Cool, moving on!"
fi

# Navigate to project directory TODO: this is the current directory!
# cd pyrinter || echo "pyrinter directory not found, fail! Exiting..."

# Install project dependencies
poetry install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
  cp .env.template .env
  echo "created .env, please edit it with discord webhooks and printer stub name"
fi

# give executable permissions
sudo chmod +x pyrinter.py

# Run the server
poetry run python pyrinter.py