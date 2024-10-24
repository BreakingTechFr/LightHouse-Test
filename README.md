# LightHouse Test

![Capture d’écran 2024-10-23 à 02 55 18](https://github.com/user-attachments/assets/c2d36f3c-986e-40a3-a5a2-892a982b74ce)

LightHouse Test est un outil en ligne de commande permettant d'analyser la performance, l'accessibilité, les meilleures pratiques et le SEO des sites web en utilisant Lighthouse.

## Fonctionnalités

- Analyse automatique des performances pour mobile et desktop.
- Visualisation des scores dans les catégories suivantes :
  - Performance
  - Accessibilité
  - Meilleures Pratiques
  - SEO
  - First Contentful Paint (FCP)
  - Largest Contentful Paint (LCP)
  - Total Blocking Time (TBT)
  - Cumulative Layout Shift (CLS)
  - Speed Index
- Export des données sous forme de tableau excel .xlsx

## Installation

Prérequis
Python 3.x

Avant d'exécuter ce script, assurez-vous d'avoir installé [Node.js](https://nodejs.org/) et [Lighthouse](https://developers.google.com/web/tools/lighthouse). 

Vous pouvez installer Lighthouse en exécutant la commande suivante :

```shell
npm install -g lighthouse
```

Utilisation
Clonez ce dépôt sur votre machine locale :
```shell
git clone https://github.com/BreakingTechFr/LightHouse-Test.git
```
Se rendre dans le dossier d'installation :
```shell
cd lighthouse-test
```
Installer les bibliothèques requises :
```shell
pip install -r requirements.txt
```
Exécutez le script :
```shell
python lighthouse_test.py
```
Suivez les instructions affichées à l'écran pour tester des URL.

![Capture d’écran 2024-10-23 à 18 03 43](https://github.com/user-attachments/assets/017dc2d5-2867-4329-9d5b-d1e869fc2f22)

Ouvrez le fichier .xlsx pour revoir ultérieurement les scores obtenus

![Capture d’écran 2024-10-24 à 21 37 54](https://github.com/user-attachments/assets/37351763-7056-4c2b-9a90-f47e394d9e01)

## Affichage des résultats

- Affichage des résultats avec un code couleur pour une interprétation rapide :
  - 🟢 **Vert** : Bon résultat.
  - 🟠 **Orange** : Moyen.
  - 🔴 **Rouge** : Doit être amélioré.
 
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 

<<<<<<< HEAD
##Scores pour Desktop
=======
## Scores pour Desktop
>>>>>>> c4a244372e48a9b9f946483aefe217732b67839d
- First Contentful Paint (FCP) : Temps nécessaire pour que le premier élément de contenu soit rendu sur la page.
  - Vert : 0 à 0.94 seconde
  - Orange : 0.95 à 1.6 secondes
  - Rouge : Plus de 2.5 secondes

- Largest Contentful Paint (LCP) : Temps nécessaire pour que le plus grand élément de contenu visible soit rendu.
  - Vert : 0 à 1.21 secondes
  - Orange : 1.22 à 2.41 secondes
  - Rouge : Plus de 2.41 secondes

- Total Blocking Time (TBT) : Temps total pendant lequel la page est bloquée pour les interactions (c'est-à-dire que les utilisateurs ne peuvent pas interagir avec la page).
  - Vert : 0 à 150 millisecondes
  - Orange : 151 à 350 millisecondes
  - Rouge : Plus de 350 millisecondes

- umulative Layout Shift (CLS) : Stabilité visuelle de la page. Un score faible indique moins de décalages de contenu inattendus.
  - Vert : 0 à 0.1
  - Orange : 0.11 à 0.25
  - Rouge : Plus de 0.25

- Speed Index : Mesure de la rapidité à laquelle le contenu est visible pour l'utilisateur.
  - Vert : 0 à 1.32 secondes
  - Orange : 1.33 à 2.31 secondes
  - Rouge : Plus de 5.0 secondes

<<<<<<< HEAD
##Scores pour Mobile
=======
## Scores pour Mobile
>>>>>>> c4a244372e48a9b9f946483aefe217732b67839d
- First Contentful Paint (FCP) : Temps nécessaire pour que le premier élément de contenu soit rendu sur la page.
  - Vert : 0 à 1.82 seconde
  - Orange : 1.83 à 3.01 secondes
  - Rouge : Plus de 3.01 secondes

- Largest Contentful Paint (LCP) : Temps nécessaire pour que le plus grand élément de contenu visible soit rendu.
  - Vert : 0 à 2.52 secondes
  - Orange : 2.53 à 4.01 secondes
  - Rouge : Plus de 4.01 secondes

- Total Blocking Time (TBT) : Temps total pendant lequel la page est bloquée pour les interactions (c'est-à-dire que les utilisateurs ne peuvent pas interagir avec la page).
  - Vert : 0 à 200 millisecondes
  - Orange : 201 à 600 millisecondes
  - Rouge : Plus de 600 millisecondes

- umulative Layout Shift (CLS) : Stabilité visuelle de la page. Un score faible indique moins de décalages de contenu inattendus.
  - Vert : 0 à 0.1
  - Orange : 0.11 à 0.25
  - Rouge : Plus de 0.25

- Speed Index : Mesure de la rapidité à laquelle le contenu est visible pour l'utilisateur.
  - Vert : 0 à 3.42 secondes
  - Orange : 3.43 à 5.82 secondes
  - Rouge : Plus de 5.0 secondes

## Suivez-nous

- [@breakingtechfr](https://twitter.com/BreakingTechFR) sur Twitter.
- [Facebook](https://www.facebook.com/BreakingTechFr/) likez notre page.
- [Instagram](https://www.instagram.com/breakingtechfr/) taguez nous sur vos publications !
- [Discord](https://discord.gg/VYNVBhk) pour parler avec nous !
