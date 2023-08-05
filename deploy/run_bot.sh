#!/bin/bash

# Run python script in the background and detach the session
nohup /home/$(whoami)/gpt/bin/python bot.py >> output.log 2>&1 &

# Disown the process to make sure it keeps running after the terminal is closed
disown
