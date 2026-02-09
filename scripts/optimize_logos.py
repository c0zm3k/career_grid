import os
import shutil
from PIL import Image

# Consolidate all images from the images directory into a flat cdn directory
source_dir = r"e:\career_grid\app\static\images"
target_dir = r"e:\career_grid\app\static\cdn"

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Flatten and optimize everything from the images folder and its subfolders
# (e.g., Recruitment Partners, partners_cdn)
for root, dirs, files in os.walk(source_dir):
    for filename in files:
        file_path = os.path.join(root, filename)
        ext = filename.lower().split('.')[-1]
        
        # Skip temp folders we created earlier to avoid duplicates
        if 'partners_cdn' in root:
            continue
            
        if ext in ['png', 'jpg', 'jpeg', 'webp', 'avif']:
            try:
                with Image.open(file_path) as img:
                    # Convert to RGBA for consistency
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    
                    # Normalize height if it's a partner logo (in that specific folder)
                    if 'Recruitment Partners' in root:
                        target_height = 80
                        aspect_ratio = img.width / img.height
                        target_width = int(target_height * aspect_ratio)
                        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    
                    # Save as webp with the same basename
                    base_name = os.path.splitext(filename)[0]
                    target_path = os.path.join(target_dir, f"{base_name}.webp")
                    img.save(target_path, "WEBP", quality=90)
                    print(f"Optimized: {filename} -> {base_name}.webp")
            except Exception as e:
                print(f"Error optimizing {filename}: {e}")
        elif ext == 'svg':
            # Copy SVGs as they are already optimized/vector
            target_path = os.path.join(target_dir, filename)
            shutil.copy2(file_path, target_path)
            print(f"Copied SVG: {filename}")
