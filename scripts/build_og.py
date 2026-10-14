"""Rebuild static/og.jpg (1200x630 link preview): the existing title band plus a fresh light-theme hero screenshot.

The title band (wordmark and tagline, the top BAND pixels of the current og.jpg) does not depend on any data, so it is
kept; the two hero chart cards below it are re-rendered from index.html so the preview matches data.js.
Usage: python scripts/build_og.py <site_dir>   (needs Playwright with Chromium and Pillow)
"""
import io
import sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

site = Path(sys.argv[1]).resolve()
og_path = site / "static" / "og.jpg"
BAND, W, H, MARGIN = 190, 1200, 630, 34
og = Image.open(og_path).convert("RGB")
canvas = Image.new("RGB", (W, H), og.getpixel((5, H - 5)))
canvas.paste(og.crop((0, 0, W, BAND)), (0, 0))
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1180, "height": 1000}, device_scale_factor=2,
                                  reduced_motion="reduce", color_scheme="light")
    context.add_init_script("try { localStorage.setItem('ovh-theme', 'light'); } catch (e) {}")
    page = context.new_page()
    page.goto((site / "index.html").as_uri(), wait_until="networkidle")
    charts = page.locator(".hero-charts")
    charts.scroll_into_view_if_needed()
    page.wait_for_timeout(2500)
    page.mouse.move(0, 0)
    shot = Image.open(io.BytesIO(charts.screenshot(animations="disabled"))).convert("RGB")
    browser.close()
avail_w, avail_h = W - 2 * MARGIN, H - BAND - 20
scale = min(avail_w / shot.width, avail_h / shot.height)
shot = shot.resize((round(shot.width * scale), round(shot.height * scale)), Image.LANCZOS)
canvas.paste(shot, ((W - shot.width) // 2, BAND + (avail_h - shot.height) // 2 + 4))
canvas.save(og_path, quality=90)
print("wrote", og_path, canvas.size)
