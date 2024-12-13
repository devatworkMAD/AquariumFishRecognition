import hashlib, io, pandas as pd

import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from pathlib import Path
from PIL import Image


options = ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

def gets_url(classes, location, source, url):
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    results = []
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name not in results:
            results.append(name.get(source))
    return results

def scrape(dir, url):
    save_dir = Path(__file__).parent / dir
    save_dir.mkdir(parents=True, exist_ok=True)

    returned_results = gets_url("s-item__image-wrapper image-treatment", "img", "src", url)
    for b in returned_results:
        image_content = requests.get(b).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert("RGB")
        file_path = save_dir / (hashlib.sha1(image_content).hexdigest()[:10] + ".png")
        image.save(file_path, "PNG", quality=80)

if __name__ == "__main__":
    scrape("images/1", "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=laptop&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=laptop")
    scrape("images/2", "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=laptop&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=laptop")
    driver.quit()