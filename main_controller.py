import json
import time
import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
ACCOUNTS_FILE = 'accounts.json'
GAME_PLACE_ID = "125370362457600"  # Remplacez par l'ID de votre jeu Roblox
MAX_CONCURRENT_BOTS = 3  # Nombre de bots à garder en ligne en même temps
RECONNECT_DELAY = 300  # Temps en secondes avant de reconnecter un bot (5 minutes)
ANTI_AFK_INTERVAL = 600 # Intervalle anti-AFK en secondes (10 minutes)

def load_accounts():
    with open(ACCOUNTS_FILE, 'r') as f:
        return json.load(f)

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f, indent=2)

def launch_bot_node(username, password, place_id):
    """Lance un script de bot individuel pour un compte donné."""
    print(f"[Contrôleur] Lancement du nœud pour {username}...")
    # On passe les infos en arguments au script du nœud
    subprocess.Popen([
        sys.executable, "bot_node.py",
        "--username", username,
        "--password", password,
        "--place_id", place_id,
        "--afk_interval", str(ANTI_AFK_INTERVAL)
    ])

def main_loop():
    accounts = load_accounts()
    
    while True:
        print("\n[Contrôleur] Vérification de l'état des bots...")
        
        # Mettre à jour le statut des bots (ici simplifié, il faudrait une vraie communication)
        # Pour cet exemple, on suppose qu'un bot lancé est "en ligne" jusqu'à ce qu'on le déconnecte.
        
        # Compter les bots actuellement en ligne
        online_bots = [acc for acc in accounts if acc['status'] == 'online']
        
        print(f"[Contrôleur] Bots en ligne : {len(online_bots)}/{MAX_CONCURRENT_BOTS}")

        # Si on a de la place, lancer de nouveaux bots
        if len(online_bots) < MAX_CONCURRENT_BOTS:
            for account in accounts:
                if account['status'] == 'offline':
                    print(f"[Contrôleur] Tentative de connexion pour {account['username']}")
                    account['status'] = 'launching' # Marquer comme en cours de lancement
                    save_accounts(accounts)
                    
                    launch_bot_node(account['username'], account['password'], GAME_PLACE_ID)
                    
                    # On attend un peu avant de lancer le suivant pour éviter de surcharger
                    time.sleep(15) 
                    break # Sortir de la boucle pour réévaluer l'état
        
        # Logique de déconnexion/reconnexion (très simplifiée)
        # Un vrai système aurait besoin de savoir depuis combien de temps un bot est en ligne.
        # Ici, on peut simuler en déconnectant un bot au hasard après un certain temps.
        
        time.sleep(60) # Vérifier toutes les minutes

if __name__ == "__main__":
    print("--- Démarrage du Contrôleur Principal de Bots Roblox ---")
    main_loop()
