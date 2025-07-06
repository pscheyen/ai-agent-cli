#!/usr/bin/env python3
"""
Simple CLI Chat Agent using OpenAI API
A beginner-friendly implementation for learning how to develop AI agents.

This file demonstrates key concepts in AI agent development:
1. API Integration - How to connect to external AI services
2. State Management - Keeping track of conversation history
3. Error Handling - Graceful handling of network/API failures
4. CLI Design - Building user-friendly command-line interfaces
5. Environment Configuration - Secure management of API keys

Features:
- Interactive CLI chat interface with emoji indicators
- Conversation history management with timestamps
- Built-in commands for saving, clearing, and viewing history
- Comprehensive error handling for various failure scenarios
- Multiple ways to configure API keys (environment, .env file, direct)
- Educational code structure with detailed comments

Learning Path:
- Start by understanding the ChatAgent class structure
- Then look at how the main() function orchestrates everything
- Finally, explore the helper methods for specific functionality
"""

# Standard library imports - these come with Python
import os          # For environment variables and file operations
import sys         # For system operations like exiting the program
import json        # For saving/loading conversation data
from typing import List, Dict, Optional  # Type hints for better code documentation
from datetime import datetime  # For timestamping messages

# Third-party imports - these need to be installed via pip
import openai      # OpenAI's official Python library for API access

# Try to import python-dotenv for .env file support
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("💡 Tip: Install python-dotenv for .env file support: pip install python-dotenv")


