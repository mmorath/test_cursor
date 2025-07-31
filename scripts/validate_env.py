#!/usr/bin/env python3
"""
Environment validation script for Hello World Codex.
Checks if required environment variables are set.
"""

from pathlib import Path

from dotenv import dotenv_values


def validate_env():
    """Validate environment configuration."""
    project_root = Path(__file__).parent.parent

    # Check if .env.example exists
    env_example_path = project_root / ".env.example"
    if not env_example_path.exists():
        print("⚠️  .env.example not found. Creating template...")
        create_env_example(env_example_path)
        return True

    # Check if .env exists
    env_path = project_root / ".env"
    if not env_path.exists():
        print("❌ .env file not found. Please create one based on .env.example")
        return False

    # Load environment files
    try:
        required = dotenv_values(env_example_path)
        current = dotenv_values(env_path)
    except Exception as e:
        print(f"❌ Error reading environment files: {e}")
        return False

    # Check for missing variables
    missing = [key for key in required if key not in current]

    if missing:
        print(f"❌ Missing entries in .env: {missing}")
        return False
    else:
        print("✅ .env complete and valid.")
        return True


def create_env_example(env_example_path):
    """Create a template .env.example file."""
    template = """# Hello World Codex Environment Configuration
# Copy this file to .env and fill in your values

# Application Settings
APP_NAME=HelloWorldCodex
APP_VERSION=1.0.0
DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database (if needed)
# DATABASE_URL=postgresql://user:password@localhost/dbname

# API Keys (if needed)
# API_KEY=your_api_key_here

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""

    with open(env_example_path, "w") as f:
        f.write(template)

    print(f"✅ Created {env_example_path}")


if __name__ == "__main__":
    success = validate_env()
    exit(0 if success else 1)
