import base64
import shutil

def save_image(file):
    """
    Guarda el archivo de imagen y lo codifica en base64
    """
    image_base64 = None
    try:
        # Asegurarse de que exista el directorio diagrams
        import os
        if not os.path.exists("diagrams"):
            os.makedirs("diagrams")
        
        # Guardar el archivo físicamente
        file_path = f"diagrams/{file.filename}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Resetear el puntero del archivo y leer para codificar
        file.file.seek(0)
        image_base64 = base64.b64encode(file.file.read()).decode('utf-8')
        
        print(f"Imagen guardada en {file_path} y codificada en base64")
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        return None
    finally:
        # Asegurarse de cerrar el archivo
        file.file.close()
    
    return image_base64
    
        
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')