# LightHouse Test

LightHouse Test est un outil en ligne de commande permettant d'analyser la performance, l'accessibilité, les meilleures pratiques et le SEO des sites web en utilisant [Lighthouse](https://developers.google.com/web/tools/lighthouse).

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Exemples](#exemples)
- [Contributions](#contributions)
- [Licence](#licence)

## Fonctionnalités

- Tester des URL individuellement ou à partir d'un fichier .txt contenant une liste d'URL.
- Analyse des performances sur mobile et desktop.
- Affichage des scores dans les catégories suivantes :
  - Performance
  - Accessibilité
  - Meilleures Pratiques
  - SEO
- Gestion des interruptions (KeyboardInterrupt) pour un arrêt propre.

## Installation

Avant d'exécuter ce script, assurez-vous d'avoir installé Node.js et Lighthouse. Vous pouvez installer Lighthouse en exécutant la commande suivante :

```shell
npm install -g lighthouse
```

Prérequis
Python 3.x
Les modules Python suivants :
tqdm
termcolor
Vous pouvez installer les modules manquants avec pip :

```shell
pip install tqdm termcolor
```
Utilisation
Clonez ce dépôt sur votre machine locale :
```shell
git clone https://github.com/votre_nom_utilisateur/lighthouse-test.git
cd lighthouse-test
```
Exécutez le script :
```shell
python votre_script.py
```
Suivez les instructions affichées à l'écran pour tester des URL.
Menu Principal
Tester une URL : Saisissez une URL commençant par http, https, ou www.
Glissez-déposez un fichier .txt : Fournissez un fichier contenant une liste d'URL valides.
Quitter le programme : Fermez l'application.
Exemples
Pour tester une seule URL :
```shell
Veuillez entrer l'URL (http, https ou www): https://example.com
```
Pour utiliser un fichier .txt contenant des URL :
```shell
Glissez-déposez ici un fichier .txt contenant les URL : urls.txt
```

## Suivez-nous

- [@breakingtechfr](https://twitter.com/BreakingTechFR) sur Twitter.
- [Facebook](https://www.facebook.com/BreakingTechFr/) likez notre page.
- [Instagram](https://www.instagram.com/breakingtechfr/) taguez nous sur vos publications !
- [Discord](https://discord.gg/VYNVBhk) pour parler avec nous !
