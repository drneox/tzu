# Main entry point for FastAPI application
# This file allows maintaining relative imports in api.py

from api import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
