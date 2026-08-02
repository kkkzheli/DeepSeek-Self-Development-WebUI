import json, sys
sys.stdout.reconfigure(encoding='utf-8')

masks = json.load(open('whale-masks.json'))

MAIN = '#4D6BFE'

def gen_rects(mask, cx, cy, diameter=57.0):
    H = len(mask); W = len(mask[0])
    cell = diameter / W
    x0 = cx - (W * cell) / 2.0
    y0 = cy - (H * cell) / 2.0
    rects = []
    for ry, row in enumerate(mask):
        for rx, ch in enumerate(row):
            if ch == '1':
                x = x0 + rx * cell
                y = y0 + ry * cell
                rects.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{cell:.2f}" height="{cell:.2f}" fill="{MAIN}" shape-rendering="crispEdges"/>')
    return ''.join(rects)

lanes = [('n1',103),('n2',269),('n3',435),('n4',601),('n5',767)]
out = {}
for name, cy in lanes:
    out[name] = gen_rects(masks[name], 515, cy)
json.dump(out, open('node-rects-v2.json','w'))
for name in out:
    print(name, len(out[name]), 'chars')
