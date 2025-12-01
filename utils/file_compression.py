"""
File Compression Utilities
Handles compression of images and documents for database storage
"""

from PIL import Image
import io
import os
from typing import Tuple, Optional
from PyPDF2 import PdfReader, PdfWriter

def get_mime_type(filename: str) -> str:
    """
    Get MIME type from filename extension
    
    Args:
        filename: Name of the file
        
    Returns:
        MIME type string (e.g., 'image/jpeg', 'application/pdf')
    """
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    mime_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp',
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    
    return mime_types.get(ext, 'application/octet-stream')


def compress_image(file, max_width: int = 800, max_height: int = 800, quality: int = 85) -> Tuple[bytes, str]:
    """
    Compress and resize an image
    
    Args:
        file: File object from Flask request.files
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: JPEG quality (1-100)
        
    Returns:
        Tuple of (compressed_bytes, mime_type)
    """
    try:
        # Open image
        img = Image.open(file)
        
        # Convert RGBA to RGB if necessary (for JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Calculate new size maintaining aspect ratio
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Save to bytes
        output = io.BytesIO()
        
        # Determine format
        format_type = 'JPEG'
        mime_type = 'image/jpeg'
        
        if file.filename.lower().endswith('.png'):
            format_type = 'PNG'
            mime_type = 'image/png'
            # PNG doesn't use quality parameter the same way
            img.save(output, format=format_type, optimize=True)
        elif file.filename.lower().endswith('.gif'):
            format_type = 'GIF'
            mime_type = 'image/gif'
            img.save(output, format=format_type, optimize=True)
        else:
            # Default to JPEG
            img.save(output, format=format_type, quality=quality, optimize=True)
        
        output.seek(0)
        return output.read(), mime_type
        
    except Exception as e:
        raise Exception(f"Error compressing image: {str(e)}")


def compress_pdf(file) -> Tuple[bytes, str]:
    """
    Compress a PDF file
    
    Args:
        file: File object from Flask request.files
        
    Returns:
        Tuple of (compressed_bytes, mime_type)
    """
    try:
        # Basic PDF compression/optimization using PyPDF2
        # This re-writes the PDF which can remove unused objects and optimize structure
        file.seek(0)
        reader = PdfReader(file)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
            
        # Compress streams if possible (PyPDF2 default behavior often does this)
        for page in writer.pages:
            page.compress_content_streams()
            
        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        
        return output.read(), 'application/pdf'
        
    except Exception as e:
        print(f"PDF compression failed, using original: {str(e)}")
        file.seek(0)
        return file.read(), 'application/pdf'


def get_file_size_mb(data: bytes) -> float:
    """
    Get file size in megabytes
    
    Args:
        data: File bytes
        
    Returns:
        Size in MB
    """
    return len(data) / (1024 * 1024)


def validate_file_size(data: bytes, max_size_mb: float = 10) -> bool:
    """
    Validate that file size is within limits
    
    Args:
        data: File bytes
        max_size_mb: Maximum allowed size in MB
        
    Returns:
        True if valid, False otherwise
    """
    return get_file_size_mb(data) <= max_size_mb
