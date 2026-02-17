from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename):
    # Create image
    img = Image.new('RGB', (size, size), color='#ffffff')
    d = ImageDraw.Draw(img)
    
    # Draw background rounded rect (simulated by circle for simplicity as icon masks handle corners)
    # Actually just a full fill is fine for android, but let's make it blue
    d.rectangle([0, 0, size, size], fill='#2563eb')
    
    # Draw "Clipboard" shape
    w, h = size, size
    padding = size // 4
    
    # Paper
    d.rectangle([padding, padding, w-padding, h-padding], fill='#ffffff')
    
    # Clip
    clip_w = size // 2.5
    clip_h = size // 6
    clip_x = (w - clip_w) // 2
    d.rectangle([clip_x, padding - (clip_h // 2), clip_x + clip_w, padding + (clip_h // 2)], fill='#1e40af')

    # Lines
    line_x = padding + (size // 10)
    line_w = w - padding - line_x
    line_h = size // 15
    for i in range(3):
        y = padding + (size // 4) + (i * (line_h * 2))
        d.rectangle([line_x, y, line_x + line_w, y + line_h], fill='#e5e7eb')

    img.save(filename)
    print(f"Created {filename}")

if __name__ == "__main__":
    create_icon(512, "icon-512.png")
    create_icon(192, "icon-192.png")
