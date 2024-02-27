#!/bin/bash
current_dir=`pwd`
command="python3 ${current_dir}/ai-chat-cli.py"
# Remove old alias
sed -i '/^alias ai=/d' ~/.bashrc
# Create new alias
echo "alias ai='${command}'" >> ~/.bashrc
echo "Installation Completed"