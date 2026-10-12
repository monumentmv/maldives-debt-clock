"""
Draws the picture shown when someone shares the site on X, Facebook, WhatsApp and so on:
assets/share.png, 1200 x 630, with today's estimate of the debt and the latest debt-to-GDP ratio.

Runs every morning in GitHub Actions after fetch_data.py. It opens tools/share-card.html in a
headless browser and takes a picture of it. To run it yourself:
    pip install playwright
    python -m playwright install chromium
    python build_share.py
"""
import functools
import http.server
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "assets" / "share.png"


def main():
    from playwright.sync_api import sync_playwright
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE))
    handler.log_message = lambda *a, **k: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1200, "height": 630})
            page.goto(f"http://127.0.0.1:{server.server_port}/tools/share-card.html")
            page.wait_for_function("document.body.dataset.ready", timeout=30000)
            if page.evaluate("document.body.dataset.ready") != "1":
                print("Couldn't read the figures for the share picture. The old picture is unchanged.")
                return
            page.wait_for_timeout(300)
            page.screenshot(path=str(OUT), type="png")
            browser.close()
        print(f"Wrote {OUT.relative_to(HERE)}.")
    except Exception as e:
        print(f"Couldn't draw the share picture ({e}). The old picture is unchanged.")
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
