import smtplib
import os
from dotenv import load_dotenv
from main import get_best_album_info

load_dotenv()

sender_email = os.getenv("email")
receiver_email = os.getenv("email")
password = os.getenv("password")

print(f"sender_email: {sender_email}, receiver_email: {receiver_email}, password: {password}")

'''
sender_email = "theoaronow@gmail.com"
receiver_email = "theoaronow@gmail.com"
password = "amvfxradmglyozos"
'''
album_info = get_best_album_info()
subject = "New Album Alert"
message = (f"Check out the new album by {album_info['artist']}:\n\n"
           f"Title: {album_info['title']}\n"
           f"Artist: {album_info['artist']}\n"
           f"Cover URL: {album_info['cover_url']}\n"
           f"Review URL: {album_info['review_url']}")

text = f"subject: {subject}\n\n{message }"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

server.login(sender_email, password)

server.sendmail(sender_email, receiver_email, text) 

print("email has been sent to " + receiver_email)