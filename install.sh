#!/bin/bash
current_dir=`pwd`
command="python3 ${current_dir}/chat-cli.py"
echo $command
echo "alias ai='${command}'" >> ~/.bashrc
echo "Installation Completed"