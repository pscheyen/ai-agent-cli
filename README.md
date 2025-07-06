# Simple CLI Chat Agent

A beginner-friendly CLI chat agent that uses OpenAI's API. Perfect for learning how to develop AI agents!

## Features

- 🤖 Interactive CLI chat interface
- 💬 Conversation history management
- 🛡️ Comprehensive error handling
- 💾 Save conversations to JSON files
- 🔧 Easy configuration with environment variables
- 📚 Educational code structure with detailed comments

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Setup

1. **Clone or download this project**
   ```bash
   cd ai-agent-cli
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key** 🔐

   **Recommended: Environment variable (most secure)**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

   **For development: .env file**
   ```bash
   # Copy the example file
   cp env_example.txt .env
   
   # Edit .env and add your API key
   nano .env
   ```

   **Direct parameter (for testing only)**
   ```python
   agent = ChatAgent(api_key="your-api-key-here")
   ```

   **🔒 Security Note:** Never commit your API key to version control!
   The `.gitignore` file is configured to prevent accidental commits of `.env` files.

## Usage

### Basic Usage

Run the chat agent:
```bash
python chat_agent.py
```

### Available Commands

Once the agent is running, you can use these commands:

- `/help` - Show help information
- `/save` - Save conversation to a JSON file
- `/clear` - Clear conversation history
- `/history` - Show conversation history
- `/security` - Show API key security best practices
- `/quit` or `/exit` - Exit the chat agent

### Example Session

```
🤖 Welcome to the Simple CLI Chat Agent!
==================================================
✅ Chat agent initialized successfully!
💡 Type /help for available commands
💡 Type /quit to exit
--------------------------------------------------

👤 You: Hello! How are you today?

🤖 AI: Hello! I'm doing great, thank you for asking! I'm here and ready to help you with any questions or tasks you might have. How can I assist you today?

👤 You: Can you explain what an AI agent is?

🤖 AI: An AI agent is a software program that can perceive its environment, make decisions, and take actions to achieve specific goals. Think of it like a digital assistant that can:

1. **Perceive**: Take in information from various sources (text, images, data, etc.)
2. **Think**: Process that information and make decisions
3. **Act**: Execute actions based on those decisions

AI agents can be simple (like a chatbot) or complex (like autonomous robots). They're designed to operate with some level of autonomy and can learn from their experiences to improve over time.

👤 You: /save

💾 Conversation saved to conversation_20241201_143022.json

👤 You: /quit

👋 Goodbye! Thanks for chatting!
```

## Learning Resources

This project is designed to be educational. Here are some concepts you'll learn:

### Key Concepts

1. **API Integration**: How to connect to external services (OpenAI)
2. **Error Handling**: Graceful handling of API errors and edge cases
3. **State Management**: Maintaining conversation history
4. **CLI Design**: Building user-friendly command-line interfaces
5. **Environment Configuration**: Managing API keys and settings securely

### Code Structure

- `ChatAgent` class: Main agent logic
- `main()` function: CLI interface and user interaction
- Helper methods: History management, file operations, etc.

### Extending the Agent

Try these modifications to learn more:

1. **Add new commands**: Implement `/config` to change model settings
2. **Memory management**: Add conversation summarization for long chats
3. **Multi-modal support**: Add image processing capabilities
4. **Plugin system**: Allow custom functions/tools
5. **Streaming responses**: Show responses as they're generated

## Troubleshooting

### Common Issues

**"OpenAI API key not found"**
- Make sure you've set the `OPENAI_API_KEY` environment variable
- Or create a `.env` file with your API key

**"Invalid API key"**
- Check that your OpenAI API key is correct
- Ensure you have credits in your OpenAI account

**"Rate limit exceeded"**
- Wait a moment and try again
- Consider upgrading your OpenAI plan if this happens frequently

**Import errors**
- Make sure you've installed the requirements: `pip install -r requirements.txt`

## Contributing

Feel free to fork this project and experiment! Some ideas:
- Add support for different AI models
- Implement conversation export in different formats
- Add a web interface
- Create a plugin system

## License

This project is open source and available under the MIT License.

## Support

If you run into issues or have questions, check the troubleshooting section above or open an issue on GitHub.

Happy coding! 🚀 