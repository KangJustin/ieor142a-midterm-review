"""Fast layout check: render every step of a video as a still (no narration), then tile them into contact sheets."""
import importlib
import os
import sys

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

from vf import ROOT, H, W, page_html

mod = importlib.import_module(sys.argv[1])
only = [int(a) for a in sys.argv[2:]] or None
V = mod.VIDEO
out = f"{ROOT}/preview/{V.slug}"
os.makedirs(out, exist_ok=True)
shots = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": W, "height": H})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    for si, sc in enumerate(V.scenes):
        if only and si not in only:
            continue
        path = f"{out}/scene{si:02d}.html"
        open(path, "w").write(page_html(V, sc))
        pg.goto("file://" + path)
        pg.wait_for_function("window.__ready===true", timeout=30000)
        for k, st in enumerate(sc.steps):
            pg.evaluate(f"setStep({k})")
            if st.anim:
                pg.evaluate(f"anim(0.55,{k})")
            f = f"{out}/s{si:02d}_{k:02d}.png"
            pg.screenshot(path=f)
            shots.append((f"{si}.{k}", f))
    b.close()
if errs:
    print("ERRORS:", *errs, sep="\n  ")
# 2x2 sheets at half size
for n in range(0, len(shots), 4):
    sheet = Image.new("RGB", (W, H), "black")
    d = ImageDraw.Draw(sheet)
    for i, (label, f) in enumerate(shots[n:n + 4]):
        im = Image.open(f).resize((W // 2, H // 2))
        x, y = (i % 2) * W // 2, (i // 2) * H // 2
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 70, y + 30], fill="black")
        d.text((x + 8, y + 8), label, fill="yellow")
    sheet.save(f"{out}/sheet{n // 4:02d}.png")
print(len(shots), "steps;", (len(shots) + 3) // 4, "sheets in", out)
