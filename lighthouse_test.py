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
| |     | | / _` || '_ \ | __||  __  | / _ \ | | | |/ __| / _ \    | |    / _ \/ __|| __|
| |____ | || (_| || | | || |_ | |  | || (_) || |_| |\__ \|  __/    | |   |  __/\__ \| |_
|______||_| \__, ||_| |_| \__||_|  |_| \___/  \__,_||___/ \___|    |_|    \___||___/ \__|
             __/ |
            |___/                                                      by BreakingTech.fr
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
    url = input(colored("Veuillez entrer l'URL (http, https ou www): ", "yellow")).strip()  # Changement en jaune
    if not (url.startswith(('http://', 'https://', 'www.')) or 
            url.endswith('nicovip.com')):
        print(colored("L'URL doit commencer par http, https, ou www.", "red"))
        sys.exit(1)
    
    if url.startswith('www.'):
        url = 'http://' + url
    
    return [url]

# Fonction pour tester un fichier .txt contenant des URLs
def test_urls_from_file():
    print(colored("Glissez-déposez ici un fichier .txt contenant les URL :", "yellow"))  # Changement en jaune
    file_path = input().strip()

    # Remplacer les séquences \ avant des espaces par de simples espaces
    file_path = file_path.replace("\\ ", " ")

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

    progress_bar = tqdm(total=100, desc="Analyse en cours", bar_format="{l_bar}{bar} [Temps écoulé: {elapsed}, Temps restant: {remaining}]")

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

# Fonction pour extraire et afficher les scores sous forme de tableau
def display_scores(data_mobile, data_desktop):
    import json
    try:
        json_data_mobile = json.loads(data_mobile)
        json_data_desktop = json.loads(data_desktop)

        # Scores mobile
        categories_mobile = json_data_mobile['categories']
        scores_mobile = {
            "Performance": int(categories_mobile['performance']['score'] * 100),
            "Accessibility": int(categories_mobile['accessibility']['score'] * 100),
            "Best Practices": int(categories_mobile['best-practices']['score'] * 100),
            "SEO": int(categories_mobile['seo']['score'] * 100)
        }

        # Extraire les scores de performance mobile
        audits_mobile = json_data_mobile['audits']
        fcp_mobile = audits_mobile['first-contentful-paint']['numericValue'] / 1000  # Conversion en secondes
        lcp_mobile = audits_mobile['largest-contentful-paint']['numericValue'] / 1000  # Conversion en secondes
        tbt_mobile = audits_mobile['total-blocking-time']['numericValue']  # En millisecondes
        cls_mobile = audits_mobile['cumulative-layout-shift']['numericValue']  # Score CLS
        speed_index_mobile = audits_mobile['speed-index']['numericValue'] / 1000  # Conversion en secondes

        # Scores desktop
        categories_desktop = json_data_desktop['categories']
        scores_desktop = {
            "Performance": int(categories_desktop['performance']['score'] * 100),
            "Accessibility": int(categories_desktop['accessibility']['score'] * 100),
            "Best Practices": int(categories_desktop['best-practices']['score'] * 100),
            "SEO": int(categories_desktop['seo']['score'] * 100)
        }

        # Extraire les scores de performance desktop
        audits_desktop = json_data_desktop['audits']
        fcp_desktop = audits_desktop['first-contentful-paint']['numericValue'] / 1000  # Conversion en secondes
        lcp_desktop = audits_desktop['largest-contentful-paint']['numericValue'] / 1000  # Conversion en secondes
        tbt_desktop = audits_desktop['total-blocking-time']['numericValue']  # En millisecondes
        cls_desktop = audits_desktop['cumulative-layout-shift']['numericValue']  # Score CLS
        speed_index_desktop = audits_desktop['speed-index']['numericValue'] / 1000  # Conversion en secondes

        # Créer le tableau d'affichage pour Mobile
        print(colored("\nScores pour Mobile", "blue"))
        print(colored("+" + "-"*70 + "+", "cyan"))
        print(colored("| {:<31} | {:<34} |".format("Critère", "Score"), "cyan"))
        print(colored("+" + "-"*70 + "+", "cyan"))

        # Afficher tous les scores dans un seul tableau pour mobile
        print(f"| {colored('Performance', 'white'):<40} | {colored(scores_mobile['Performance'], 'green' if scores_mobile['Performance'] >= 90 else 'yellow' if scores_mobile['Performance'] >= 50 else 'red'):<43} |")
        print(f"| {colored('Accessibility', 'white'):<40} | {colored(scores_mobile['Accessibility'], 'green' if scores_mobile['Accessibility'] >= 90 else 'yellow' if scores_mobile['Accessibility'] >= 50 else 'red'):<43} |")
        print(f"| {colored('Best Practices', 'white'):<40} | {colored(scores_mobile['Best Practices'], 'green' if scores_mobile['Best Practices'] >= 90 else 'yellow' if scores_mobile['Best Practices'] >= 50 else 'red'):<43} |")
        print(f"| {colored('SEO', 'white'):<40} | {colored(scores_mobile['SEO'], 'green' if scores_mobile['SEO'] >= 90 else 'yellow' if scores_mobile['SEO'] >= 50 else 'red'):<43} |")
        print(colored("+" + "-"*70 + "+", "cyan"))

        # Afficher les scores de performance mobile dans le même tableau
        print(f"| {colored('First Contentful Paint (FCP)', 'white'):<40} | {colored(f'{fcp_mobile:.1f}s', 'green' if fcp_mobile <= 1.0 else 'yellow' if fcp_mobile <= 2.5 else 'red'):<43} |")
        print(f"| {colored('Largest Contentful Paint (LCP)', 'white'):<40} | {colored(f'{lcp_mobile:.1f}s', 'green' if lcp_mobile <= 2.5 else 'red'):<43} |")
        print(f"| {colored('Total Blocking Time (TBT)', 'white'):<40} | {colored(f'{tbt_mobile:.4f}ms', 'green' if tbt_mobile <= 300 else 'yellow' if tbt_mobile <= 600 else 'red'):<43} |")
        print(f"| {colored('Cumulative Layout Shift (CLS)', 'white'):<40} | {colored(f'{cls_mobile:.4f}' if cls_mobile > 0 else '0', 'green' if cls_mobile <= 0.1 else 'orange' if cls_mobile <= 0.25 else 'red'):<43} |")
        print(f"| {colored('Speed Index', 'white'):<40} | {colored(f'{speed_index_mobile:.1f}s', 'green' if speed_index_mobile <= 1.0 else 'yellow' if speed_index_mobile <= 2.5 else 'red'):<43} |")
        print(colored("+" + "-"*70 + "+", "cyan"))

        # Créer le tableau d'affichage pour Desktop
        print(colored("\nScores pour Desktop", "blue"))
        print(colored("+" + "-"*70 + "+", "cyan"))
        print(colored("| {:<31} | {:<34} |".format("Critère", "Score"), "cyan"))
        print(colored("+" + "-"*70 + "+", "cyan"))

        # Afficher tous les scores dans un seul tableau pour desktop
        print(f"| {colored('Performance', 'white'):<40} | {colored(scores_desktop['Performance'], 'green' if scores_desktop['Performance'] >= 90 else 'yellow' if scores_desktop['Performance'] >= 50 else 'red'):<43} |")
        print(f"| {colored('Accessibility', 'white'):<40} | {colored(scores_desktop['Accessibility'], 'green' if scores_desktop['Accessibility'] >= 90 else 'yellow' if scores_desktop['Accessibility'] >= 50 else 'red'):<43} |")
        print(f"| {colored('Best Practices', 'white'):<40} | {colored(scores_desktop['Best Practices'], 'green' if scores_desktop['Best Practices'] >= 90 else 'yellow' if scores_desktop['Best Practices'] >= 50 else 'red'):<43} |")
        print(f"| {colored('SEO', 'white'):<40} | {colored(scores_desktop['SEO'], 'green' if scores_desktop['SEO'] >= 90 else 'yellow' if scores_desktop['SEO'] >= 50 else 'red'):<43} |")
        print(colored("+" + "-"*70 + "+", "cyan"))

        # Afficher les scores de performance desktop dans le même tableau
        print(f"| {colored('First Contentful Paint (FCP)', 'white'):<40} | {colored(f'{fcp_desktop:.1f}s', 'green' if fcp_desktop <= 1.0 else 'yellow' if fcp_desktop <= 2.5 else 'red'):<43} |")
        print(f"| {colored('Largest Contentful Paint (LCP)', 'white'):<40} | {colored(f'{lcp_desktop:.1f}s', 'green' if lcp_desktop <= 2.5 else 'red'):<43} |")
        print(f"| {colored('Total Blocking Time (TBT)', 'white'):<40} | {colored(f'{tbt_desktop:.4f}ms', 'green' if tbt_desktop <= 300 else 'yellow' if tbt_desktop <= 600 else 'red'):<43} |")
        print(f"| {colored('Cumulative Layout Shift (CLS)', 'white'):<40} | {colored(f'{cls_desktop:.4f}' if cls_desktop > 0 else '0', 'green' if cls_desktop <= 0.1 else 'orange' if cls_desktop <= 0.25 else 'red'):<43} |")
        print(f"| {colored('Speed Index', 'white'):<40} | {colored(f'{speed_index_desktop:.1f}s', 'green' if speed_index_desktop <= 1.0 else 'yellow' if speed_index_desktop <= 2.5 else 'red'):<43} |")
        print(colored("+" + "-"*70 + "+", "cyan"))

    except json.JSONDecodeError:
        print(colored("Erreur lors de l'analyse des données de Lighthouse.", "red"))

# Fonction principale pour exécuter le programme
def main():
    clear_terminal()
    display_logo()

    while True:
        choice = menu()
        if choice == '1':
            urls = test_single_url()
            for url in urls:
                mobile_data = get_lighthouse_scores(url, "mobile")
                desktop_data = get_lighthouse_scores(url, "desktop")
                if mobile_data and desktop_data:
                    display_scores(mobile_data, desktop_data)
        elif choice == '2':
            urls = test_urls_from_file()
            for url in urls:
                mobile_data = get_lighthouse_scores(url, "mobile")
                desktop_data = get_lighthouse_scores(url, "desktop")
                if mobile_data and desktop_data:
                    display_scores(mobile_data, desktop_data)
        elif choice == '3':
            print(colored("Merci d'avoir utilisé LightHouse Test", "white"))
            break
        else:
            print(colored("Choix invalide, veuillez réessayer.", "red"))

# Point d'entrée du programme
if __name__ == "__main__":
    main()