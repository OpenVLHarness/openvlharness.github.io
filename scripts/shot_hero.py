"""Screenshot the hero charts (light and dark) for the code repository's README teaser.

Usage: python scripts/shot_hero.py <site_dir> <out_dir> [scale]   (needs Playwright with Chromium)
Writes hero_light.png and hero_dark.png at `scale` device pixels per CSS pixel (README uses 4). The site picks its
theme from localStorage['ovh-theme'], so each theme is set there before the page loads. Exits non-zero if the
page logs a JavaScript error.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

site, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
scale = int(sys.argv[3]) if len(sys.argv) > 3 else 4
out_dir.mkdir(parents=True, exist_ok=True)
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for theme in ("light", "dark"):
        context = browser.new_context(viewport={"width": 1280, "height": 1000}, device_scale_factor=scale,
                                      reduced_motion="reduce", color_scheme=theme)
        context.add_init_script(f"try {{ localStorage.setItem('ovh-theme', '{theme}'); }} catch (e) {{}}")
        page = context.new_page()
        page.on("pageerror", lambda e: errors.append(f"{theme}: {e}"))
        page.goto((site / "index.html").resolve().as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        charts = page.locator(".hero-charts")
        charts.scroll_into_view_if_needed()
        page.wait_for_timeout(2500)  # charts animate in once scrolled into view
        page.mouse.move(0, 0)
        box = charts.bounding_box()
        pad = 14
        page.screenshot(path=str(out_dir / f"hero_{theme}.png"), animations="disabled", full_page=True,
                        clip={"x": box["x"] - pad, "y": box["y"] + page.evaluate("window.scrollY") - pad,
                              "width": box["width"] + 2 * pad, "height": box["height"] + 2 * pad})
        context.close()
    browser.close()
# demo.js is an ES module that may not load from file://; it does not affect the hero charts.
errors = [e for e in errors if "demo" not in e.lower()]
if errors:
    sys.exit("page errors:\n" + "\n".join(errors))
print("wrote", out_dir / "hero_light.png", out_dir / "hero_dark.png")
