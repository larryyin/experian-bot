#!/bin/bash

# Update the package lists
sudo yum update -y

# Install necessary packages for building Python
sudo yum install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Install pyenv
curl https://pyenv.run | bash

# Add pyenv to bash so command line can use it
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

# Install Python 3.11 using pyenv
pyenv install 3.11.0
pyenv global 3.11.0

# Verify that the correct version of Python is being used
python --version

# Install virtualenv
pip install virtualenv

# Create a virtual environment named "gpt"
python -m venv gpt

# Activate the virtual environment
source gpt/bin/activate

# Update pip
pip install --upgrade pip

# Install the required Python packages
pip install python-dotenv openai gradio langchain pgvector tiktoken psycopg2-binary

chmod +x run_bot.sh