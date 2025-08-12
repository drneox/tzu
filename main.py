# Point de entrada principal para la aplicación FastAPI
# Este archivo permite mantener las importaciones relativas en api.py

from .api import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
