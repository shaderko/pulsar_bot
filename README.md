# Pulsar Bot

A feature-rich Discord bot built with py-cord for managing community servers with levels, voting, birthday tracking, and dynamic channel management.

## Features

### Core Systems
- **Level System**: XP-based ranking with 21 custom ranks from Initiate to Overlord
- **Birthday Tracking**: Automated birthday announcements and reminders
- **Voting System**: Create and manage polls within Discord
- **Split Channels**: Dynamic voice channel creation for organized discussions
- **Activity Monitoring**: Track user engagement and presence

### Commands
- **Basic Commands**: Essential utility functions
- **Admin Tools**: Server management capabilities
- **Reminder System**: Set and manage personal reminders
- **Image Generation**: Dynamic banner and image creation

## Quick Start

### Prerequisites
- Python 3.10+
- MongoDB instance
- Discord Bot Token
- Mistral AI API Key (optional, for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pulsar_bot
   ```

2. **Install dependencies**
   ```bash
   pipenv install
   pipenv shell
   ```

3. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your tokens and configuration
   ```

4. **Run with Docker (recommended)**
   ```bash
   docker-compose up -d
   ```

   **Or run locally**
   ```bash
   python bot.py
   ```

### Environment Variables
```env
DISCORD_TOKEN=your_discord_bot_token
MISTRAL_API_KEY=your_mistral_api_key
MONGO_URL=mongodb://localhost:27017/pulsar_bot
```

## Configuration

Key settings in `config.py`:
- **Guild IDs**: Target Discord servers
- **XP System**: Base XP (200), active XP (15), level curve (1.4)
- **Rank Names**: 21-tier progression system
- **Channel IDs**: AFK and birthday announcement channels

## Project Structure

```
pulsar_bot/
├── bot.py              # Main bot entry point
├── config.py           # Configuration and settings
├── models/             # Database models
├── cogs/
│   ├── commands/       # Slash command implementations
│   └── events/         # Event handlers
├── images/             # Image generation and assets
├── markov/             # Markov chain models
└── db_backup/          # Database backup utilities
```

## Development

### Adding New Features
1. Create new cogs in `cogs/commands/` or `cogs/events/`
2. Add extension to `config.startup_extensions`
3. Follow existing patterns for database models in `models/`

### Database
Uses MongoDB with MongoEngine ODM. Models are defined in `models/models.py`.

## Tech Stack

- **Framework**: py-cord (Discord.py fork)
- **Database**: MongoDB with MongoEngine
- **Image Processing**: Pillow
- **AI Integration**: Mistral AI
- **Text Generation**: Markovify
- **Deployment**: Docker + Docker Compose

## License

MIT License