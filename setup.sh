#!/bin/bash

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Install Qwen Code CLI globally
npm install -g @qwen-code/qwen-code

# Verify installation
qwen-code --version