import os
import sys
from PIL import Image, ImageDraw

def create_untold_icon(output_path="libraries_of_the_untold.ico"):
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []

    for size in sizes:
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        w, h = size
        
        # Background Circle - Deep Cosmic Void with Gold Rim
        pad = int(w * 0.05)
        draw.ellipse([pad, pad, w - pad, h - pad], fill=(12, 14, 28, 255), outline=(218, 165, 32, 255), width=max(1, int(w * 0.03)))
        
        # Center Vertical Beam (The Axis) - Cyan / Gold
        beam_w = max(2, int(w * 0.06))
        cx = w // 2
        draw.line([(cx, pad * 2), (cx, h - pad * 2)], fill=(0, 240, 255, 230), width=beam_w)
        
        # Center Monad Eye / Diamond
        mid_y = h // 2
        d_size = int(w * 0.22)
        draw.polygon([
            (cx, mid_y - d_size),
            (cx + d_size, mid_y),
            (cx, mid_y + d_size),
            (cx - d_size, mid_y)
        ], outline=(255, 215, 0, 255), fill=(20, 25, 45, 220))
        
        # Inner Core Glow
        r = max(2, int(w * 0.08))
        draw.ellipse([cx - r, mid_y - r, cx + r, mid_y + r], fill=(0, 255, 220, 255))
        
        images.append(img)

    images[0].save(output_path, format="ICO", sizes=sizes)
    print(f"[+] Icon generated: {os.path.abspath(output_path)}")
    return os.path.abspath(output_path)

if __name__ == "__main__":
    icon_p = create_untold_icon("C:\\Users\\ole_a\\libraries_of_the_untold\\libraries_of_the_untold.ico")
