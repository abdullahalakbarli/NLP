import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(url, filename="wikipedia_data.txt"):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = [para.text.strip() for para in soup.find_all('p') if para.text.strip()]
        with open(filename, "w", encoding="utf-8") as file:
            for para in paragraphs:
                file.write(para + "\n\n")
        return {"text_data": paragraphs, "message": f"Data saved to {filename}"}

    else:
        return {"error": f"Failed to fetch page, status code: {response.status_code}"}

url = "https://en.wikipedia.org/wiki/Azerbaijan"
data = scrape_wikipedia(url)

if "error" in data:
    print(data["error"])
else:
    print(data["message"])
