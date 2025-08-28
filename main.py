import requests
from bs4 import BeautifulSoup


URL = "https://pitchfork.com/best/"

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")


#container = soup.select_one("div", class_="SubtopicDiscoveryItemContainer-kdbIDR fhvuqf")

#print(container.get_text())

best_new_album_section = soup.find(
    lambda tag: tag.name in ["h2", "h3", "div"] and "Best New Album" in tag.get_text(strip=True)
)

if best_new_album_section:
    # Find the album title (usually in a <h3> or <h2> tag nearby)
    title_tag = soup.find("h3", {"data-testid": "SummaryItemHed"})
    title = title_tag.get_text(strip=True) if title_tag else "N/A"

    # Find the artist (often in a <p> or <span> nearby)
    artist_tag = soup.find("div", {"data-testid": "SummaryItemHed"})
    artist = artist_tag.get_text(strip=True) if artist_tag else "N/A"

    # Find the cover image link (usually an <a> tag nearby)
    review_link = soup.find("a", {"data-recirc-pattern": "summary-item"})
    review_url = review_link["href"] if review_link and review_link.has_attr("href") else "N/A"

    img_tag = soup.find("img", {"alt": title})
    if img_tag:
        cover_url = img_tag["src"]
    else:
        cover_url = "N/A"

    print(f"Title: {title}")
    print(f"Artist: {artist}")
    print(f"Cover URL: {cover_url}")
    print(f"Review URL: {review_url}")
else:
    print("Best New Album section not found.")