class ChatAgent:
    """
    A simple chat agent that uses OpenAI's API for conversation.
    
    This class demonstrates several important concepts in AI agent development:
    
    1. **Encapsulation**: All agent functionality is contained within this class
    2. **State Management**: The agent maintains conversation history and configuration
    3. **API Integration**: Handles communication with OpenAI's API
    4. **Error Handling**: Graceful handling of API failures and configuration issues
    5. **Configuration Management**: Multiple ways to set up API keys
    
    Key Attributes:
    - model: Which OpenAI model to use (e.g., gpt-3.5-turbo, gpt-4)
    - conversation_history: List of all messages in the current conversation
    - api_key: The OpenAI API key for authentication
    - client: The OpenAI client instance for making API calls
    - system_message: Instructions that define the AI's behavior and personality
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the chat agent with configuration and setup.
        
        This is the constructor method that runs when you create a new ChatAgent instance.
        It sets up all the necessary components for the agent to function.
        
        Args:
            api_key: OpenAI API key (will try to get from environment if not provided)
                     This allows flexibility in how you configure the agent
            model: The OpenAI model to use for responses
                   Different models have different capabilities and costs
                   - gpt-3.5-turbo: Fast, cost-effective, good for most tasks
                   - gpt-4: More capable, but slower and more expensive
        """
        # Store the model name for API calls
        self.model = model
        
        # Initialize empty conversation history
        # This will store all messages as dictionaries with role, content, and timestamp
        self.conversation_history: List[Dict[str, str]] = []
        
        # Get API key from parameter or try to find it automatically
        # The or operator means "use api_key if provided, otherwise call _get_api_key()"
        self.api_key = api_key or self._get_api_key()
        
        # Validate that we have an API key - without it, we can't make API calls
        if not self.api_key:
            print("❌ Error: OpenAI API key not found!")
            print("\nPlease set your OpenAI API key in one of these ways:")
            print("1. Set the OPENAI_API_KEY environment variable:")
            print("   export OPENAI_API_KEY='your-api-key-here'")
            print("2. Pass it as a parameter when creating the ChatAgent")
            print("3. Create a .env file with OPENAI_API_KEY=your_key_here")
            print("\n💡 Copy env_example.txt to .env and add your key")
            
            # Show security tips to help the user
            self._show_security_tips()
            
            # Exit the program if no API key is available
            sys.exit(1)
        
        # Validate the API key format
        if not self._validate_api_key(self.api_key):
            print("⚠️  Warning: API key format looks unusual")
            print("   OpenAI API keys typically start with 'sk-' and are ~51 characters")
            print("   Please check your API key format")
            # Don't exit - let the API call fail if the key is actually invalid
        
        # Initialize OpenAI client with our API key
        # This client will handle all communication with OpenAI's servers
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Define the system message that sets the AI's behavior
        # This message is sent with every API call to instruct the AI how to respond
        self.system_message = {
            "role": "system",  # Special role that defines the AI's instructions
            "content": "You are a helpful AI assistant. Be friendly, informative, and concise in your responses."
        }
    
    def _get_api_key(self) -> Optional[str]:
        """
        Try to get API key from multiple secure sources.
        
        This method demonstrates a common pattern in software development:
        "Configuration Fallback" - try multiple sources for configuration in order of preference.
        
        Security Best Practices Implemented:
        1. Environment variables (most secure for production)
        2. .env files (convenient for development)
        3. Clear error messages for missing configuration
        
        The underscore prefix (_get_api_key) indicates this is a "private" method
        that's intended for internal use within the class, not for external calling.
        
        Returns:
            The API key if found, None otherwise
        """
        # Method 1: Try to get from environment variable (BEST PRACTICE)
        # Environment variables are the most secure way to store sensitive data
        # They're not stored in your code and can be different on different machines
        # This is the recommended approach for production environments
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key.strip():  # Check it's not empty
            print("🔑 Using API key from environment variable")
            return api_key.strip()
        
        # Method 2: Try to load from .env file (GOOD FOR DEVELOPMENT)
        # .env files are convenient for local development
        # They should NEVER be committed to version control
        if DOTENV_AVAILABLE:
            try:
                # Load environment variables from .env file
                load_dotenv()
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key and api_key.strip():
                    print("🔑 Using API key from .env file")
                    return api_key.strip()
            except Exception as e:
                print(f"⚠️  Warning: Could not load .env file: {e}")
        
        # Method 3: Try to read .env file manually (fallback)
        # This is a backup method if python-dotenv is not available
        try:
            with open(".env", "r") as f:  # Open file in read mode
                for line in f:  # Read file line by line
                    # Skip comments and empty lines
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Look for line that starts with OPENAI_API_KEY=
                        if line.startswith("OPENAI_API_KEY="):
                            # Split on first = and take everything after it
                            api_key = line.split("=", 1)[1].strip()
                            if api_key:
                                print("🔑 Using API key from .env file (manual read)")
                                return api_key
        except FileNotFoundError:
            # If .env file doesn't exist, that's okay - just continue
            pass
        except Exception as e:
            print(f"⚠️  Warning: Could not read .env file: {e}")
        
        # If we get here, no API key was found
        return None
    
    def _validate_api_key(self, api_key: str) -> bool:
        """
        Validate that an API key looks correct.
        
        This is a basic validation - it doesn't test if the key actually works,
        but it checks for common formatting issues.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            True if the key looks valid, False otherwise
        """
        if not api_key:
            return False
        
        # OpenAI API keys typically start with 'sk-' and are 51 characters long
        if not api_key.startswith("sk-"):
            return False
        
        if len(api_key) < 20:  # Minimum reasonable length
            return False
        
        return True
    
    def _show_security_tips(self):
        """
        Display security best practices for API key management.
        
        This helps users understand how to properly secure their API keys.
        """
        print("\n🔐 Security Best Practices for API Keys:")
        print("=" * 50)
        print("✅ DO:")
        print("   • Use environment variables: export OPENAI_API_KEY='your-key'")
        print("   • Use .env files (add to .gitignore)")
        print("   • Rotate keys regularly")
        print("   • Use different keys for development/production")
        print("   • Set up billing alerts in OpenAI dashboard")
        print()
        print("❌ DON'T:")
        print("   • Hardcode keys in your source code")
        print("   • Commit .env files to version control")
        print("   • Share keys in chat logs or screenshots")
        print("   • Use the same key across multiple projects")
        print("   • Leave keys in public repositories")
        print()
        print("💡 For production: Consider using secret management services")
        print("   (AWS Secrets Manager, Azure Key Vault, etc.)")
        print("=" * 50)
    
    def add_message(self, role: str, content: str):
        """
        Add a message to the conversation history.
        
        This method demonstrates data persistence and state management.
        Every message (both from user and AI) gets stored with metadata
        so we can maintain context and provide features like conversation history.
        
        Args:
            role: Who sent the message ("user" or "assistant")
            content: The actual message text
        """
        # Create a message dictionary with all relevant information
        message = {
            "role": role,                    # Who sent it
            "content": content,              # What was said
            "timestamp": datetime.now().isoformat()  # When it was sent (ISO format)
        }
        
        # Add the message to our conversation history list
        # append() adds the item to the end of the list
        self.conversation_history.append(message)
    
    def get_response(self, user_message: str) -> str:
        """
        Get a response from the AI agent.
        
        This is the core method that demonstrates AI agent functionality:
        1. Takes user input
        2. Maintains conversation context
        3. Makes API call to AI service
        4. Handles various types of errors
        5. Returns formatted response
        
        Args:
            user_message: The user's input message
            
        Returns:
            The AI agent's response (or error message if something went wrong)
        """
        try:
            # Step 1: Store the user's message in our conversation history
            # This ensures we have a complete record of the conversation
            self.add_message("user", user_message)
            
            # Step 2: Prepare the messages for the API call
            # OpenAI's API expects a list of message dictionaries
            # We include the system message first, then recent conversation history
            
            # Start with the system message that defines AI behavior
            messages = [self.system_message]
            
            # Add recent conversation history (last 10 messages)
            # This provides context so the AI knows what was discussed before
            # We limit to 10 messages to avoid hitting token limits and keep costs down
            recent_messages = self.conversation_history[-10:]  # Get last 10 messages
            for msg in recent_messages:
                # Extract just the role and content (API doesn't need timestamp)
                messages.append({
                    "role": msg["role"], 
                    "content": msg["content"]
                })
            
            # Step 3: Make the API call to OpenAI
            # This is where we actually communicate with the AI service
            response = self.client.chat.completions.create(
                model=self.model,        # Which AI model to use
                messages=messages,       # The conversation context
                max_tokens=500,          # Maximum length of response (controls cost)
                temperature=0.7          # Creativity level (0.0 = very focused, 1.0 = very creative)
            )
            
            # Step 4: Extract the AI's response from the API response
            # The API returns a complex object, we need to get the actual text
            ai_response = response.choices[0].message.content
            
            # Step 5: Store the AI's response in our conversation history
            self.add_message("assistant", ai_response)
            
            # Step 6: Return the response to the user
            return ai_response
            
        # Error handling - this is crucial for a robust application
        # Different types of errors require different responses
        
        except openai.AuthenticationError:
            # This happens if the API key is invalid or missing
            return "❌ Error: Invalid API key. Please check your OpenAI API key."
            
        except openai.RateLimitError:
            # This happens if you've made too many requests too quickly
            return "❌ Error: Rate limit exceeded. Please wait a moment and try again."
            
        except openai.APIError as e:
            # This catches other API-related errors
            return f"❌ Error: OpenAI API error: {str(e)}"
            
        except Exception as e:
            # This catches any other unexpected errors (network issues, etc.)
            return f"❌ Error: Unexpected error: {str(e)}"
    
    def save_conversation(self, filename: Optional[str] = None):
        """
        Save the conversation history to a JSON file.
        
        This method demonstrates file I/O (Input/Output) operations and data persistence.
        It allows users to save their conversations for later review or analysis.
        
        Args:
            filename: Optional custom filename. If not provided, generates one with timestamp.
        """
        # Generate a filename if none was provided
        # This ensures each saved conversation has a unique name
        if not filename:
            # Create timestamp in format: YYYYMMDD_HHMMSS
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        try:
            # Open file in write mode ("w") - this will create the file if it doesn't exist
            # or overwrite it if it does exist
            with open(filename, "w") as f:
                # json.dump() converts Python objects to JSON format
                # indent=2 makes the JSON file human-readable with proper formatting
                json.dump(self.conversation_history, f, indent=2)
            
            # Confirm successful save to the user
            print(f"💾 Conversation saved to {filename}")
            
        except Exception as e:
            # Handle any file writing errors (permissions, disk full, etc.)
            print(f"❌ Error saving conversation: {str(e)}")
    
    def clear_history(self):
        """
        Clear the conversation history.
        
        This method demonstrates state management - the ability to reset
        the agent's memory and start fresh. This is useful when you want
        to start a new conversation without the context of previous messages.
        """
        # clear() removes all items from the list, making it empty again
        # This is more efficient than setting to [] because it doesn't create a new list
        self.conversation_history.clear()
        
        # Provide user feedback that the operation was successful
        print("🗑️  Conversation history cleared!")
    
    def show_help(self):
        """
        Display help information.
        
        This method demonstrates user interface design - providing clear,
        accessible information about how to use the application. Good help
        text is essential for user experience.
        """
        # Multi-line string (triple quotes) allows for formatted text
        # This creates a clean, readable help display
        help_text = """
🤖 Chat Agent Help

Commands:
  /help     - Show this help message
  /save     - Save conversation to file
  /clear    - Clear conversation history
  /quit     - Exit the chat agent
  /history  - Show conversation history
  /security - Show API key security best practices

Just type your message to chat with the AI!
        """
        print(help_text)
    
    def show_history(self):
        """
        Display the conversation history.
        
        This method demonstrates data presentation and user interface design.
        It shows how to format and display complex data (conversation history)
        in a user-friendly way, with proper formatting and truncation for readability.
        """
        # Check if there's any history to show
        if not self.conversation_history:
            print("📝 No conversation history yet.")
            return
        
        # Display header with visual separator
        print("\n📝 Conversation History:")
        print("-" * 50)  # Create a line of dashes for visual separation
        
        # Loop through all messages with enumeration
        # enumerate() gives us both the index (i) and the message (msg)
        # start=1 makes the numbering start at 1 instead of 0
        for i, msg in enumerate(self.conversation_history, 1):
            # Capitalize the role for better display (e.g., "user" -> "User")
            role = msg["role"].title()
            
            # Truncate long messages to keep display clean
            # If message is longer than 100 characters, show first 100 + "..."
            content = msg["content"]
            if len(content) > 100:
                content = content[:100] + "..."  # Truncate and add ellipsis
            
            # Display the message with number, role, and content
            print(f"{i}. {role}: {content}")
        
        # Add closing separator for visual consistency
        print("-" * 50)


