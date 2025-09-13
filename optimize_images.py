import os
from PIL import Image
from io import BytesIO
import shutil

def optimize_image(input_path, output_path, quality=85, max_size=(2000, 2000)):
    """Optimize an image by resizing and compressing it."""
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if image has an alpha channel
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])  # Paste using alpha channel as mask
                img = background
            
            # Resize if image is larger than max_size
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save with optimization
            img.save(
                output_path,
                'JPEG' if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg') else 'PNG',
                optimize=True,
                quality=quality
            )
            
            # Get file size before and after optimization
            original_size = os.path.getsize(input_path)
            optimized_size = os.path.getsize(output_path)
            
            print(f"Optimized: {input_path} ({original_size/1024:.1f}KB -> {optimized_size/1024:.1f}KB, "
                  f"{100 - (optimized_size / original_size * 100):.1f}% reduction)")
            
            return True
    except Exception as e:
        print(f"Error optimizing {input_path}: {e}")
        return False

def optimize_directory(directory, output_dir=None, quality=85, max_size=(2000, 2000)):
    """Optimize all images in a directory and its subdirectories."""
    if output_dir is None:
        output_dir = directory
    
    for root, _, files in os.walk(directory):
        # Create corresponding output directory structure
        rel_path = os.path.relpath(root, directory)
        current_output_dir = os.path.join(output_dir, rel_path)
        
        # Skip if it's the output directory itself to avoid recursion
        if os.path.abspath(root) == os.path.abspath(output_dir):
            continue
            
        os.makedirs(current_output_dir, exist_ok=True)
        
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                input_path = os.path.join(root, file)
                output_path = os.path.join(current_output_dir, file)
                
                # Skip if output file already exists and is newer than input
                if os.path.exists(output_path) and os.path.getmtime(output_path) >= os.path.getmtime(input_path):
                    print(f"Skipping (up to date): {input_path}")
                    continue
                
                # Optimize the image
                optimize_image(input_path, output_path, quality, max_size)

def main():
    # Define directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, 'images')
    optimized_dir = os.path.join(base_dir, 'optimized_images')
    
    print(f"Optimizing images in: {images_dir}")
    print(f"Output directory: {optimized_dir}")
    
    # Optimize images
    optimize_directory(images_dir, optimized_dir, quality=80, max_size=(1920, 1920))
    
    print("\nOptimization complete!")
    print(f"To use the optimized images, copy the contents of '{optimized_dir}' to your web server.")
    print("You can replace the original 'images' directory with the 'optimized_images' directory.")

if __name__ == "__main__":
    main()
