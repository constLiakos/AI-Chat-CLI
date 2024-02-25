# Chat-CLI: Terminal AI Assistant & Command Executor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Chat-CLI** is a terminal AI assistant that uses OpenAI Compatible API for natural language processing. It allows users to interact with the AI assistant through a command-line interface. Complex linux commands could be executed just by describing the desired result. 

- 💬 **Chat with AI** - Chat with LLM models throught terminal
- 🧠 **Personas** - Create Desired Persona based on the given system prompt.
- ⚡ **Run Command** - Run terminal commands by describing desired result.

## Features
- Utilizes the LLM model for natural language processing
- Can provide information such as the current date, time, user's name, and AI assistant's name
- Allows users to input commands for the AI assistant to execute
- Provides execution results for commands

## Setup
1. Install the required dependencies by running `pip install -r requirements.txt`
2. Create a `.env` file and set the environment variables, you can use as a reference the `.env.example` file
3. Create a prompt file with the initial prompt for the AI assistant to respond to.
4. Run ./install.sh to create an alias as ai.
5. Exit terminal and open a new one

## Usage
1. Run chat-cli `ai <User Prompt (Optional)>`
2. Enter your input when prompted by the AI assistant
3. To exit the program, type `quit` or `exit` when prompted for input

### Functions
#### AI Assistant Chat 
```bash
<User Prompt (Optional)>
```

#### Execute Command - `cmd`
Describe a command you want to execute
```bash
cmd <User prompt>
``` 

## Contributing
If you would like to contribute to this project, feel free to submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
