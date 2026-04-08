#!/usr/bin/env python3
"""
Battery-Life Lab Backend Runner
Run the FastAPI server for the battery optimization platform
"""

import uvicorn
import os
import sys

def main():
    """Main entry point"""
    print("🚀 Starting Battery-Life Lab Backend")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found. Please run from the project root directory.")
        sys.exit(1)

    # Check if dependencies are installed
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencies loaded successfully")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)

    print("🌐 Starting FastAPI server on http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print("=" * 50)

    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )

if __name__ == "__main__":
    main()