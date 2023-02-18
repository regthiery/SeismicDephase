# Programme d'animation d'ondes unidimensionnelles et d'interférences

Ce programme Python permet de créer des animations représentant des ondes unidimensionnelles 
et leurs interférences créées par leur superposition.


## Installation


Le programme nécessite Python 3 pour fonctionner. Pour installer les dépendances, exécutez la commande suivante :

pip install -r requirements.txt



## Utilisation

La syntaxe de la commande pour exécuter le programme est la suivante :

python3 seismicDephase filename --parallel 6

- `filename` est le nom du fichier script où sont définies les caractéristiques des ondes. 
- `--parallel` est un paramètre optionnel qui indique le nombre de processus parallèles à utiliser pour accélérer le traitement. La valeur par défaut est 1.


## Exemples

Voici quelques exemples de commande pour exécuter le programme :

python3 seismicDephase a00 --parallel 4

Cette commande va créer une animation dans le fichier `a00.mp4` dans le dossier `animations`
 en utilisant 4 processus parallèles pour accélérer le traitement.

## Scripting

Vous pouvez utiliser un script pour personnaliser les paramètres de l'animation et créer des configurations d'ondes spécifiques. 
Le script utilisé par le programme est un simple fichier .txt qui peut être édité à l'aide d'un éditeur de texte standard.

### Paramètres
Les paramètres du script définissent les caractéristiques générales de l'animation, 
telles que les dimensions de l'animation, la durée de l'animation, la fréquence d'images et la position des ondes.

Les paramètres sont stockés dans des variables Python qui peuvent être modifiées directement dans le script. Voici les paramètres les plus courants :

xmin, xmax, tmin, tmax : les limites des axes X et Y de l'animation.
x0 : la position de l'observateur sur l'axe X.
fps : le nombre d'images par seconde de l'animation.

#### Ondes
Les ondes sont définies dans le script à l'aide de la mot clé `wave`. 
Vous pouvez ajouter autant d'ondes que vous le souhaitez.

Voici les paramètres disponibles pour `wave` :

v : la vitesse de propagation de l'onde en m/s.
f : la fréquence de l'onde en Hz.
phase : la phase de l'onde en degrés.

#### Exécution
Une fois que vous avez modifié les paramètres et ajouté des ondes à votre script, vous pouvez l'exécuter en utilisant la commande suivante :

python3 seismicDephase filename --parallel 4
où `filename` est le nom du script (sans son extension .txt) stocké dans le dossier `scripts`.

Le script vous permet de créer des configurations d'ondes complexes et de personnaliser tous les paramètres de l'animation. 






