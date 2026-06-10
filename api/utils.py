import base64
import io
import os
import uuid
from pathlib import Path
from PIL import Image

MAX_DIMENSION = 1280

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
TEXT_EXTENSIONS = {'.txt', '.md', '.xml', '.json', '.svg'}
PDF_EXTENSIONS = {'.pdf'}
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | TEXT_EXTENSIONS | PDF_EXTENSIONS


def _ensure_diagrams_dir():
    if not os.path.exists("diagrams"):
        os.makedirs("diagrams")


def save_image(file):
    """
    Save image file with UUID name and encode a resized JPEG copy to base64.
    Images larger than MAX_DIMENSION px on any side are scaled down (aspect ratio preserved).
    Returns: tuple (image_base64, saved_filename)
    """
    try:
        content, content_type, saved_filename = process_file(file)
        if content_type != "image":
            return None, None
        return content, saved_filename
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        return None, None


def process_file(file):
    """
    Process an uploaded file of any supported type.
    Returns: tuple (content, content_type, saved_filename)
      - content_type = 'image': content is base64-encoded JPEG string
      - content_type = 'text':  content is plain text string
    Supported formats: PNG, JPG, JPEG, GIF, BMP, WebP (image),
                       PDF, TXT, MD, XML, JSON, SVG (text extraction)
    """
    _ensure_diagrams_dir()

    original_filename = file.filename
    file_extension = Path(original_filename).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Tipo de archivo no permitido: {file_extension}. "
                         f"Formatos soportados: {', '.join(sorted(ALLOWED_EXTENSIONS))}")

    raw_bytes = file.file.read()

    try:
        if file_extension in IMAGE_EXTENSIONS:
            return _process_image(raw_bytes, original_filename)
        elif file_extension in PDF_EXTENSIONS:
            return _process_pdf(raw_bytes)
        else:
            return _process_text_file(raw_bytes, file_extension)
    finally:
        if hasattr(file, 'file') and hasattr(file.file, 'close'):
            file.file.close()


def _process_image(raw_bytes, original_filename):
    """Convert raw image bytes to base64 JPEG and save to disk."""
    # Save original full-quality copy to disk for the report.
    img_display = Image.open(io.BytesIO(raw_bytes)).convert("RGB")

    unique_id = str(uuid.uuid4())
    saved_filename = f"{unique_id}.jpg"
    file_path = f"diagrams/{saved_filename}"
    img_display.save(file_path, format="JPEG", quality=85, optimize=True)

    # Resize by longest side preserving aspect ratio (handles both landscape and portrait)
    # Keep RGB colour — it helps the LLM distinguish components, trust boundaries,
    # and data-flow arrows in architecture diagrams.  Grayscale loses too much info.
    img_llm = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    longest = max(img_llm.width, img_llm.height)
    if longest > MAX_DIMENSION:
        ratio = MAX_DIMENSION / longest
        new_size = (int(img_llm.width * ratio), int(img_llm.height * ratio))
        img_llm = img_llm.resize(new_size, Image.LANCZOS)
        print(f"Imagen reducida para LLM a {img_llm.width}x{img_llm.height}px (RGB)")

    buf = io.BytesIO()
    img_llm.save(buf, format="JPEG", quality=85, optimize=True)
    image_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    print(f"Imagen '{original_filename}' guardada como '{saved_filename}'")
    return image_b64, "image", saved_filename


def _process_pdf(raw_bytes):
    """Extract text from a PDF using pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        raise ValueError(
            "Soporte para PDF no disponible. "
            "Instale la dependencia: pip install pdfplumber"
        )

    text_parts = []
    with pdfplumber.open(io.BytesIO(raw_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    content = "\n\n".join(text_parts)
    if not content.strip():
        raise ValueError("No se pudo extraer texto del PDF. Puede ser un PDF basado en imágenes.")

    saved_filename = _save_text_to_disk(content, "pdf")
    return content, "text", saved_filename


def _process_text_file(raw_bytes, file_extension):
    """Decode text-based files (TXT, MD, XML, JSON, SVG)."""
    content = raw_bytes.decode('utf-8', errors='replace')
    ext = file_extension.lstrip('.')
    saved_filename = _save_text_to_disk(content, ext)
    return content, "text", saved_filename


def _save_text_to_disk(content, ext):
    """Persist text content to the diagrams folder and return the filename."""
    unique_id = str(uuid.uuid4())
    saved_filename = f"{unique_id}.{ext}"
    file_path = f"diagrams/{saved_filename}"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return saved_filename


def save_text_content(text_content):
    """
    Save raw text content (from textarea) to disk.
    Returns: tuple (text_content, saved_filename)
    """
    _ensure_diagrams_dir()
    saved_filename = _save_text_to_disk(text_content, "txt")
    print(f"Contenido de texto guardado como '{saved_filename}'")
    return text_content, saved_filename


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')