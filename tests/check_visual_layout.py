"""Run after build: uv run --with playwright python tests/check_visual_layout.py."""

import functools
import http.server
import os
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
        )
        page = browser.new_page(reduced_motion="reduce")
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        for width in (320, 390, 760, 768, 1024, 1440):
            page.set_viewport_size({"width": width, "height": 900})
            page.goto(f"http://127.0.0.1:{server.server_port}/dist/")
            page.locator(".about-image").scroll_into_view_if_needed()
            page.wait_for_function("Array.from(document.images).every(i => i.complete)")
            issues = page.evaluate("""() => {
                const issues = [];
                const check = (ok, message) => { if (!ok) issues.push(message); };
                const rect = s => document.querySelector(s).getBoundingClientRect();
                const style = s => getComputedStyle(document.querySelector(s));
                const center = r => r.x + r.width / 2;
                check(document.documentElement.scrollWidth <= innerWidth, 'horizontal overflow');
                check(style('h1').textAlign === 'center', 'title not centered');
                check(parseFloat(style('h1').fontSize) <= Math.max(36, Math.min(72, innerWidth * .04)) + 1, 'title too large');
                const frame = rect('.about-image'), image = rect('.about-image img');
                check(Math.abs(frame.height - image.height) < 1 && Math.abs(frame.y - image.y) < 1, 'band below house image');
                for (const selector of ['.contact h2', '.contact > p:not(.eyebrow)', '.contact > .button']) {
                    check(Math.abs(center(rect(selector)) - innerWidth / 2) < 1, selector + ' not centered');
                }
                for (const card of document.querySelectorAll('.proof article, .service-card')) {
                    const x = card.querySelector('span').getBoundingClientRect().x;
                    check(Math.abs(x - card.querySelector('h2, h3').getBoundingClientRect().x) < 1, 'number/title alignment');
                    if (innerWidth <= 760 && card.matches('.service-card')) {
                        check(Math.abs(x - rect('.service-list').x) < 1, 'mobile card inset');
                    }
                }
                check([...document.images].every(i => i.naturalWidth > 0), 'image failed to load');
                check([...document.querySelectorAll('[data-contact-link="whatsapp"]')].every(a => a.href.startsWith('https://wa.me/')), 'WhatsApp link');
                return issues;
            }""")
            assert not issues, f"{width}px: {issues}"
            if width <= 760:
                page.get_by_role("button", name="Menu").click()
                assert page.locator(".menu-button").get_attribute("aria-expanded") == "true"
                page.locator(".site-nav a[href='#servicos']").click()
                assert page.locator(".menu-button").get_attribute("aria-expanded") == "false"
            print(f"PASS: {width}px")
        assert not errors, errors
        browser.close()
finally:
    server.shutdown()
    server.server_close()
