# Pitchfork Best New Album Scraper

This project scrapes Pitchfork's "Best New Album" section, checks if a new album has been posted, and sends an email notification with album details.

## Features

- Scrapes album title, artist, cover image, and review link from Pitchfork.
- Tracks previously seen albums in `last_album.txt`.
- Sends a styled HTML email alert when a new album is found.

## Setup

1. **Clone or download the repository.**

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Configure your email credentials:**
   - Create a `.env` file in the project folder with:
     ```
     email=your_gmail_address@gmail.com
     password=your_gmail_app_password
     receiver_email=recipient_address@gmail.com
     ```
   - For Gmail, you must use an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if 2-Step Verification is enabled.

4. **Run the script:**
   ```
   python main.py
   ```

## How It Works

- The script scrapes Pitchfork's "Best New Album" page.
- If the latest album is not already listed in `last_album.txt`, it saves the title and sends an email notification.
- The email includes the album cover, artist, title, and a link to the review.

## Files

- `main.py` — Main script for scraping and emailing.
- `.env` — Stores your email credentials (not tracked by git).
- `requirements.txt` — Python dependencies.
- `last_album.txt` — Tracks previously notified albums.
- `README.txt` — Project documentation.

## Notes

- Only the latest album is checked and notified.
- The email is sent using Gmail's SMTP server.
- You can customize the HTML email template in `main.py`.

## License
