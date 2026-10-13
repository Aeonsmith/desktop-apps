import math
from PIL import Image, ImageDraw, ImageFont

def create_kaluza_klein_icon():
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size / 2
    r_outer = 116

    # 1. Outer Dark Rounded Hexagon / Circle Backdrop with Gradient Glow
    for r in range(int(r_outer), 0, -1):
        ratio = r / r_outer
        # Dark space to deep indigo/cyan gradient
        red = int(10 + (1 - ratio) * 15)
        green = int(15 + (1 - ratio) * 25 + ratio * 20)
        blue = int(30 + (1 - ratio) * 60 + ratio * 80)
        alpha = 255 if r < r_outer - 4 else int(255 * (r_outer - r) / 4)
        draw.ellipse(
            [center - r, center - r, center + r, center + r],
            fill=(red, green, blue, alpha)
        )

    # 2. Glowing Outer Rings (representing the compact extra dimension S¹)
    ring_r = 100
    for i in range(3):
        color = (6, 182, 212, 160 - i * 40)
        draw.ellipse(
            [center - ring_r - i, center - ring_r - i, center + ring_r + i, center + ring_r + i],
            outline=color,
            width=2
        )

    # 3. 5D Cylinder / Fiber Bundle Torus Grid Lines
    num_meridians = 12
    for m in range(num_meridians):
        angle = m * (math.pi / num_meridians)
        # Draw tilted orbital ellipses
        rx = 85
        ry = 32
        bbox = [center - rx, center - ry, center + rx, center + ry]
        
        # Draw rotated ellipse approximation via polygon
        pts = []
        for step in range(60):
            t = step * (2 * math.pi / 60)
            ex = rx * math.cos(t)
            ey = ry * math.sin(t)
            # rotate by angle
            rot_x = ex * math.cos(angle) - ey * math.sin(angle)
            rot_y = ex * math.sin(angle) + ey * math.cos(angle)
            pts.append((center + rot_x, center + rot_y))
        
        stroke_color = (99, 102, 241, 100) if m % 2 == 0 else (14, 165, 233, 90)
        draw.line(pts + [pts[0]], fill=stroke_color, width=1)

    # 4. Central Glowing Hyperspace Vortex & Phase Winding Spiral
    spiral_pts = []
    turns = 3.2
    max_sp_r = 72
    for step in range(120):
        t = step / 120.0
        cur_r = 8 + t * max_sp_r
        cur_angle = t * (turns * 2 * math.pi)
        sx = center + cur_r * math.cos(cur_angle)
        sy = center + cur_r * math.sin(cur_angle)
        spiral_pts.append((sx, sy))

    # Glow under spiral
    for w in range(5, 0, -1):
        alpha = int(60 * (6 - w) / 5)
        draw.line(spiral_pts, fill=(6, 182, 212, alpha), width=w * 2)

    # Sharp bright spiral
    draw.line(spiral_pts, fill=(245, 158, 11, 230), width=3)

    # 5. Central 5D Core Ring
    core_r = 24
    draw.ellipse([center - core_r, center - core_r, center + core_r, center + core_r], fill=(15, 23, 42, 240), outline=(245, 158, 11, 255), width=2)

    # 6. Center Text "5D"
    try:
        font = ImageFont.truetype("arialbd.ttf", 26)
    except Exception:
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 26)
        except Exception:
            font = ImageFont.load_default()

    text = "5D"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((center - tw / 2, center - th / 2 - 2), text, font=font, fill=(255, 255, 255, 255))

    # 7. Multi-resolution icon save
    ico_path = "C:\\Users\\ole_a\\kaluza_klein.ico"
    img.save(
        ico_path,
        format="ICO",
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    )

    # Also save PNG for UI/assets
    png_path = "C:\\Users\\ole_a\\kaluza_klein_icon.png"
    img.save(png_path, format="PNG")

    print(f"✅ Generated icon at: {ico_path}")
    print(f"✅ Generated PNG at: {png_path}")

if __name__ == "__main__":
    create_kaluza_klein_icon()
