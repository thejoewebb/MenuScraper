import requests
from bs4 import BeautifulSoup

def scrape_tabelog_menu(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Look for images
    image_tags = soup.find_all("img")

    for i, img in enumerate(image_tags):
        src = img.get("src")
        if src and "menu" in src:  # crude filter
            print(f"[{i}] {src}")

# Example restaurant (pick one manually from Tabelog to start)
if __name__ == "__main__":
    test_url = "https://tabelog.com/tokyo/A1301/A130101/13208304/"
    scrape_tabelog_menu(test_url)
