import os
import subprocess
import sys
import signal
import time
from tqdm import tqdm
from termcolor import colored
import threading

# Fonction pour effacer le terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Variable globale pour gérer l'état d'arrêt
stop_signal = False

# Fonction pour arrêter proprement le script lors d'un KeyboardInterrupt
def signal_handler(sig, frame):
    global stop_signal
    stop_signal = True  # Mettre le drapeau à True pour indiquer l'arrêt
    print(colored("\nMerci d'avoir utilisé LightHouse Test", "white"))  # Message à afficher
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Fonction pour afficher le logo
def display_logo():
    logo = """
 _       _         _      _    _    _                            _______             _
| |     (_)       | |    | |  | |  | |                          |__   __|           | |
| |      _   __ _ | |__  | |_ | |__| |  ___   _   _  ___   ___     | |     ___  ___ | |_
| |     | | / _` || '_ \\ | __||  __  | / _ \\ | | | |/ __| / _ \\    | |    / _ \\/ __|| __|
| |____ | || (_| || | | || |_ | |  | || (_) || |_| |\\__ \\|  __/    | |   |  __/\\__ \\| |_ 
|______||_| \\__, ||_| |_| \\__||_|  |_| \\___/  \\__,_||___/ \\___|    |_|    \\___||___/ \\__|
             __/ |                                                    
            |___/                                                    by BreakingTech.fr
    """
    print(colored(logo, "red"))

# Menu principal
def menu():
    print(colored("\nBienvenue dans Lighthouse Test", "cyan"))
    print("1. Tester une URL commençant par http, https ou www.")
    print("2. Glissez-déposez un fichier .txt contenant une liste d'URLs")
    print("3. Quitter le programme")
    choice = input(colored("\nFaites votre choix (1, 2 ou 3): ", "green")).strip()
    return choice

# Fonction pour tester une seule URL
def test_single_url():
    url = input(colored("Veuillez entrer l'URL (http, https ou www): ", "white")).strip()
    if not (url.startswith(('http://', 'https://', 'www.')) or 
            url.endswith('nicovip.com')):
        print(colored("L'URL doit commencer par http, https, ou www.", "red"))
        sys.exit(1)
    
    if url.startswith('www.'):
        url = 'http://' + url
    
    return [url]

# Fonction pour tester un fichier .txt contenant des URLs
def test_urls_from_file():
    print(colored("Glissez-déposez ici un fichier .txt contenant les URL :", "white"))
    file_path = input().strip()

    if not os.path.isfile(file_path):
        print(colored("Le fichier spécifié n'existe pas.", "red"))
        sys.exit(1)

    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip().startswith(('http://', 'https://', 'www.')) or
                line.strip() == 'nicovip.com']
    
    if not urls:
        print(colored("Aucune URL valide trouvée dans le fichier.", "red"))
        sys.exit(1)
    
    for i in range(len(urls)):
        if urls[i].startswith('www.'):
            urls[i] = 'http://' + urls[i]

    return urls

# Fonction pour exécuter Lighthouse et récupérer les scores pour une URL
def get_lighthouse_scores(url, strategy):
    print(colored(f"\nAnalyse de {url} ({strategy})", "magenta"))
    
    if strategy == "mobile":
        command = ['lighthouse', url, '--only-categories=performance,accessibility,best-practices,seo', 
                   '--output=json', '--emulated-form-factor=mobile', '--quiet', '--chrome-flags="--headless"']
    else:
        command = ['lighthouse', url, '--only-categories=performance,accessibility,best-practices,seo', 
                   '--output=json', '--preset=desktop', '--quiet', '--chrome-flags="--headless"']

    progress_bar = tqdm(total=100, desc="Analyse en cours", bar_format="{l_bar}{bar} [elapsed: {elapsed}, remaining: {remaining}]")

    def update_progress_bar():
        while progress_bar.n < 100 and not stop_signal:
            time.sleep(0.5)
            progress_bar.update(1)

    thread = threading.Thread(target=update_progress_bar)
    thread.start()

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    progress_bar.n = 100
    progress_bar.close()

    thread.join()  # Assurez-vous que le thread se termine avant de continuer

    if result.returncode != 0:
        print(colored(f"Erreur lors de l'analyse de {url}", "red"))
        return None
    return result.stdout

# Fonction pour extraire et afficher les scores
def display_scores(data, strategy):
    import json
    try:
        json_data = json.loads(data)
        categories = json_data['categories']
        scores = {
            "Performance": int(categories['performance']['score'] * 100),
            "Accessibility": int(categories['accessibility']['score'] * 100),
            "Best Practices": int(categories['best-practices']['score'] * 100),
            "SEO": int(categories['seo']['score'] * 100)
        }
        print(f"\nScores pour {strategy}:")
        for key, score in scores.items():
            color = "red" if score < 50 else "yellow" if score < 90 else "green"
            print(f"{key}: {colored(score, color)}")
    except Exception as e:
        print(colored(f"Erreur lors de la récupération des scores: {e}", "red"))

# Boucle principale
clear_terminal()  # Effacer le terminal au lancement du programme
display_logo()  # Afficher le logo

while True:
    choice = menu()

    if choice == '1':
        urls = test_single_url()
    elif choice == '2':
        urls = test_urls_from_file()
    elif choice == '3':
        print(colored("Merci d'avoir utilisé LightHouse Test. Au revoir !", "white"))  # Message à afficher en blanc
        sys.exit(0)
    else:
        print(colored("Choix invalide.", "red"))
        continue

    for url in urls:
        mobile_data = get_lighthouse_scores(url, "mobile")
        if mobile_data:
            display_scores(mobile_data, "Mobile")

        desktop_data = get_lighthouse_scores(url, "desktop")
        if desktop_data:
            display_scores(desktop_data, "Desktop")

    print(colored("\nAnalyse terminée pour toutes les URLs.", "green"))
    print(colored("\nRetour au menu principal...", "cyan"))
