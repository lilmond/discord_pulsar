import threading
import requests
import time

TOKEN = "" # !~ Edit here ~!
SLEEP_TIME = 2

# !~ Edit your Discord token above.
# You may get it via your browser's developer options, in the Network tab.
# Try to interact within the Discord application to gather requests if it is not doing that.
# E.g: typing "something..." in the message box of the DM panel. 
# Inspect every request until you find a header titled "Authorization".
# Copy the whole value of that header.
# And then paste it above this very long comment. ~!

def edit_status(text, emoji_id, emoji_name):
    emoji_id = None if not emoji_id else emoji_id
    emoji_name = None if not emoji_name else emoji_name
    
    return requests.patch("https://discord.com/api/v9/users/@me/settings", headers={"Authorization": TOKEN}, json={"custom_status": {"text": text, "emoji_id": emoji_id, "emoji_name": emoji_name}}).json()

def discord_pulsar():
    while True:
        with open("discord_pulsar_script.txt", "rb") as file:
            text_lines = file.read().strip().splitlines()
            file.close()

        status_config = {
            "emoji_id": None,
            "emoji_name": None,
            "sleep_time": SLEEP_TIME
        }

        for text_line in text_lines:
            if not text_line.strip():
                continue

            text_line = text_line.decode(errors="replace").strip()
            
            if text_line.startswith("##"):
                continue

            if text_line.startswith("::"):
                text_line = text_line[2:].strip()
                variable_name, variable_value = [x.strip() for x in text_line.split("=", 1)]

                if variable_name in status_config:
                    status_config[variable_name] = variable_value
                
                continue
                
            text = text_line

            try:
                response = edit_status(text=text, emoji_id=status_config["emoji_id"], emoji_name=status_config["emoji_name"])
            except Exception:
                continue

            try:
                sleep_time = int(status_config["sleep_time"])
                time.sleep(sleep_time)
            except Exception:
                pass

def main():
    try:
        input("Press ENTER to start.")
        threading.Thread(target=discord_pulsar, daemon=True).start()
        input("Press ENTER or CTRL+C to exit.")
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
