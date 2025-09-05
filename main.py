import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image
import numpy as np
from io import BytesIO
import colorGenerator as cG

load_dotenv()

sender_email = os.getenv("email")
receiver_email = os.getenv("email")
password = os.getenv("password")

spot_id = os.getenv("client_id")
spot_secret = os.getenv("client_secret")


URL = "https://pitchfork.com/best/"

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

# 1. Authenticate
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=spot_id,
    client_secret=spot_secret
))

def get_best_album_info():
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

        '''
        print(f"Title: {title}")
        print(f"Artist: {artist}")
        print(f"Cover URL: {cover_url}")
        print(f"Review URL: {review_url}")
        '''
        best_album_info = {
            "title": title,
            "artist": artist,
            "cover_url": cover_url,
            "review_url": " https://pitchfork.com" + review_url,
            "spotify_url": find_album(title)
        }
        return(best_album_info)
    else:
        print("Best New Album section not found.")
        return(None)


def has_new_album(latest_title):
    if not os.path.exists("last_album.txt"):
        return True
    with open("last_album.txt", "r") as f:
        lines = f.readlines()
        if not lines:
            return True
        last = lines[-1].strip()
    return latest_title != last

def save_album(latest_title):
    with open("last_album.txt", "a") as f:  # "a" mode appends to the file
        f.write(latest_title + "\n")        # add a newline after each title



def find_album(album_name):
    # 2. Search Spotify
    results = sp.search(q=f"album:{album_name}", type="album", limit=1)

    # 3. Check if any album found
    albums = results.get("albums", {}).get("items", [])
    if not albums:
        return None  # Album not found

    # 4. Return the Spotify link
    album = albums[0]
    return album["external_urls"]["spotify"]


fake_album_info = {
    "title": "Echoes of Tomorrow13",
    "artist": "The Soundscapers",
    "cover_url": "https://example.com/images/echoes-of-tomorrow.jpg",
    "review_url": "https://pitchfork.com/reviews/albums/the-soundscapers-echoes-of-tomorrow"
} 

def get_average_color(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    np_img = np.array(img)

    # Flatten the image array and compute mean across RGB channels
    avg_color = np_img.mean(axis=(0, 1))
    r, g, b = map(int, avg_color)
    return (r, g, b)



def load_email_template(context, background_color):
    html_path = os.path.join("templates", "email.html")
    css_path = os.path.join("templates", "email.css")

    with open(html_path, "r", encoding="utf-8") as f:
      html = f.read()

    # First substitute variables into HTML
    html = html.format(**context)

    # Then inject raw CSS (no formatting here)
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    background_color = cG.Color(rgb=background_color)
    comp_background = background_color.complementary()

    back_color = str(background_color)[2:]
    comp_back_color = str(comp_background)[2:]
    print(f"back color: {back_color}")
    print(f"comp back color: {comp_back_color}")

    # Replace placeholders in CSS
    css = css.replace("{background_color}", back_color)
    css = css.replace("{comp_background}", comp_back_color)

    html = html.replace(
        '<link rel="stylesheet" href="email.css">',
        f"<style>{css}</style>"
    )
    # Format with context values
    return html


def send_email( album_infoset, sender_email, receiver_email, password_info):
    subject = f"🎶 New Album Alert: {album_infoset['title']}"

    # Create message container
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr(("Pitchfork Scraper", sender_email))
    msg["To"] = receiver_email

    background_color = get_average_color(album_infoset["cover_url"])
    # Path to your HTML template
    html = load_email_template(album_infoset, background_color)

    part = MIMEText(html, "html")
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password_info)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print("successfully sent email")


def main():
    album_info = get_best_album_info()
    print(album_info)
    print("scrape finished")

    if album_info:
        if has_new_album(album_info["title"]):
            print("New album found! Saving...")
            save_album(album_info["title"])
            send_email(album_info, sender_email, receiver_email, password)        
        else:
            print("No new album.")


if __name__ == "__main__":
    main()