import json
import urllib.request

# Impostazioni target
REPO_TARGET = "surrel14/RedditFilter"
OUTPUT_FILE = "apps.json"

# URL delle API di GitHub per l'ultima release
api_url = f"https://api.github.com/repos/{REPO_TARGET}/releases/latest"

req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
        # Cerca l'asset con estensione .ipa
        ipa_asset = None
        for asset in data.get("assets", []):
            if asset["name"].endswith(".ipa"):
                ipa_asset = asset
                break

        if ipa_asset:
            source_data = {
                "name": "Community Apps",
                "identifier": "com.custom.sidestoresource",
                "apps": [
                    {
                        "name": "RedditFilter",
                        "bundleIdentifier": "com.reddit.Reddit", # Bundle ID base di Reddit
                        "developerName": "surrel14",
                        "version": data["tag_name"].lstrip("v"),
                        "versionDate": data["published_at"],
                        "versionDescription": data.get("body", "Nuova release di RedditFilter"),
                        "downloadURL": ipa_asset["browser_download_url"],
                        "localizedDescription": "Reddit patched con tweak e filtri personalizzati.",
                        "iconURL": "https://raw.githubusercontent.com/surrel14/RedditFilter/main/icon.png",
                        "tintColor": "FF4500",
                        "size": ipa_asset["size"]
                    }
                ]
            }

            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(source_data, f, indent=2, ensure_ascii=False)
            
            print("apps.json generato con successo!")
        else:
            print("Nessun file .ipa trovato nell'ultima release.")

except Exception as e:
    print(f"Errore durante la generazione del file: {e}")
