import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv("email")
receiver_email = os.getenv("email")
password = os.getenv("password")

#receiver_email="clara.r.s.rose@gmail.com"

URL = "https://pitchfork.com/best/"

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")


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
            "review_url": " https://pitchfork.com" + review_url
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

fake_album_info = {
    "title": "Echoes of Tomorrow13",
    "artist": "The Soundscapers",
    "cover_url": "https://example.com/images/echoes-of-tomorrow.jpg",
    "review_url": "https://pitchfork.com/reviews/albums/the-soundscapers-echoes-of-tomorrow"
} 


def send_email( album_infoset, sender_email, receiver_email, password_info):
    subject = f"New Album Alert: {album_infoset['title']}"
    message = (f"Check out the new album by {album_infoset['artist']}:\n\n"
            f"Title: {album_infoset['title']}\n"
            f"Artist: {album_infoset['artist']}\n"
            f"Cover URL: {album_infoset['cover_url']}\n"
            f"Review URL: {album_infoset['review_url']}")
            

    text = f"Subject: {subject}\nFrom: Pitchfork Scraper <{sender_email}>\nTo: {receiver_email}\n\n{message}"
    

    text = f"subject: {subject}\n\n{message }"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password_info)
    server.sendmail(sender_email, receiver_email, text)
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


