import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# Load the official whale path
path = json.load(open('whale-path.json'))['path']

# Build an SVG icon: blue rounded-square bg + white whale
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="96" fill="#4d6bfe"/>
  <g transform="translate(256, 256) scale(7.6) translate(-13.5, -10.5)">
    <path d="{path}" fill="#ffffff"/>
  </g>
</svg>'''
open('icon.svg', 'w', encoding='utf-8').write(svg)
print('saved icon.svg')

# Maskable icon: whale fills more of the canvas (safe zone ~40%)
svg_m = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <rect width="512" height="512" fill="#4d6bfe"/>
  <g transform="translate(256, 256) scale(5.6) translate(-13.5, -10.5)">
    <path d="{path}" fill="#ffffff"/>
  </g>
</svg>'''
open('icon-maskable.svg', 'w', encoding='utf-8').write(svg_m)
print('saved icon-maskable.svg')

# Render PNGs from the SVG using PIL (via cairosvg if available, else PIL manual)
from PIL import Image, ImageDraw
import subprocess, os

def svg_to_png(svgfile, pngfile, size):
    # Try cairosvg
    try:
        import cairosvg
        cairosvg.svg2png(url=svgfile, write_to=pngfile, output_width=size, output_height=size)
        return True
    except Exception:
        pass
    # Try resvg/inkscape
    for cmd in [['inkscape', svgfile, '--export-type=png', f'--export-filename={pngfile}', f'-w', str(size), f'-h', str(size)],
                ['rsvg-convert', '-w', str(size), '-h', str(size), '-o', pngfile, svgfile]]:
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=30)
            if os.path.exists(pngfile) and os.path.getsize(pngfile) > 100:
                return True
        except Exception:
            continue
    return False

ok = True
for src, dst, size in [('icon.svg','icon-192.png',192), ('icon.svg','icon-512.png',512), ('icon-maskable.svg','icon-maskable-512.png',512)]:
    r = svg_to_png(src, dst, size)
    ok = ok and r
    print(dst, '->', 'OK' if r else 'FAIL')
print('all ok:', ok)
