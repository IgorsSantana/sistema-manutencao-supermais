"""
Utilitários para upload de imagens no Cloudinary
"""
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from PIL import Image
import io
from werkzeug.utils import secure_filename

# Configuração do Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)

def resize_image_for_cloudinary(image_data, max_width=1200, max_height=1200, quality=85):
    """
    Redimensiona uma imagem para upload no Cloudinary
    
    Args:
        image_data: Dados da imagem (bytes ou PIL Image)
        max_width (int): Largura máxima em pixels
        max_height (int): Altura máxima em pixels
        quality (int): Qualidade da compressão JPEG (1-100)
    
    Returns:
        bytes: Dados da imagem redimensionada
    """
    try:
        # Se for bytes, converter para PIL Image
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data))
        else:
            image = image_data
        
        # Converter para RGB se necessário
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        
        # Obter dimensões originais
        original_width, original_height = image.size
        
        # Calcular novas dimensões mantendo proporção
        if original_width <= max_width and original_height <= max_height:
            # Imagem já é menor que o máximo, não precisa redimensionar
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=quality, optimize=True)
            return output.getvalue()
        
        # Calcular proporção de redimensionamento
        width_ratio = max_width / original_width
        height_ratio = max_height / original_height
        ratio = min(width_ratio, height_ratio)
        
        # Calcular novas dimensões
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # Redimensionar a imagem
        resized_img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Salvar em bytes
        output = io.BytesIO()
        resized_img.save(output, format='JPEG', quality=quality, optimize=True)
        return output.getvalue()
        
    except Exception as e:
        print(f"Erro ao redimensionar imagem para Cloudinary: {str(e)}")
        return image_data

def upload_to_cloudinary(file, folder="manutencao_supermais"):
    """
    Faz upload de uma imagem para o Cloudinary
    
    Args:
        file: Arquivo de imagem (Werkzeug FileStorage)
        folder (str): Pasta no Cloudinary
    
    Returns:
        dict: Informações do upload (public_id, url, secure_url)
    """
    try:
        # Ler dados do arquivo
        file_data = file.read()
        
        # Redimensionar imagem
        resized_data = resize_image_for_cloudinary(file_data)
        
        # Gerar nome único para o arquivo
        filename = secure_filename(file.filename)
        timestamp = os.environ.get('RENDER_TIMESTAMP', 'local')
        unique_filename = f"{timestamp}_{filename}"
        
        # Upload para Cloudinary
        result = cloudinary.uploader.upload(
            resized_data,
            folder=folder,
            public_id=unique_filename,
            resource_type="image",
            quality="auto",
            fetch_format="auto"
        )
        
        return {
            'public_id': result['public_id'],
            'url': result['url'],
            'secure_url': result['secure_url'],
            'filename': unique_filename
        }
        
    except Exception as e:
        print(f"Erro ao fazer upload para Cloudinary: {str(e)}")
        return None

def delete_from_cloudinary(public_id):
    """
    Deleta uma imagem do Cloudinary
    
    Args:
        public_id (str): ID público da imagem no Cloudinary
    
    Returns:
        bool: True se deletado com sucesso
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result.get('result') == 'ok'
    except Exception as e:
        print(f"Erro ao deletar imagem do Cloudinary: {str(e)}")
        return False

def get_cloudinary_url(public_id, transformation=None):
    """
    Gera URL da imagem no Cloudinary com transformações opcionais
    
    Args:
        public_id (str): ID público da imagem
        transformation (dict): Transformações a aplicar
    
    Returns:
        str: URL da imagem
    """
    try:
        if transformation:
            return cloudinary.CloudinaryImage(public_id).build_url(**transformation)
        else:
            return cloudinary.CloudinaryImage(public_id).build_url()
    except Exception as e:
        print(f"Erro ao gerar URL do Cloudinary: {str(e)}")
        return None

def is_cloudinary_configured():
    """
    Verifica se o Cloudinary está configurado
    
    Returns:
        bool: True se configurado
    """
    return all([
        os.environ.get('CLOUDINARY_CLOUD_NAME'),
        os.environ.get('CLOUDINARY_API_KEY'),
        os.environ.get('CLOUDINARY_API_SECRET')
    ])
