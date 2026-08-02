import json, sys
sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw

# Load the clean 60x45 whale mask
whale = json.load(open('whale-hero.json'))
cells = whale['cells']
W, H = whale['W'], whale['H']

def make_png(size, maskable=False):
    img = Image.new('RGBA', (size, size), (77, 107, 254, 255))  # #4d6bfe bg
    draw = ImageDraw.Draw(img)
    # Draw rounded-rect bg
    radius = 0 if maskable else int(size * 0.2)
    draw.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=(77, 107, 254, 255))
    # Whale white silhouette
    pad = int(size * (0.28 if maskable else 0.16))
    cellW = (size - 2*pad) / W
    cellH = (size - 2*pad) / H
    cell = min(cellW, cellH)
    ox = (size - cell*W) / 2
    oy = (size - cell*H) / 2
    for c in cells:
        x = ox + c[0]*cell
        y = oy + c[1]*cell
        draw.rectangle([x, y, x+cell, y+cell], fill=(255,255,255,255))
    return img

make_png(192).save('icon-192.png')
make_png(512).save('icon-512.png')
make_png(512, maskable=True).save('icon-maskable-512.png')
print('PNG icons saved')

# Also regenerate icon.svg as a proper standalone
path = json.load(open('whale-path.json'))['path']
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="96" fill="#4d6bfe"/>
  <g transform="translate(256, 256) scale(7.6) translate(-13.5, -10.5)">
    <path d="{path}" fill="#ffffff"/>
  </g>
</svg>'''
open('icon.svg', 'w', encoding='utf-8').write(svg)
svg_m = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <rect width="512" height="512" fill="#4d6bfe"/>
  <g transform="translate(256, 256) scale(5.6) translate(-13.5, -10.5)">
    <path d="{path}" fill="#ffffff"/>
  </g>
</svg>'''
open('icon-maskable.svg', 'w', encoding='utf-8').write(svg_m)
print('icon svgs saved')
