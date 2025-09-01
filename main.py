import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv("email")
receiver_email = os.getenv("email")
password = os.getenv("password")


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
    subject = f"🎶 New Album Alert: {album_infoset['title']}"

    # Create message container
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr(("Pitchfork Scraper", sender_email))
    msg["To"] = receiver_email

    # HTML version with image + styling
    html = f"""
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #D8D5DB;
        margin: 0;
        padding: 20px;
      }}
      .container {{
        max-width: 500px;
        margin: auto;
        background: #D8D5DB;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        text-align: center;
      }}
      h2 {{
        color: #2D3142;
        margin-bottom: 10px;
      }}
      img {{
        max-width: 100%;
        border-radius: 12px;
        margin: 15px 0;
      }}
      p {{
        font-size: 16px;
        color: #333333;
        margin: 6px 0;
      }}
      .button {{
        display: inline-block;
        padding: 10px 18px;
        margin-top: 15px;
        background-color: #ADACB5;
        color: #2D3142 !important;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
      }}
      .button:hover {{
        background-color: #1a242f;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <h2>🎶 New Album Alert 🎶</h2>
      <img src="{album_infoset['cover_url']}" alt="Album Cover">
      <p><b>Artist:</b> {album_infoset['artist']}</p>
      <p><b>Title:</b> {album_infoset['title']}</p>
      <a class="button" href="{album_infoset['review_url']}">Read the Full Review</a>
    </div>
  </body>
</html>
"""


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