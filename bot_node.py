import argparse
import time
import sys
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

def anti_afk(interval):
    """Boucle anti-AFK."""
    print(f"[{username}] Démarrage du mode anti-AFK (intervalle: {interval}s).")
    try:
        while True:
            time.sleep(interval)
            # Action simple : bouger la souris un peu
            print(f"[{username}] Action anti-AFK : mouvement de souris.")
            pyautogui.moveRel(50, 50, duration=0.5)
            pyautogui.moveRel(-50, -50, duration=0.5)
    except KeyboardInterrupt:
        print(f"[{username}] Arrêt du mode anti-AFK.")
        sys.exit(0)

def login_and_launch_game(username, password, place_id):
    """Utilise Selenium pour se connecter et lancer le jeu."""
    print(f"[{username}] Initialisation du navigateur...")
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3") # Réduire les logs du navigateur
    # Pour éviter les popups de notification, etc.
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        print(f"[{username}] Navigation vers la page de connexion Roblox...")
        driver.get("https://www.roblox.com/login")
        time.sleep(3)

        print(f"[{username}] Saisie des identifiants...")
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(5) # Attendre la redirection et les vérifications

        # Vérification 2FA ou autre (à gérer manuellement ou avec plus de complexité)
        if "login" in driver.current_url:
            print(f"[{username}] Échec de la connexion (vér
