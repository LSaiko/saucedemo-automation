import base64
from functools import reduce
from pathlib import Path

from PIL import Image, ImageChops
from selenium.webdriver.support.ui import WebDriverWait

BASELINES = Path(__file__).parent / "baselines"
DIFFS = Path(__file__).parent / "diffs"
PIXEL_TOLERANCE = 32  # per-channel 0-255; absorbs anti-aliasing jitter without hiding real changes


def capture_screenshot(driver, name):
    """Full-page PNG. First run writes the baseline; later runs write to diffs/. Returns the path written."""
    baseline = BASELINES / f"{name}.png"
    target = DIFFS / f"{name}.png" if baseline.exists() else baseline
    target.parent.mkdir(parents=True, exist_ok=True)
    # fonts too: a shot taken while the web font is still loading renders fallback glyphs and blows the threshold
    WebDriverWait(driver, 10).until(lambda d: d.execute_script(
        "return document.fonts.status === 'loaded' && [...document.images].every(i => i.complete)"))
    # ponytail: CDP call instead of resizing the window; Chrome-only, same as the driver fixture
    png = driver.execute_cdp_cmd("Page.captureScreenshot", {"captureBeyondViewport": True})["data"]
    target.write_bytes(base64.b64decode(png))
    return target


def compare_screenshots(baseline_path, current_path, threshold=0.02):
    """True if the share of changed pixels is <= threshold. Writes <current>_diff.png mask for review."""
    a = Image.open(baseline_path).convert("RGB")
    b = Image.open(current_path).convert("RGB")
    if a.size != b.size:
        return False
    changed = reduce(ImageChops.lighter, ImageChops.difference(a, b).split()).point(lambda v: 255 if v > PIXEL_TOLERANCE else 0)
    changed.save(Path(current_path).with_name(f"{Path(current_path).stem}_diff.png"))
    return changed.histogram()[255] / (a.width * a.height) <= threshold
