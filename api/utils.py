import base64
import shutil

def save_image(file):
    """
    Save image file and encode it to base64
    """
    image_base64 = None
    try:
        # Ensure diagrams directory exists
        import os
        if not os.path.exists("diagrams"):
            os.makedirs("diagrams")
        
        # Save file physically
        file_path = f"diagrams/{file.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Reset file pointer and read to encode
        file.file.seek(0)
        image_base64 = base64.b64encode(file.file.read()).decode('utf-8')
        
        print(f"Imagen guardada en {file_path} y codificada en base64")
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        return None
    finally:
        # Ensure file is closed
        file.file.close()
    
    return image_base64
    
        
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')