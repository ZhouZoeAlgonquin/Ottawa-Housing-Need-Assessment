"""Setup script for the Housing Needs Assessment Catalog."""
import os
import subprocess
import sys
import shutil
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.11."""
    if sys.version_info.major != 3 or sys.version_info.minor != 11:
        print("Error: Python version must be exactly 3.11 (e.g., 3.11.x)")
        sys.exit(1)
    print(f"Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_dependencies():
    """Install Python dependencies."""
    print("\n Installing Python dependencies...")
    try:
        print("  -> Upgrading pip...")
        try:
            subprocess.check_call([
                sys.executable,
                "-m", "pip", "install", "--upgrade", "pip"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("pip upgraded")
        except:
            print("pip upgrade skipped (continuing anyway)")

        # Install requirements
        print("  -> Installing requirements...")
        subprocess.check_call([
            sys.executable,
            "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        print("\n  Troubleshooting:")
        print("  Try upgrading pip: python -m pip install --upgrade pip")
        print("  Then install requirements: pip install -r requirements.txt")
        sys.exit(1)


def create_env_file():
    """Create .env file if it doesn't exist."""
    print("\n[2/4] Setting up environment variables...")
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print(".env file already exists (skipping)")
        return
    
    if env_example.exists():
        print("  -> Copying .env.example to .env...")
        shutil.copy(env_example, env_file)
        print(".env file created from .env.example")
    else:
        print(".env.example not found. Creating default .env file...")
        default_env = """# MongoDB Configuration
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USERNAME=admin
MONGODB_PASSWORD=admin123
MONGODB_AUTH_SOURCE=admin
MONGODB_DB_NAME=hna_catalog

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
"""
        with open(env_file, "w") as f:
            f.write(default_env)
        print("Default .env file created")
    
    print("Please review and update .env file with your configuration if needed")


def check_docker():
    """Check if Docker is available."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return False


def check_docker_compose():
    """Check if docker-compose is available."""
    try:
        result = subprocess.run(
            ["docker-compose", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return False

def check_docker_daemon() -> bool:
    """
    Checks if the Docker CLI tool is installed AND the Docker daemon is running.
    Returns True if both are ready, False otherwise.
    """
    print("\n[3/4] Checking Docker daemon status (Pre-check for MongoDB Docker start)...")
    try:
        # Run a simple Docker command, suppressing output, and check for success (exit code 0)
        subprocess.run(
            ['docker', 'info'], 
            check=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL,
            timeout=10 # Set a timeout
        )
        print("  Docker daemon is running.")
        return True
    
    except FileNotFoundError:
        print("  Docker command not found. Please ensure Docker Desktop is installed and in your system's PATH.")
        return False
    
    except subprocess.CalledProcessError:
        print("  Docker daemon is not running. Please start **Docker Desktop**.")
        return False
        
    except subprocess.TimeoutExpired:
        print("  Docker command timed out after 10 seconds.")
        return False

def start_mongodb_docker():
    """Start MongoDB using Docker Compose."""
    print("\n[3/4] Starting MongoDB with Docker...")
    
    if not check_docker():
        print("Docker not found. Skipping Docker MongoDB setup.")
        return False
    
    docker_compose_file = Path("docker-compose.yml")
    if not docker_compose_file.exists():
        print("docker-compose.yml not found. Skipping Docker MongoDB setup.")
        return False
    
    try:
        # Check if MongoDB container is already running
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=hna_mongodb", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "hna_mongodb" in result.stdout:
            print("MongoDB container is already running")
            return True
        
        # Start MongoDB container
        print("  -> Starting MongoDB container...")
        if check_docker_compose():
            subprocess.check_call(
                ["docker-compose", "up", "-d", "mongodb"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            # Try with docker compose (newer syntax)
            subprocess.check_call(
                ["docker", "compose", "up", "-d", "mongodb"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        # Wait a moment for MongoDB to start
        import time
        print("  -> Waiting for MongoDB to start...")
        time.sleep(6)
        
        print("MongoDB started successfully with Docker")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to start MongoDB with Docker: {e}")
        print("  You may need to start MongoDB manually")
        return False
    except Exception as e:
        print(f"Error starting MongoDB with Docker: {e}")
        return False


def check_mongodb_connection():
    """Check if MongoDB is accessible."""
    print("\n[4/4] Checking MongoDB connection...")
    try:
        from pymongo import MongoClient
        from app.config import settings
        
        client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        print("MongoDB connection successful")
        print("(This confirms an existing MongoDB server is running.)")
        client.close()
        return True
    except ImportError:
        print("pymongo not installed yet (this is normal during setup)")
        return False
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        print("  Please ensure MongoDB is running:")
        print("    - Docker: docker-compose up -d mongodb")
        print("    - Or Local: mongod --dbpath /path/to/your/db")
        print("    - Or update MONGODB_URI in .env")
        return False


def main():
    """Main setup function."""
    print("=" * 60)
    print("Housing Needs Assessment Catalog - Setup")
    print("=" * 60)
    
    check_python_version()
    install_dependencies()
    create_env_file()

    # Check if Docker is available and running
    docker_is_ready = check_docker_daemon()

    # Only try to start MongoDB with Docker if the daemon is ready
    if docker_is_ready:
        start_mongodb_docker()
    else:
        print("  Skipping attempt to start MongoDB via Docker Compose.")

    # Check MongoDB connection (Will succeed if local/external DB is running)
    mongodb_connected = check_mongodb_connection()

    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)

    if not mongodb_connected:
        print("\nMongoDB is not connected. Please:")
        print("Start MongoDB:")
        print("  - Docker: docker-compose up -d mongodb")
        print("  - Or Local: mongod --dbpath /path/to/your/db")
        print("  - Or update MONGODB_URI in .env if using remote MongoDB")
    
    print("\nNext steps:")
    print("1. Review and update .env file with your configuration")
    print("2. Load data: python data_load/run_all.py")
    print("=" * 60)


if __name__ == "__main__":
    main()

