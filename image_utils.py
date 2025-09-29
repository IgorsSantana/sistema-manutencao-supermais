"""
Utilitários para processamento de imagens
"""
import os
from PIL import Image
from werkzeug.utils import secure_filename

def resize_image(image_path, max_width=1200, max_height=1200, quality=85):
    """
    Redimensiona uma imagem mantendo a proporção e otimizando o tamanho do arquivo
    
    Args:
        image_path (str): Caminho da imagem original
        max_width (int): Largura máxima em pixels (padrão: 1200)
        max_height (int): Altura máxima em pixels (padrão: 1200)
        quality (int): Qualidade da compressão JPEG (1-100, padrão: 85)
    
    Returns:
        str: Caminho da imagem redimensionada
    """
    try:
        # Abrir a imagem
        with Image.open(image_path) as img:
            # Converter para RGB se necessário (para JPEG)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Obter dimensões originais
            original_width, original_height = img.size
            
            # Calcular novas dimensões mantendo proporção
            if original_width <= max_width and original_height <= max_height:
                # Imagem já é menor que o máximo, não precisa redimensionar
                return image_path
            
            # Calcular proporção de redimensionamento
            width_ratio = max_width / original_width
            height_ratio = max_height / original_height
            ratio = min(width_ratio, height_ratio)
            
            # Calcular novas dimensões
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            # Redimensionar a imagem
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Criar novo nome de arquivo
            base_name = os.path.splitext(image_path)[0]
            extension = os.path.splitext(image_path)[1]
            resized_path = f"{base_name}_resized{extension}"
            
            # Salvar imagem redimensionada
            resized_img.save(resized_path, 'JPEG', quality=quality, optimize=True)
            
            # Remover arquivo original
            os.remove(image_path)
            
            # Renomear arquivo redimensionado para o nome original
            os.rename(resized_path, image_path)
            
            return image_path
            
    except Exception as e:
        print(f"Erro ao redimensionar imagem {image_path}: {str(e)}")
        return image_path

def process_uploaded_images(files, upload_folder):
    """
    Processa múltiplas imagens enviadas, redimensionando-as
    
    Args:
        files: Lista de arquivos enviados
        upload_folder (str): Pasta de upload
    
    Returns:
        list: Lista de nomes de arquivos processados
    """
    processed_files = []
    
    for file in files:
        if file and file.filename:
            # Gerar nome seguro para o arquivo
            filename = secure_filename(file.filename)
            
            # Garantir que o nome seja único
            counter = 1
            original_filename = filename
            while os.path.exists(os.path.join(upload_folder, filename)):
                name, ext = os.path.splitext(original_filename)
                filename = f"{name}_{counter}{ext}"
                counter += 1
            
            # Salvar arquivo original
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            # Redimensionar imagem
            resized_path = resize_image(file_path)
            
            processed_files.append(filename)
    
    return processed_files

def get_image_info(image_path):
    """
    Obtém informações sobre uma imagem
    
    Args:
        image_path (str): Caminho da imagem
    
    Returns:
        dict: Informações da imagem (largura, altura, tamanho do arquivo)
    """
    try:
        with Image.open(image_path) as img:
            file_size = os.path.getsize(image_path)
            return {
                'width': img.width,
                'height': img.height,
                'mode': img.mode,
                'file_size': file_size,
                'file_size_mb': round(file_size / (1024 * 1024), 2)
            }
    except Exception as e:
        print(f"Erro ao obter informações da imagem {image_path}: {str(e)}")
        return None
