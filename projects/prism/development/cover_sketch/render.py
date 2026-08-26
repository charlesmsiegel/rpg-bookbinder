import asyncio, sys, os
from playwright.async_api import async_playwright

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page(viewport={"width": 900, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append("console:" + m.text) if m.type == "error" else None)
        await pg.goto("file://" + os.path.join(SRC, "index.html"))
        try:
            await pg.wait_for_function("window.__coverReady === true", timeout=240000)
        except Exception as e:
            print("TIMEOUT", e); print("\n".join(errs[:10])); await b.close(); sys.exit(1)
        data = await pg.evaluate("document.querySelector('canvas').toDataURL('image/png')")
        await b.close()
    import base64
    open(OUT, "wb").write(base64.b64decode(data.split(",", 1)[1]))
    print("saved", OUT, os.path.getsize(OUT) // 1024, "KB")
    if errs: print("errors:", errs[:5])

asyncio.run(main())
