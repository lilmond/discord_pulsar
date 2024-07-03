import threading
import requests
import random
import time

TOKEN = "" # Edit your Discord token here.

def change_status(text):
    return requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"Authorization": TOKEN}, json={"custom_status": {"text": text, "emoji_id": None}}).json()

def changer():
    while True:
        with open("discord_pulsar_texts.txt", "rb") as file:
            texts = file.read().strip().splitlines()
            file.close()
        
        random.shuffle(texts)

        for text in texts:
            try:
                response = change_status(text.decode())
            except Exception:
                pass
            finally:
                time.sleep(3)

def main():
    try:
        input("Press ENTER to start.")
        threading.Thread(target=changer, daemon=True).start()
        input("Press ENTER or CTRL+C to exit.")
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
