import base64
import shutil

def save_image(file):
    image_base64 = None
    try:
        with open(f"diagrams/{file.filename}", "wb") as f:
            shutil.copyfileobj(file.file, f)
            file.file.seek(0)
            image_base64 = base64.b64encode(file.file.read()).decode('utf-8')
            
            print(image_base64)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return image_base64
    
        
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')