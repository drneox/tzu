import base64
import io
import os
import uuid
from pathlib import Path
from PIL import Image

MAX_DIMENSION = 4096

def save_image(file):
    """
    Save image file with UUID name and encode a resized JPEG copy to base64.
    Images larger than MAX_DIMENSION px on any side are scaled down (aspect ratio preserved).
    Returns: tuple (image_base64, saved_filename)
    """
    image_base64 = None
    saved_filename = None

    try:
        if not os.path.exists("diagrams"):
            os.makedirs("diagrams")

        original_filename = file.filename
        file_extension = Path(original_filename).suffix.lower()

        allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        if file_extension not in allowed_extensions:
            raise ValueError(f"Tipo de archivo no permitido: {file_extension}")

        raw_bytes = file.file.read()
        img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")

        if img.width > MAX_DIMENSION or img.height > MAX_DIMENSION:
            img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.LANCZOS)
            print(f"Imagen redimensionada a {img.width}x{img.height}px")

        unique_id = str(uuid.uuid4())
        saved_filename = f"{unique_id}.jpg"
        file_path = f"diagrams/{saved_filename}"

        img.save(file_path, format="JPEG", quality=85, optimize=True)

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85, optimize=True)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        print(f"Imagen '{original_filename}' guardada como '{saved_filename}'")

    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        return None, None
    finally:
        if hasattr(file.file, 'close'):
            file.file.close()

    return image_base64, saved_filename
    
        
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')