#!/usr/bin/env python3
"""
Create MCOS app icon - simple monospace terminal-style icon
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_mcos_icon():
    # Create a 512x512 icon (standard macOS size)
    size = 512
    icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(icon)
    
    # Draw rounded rectangle background
    margin = 40
    corner_radius = 80
    
    # Create a rounded rectangle background (black)
    draw.rounded_rectangle(
        [margin, margin, size-margin, size-margin],
        radius=corner_radius,
        fill=(0, 0, 0, 255)
    )
    
    # Draw white rounded border
    draw.rounded_rectangle(
        [margin, margin, size-margin, size-margin],
        radius=corner_radius,
        outline=(255, 255, 255, 255),
        width=6
    )
    
    # Draw the `<_` prompt symbol in large monospace font
    try:
        # Try to use a monospace font, larger size
        font = ImageFont.truetype("/System/Library/Fonts/Monaco.ttf", 140)
    except:
        # Fallback to default
        font = ImageFont.load_default()
    
    # Draw `<_` text
    text = "<_"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Save as PNG
    icon.save('mcos_icon.png')
    print("Created mcos_icon.png")
    
    # Also create smaller sizes for the iconset
    sizes = [16, 32, 64, 128, 256, 512]
    os.makedirs('mcos.iconset', exist_ok=True)
    
    for s in sizes:
        resized = icon.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f'mcos.iconset/icon_{s}x{s}.png')
        if s <= 256:  # Also create @2x versions
            resized.save(f'mcos.iconset/icon_{s//2}x{s//2}@2x.png')
    
    print("Created mcos.iconset directory")
    print("Run: iconutil -c icns mcos.iconset")

if __name__ == "__main__":
    create_mcos_icon()
