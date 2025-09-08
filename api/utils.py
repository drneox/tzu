import base64
import shutil
import os
import uuid
from pathlib import Path

def save_image(file):
    """
    Save image file with UUID name and encode it to base64
    Returns: tuple (image_base64, saved_filename)
    """
    image_base64 = None
    saved_filename = None
    
    try:
        # Ensure diagrams directory exists
        if not os.path.exists("diagrams"):
            os.makedirs("diagrams")
        
        # Get file extension from original filename
        original_filename = file.filename
        file_extension = Path(original_filename).suffix.lower()
        
        # Validate file extension (security measure)
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg'}
        if file_extension not in allowed_extensions:
            raise ValueError(f"Tipo de archivo no permitido: {file_extension}")
        
        # Generate UUID-based filename
        unique_id = str(uuid.uuid4())
        saved_filename = f"{unique_id}{file_extension}"
        file_path = f"diagrams/{saved_filename}"
        
        # Save file physically
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Reset file pointer and read to encode
        file.file.seek(0)
        image_base64 = base64.b64encode(file.file.read()).decode('utf-8')
        
        print(f"Imagen '{original_filename}' guardada como '{saved_filename}' y codificada en base64")
        
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        return None, None
    finally:
        # Ensure file is closed
        if hasattr(file.file, 'close'):
            file.file.close()
    
    return image_base64, saved_filename
    
        
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')