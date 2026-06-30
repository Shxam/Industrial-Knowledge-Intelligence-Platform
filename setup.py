"""
Setup script for IKIP development environment
"""
import os
import sys
import subprocess
from pathlib import Path


def print_step(message):
    """Print a setup step"""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")


def run_command(command, cwd=None):
    """Run a shell command"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"Error executing command: {e}")
        return False


def check_prerequisites():
    """Check if required tools are installed"""
    print_step("Checking Prerequisites")
    
    required = {
        "docker": "docker --version",
        "docker-compose": "docker-compose --version",
        "python": "python --version",
        "node": "node --version",
        "npm": "npm --version"
    }
    
    missing = []
    for tool, command in required.items():
        print(f"Checking {tool}...", end=" ")
        if run_command(command):
            print("✓")
        else:
            print("✗ (Not found)")
            missing.append(tool)
    
    if missing:
        print(f"\nMissing tools: {', '.join(missing)}")
        print("Please install them before continuing.")
        return False
    
    return True


def create_env_file():
    """Create .env file from example"""
    print_step("Creating Environment Configuration")
    
    if os.path.exists(".env"):
        print(".env file already exists. Skipping.")
        return True
    
    if os.path.exists(".env.example"):
        import shutil
        shutil.copy(".env.example", ".env")
        print("Created .env file from .env.example")
        print("⚠️  Please edit .env and add your API keys!")
        return True
    else:
        print("Error: .env.example not found")
        return False


def create_directories():
    """Create required directories"""
    print_step("Creating Required Directories")
    
    dirs = [
        "data/faiss_index",
        "data/uploads",
        "data/processed",
        "backend/logs",
        "frontend/build"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created: {dir_path}")
    
    return True


def setup_backend():
    """Setup backend environment"""
    print_step("Setting Up Backend")
    
    backend_dir = Path("backend")
    
    # Create virtual environment
    print("Creating Python virtual environment...")
    if not run_command("python -m venv venv", cwd=backend_dir):
        print("Failed to create virtual environment")
        return False
    
    # Activate and install dependencies
    print("\nInstalling Python dependencies...")
    if sys.platform == "win32":
        pip_cmd = r"venv\Scripts\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir):
        print("Failed to install dependencies")
        return False
    
    # Download spaCy model
    print("\nDownloading spaCy model...")
    if sys.platform == "win32":
        python_cmd = r"venv\Scripts\python"
    else:
        python_cmd = "venv/bin/python"
    
    run_command(f"{python_cmd} -m spacy download en_core_web_sm", cwd=backend_dir)
    
    return True


def setup_frontend():
    """Setup frontend environment"""
    print_step("Setting Up Frontend")
    
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("Frontend directory not found. Skipping for now.")
        return True
    
    # Install dependencies
    print("Installing Node.js dependencies...")
    if not run_command("npm install", cwd=frontend_dir):
        print("Failed to install dependencies")
        return False
    
    return True


def start_services():
    """Start Docker services"""
    print_step("Starting Docker Services")
    
    print("Starting Postgres, Neo4j, Redis, MinIO...")
    if not run_command("docker-compose up -d"):
        print("Failed to start Docker services")
        return False
    
    print("\nWaiting for services to be healthy...")
    run_command("docker-compose ps")
    
    return True


def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  IKIP (Pragya) - Development Environment Setup")
    print("="*60)
    
    steps = [
        ("Prerequisites Check", check_prerequisites),
        ("Environment Configuration", create_env_file),
        ("Directory Structure", create_directories),
        ("Backend Setup", setup_backend),
        # ("Frontend Setup", setup_frontend),  # Uncomment when frontend is ready
        ("Docker Services", start_services)
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please fix the errors and run setup.py again.")
            sys.exit(1)
    
    print_step("Setup Complete! 🎉")
    
    print("Next steps:")
    print("1. Edit .env file and add your API keys")
    print("2. Start the backend:")
    print("   cd backend")
    if sys.platform == "win32":
        print(r"   venv\Scripts\activate")
    else:
        print("   source venv/bin/activate")
    print("   uvicorn app.main:app --reload")
    print("\n3. Access the services:")
    print("   - API: http://localhost:8000")
    print("   - API Docs: http://localhost:8000/docs")
    print("   - Neo4j: http://localhost:7474")
    print("   - MinIO: http://localhost:9001")
    

if __name__ == "__main__":
    main()
