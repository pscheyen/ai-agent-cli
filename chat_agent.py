#!/usr/bin/env python3
"""
Simple CLI Chat Agent using OpenAI API
A beginner-friendly implementation for learning how to develop AI agents.

Features:
- Interactive CLI chat interface
- Conversation history management
- Error handling and graceful exits
- Environment variable configuration
- Simple and educational code structure
"""

import os
import sys
import json
from typing import List, Dict, Optional
import openai
from datetime import datetime


class ChatAgent:
    """A simple chat agent that uses OpenAI's API for conversation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the chat agent.
        
        Args:
            api_key: OpenAI API key (will try to get from environment if not provided)
            model: The OpenAI model to use for responses
        """
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.api_key = api_key or self._get_api_key()
        
        if not self.api_key:
            print("❌ Error: OpenAI API key not found!")
            print("Please set your OpenAI API key in one of these ways:")
            print("1. Set the OPENAI_API_KEY environment variable")
            print("2. Pass it as a parameter when creating the ChatAgent")
            print("3. Create a .env file with OPENAI_API_KEY=your_key_here")
            sys.exit(1)
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # System message to define the agent's behavior
        self.system_message = {
            "role": "system",
            "content": "You are a helpful AI assistant. Be friendly, informative, and concise in your responses."
        }
    
    def _get_api_key(self) -> Optional[str]:
        """Try to get API key from environment variables or .env file."""
        # First try environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return api_key
        
        # Try to read from .env file
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("OPENAI_API_KEY="):
                        return line.split("=", 1)[1].strip()
        except FileNotFoundError:
            pass
        
        return None
    
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_response(self, user_message: str) -> str:
        """
        Get a response from the AI agent.
        
        Args:
            user_message: The user's input message
            
        Returns:
            The AI agent's response
        """
        try:
            # Add user message to history
            self.add_message("user", user_message)
            
            # Prepare messages for API call
            messages = [self.system_message] + [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in self.conversation_history[-10:]  # Keep last 10 messages for context
            ]
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            # Extract and add AI response
            ai_response = response.choices[0].message.content
            self.add_message("assistant", ai_response)
            
            return ai_response
            
        except openai.AuthenticationError:
            return "❌ Error: Invalid API key. Please check your OpenAI API key."
        except openai.RateLimitError:
            return "❌ Error: Rate limit exceeded. Please wait a moment and try again."
        except openai.APIError as e:
            return f"❌ Error: OpenAI API error: {str(e)}"
        except Exception as e:
            return f"❌ Error: Unexpected error: {str(e)}"
    
    def save_conversation(self, filename: Optional[str] = None):
        """Save the conversation history to a JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        try:
            with open(filename, "w") as f:
                json.dump(self.conversation_history, f, indent=2)
            print(f"💾 Conversation saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving conversation: {str(e)}")
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history.clear()
        print("🗑️  Conversation history cleared!")
    
    def show_help(self):
        """Display help information."""
        help_text = """
🤖 Chat Agent Help

Commands:
  /help     - Show this help message
  /save     - Save conversation to file
  /clear    - Clear conversation history
  /quit     - Exit the chat agent
  /history  - Show conversation history

Just type your message to chat with the AI!
        """
        print(help_text)
    
    def show_history(self):
        """Display the conversation history."""
        if not self.conversation_history:
            print("📝 No conversation history yet.")
            return
        
        print("\n📝 Conversation History:")
        print("-" * 50)
        for i, msg in enumerate(self.conversation_history, 1):
            role = msg["role"].title()
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            print(f"{i}. {role}: {content}")
        print("-" * 50)


def main():
    """Main function to run the chat agent."""
    print("🤖 Welcome to the Simple CLI Chat Agent!")
    print("=" * 50)
    
    # Initialize the chat agent
    try:
        agent = ChatAgent()
        print("✅ Chat agent initialized successfully!")
        print("💡 Type /help for available commands")
        print("💡 Type /quit to exit")
        print("-" * 50)
    except Exception as e:
        print(f"❌ Failed to initialize chat agent: {str(e)}")
        return
    
    # Main chat loop
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                command = user_input.lower()
                
                if command == "/quit" or command == "/exit":
                    print("👋 Goodbye! Thanks for chatting!")
                    break
                elif command == "/help":
                    agent.show_help()
                    continue
                elif command == "/save":
                    agent.save_conversation()
                    continue
                elif command == "/clear":
                    agent.clear_history()
                    continue
                elif command == "/history":
                    agent.show_history()
                    continue
                else:
                    print(f"❓ Unknown command: {user_input}")
                    print("💡 Type /help for available commands")
                    continue
            
            # Get AI response
            print("🤖 AI: ", end="", flush=True)
            response = agent.get_response(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for chatting!")
            break
        except EOFError:
            print("\n👋 Goodbye! Thanks for chatting!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main() 
