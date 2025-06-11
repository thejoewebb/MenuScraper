import requests
from bs4 import BeautifulSoup
import os, time, random

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_tabelog_menu(url):

    #Load the page
    response = requests.get(url, headers=HEADERS)
    #print(response.status_code)
    if response.status_code != 200:
        print(f"Failed to load page: {response.status_code}")
        return
    
    #save response for testing
    with open("data/raw_html/test_page.html", "w", encoding="utf-8") as f:
        f.write(response.text)

def process_html(path, output_dir="data/images"):

    os.makedirs(output_dir, exist_ok=True)

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Find all <a> tags that wrap full-res images
    links = soup.select("a.js-imagebox-trigger[href*='/images/'][href*='640x640']")

    if len(links)>0:
        for i, link in enumerate(links):
            href = link.get("href")
            try:
                #Skip empty or malformed hrefs
                if not href or not href.startswith("http"):
                    continue
                # Download the image
                img_data = requests.get(href, headers=HEADERS).content
                file_name = f"menu_{i:03}.jpg"
                file_path = os.path.join(output_dir, file_name)
                with open(file_path, "wb") as f:
                    f.write(img_data)
                print(f"Saved: {file_name}")

                # Add a random delay between 1.5 to 4.5 seconds
                delay = random.uniform(1.5, 4.5)
                time.sleep(delay)

            except Exception as e:
                print(f"Failed to download {href}: {e}")
    else:
        print("no images found")

# Example restaurant (pick one manually from Tabelog to start)
if __name__ == "__main__":
    print("start")
    test_url = "https://tabelog.com/tokyo/A1307/A130701/13275212/dtlmenu/photo/"
    #scrape_tabelog_menu(test_url)
    process_html("data/raw_html/test_page.html")
    print("stop")
