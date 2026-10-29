# Bot GRM - Discord Assistant for Search Task Evaluation

## Overview

This is a Discord bot designed to assist GRM (Search Task Evaluation) markers at Shopee. The bot provides quick and accurate responses based on official documentation and product policies. It helps team members understand marking guidelines, analyze specific cases, verify prohibited products, and clarify task-related concepts through interactive Discord commands and direct messaging.

The bot has been fully integrated with Replit hosting infrastructure, including keep-alive functionality and proper environment configuration management.

## User Preferences

Preferred communication style: Simple, everyday language (Portuguese).

## Recent Changes (August 2025)

**Task Analysis Improvements:**
- Enhanced command `!analisar` to properly separate SKIP analysis from individual product marking
- Clear distinction between task-level issues (SKIP) and product-level relevance marking
- Structured response format with separate sections for different analysis types
- Improved prompt engineering to prevent mixing of analysis contexts

**Prohibited Products Enhancement:**
- Added specific policy citation for products identified as PROIBIDO
- Enhanced `!verificar` command with structured output showing status, classification, and applicable policies
- New section in `!analisar` responses: "Produtos Proibidos e Políticas Aplicáveis"
- Visual indicators (🚫 for prohibited, ⚠️ for restricted, ✅ for allowed products)
- Direct connection between prohibited product detection and specific Shopee policy violations

## System Architecture

### Bot Framework
- **Discord.py Library**: Uses the discord.py library with command extensions for handling Discord interactions
- **Command System**: Implements a prefix-based command system (!command) with additional support for mentions and direct messages
- **Event-Driven Architecture**: Utilizes Discord's event system (on_ready, on_message) for handling bot lifecycle and user interactions
- **Replit Integration**: Fully integrated with Replit's workflow system and keep-alive server for 24/7 operation

### AI Integration
- **Google Gemini API**: Integrates Google's Gemini 1.5 Flash model for natural language processing and intelligent responses
- **Context-Aware Responses**: Uses loaded documentation to provide context-specific answers about GRM tasks and Shopee policies
- **Unicode Normalization**: Implements text normalization for better text processing and search capabilities
- **Embedded Service**: GeminiService class is embedded directly in the main bot file for simplified deployment

### Data Management
- **File-Based Documentation**: Stores knowledge base in text files (Search Task Evaluation.txt, Politicas Proibidos - Shopee.txt, REGRAS_IA.txt)
- **Enhanced AI Rules**: Includes specific interpretation rules and examples for precise task evaluation responses
- **Dynamic Content Loading**: Reads documentation files at runtime to provide up-to-date information
- **Multilingual Support**: Handles Portuguese content with proper UTF-8 encoding
- **Automatic File Setup**: Copies documentation files from source directory to root for easy access

### Configuration Management
- **Environment Variables**: Uses python-dotenv for secure credential management
- **Replit Secrets Integration**: Configured to read DISCORD_TOKEN and GEMINI_API_KEY from Replit secrets
- **Keep-Alive Server**: Flask server running on port 5000 for Replit hosting requirements

### Interaction Patterns
- **Multiple Input Methods**: Supports commands, mentions, and direct messages for flexible user interaction
- **Structured Responses**: Provides organized, easy-to-read responses with clear formatting using Discord embeds
- **Error Handling**: Implements comprehensive error handling for API failures, missing documentation, and command errors
- **Long Message Support**: Automatically splits long responses into multiple messages when needed

### Command Structure
- **!ajuda**: Shows all available commands and usage examples
- **!pergunta <pergunta>**: Answers questions about GRM tasks using official documentation
- **!explicar <conceito>**: Explains specific GRM concepts in detail
- **!analisar <keyword> <produtos>**: Analyzes specific marking cases with structured output separating SKIP analysis from individual product marking
- **!verificar <produto>**: Verifies if products are prohibited or restricted on Shopee
- **@mention**: Direct interaction through mentions for general questions
- **Direct Messages**: Private conversation support for one-on-one assistance

## External Dependencies

### APIs and Services
- **Google Gemini API**: For natural language processing and AI-powered responses
- **Discord API**: For bot functionality and server integration

### Python Libraries
- **discord.py**: Discord bot framework and API wrapper
- **python-dotenv**: Environment variable management
- **google-generativeai**: Google Gemini API client library

### Documentation Sources
- **Search Task Evaluation Documentation**: Internal guidelines for GRM task marking
- **Shopee Product Policies**: Official prohibited and restricted products documentation
- **AI Interpretation Rules (REGRAS_IA.txt)**: Detailed rules and examples for precise interpretation of task guidelines, including specific formatting requirements and response protocols

### Infrastructure Requirements
- **Python Runtime**: Requires Python environment with package management
- **Discord Bot Token**: Requires registered Discord application and bot token
- **Google AI API Key**: Requires Google AI Studio API access for Gemini integration