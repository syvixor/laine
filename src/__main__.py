import os
import io
import time
import zipfile
import tempfile
import requests
import json
import html
from PIL import Image
from bs4 import BeautifulSoup
from tqdm import tqdm

# Fetches a URL with retry logic in case of failure
def fetch_with_retries(url):
    max_retries = 5
    for i in range(max_retries):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Referer": "https://comic-days.com"
            }
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            return resp
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(2 * (2 ** i))  # exponential backoff
            else:
                raise e

# Extracts JSON data embedded in the HTML of the chapter page
def extract_chapter_json(page_url):
    resp = fetch_with_retries(page_url)
    soup = BeautifulSoup(resp.text, "lxml")
    json_data = soup.find(id="episode-json")
    if not json_data or not json_data.has_attr("data-value"):
        raise ValueError("Chapter data could not be found!")
    unescaped = html.unescape(json_data["data-value"])
    return json.loads(unescaped)

# Parses and returns list of pages with image metadata (src, width, height)
def parse_pages(json_blob):
    pages = json_blob["readableProduct"]["pageStructure"]["pages"]
    parsed = []
    for page in pages:
        src = page.get("src")
        width = int(page.get("width", 0))
        height = int(page.get("height", 0))
        if src and width and height:
            parsed.append({
                "src": src,
                "width": width,
                "height": height
            })
    parsed.sort(key=lambda p: p["src"])  # ensure consistent order
    return parsed

# Detects how much transparent space is on the right of an image
def detect_transparent_strip(img):
    width, height = img.size
    max_transparent_width = 0
    for x in reversed(range(width)):
        transparent = True
        for y in range(height):
            _, _, _, a = img.getpixel((x, y))  # get alpha channel
            if a != 0:
                transparent = False
                break
        if transparent:
            max_transparent_width += 1
        else:
            break
    return max_transparent_width

# Reverses the obfuscation applied to the image by swapping grid blocks
def deobfuscate(img, width, height):
    spacing_w = (width // 32) * 8
    spacing_h = (height // 32) * 8
    dst = Image.new("RGBA", (width, height))

    for x in range(0, width, spacing_w):
        for y_offset in range(0, height, spacing_h):
            initial_y_start = (x // spacing_w) * spacing_h + spacing_h

            for y in range(initial_y_start, height, spacing_h):
                if y + spacing_h > height:
                    continue

                old_rect = (x, y, x + spacing_w, y + spacing_h)

                new_x = (y // spacing_h) * spacing_w
                new_y = (x // spacing_w) * spacing_h
                new_rect = (new_x, new_y, new_x + spacing_w, new_y + spacing_h)

                dst.paste(img.crop(new_rect), old_rect[:2])
                dst.paste(img.crop(old_rect), new_rect[:2])

    # Keep the diagonal blocks unchanged
    for i in range(4):
        mx, my = i * spacing_w, i * spacing_h
        mid_rect = (mx, my, mx + spacing_w, my + spacing_h)
        dst.paste(img.crop(mid_rect), mid_rect[:2])

    return dst

# Restores the transparent strip on the right side if it was lost
def restore_right_strip(deob_img, orig_img, width, height, strip_width):
    if strip_width <= 0:
        return
    box = (width - strip_width, 0, width, height)
    strip = orig_img.crop(box)
    deob_img.paste(strip, (width - strip_width, 0))

# Downloads and processes a single image page
def process_page(page, index, output_dir):
    img_resp = fetch_with_retries(page["src"])
    orig_img = Image.open(io.BytesIO(img_resp.content)).convert("RGBA")

    deob = deobfuscate(orig_img, page["width"], page["height"])
    strip_width = detect_transparent_strip(deob)
    restore_right_strip(deob, orig_img, page["width"], page["height"], strip_width)

    file_path = os.path.join(output_dir, f"{index:03d}.png")
    deob.save(file_path)

# Downloads an entire chapter and saves as a ZIP archive
def download_chapter(chapter_id, output_path):
    chapter_url = f"https://comic-days.com/episode/{chapter_id}"

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"[+] Fetching...")
        json_blob = extract_chapter_json(chapter_url)
        pages = parse_pages(json_blob)

        print(f"[+] Processing {len(pages)} Pages...")
        for i, page in enumerate(tqdm(pages, desc="[+] Processing", bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}"), 1):
            process_page(page, i, temp_dir)

        zip_filename = os.path.abspath(output_path or f"{chapter_id}.zip")
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for img_file in sorted(os.listdir(temp_dir)):
                if img_file.endswith(".png"):
                    zipf.write(os.path.join(temp_dir, img_file), arcname=img_file)

        print(f"[✓] Deobfuscated & Downloaded")

# Main entry point
def main():
    print("=== Comic-Days Chapter Downloader ===")
    chapter_id = input("Chapter ID: ").strip()

    try:
        download_chapter(chapter_id, f"{chapter_id}.zip")
    except Exception as e:
        print(f"[✗] Error: {e}")

if __name__ == "__main__":
    main()