def main():
    """
    Main function to run the chat agent.
    
    This function demonstrates the overall application flow and user interaction.
    It's the entry point of the program and shows how to:
    1. Initialize components
    2. Handle user input in a loop
    3. Process commands and regular messages
    4. Handle various types of program termination
    5. Provide user feedback throughout the process
    """
    # Welcome message and visual setup
    print("🤖 Welcome to the Simple CLI Chat Agent!")
    print("=" * 50)  # Visual separator for better readability
    
    # Step 1: Initialize the chat agent
    # This is where we create our ChatAgent instance and handle any setup errors
    try:
        # Create a new ChatAgent instance
        # This will automatically try to get the API key and set up the OpenAI client
        agent = ChatAgent()
        
        # Success feedback
        print("✅ Chat agent initialized successfully!")
        print("💡 Type /help for available commands")
        print("💡 Type /quit to exit")
        print("-" * 50)  # Visual separator
        
    except Exception as e:
        # If initialization fails (e.g., no API key), show error and exit gracefully
        print(f"❌ Failed to initialize chat agent: {str(e)}")
        return  # Exit the function, which ends the program
    
    # Step 2: Main chat loop
    # This is the core of the application - it runs continuously until the user quits
    while True:
        try:
            # Get user input with a prompt
            # strip() removes any leading/trailing whitespace
            user_input = input("\n👤 You: ").strip()
            
            # Handle empty input (user just pressed Enter)
            # continue skips the rest of the loop and starts over
            if not user_input:
                continue
            
            # Step 3: Handle commands (messages starting with /)
            if user_input.startswith("/"):
                # Convert to lowercase for case-insensitive command matching
                command = user_input.lower()
                
                # Command processing - each command has a specific action
                if command == "/quit" or command == "/exit":
                    # Exit the program gracefully
                    print("👋 Goodbye! Thanks for chatting!")
                    break  # Exit the while loop
                    
                elif command == "/help":
                    # Show help information
                    agent.show_help()
                    continue  # Skip to next iteration (don't process as AI message)
                    
                elif command == "/save":
                    # Save conversation to file
                    agent.save_conversation()
                    continue
                    
                elif command == "/clear":
                    # Clear conversation history
                    agent.clear_history()
                    continue
                    
                elif command == "/history":
                    # Show conversation history
                    agent.show_history()
                    continue
                    
                elif command == "/security":
                    # Show security best practices
                    agent._show_security_tips()
                    continue
                    
                else:
                    # Unknown command - provide helpful feedback
                    print(f"❓ Unknown command: {user_input}")
                    print("💡 Type /help for available commands")
                    continue
            
            # Step 4: Handle regular messages (not commands)
            # This is where we actually interact with the AI
            
            # Show that we're processing (the AI is thinking)
            print("🤖 AI: ", end="", flush=True)
            # end="" prevents a newline, flush=True ensures immediate display
            
            # Get response from the AI agent
            response = agent.get_response(user_input)
            
            # Display the AI's response
            print(response)
            
        # Step 5: Handle various ways the program might end
        
        except KeyboardInterrupt:
            # User pressed Ctrl+C - exit gracefully
            print("\n\n👋 Goodbye! Thanks for chatting!")
            break
            
        except EOFError:
            # User pressed Ctrl+D (EOF) - exit gracefully
            print("\n👋 Goodbye! Thanks for chatting!")
            break
            
        except Exception as e:
            # Catch any other unexpected errors
            print(f"\n❌ Unexpected error: {str(e)}")


# This is a Python idiom that ensures the main() function only runs
# when this file is executed directly (not when imported as a module)
if __name__ == "__main__":
    main() 
