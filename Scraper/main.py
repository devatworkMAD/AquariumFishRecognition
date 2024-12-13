import hashlib
import io
import time
import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image

options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)


def gets_url(classes, source, url):
    driver.get(url)

    # Wait for the page to load completely
    time.sleep(5)

    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")


    print("Page source length:", len(content))

    results = []
    images = soup.findAll("img", class_=classes)
    print(f"Found {len(images)} images with class '{classes}'")

    for img in images:
        image_url = img.get(source) or img.get('src')
        print("Image URL found:", image_url)

        if image_url:
            if image_url.startswith("//"):
                image_url = "https:" + image_url
            results.append(image_url)
    return results


def scrape(dir, url):
    save_dir = Path(__file__).parent / dir
    save_dir.mkdir(parents=True, exist_ok=True)

    returned_results = gets_url("tile--img__img", "data-src", url)

    if not returned_results:
        print("No images found to download.")

    for b in returned_results:
        try:
            image_content = requests.get(b).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert("RGB")
            file_path = save_dir / (hashlib.sha1(image_content).hexdigest()[:10] + ".png")
            image.save(file_path, "PNG", quality=80)
            print(f"Saved image: {file_path}")
        except Exception as e:
            print(f"Error downloading image {b}: {e}")


def build_dir_name(name_vector):
    resault = "images/"
    for index, word in enumerate(name_vector):
        if index < len(name_vector) - 1:
            resault += word + "_"
        else:
            resault += word
    return resault

def build_url_search(name_vector):
    resault = ""
    for index, word in enumerate(name_vector):
        if index < len(name_vector) - 1:
            resault += word + "+"
        else:
            resault += word
    return resault


if __name__ == "__main__":
    with open("fish_list.txt") as file:
        for line in file:
            name = line.rstrip()
            name_vector = name.split()

            dir = build_dir_name(name_vector)
            url_search = build_url_search(name_vector)

            url = "https://duckduckgo.com/?q=" + url_search + "&t=h_&iar=images&iax=images&ia=images"
            scrape(dir, url)
    driver.quit()
