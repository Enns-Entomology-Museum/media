import sys, base64
from playwright.sync_api import sync_playwright
S=sys.argv[1]
logo=base64.b64encode(open(f'{S}/logo.png','rb').read()).decode()
def page(w,h,title_size,pad,logo_h,square=False):
    # a "drawer" of pin points on the right, like a specimen drawer seen from above
    dots=''
    cols,rows=(7,5) if not square else (10,4)
    for r in range(rows):
        for c in range(cols):
            dots+=f'<span style="opacity:{0.18+0.5*((r*cols+c)%5==0)}"></span>'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;background:#111;color:#fff;font-family:'Liberation Sans','DejaVu Sans',sans-serif;overflow:hidden;position:relative}}
.wrap{{position:absolute;inset:0;padding:{pad}px;display:flex;flex-direction:column}}
.bar{{position:absolute;left:0;top:0;bottom:0;width:14px;background:#F1B82D}}
.logo{{height:{logo_h}px;width:auto;align-self:flex-start}}
.eyebrow{{margin-top:auto;color:#F1B82D;font-weight:700;letter-spacing:.22em;font-size:{int(title_size*0.36)}px;text-transform:uppercase}}
.src{{margin-top:{int(pad*0.25)}px;font-size:{int(title_size*0.5)}px;color:#ddd}}
.src b{{color:#fff}}
h1{{margin-top:{int(pad*0.35)}px;font-family:'Lora',serif;font-weight:700;font-size:{title_size}px;line-height:1.15;max-width:{int(w*(0.92 if square else 0.74))}px}}
.date{{margin-top:{int(pad*0.4)}px;font-size:{int(title_size*0.42)}px;color:#bbb;display:flex;align-items:center;gap:14px}}
.date i{{display:inline-block;width:46px;height:3px;background:#F1B82D}}
.drawer{{position:absolute;right:{pad}px;top:{pad}px;display:grid;grid-template-columns:repeat({cols},14px);gap:{22 if not square else 40}px {22 if not square else 60}px}}
.drawer.sq{{top:{int(h*0.34)}px;left:{pad+6}px;right:auto;grid-template-columns:repeat({cols},14px)}}
.drawer span{{width:8px;height:8px;border-radius:50%;background:#F1B82D}}
</style></head><body><div class="bar"></div><div class="drawer{' sq' if square else ''}">{dots}</div><div class="wrap">
<img class="logo" src="data:image/png;base64,{logo}">
<div class="eyebrow">In the news</div>
<div class="src">Featured in the <b>Columbia Missourian</b></div>
<h1>7 million bugs are housed on the MU&nbsp;campus — a real gift for science</h1>
<div class="date"><i></i>November 16, 2026</div>
</div></body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,w,h,ts,pad,lh,sq in [('linkedin',1200,627,54,64,72,False),('square',1080,1080,72,80,80,True)]:
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=2)
        pg.set_content(page(w,h,ts,pad,lh,sq)); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{S}/enns-in-the-news-{name}.png')
    b.close()
