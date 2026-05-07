# **Conception Architecturale et Modélisation Biologique d'une Simulation Écosystémique Émergente pour le Jeu Vidéo**

## **Introduction à la Complexité Émergente et aux Écosystèmes Virtuels**

La création de mondes virtuels capables de simuler la vie de manière autonome représente l'un des sommets de l'ingénierie vidéoludique contemporaine. Traditionnellement, l'industrie du jeu vidéo s'est appuyée sur des apparitions d'ennemis scriptées (spawning), des points d'intérêt statiques et des routines comportementales rigides déclenchées par la proximité du joueur. Cependant, des œuvres pionnières telles que *Dwarf Fortress*, *Rain World*, ou encore les écosystèmes complexes observables dans *Red Dead Redemption 2*, ont démontré la viabilité et l'attrait immersif des systèmes émergents.1 Dans ces environnements, la faune et la flore interagissent selon des règles systémiques locales, générant des comportements macroscopiques imprévisibles qui donnent l'illusion d'un monde préexistant à l'intervention humaine.2

Le projet d'élaborer une simulation de monstres pour un jeu de gestion de guilde (de type "Isekai Fantasy") nécessite de s'affranchir totalement des mécaniques d'apparition arbitraires. La proposition centrale consiste à concevoir un écosystème autogéré, fondé sur des recherches en biologie comportementale et en dynamique des populations, où le joueur, en tant que maître de guilde, agit non pas comme le centre de l'univers, mais comme une force régulatrice au sein d'un réseau trophique fragile.6 L'objectif est de simuler des croissances de populations, des dynamiques de meutes avec des chefs pouvant évoluer en "bosses", des zones d'influence territoriales strictes, et des mécanismes d'évolution sélective créant des lignées familiales et des anomalies biologiques (monstres de rang S).8

La viabilité d'un tel système repose sur un équilibre délicat entre la rigueur de la simulation biologique et les contraintes computationnelles inhérentes au traitement en temps réel d'un grand nombre d'entités.1 Les Modèles Centrés sur l'Individu (Agent-Based Models ou ABM) constituent la fondation algorithmique idéale pour capturer ces interactions complexes, permettant aux propriétés de niveau populationnel d'émerger organiquement des simulations au niveau individuel.8 Ce rapport exhaustif détaille les fondements mathématiques, biologiques et architecturaux nécessaires pour concrétiser cette vision, culminant avec un cahier des charges opératoire (prompt) destiné à un agent d'intelligence artificielle pour l'implémentation d'un prototype visuel via la bibliothèque Pygame.

## **Modélisation Mathématique de la Dynamique des Populations**

Pour qu'un écosystème virtuel transcende la simple illusion et devienne une entité gérable par le joueur, il doit obéir à des lois de conservation métabolique et de dynamique des populations. La présence de proies et de prédateurs ne peut être laissée au hasard ; elle doit fluctuer en réponse à des pressions environnementales modélisables.

### **Le Modèle de Lotka-Volterra et ses Extensions**

Le fondement théorique de toute simulation prédateur-proie repose sur les équations de Lotka-Volterra, un système d'équations différentielles non linéaires du premier ordre développé indépendamment par Alfred J. Lotka et Vito Volterra au début du vingtième siècle.16 Ces équations décrivent la dynamique temporelle de systèmes biologiques dans lesquels deux espèces interagissent, l'une en tant que prédateur et l'autre en tant que proie.

Les équations fondamentales s'expriment de la manière suivante :

$$\frac{dx}{dt} = \alpha x - \beta xy$$

$$\frac{dy}{dt} = -\gamma y + \delta xy$$

Dans ce formalisme continu, la variable $x$ représente la densité de la population de proies (par exemple, des monstres herbivores mineurs), tandis que $y$ désigne la densité de la population de prédateurs (les carnivores ou monstres supérieurs).16 Le paramètre $\alpha$ définit le taux de croissance per capita des proies en l'absence de toute menace prédatrice, modélisant une croissance exponentielle théorique. Le paramètre $\beta$ quantifie l'effet négatif de l'interaction entre les deux espèces sur la population de proies, c'est-à-dire le taux de mortalité dû à la prédation. Du côté des prédateurs, $\gamma$ représente leur taux de mortalité naturel (ou taux de déclin) lorsqu'ils sont privés de source de nourriture, et $\delta$ illustre l'efficacité avec laquelle la consommation des proies se traduit par la naissance de nouveaux prédateurs.16

Cependant, l'application directe et naïve de ce modèle dans un jeu vidéo pose des défis majeurs. Le système classique de Lotka-Volterra est structurellement instable sur le long terme dans un environnement discret, générant des oscillations perpétuelles dont l'amplitude dépend uniquement des conditions initiales. Si les populations simulées sont limitées (ce qui est toujours le cas dans un jeu en raison des contraintes de mémoire), une baisse sévère de la courbe peut amener une population à tomber en dessous d'un seuil critique (moins d'un individu), provoquant une "pseudo-extinction" irréversible qui briserait la boucle de gameplay.17 De plus, le modèle original postule un taux d'attaque constant et une croissance illimitée des proies, ce qui est écologiquement irréaliste.

Pour adapter ce modèle mathématique aux exigences d'un écosystème vidéoludique résilient, plusieurs améliorations s'imposent. L'introduction de la notion de capacité de charge environnementale ($K$) transforme la croissance exponentielle en croissance logistique, simulant la compétition intraspécifique pour des ressources finies (comme l'herbe, le mana ambiant ou l'espace).18 De plus, la recherche contemporaine en écologie théorique démontre que l'intégration de variations intraspécifiques (différents phénotypes au sein d'une même espèce, comme des individus plus vulnérables et d'autres mieux défendus) fournit une voie alternative puissante vers la stabilisation du système.19 En dotant les agents de traits comportementaux hétérogènes, tels que la capacité de se réfugier dans des zones inaccessibles aux prédateurs au prix d'une dépense énergétique moindre, le système évite l'effondrement simultané des populations.20 Dans le jeu, cela se traduira par des tanières ou des environnements topographiquement complexes où les proies peuvent échapper à l'annihilation totale, garantissant un cycle perpétuel d'émergence.

### **La Théorie de la Sélection r/K et la Diversité du Bestiaire**

Afin de générer une taxonomie de monstres variée et de justifier biologiquement la coexistence de hordes d'ennemis faibles et de créatures solitaires surpuissantes (les "bosses"), la simulation doit intégrer les principes de la théorie de la sélection r/K.21 Formulée dans les années 1960 par les écologistes Robert MacArthur et E. O. Wilson dans le cadre de leurs travaux sur la biogéographie insulaire, cette hypothèse évolutive examine comment les organismes opèrent un compromis fondamental entre la quantité et la qualité de leur progéniture en réponse à la stabilité de leur environnement.21

| Stratégie Évolutive | Profil Biologique et Investissement | Traduction dans le Game Design (Types de Monstres) |
| :---- | :---- | :---- |
| **Sélection r (r-strategists)** | Production massive d'une progéniture "bon marché" sur le plan métabolique. Croissance rapide, maturité sexuelle précoce, espérance de vie courte, faible investissement parental. Prospère dans des environnements instables ou perturbés.21 | Monstres de type "essaim" (Slimes, Gobelins, Insectes géants). Faibles points de vie, dégâts minimes, mais redoutables en nombre. Ils colonisent rapidement les zones récemment vidées par les expéditions de la guilde. |
| **Sélection K (K-strategists)** | Progéniture numériquement restreinte mais "coûteuse". Longue gestation, soins parentaux intenses, maturité tardive, grande longévité. Adaptés aux environnements stables, proches de la capacité de charge maximale du milieu.21 | Monstres d'élite et Bosses (Dragons, Béhémoths, Lycans anciens). Statistiques massives, apprentissage au combat (évasion, parades). Nécessitent des ressources colossales, d'où leur nature hautement territoriale et solitaire.21 |

Cette dichotomie biologique fournit un cadre de conception élégant pour la structuration de la difficulté et de l'économie du jeu. Les espèces à stratégie "r" fourniront au joueur un flux constant de matériaux d'artisanat de bas niveau, nécessitant une régulation de masse pour éviter qu'ils ne détruisent l'infrastructure locale. À l'inverse, l'apparition d'un stratège "K" constituera un événement majeur. Si l'environnement de la simulation reste stable pendant une longue période (par exemple, si le joueur néglige d'explorer ou de chasser dans un secteur spécifique), ce secteur atteindra sa capacité de charge. Les individus qui y survivent investiront massivement dans leur survie individuelle, évoluant lentement vers des statuts de prédateurs apex (bosses).

## **Génétique Appliquée, Évolution Sélective et Émergence des Anomalies**

La promesse d'une simulation autogérée repose sur l'idée que les monstres ne sont pas des entités immuables, mais des organismes capables de s'adapter, de croître et de muter. Le joueur ne doit jamais affronter deux fois exactement la même créature si un temps significatif s'est écoulé. L'implémentation de la génétique et de l'évolution sélective est le moteur de cette variabilité systémique.

### **Implémentation des Algorithmes Génétiques**

L'algorithme génétique (GA) est une heuristique de recherche et d'optimisation qui mime le processus de la sélection naturelle darwinienne.22 Dans le cadre du développement de jeux, et plus spécifiquement pour la création de comportements émergents, les algorithmes génétiques permettent d'ajuster dynamiquement la difficulté et de générer des ennemis de plus en plus compétents sans intervention manuelle des concepteurs.24

Le génome de chaque monstre de la simulation doit être représenté par une structure de données (généralement un tableau de valeurs flottantes ou un codage binaire) englobant ses traits fonctionnels : vitesse de déplacement, force d'attaque, rayon de perception visuelle et olfactive, taux d'assimilation de la biomasse, et seuil de tolérance à la douleur.22 La boucle évolutive s'articule autour des étapes suivantes :

| Étape de l'Algorithme | Processus Biologique Simulé | Fonction Computationnelle dans le Moteur Pygame |
| :---- | :---- | :---- |
| **Évaluation (Fitness)** | La survie du plus apte. Capacité à trouver de la nourriture et à éviter les prédateurs. | Une fonction évaluant la performance de l'agent. Le score est incrémenté pour chaque proie consommée et chaque minute survécue, et pénalisé pour les dégâts subis.22 |
| **Sélection (Selection)** | La compétition pour la reproduction. | Choix des parents via une méthode de roulette ou de tournoi. Une stratégie d'"élitisme" (préservation des 10 % des meilleurs individus) garantit que les traits exceptionnels ne régressent pas d'une génération à l'autre.11 |
| **Croisement (Crossover)** | L'hérédité. L'échange de matériel génétique créant de nouvelles combinaisons. | Interpolation linéaire ou échange de segments de tableaux entre deux agents parents pour générer les attributs de la progéniture (les nouveaux objets instanciés dans la simulation).22 |
| **Mutation (Mutation)** | L'introduction aléatoire de nouveauté génétique. | Altération probabiliste (ex: 5% de chance) d'un ou plusieurs gènes de la progéniture, ajoutant ou soustrayant une valeur aléatoire dans des limites définies, prévenant ainsi la stagnation locale de la population.22 |

La magie de ce système réside dans l'interaction avec le joueur. Si la guilde adopte une stratégie consistant à éliminer systématiquement les monstres lents (car plus faciles à cibler), le processus de sélection naturelle de la simulation favorisera automatiquement les individus ayant hérité d'une grande vitesse. Quelques heures de jeu plus tard, la population entière de cette espèce aura considérablement augmenté sa célérité globale, forçant le joueur à revoir ses tactiques. C'est l'essence même de la coévolution en boucle fermée.

### **Robustesse Dérivationnelle, Effondrement Mutationnel et Création de Bosses**

L'une des demandes les plus spécifiques concerne la création organique de monstres aberrants, des "anomalies" de Rang S qui apparaissent de manière imprévue et terrorisent les autres créatures. Les mécanismes de la génétique des populations offrent une solution élégante à travers l'étude des petites populations.

Dans des populations larges et panmictiques, les mutations extrêmes sont généralement lissées et ramenées vers la moyenne par le brassage génétique. Cependant, la dynamique change drastiquement lorsque la taille de la population diminue de manière critique. Les modèles mathématiques d'évolution soulignent le rôle de la dérive génétique, un phénomène stochastique où la fréquence des allèles fluctue aléatoirement, qui devient prédominant dans les petits groupes.31 Lorsque la taille d'une population chute (par exemple, à la suite d'une campagne de purification intense menée par la guilde), la sélection naturelle est affaiblie au profit de la dérive.31

Ce goulot d'étranglement peut conduire à deux résultats opposés, tous deux fascinants pour le gameplay. D'une part, le "mutational meltdown" (effondrement mutationnel) théorisé par les généticiens des populations (comme le modèle du rochet de Muller) décrit l'accumulation excessive de mutations délétères conduisant à l'extinction locale.31 D'autre part, les recherches sur la "drift robustness" (robustesse face à la dérive) indiquent que dans des paysages de fitness complexes (complex fitness landscapes), une petite population peut explorer des pics évolutifs étroits et abrupts qu'une grande population ne pourrait jamais atteindre.33

Concrètement, dans le code du jeu, si le nombre d'individus d'une espèce dans un secteur donné tombe sous un seuil critique, le taux de mutation et les bornes d'amplitude de mutation (les variables mutation_rate et mutation_amount de l'algorithme génétique 22) doivent être artificiellement amplifiés par le moteur. Les quelques survivants muteront de façon chaotique. La plupart mourront, mais occasionnellement, un individu héritera d'une combinaison de gènes synergique extraordinaire : une taille doublée, une armure épaisse, et une hyper-agressivité. Ce "Super-individu" brise la symétrie de son espèce.34 Il survivra, éliminera ses concurrents restants, et s'établira comme un Boss territorial unique. L'anomalie n'a donc pas été artificiellement injectée par un script ; elle a émergé d'un désastre écologique provoqué par le joueur.

### **La Règle Insulaire (Gigantisme et Nanisme)**

Pour enrichir davantage la génération procédurale d'anomalies, le système doit intégrer les principes biogéographiques de la "Règle Insulaire" (Island Rule), postulée par le biologiste J. Bristol Foster en 1964.36 L'analyse de milliers d'espèces vertébrées a confirmé que, lorsqu'elles sont isolées dans des environnements clos (îles réelles ou habitats très fragmentés), les espèces subissent des pressions sélectives uniques modifiant radicalement leur morphologie.9

Selon cette règle écologique, les espèces de petite taille (comme les rongeurs ou les insectes) ayant colonisé un milieu isolé ont tendance à évoluer vers le gigantisme.9 Libérés de la pression de leurs prédateurs continentaux et capables d'exploiter de nouvelles niches écologiques, leur taille corporelle s'accroît sur quelques centaines de générations.9 À l'inverse, les grands mammifères isolés sur des îles font face à une pénurie chronique de ressources spatiales et alimentaires, ce qui favorise une forte sélection pour une réduction de taille, aboutissant au nanisme insulaire (tels que les éléphants nains de la Méditerranée préhistorique).9

Dans la topologie du jeu (2D top-down), certaines zones peuvent être conçues comme des "îles" terrestres : de profondes vallées entourées de montagnes infranchissables, ou des systèmes de grottes sans issue facile.40 L'algorithme de partitionnement spatial surveillera la connectivité de ces zones. Si un petit groupe de monstres mineurs (ex: Gobelins ou Rats géants) se retrouve isolé dans l'une de ces poches et qu'aucun grand prédateur n'y a accès, le moteur de simulation ajustera l'optimum phénotypique de leur taille vers le haut. Au fil du temps, le joueur, lors d'une expédition d'exploration lointaine (qui prend des jours dans l'univers du jeu 40), découvrira avec stupeur une colonie de rats gigantesques, terrifiants et aux statistiques démesurées. Cette mécanique récompense l'exploration spatiale par la découverte de la curiosité biologique.4

## **Structuration Sociale : Territoires, Meutes et Lignées Familiales**

L'émergence d'une intelligence collective et la gestion de territoires définissent le passage d'une simple simulation de particules à un écosystème vivant et réactif. L'organisation sociale des monstres doit aller au-delà du comportement d'essaimage aveugle.

### **Le Cycle de Vie des Meutes et les Lignées**

Pour simuler des espèces prédatrices avancées (comme les loups de fantasy), il est crucial d'implémenter des Modèles Centrés sur l'Individu capables de représenter des interactions sociales complexes.8 Les meutes ne sont pas de simples groupes agglomérés ; elles possèdent une structure hiérarchique et un cycle de vie dictés par l'écologie comportementale.8

Les recherches sur le cycle de vie sociétal des loups identifient des processus clés qui régissent la dynamique de la population et qui doivent être transcrits en règles algorithmiques : la dissolution de la meute suite à la perte d'un reproducteur, l'adoption de jeunes disperseurs, l'établissement de nouveaux territoires par "bourgeonnement" (budding) et le remplacement du leader.8

1. **Lignées et Reconnaissance Familiale :** Chaque agent doit posséder un identifiant de lignée (un marqueur génétique simple). Les comportements de sélection de parentèle (kin selection) postulent que les individus favorisent le succès reproducteur de leurs apparentés. Dans le code, la routine d'agression vérifiera l'identifiant de lignée avant d'attaquer ; des meutes apparentées pourraient ainsi partager des territoires de chasse limitrophes avec une hostilité réduite, créant des "super-familles" régionales.  
2. **Remplacement et Adoption :** La meute est structurée autour d'un Alpha (le monstre ayant le fitness ou les statistiques de combat les plus élevés). Si un monstre extérieur solitaire, possédant de meilleures statistiques, rencontre la meute, il peut y avoir un duel. Le vainqueur devient le nouvel Alpha, absorbant la meute (remplacement). De même, de jeunes monstres errants peuvent être adoptés par des meutes existantes si la capacité de charge locale n'est pas atteinte.8  
3. **Fragmentation et Bourgeonnement (Budding) :** Lorsqu'une meute devient trop grande et épuise les ressources locales, l'algorithme doit déclencher une scission. Un sous-groupe (souvent mené par un Beta ambitieux) se détachera pour former une nouvelle meute et migrer vers un territoire adjacent non réclamé.8  
4. **Conséquences de l'Intervention du Joueur :** Si la guilde assassine l'Alpha d'une meute bien établie (pour récupérer un trophée de grande valeur), la simulation calcule une probabilité de dissolution. La meute peut se disloquer en une douzaine de monstres solitaires et agressifs qui se répandront sur la carte, causant un chaos imprévu sur les routes commerciales. Le joueur réalise alors que l'élimination d'un "boss" engendre des répercussions sociales dramatiques.8

### **Distanciation Sociale Animale et Zones d'Influence**

Les territoires servent de multiples fonctions biologiques. Non seulement ils assurent le monopole des ressources alimentaires et des opportunités d'accouplement 12, mais ils agissent également comme une barrière épidémiologique. Des modèles mathématiques de transmission des maladies, intégrant les mouvements animaux, démontrent que le comportement territorial aide à "aplatir la courbe" des infections au sein d'une population sauvage.41

En marquant leurs frontières (notamment par des phéromones ou signaux olfactifs), les animaux maintiennent une forme de distanciation sociale.41 Si la simulation intègre des maladies (par exemple, un poison ou une peste que la guilde tente d'utiliser pour réduire les populations), l'efficacité de cette arme biologique dépendra de la structure territoriale. Les espèces hautement territoriales limiteront la propagation de la maladie, l'épidémie durant plus longtemps mais touchant moins d'individus simultanément, tandis que les espèces grégaires de type r seront décimées rapidement.41 Ces dynamiques spatiales complexes valident l'approche par simulation mécanistique : les processus locaux engendrent des modèles globaux observables.12

## **Systèmes de Navigation Sensorielle : Cartes Olfactives et Champs de Vecteurs**

Le défi technique majeur de la simulation réside dans le déplacement intelligent de milliers de créatures autonomes sur une grande carte 2D. L'utilisation d'algorithmes de recherche de chemin standard, tels que A* (A-Star) ou l'algorithme de Dijkstra, calculerait la route optimale en contournant les obstacles de manière rigide. Appliqué à des milliers d'agents simultanément, ce processus saturerait instantanément l'unité centrale (CPU), entraînant un effondrement des performances.42 De surcroît, les animaux sauvages ne connaissent pas l'architecture absolue d'un labyrinthe ; ils naviguent par l'instinct, la vision directe et, surtout, l'odorat.

### **La Diffusion Collaborative (Scent Maps)**

Pour émuler le comportement territorial et les traques prédatrices de manière hautement optimisée, l'architecture doit s'appuyer sur des Champs de Diffusion Collaborative (Collaborative Diffusion) ou des "Cartes Olfactives" (Scent Maps).42 Cette approche remplace le calcul vectoriel complexe par une simple lecture de grille thermique.

Le principe est le suivant : l'espace de jeu est divisé en une matrice bidimensionnelle (une grille). Lorsqu'un joueur, un monstre proie, ou un prédateur se déplace, il "dépose" une valeur numérique élevée (l'odeur) sur la cellule qu'il occupe.42 À chaque itération de la boucle de jeu, cette carte subit deux processus mathématiques parallèles : la dégradation spatio-temporelle (Decay) et la diffusion spatiale.43

L'équation gouvernant l'état d'une cellule $(x, y)$ à l'instant $t+1$ peut être conceptualisée ainsi :

$$S_{(x,y)}^{t+1} = (S_{(x,y)}^t \times \lambda) + \frac{\alpha}{N} \sum_{i=1}^{N} S_{i}^t$$

Où $\lambda$ est un coefficient de dégradation stricte (compris entre 0 et 1), $\alpha$ est le taux de diffusion, et $\sum S_i^t$ représente la somme des valeurs d'odeur des $N$ cellules immédiatement adjacentes. L'odeur la plus intense se situe donc à la source, s'atténuant progressivement en s'éloignant pour former un dégradé ou un gradient thermique continu.42

### **Comportements Émergents par Gradients**

Les avantages computationnels et comportementaux de cette méthode sont inestimables pour la simulation :

* **Performance Asymétrique :** Au lieu de calculer $M$ chemins pour $M$ monstres, le système ne met à jour la carte de diffusion qu'à des intervalles réguliers (par exemple, tous les dixièmes de seconde). Les prédateurs n'ont alors besoin d'aucun algorithme de *pathfinding* : ils inspectent simplement les 8 cellules qui les entourent et avancent vers celle ayant la plus forte concentration de l'odeur de la proie désirée.42 Le coût CPU est infinitésimal comparé à A*.42  
* **Contournement d'Obstacles Organique :** L'algorithme de diffusion est conçu pour que la propagation de l'odeur soit bloquée par les murs et les éléments topographiques infranchissables.43 L'odeur doit donc "s'infiltrer" autour des murs. Un loup traquant un gobelin caché derrière une colline suivra naturellement le flux d'odeur contournant l'obstacle, sans jamais se retrouver bloqué contre une surface plane, imitant une traque sensorielle parfaitement crédible.43  
* **Manœuvres de Meute par Répulsion :** C'est ici que l'émergence devient spectaculaire. Si l'on configure les monstres de la même espèce pour qu'ils émettent simultanément une odeur attractive pour leurs proies et une odeur légèrement *répulsive* (valeur négative) pour leurs congénères, les membres d'une meute éviteront naturellement de se superposer sur la même trajectoire.43 En suivant la proie tout en se repoussant mutuellement, les prédateurs vont se déployer, se diviser autour des obstacles, et finir par encercler la cible (Flanking) de multiples côtés. Une manœuvre tactique complexe a émergé d'une simple addition de champs scalaires.43  
* **Cartographie Territoriale Émergente :** Si un Boss (Super-individu) dépose une "Odeur de Terreur" persistante, les monstres mineurs fuyant cette odeur créeront une zone circulaire vide d'activité autour du repaire du monstre de Rang S. En observant la densité de la carte, le joueur identifiera immédiatement les "Zones d'Influence", visualisant les luttes d'hégémonie invisibles qui se jouent dans le code.44 Les traces odorantes cumulées peuvent générer des motifs spatiaux périodiques structurant le déplacement entier des animaux.44

## **Réseaux Trophiques, Gestion de Guilde et Cascades Écologiques**

Le cœur ludique du projet ne réside pas dans la simple observation d'un aquarium virtuel, mais dans l'interaction entre les impératifs économiques de la guilde et la préservation de l'écosystème. Le gestionnaire de la guilde tire ses profits de l'extraction de matières premières sur les cadavres de monstres. La rentabilité est donc indissociable de la gestion des ressources naturelles, créant un paradigme inspiré de la "tragédie des biens communs".7

### **Architecture des Niveaux Trophiques**

La simulation doit modéliser fidèlement la structure d'un réseau trophique (food web), décrivant les relations séquentielles de "qui mange qui" et le transfert unidirectionnel de l'énergie et de la biomasse.47 Les fondements thermodynamiques des écosystèmes dictent qu'à chaque niveau trophique, une immense quantité d'énergie est perdue sous forme de chaleur métabolique (la fameuse règle écologique de l'efficience de 10 %).49 Pour maintenir un seul prédateur apex, la simulation doit générer des dizaines de prédateurs intermédiaires, des centaines de proies, et des milliers d'unités de biomasse végétale.49

| Classification Trophique | Description et Source d'Énergie | Rôle Systémique et Économique dans le Jeu |
| :---- | :---- | :---- |
| **Producteurs (Autotrophes)** | Entités capables de synthétiser leur propre énergie (Plantes, Cristaux de Mana, Algues). Croissance exponentielle freinée par la saturation spatiale.47 | Ressource de base absolue. Si la guilde rase les forêts pour le bois, l'écosystème entier périclite. |
| **Consommateurs Primaires (Hétérotrophes de base)** | Herbivores et brouteurs (Monstres de rang F ou E). Nourrissement exclusif par broutage des producteurs.47 | Maintenir la biomasse végétale sous contrôle (empêcher la sursaturation algorithmique). Matériaux de craft bas de gamme mais abondants.51 |
| **Consommateurs Secondaires/Tertiaires** | Prédateurs carnivores chassant les herbivores et les petits monstres.47 | Régulation des herbivores. Cibles principales des quêtes d'élimination de la guilde pour obtenir des peaux et des noyaux magiques de qualité marchande. |
| **Prédateurs Apex (Bosses / Rang S)** | Le sommet absolu de la pyramide. N'ont aucun prédateur naturel (excepté la Guilde du joueur).49 | Contrôleurs de la stabilité descendante (Top-Down). Fournissent des matériaux légendaires, mais posent une menace cataclysmique s'ils migrent près des installations humaines.6 |

### **Le Piège des Cascades Trophiques**

L'ingérence du joueur dans cet écosystème déclenchera inévitablement des cascades trophiques, concept majeur popularisé par le zoologiste américain Robert Paine.6 Une cascade trophique représente les bouleversements spectaculaires et indirects induits par la suppression d'un maillon de la chaîne, modifiant l'abondance de multiples espèces aux niveaux inférieurs.6

L'exemple canonique, parfaitement transposable au gameplay, est la suppression du Prédateur Apex.6 Imaginons que le joueur, attiré par la perspective de récolter un trophée d'une immense valeur financière, mobilise toutes les ressources de sa guilde pour abattre un "Dragon" territorial (Prédateur Apex). Sa mort génère un profit immédiat, mais provoque une réaction en chaîne catastrophique : le relâchement des mésoprédateurs (mesopredator release).6

Sans le Dragon pour chasser, tuer et intimider les loups géants ou autres prédateurs intermédiaires, la population de ces derniers va croître de manière exponentielle.6 Ces meutes de loups surpeuplées vont alors exercer une pression écrasante sur les consommateurs primaires (les proies herbivores), les conduisant vers une éradication locale.6 Sans herbivores, la végétation s'étouffe, et la famine frappe les loups qui, désespérés, commencent à attaquer frénétiquement les villages protégés par la guilde.54 Le joueur réalise que sa quête de profit a détruit la base renouvelable de son économie.45 La guilde doit alors agir en véritable gestionnaire forestier, opérant des abattages sélectifs (culling) sur les niveaux intermédiaires pour restaurer un équilibre artificiel, respectant le principe selon lequel l'humanité ne peut survivre qu'en imitant la nature et en récoltant avec parcimonie.7

### **Perturbations Exogènes : Gestion des Espèces Invasives**

Pour maintenir l'imprévisibilité et la tension sur le long terme, des anomalies supplémentaires sous forme d'espèces invasives peuvent être introduites aléatoirement.57 Ces espèces non-indigènes, introduites par des migrations accidentelles, sont dépourvues de prédateurs naturels dans le nouvel environnement et bénéficient de traits génétiques souvent dévastateurs pour les espèces locales.58

La gestion de ces invasions devient un problème économique et stratégique. Si le joueur tarde à réagir, l'espèce invasive monopolise les ressources, détruit la biodiversité indigène dont dépend la guilde, et s'installe définitivement.57 Cependant, les modèles génétiques montrent que, bien que les espèces invasives prolifèrent numériquement, elles souffrent souvent d'un déficit initial de diversité génétique (effet fondateur) par rapport aux espèces natives endémiques.60 Le joueur pourrait exploiter cette faiblesse, par exemple en identifiant (via des outils d'analyse de la guilde) une vulnérabilité biologique spécifique à cette espèce homogène pour développer un traitement ciblé avant qu'elle ne s'adapte, soulignant que la prévention coûte infiniment moins cher que l'éradication une fois l'ancrage écologique établi.57

## **Architecture Logicielle, Partitionnement Spatial et Optimisation**

L'ensemble de ce corpus théorique, aussi riche soit-il, est inutile s'il paralyse le processeur (CPU) après quelques minutes de fonctionnement. La transcription des modèles écologiques en une simulation logicielle via Python et la bibliothèque Pygame requiert une optimisation computationnelle draconienne, fondée sur des motifs de conception (Design Patterns) et des structures de données géométriques avancées.61

### **La Fin de la Force Brute : Le Quadtree**

Dans un moteur de jeu naif, la détection des collisions, du champ de vision, ou de la simple proximité nécessite que chaque entité vérifie sa position par rapport à toutes les autres. Pour un écosystème de $N$ monstres, le nombre d'opérations par itération (frame) s'élève à $N \times N$ (soit $O(N^2)$). Si l'on souhaite simuler 1000 entités, le système devra effectuer 1 000 000 de calculs de distance par dixième de seconde, ce qui effondrera le taux de rafraîchissement (framerate).65

La solution algorithmique indispensable est le partitionnement spatial, et plus spécifiquement l'implémentation d'un Quadtree.65

| Algorithme de Recherche | Complexité Théorique | Impact sur la Simulation de l'Écosystème |
| :---- | :---- | :---- |
| **Comparaison Force Brute** | **$O(N^2)$** | Paralysie du moteur au-delà de 300 agents. Les interactions sociales et les algorithmes génétiques deviennent impossibles en temps réel.65 |
| **Partitionnement Spatial (Quadtree)** | **$O(N \log N)$** | Permet de simuler des milliers d'entités simultanément, de calculer les essaims (flocking boids) et les chaînes alimentaires de manière fluide.65 |

Le Quadtree est une structure de données arborescente.68 L'espace virtuel (la carte totale) constitue le nœud racine. À chaque étape de la boucle de jeu (Game Loop), le Quadtree est vidé puis reconstruit. Lorsqu'une entité est insérée, le Quadtree vérifie le nombre d'objets présents dans le quadrant. Si le nombre dépasse une capacité définie (le seuil de subdivision, par exemple 4 ou 10 objets), le quadrant se scinde de manière récursive en quatre sous-quadrants égaux (Nord-Ouest, Nord-Est, Sud-Ouest, Sud-Est).67 Les entités sont redistribuées dans ces sous-divisions.

Grâce à cette arborescence, lorsqu'un loup doit chercher la proie la plus proche ou vérifier s'il entre en collision avec un arbre, il n'interroge que la liste des objets stockés dans son propre nœud de profondeur maximale (ou les nœuds adjacents si son rayon de recherche empiète sur les bordures).65 Une recherche qui nécessitait auparavant mille comparaisons s'exécute désormais en moins d'une dizaine d'opérations. L'ajout, la suppression et le déplacement d'entités s'effectuent à une vitesse fulgurante.67 Ce composant est l'épine dorsale absolue de tout modèle de dynamique des populations computationnel.

### **Principes SOLID, Boucle de Jeu et Machines à États**

L'architecture du code doit strictement séparer la logique de simulation de la logique d'affichage, suivant les principes SOLID.62 La "Game Loop" (boucle de jeu) gère le flux temporel. Elle doit impérativement utiliser un pas de temps fixe (Fixed Timestep ou deltaTime), permettant de découpler la vitesse de la simulation biologique des capacités de rafraîchissement de l'ordinateur exécutant le programme.13 Sans deltaTime, une chute de FPS ralentirait artificiellement la reproduction des monstres et fausserait les équations de Lotka-Volterra.

Chaque agent autonome (plante, proie, prédateur) est instancié selon le patron *Factory Method* 61 et intègre une Machine à États Finis (FSM - Finite State Machine).13 La FSM de l'agent l'oblige à adopter un état exclusif à la fois :

1. **Errance (WANDER) :** Mouvement pseudo-aléatoire fluide (souvent calculé par le bruit de Perlin ou des mécanismes de steering) pour explorer la carte.  
2. **Traque (PURSUE) :** Guidé par le gradient de la Scent Map vers une source de nourriture.42  
3. **Fuite (FLEE) :** Guidé par le vecteur opposé à la menace perçue ou à l'odeur répulsive d'un prédateur territorial.43  
4. **Reproduction (REPRODUCE) :** Immobilisation temporaire permettant le déclenchement de l'algorithme génétique (croisement, mutation) dès lors que les jauges de biomasse et d'énergie atteignent le seuil d'investissement requis (selon qu'il s'agisse d'une stratégie r ou K).13

L'utilisation de la programmation événementielle (Event-Driven Programming / Observer Pattern) permet aux systèmes de communiquer sans être fortement couplés.61 Par exemple, si une anomalie statistique (un taux de croissance exceptionnel) est détectée dans la routine de fitness d'un individu lors du passage à la génération suivante, l'agent émet un événement "Boss_Emerged". Le gestionnaire global capte cet événement et peut déclencher une notification visuelle, transformant le statut du monstre en Rang S et changeant son sprite.

## **Prompt pour Agent IA : Implémentation du Prototype**

L'objectif pratique de cette recherche est de fournir les spécifications complètes pour guider un agent d'intelligence artificielle (Copilot Agent en mode Plan via VSCode) dans la création du prototype visuel en Python/Pygame. Le prompt ci-dessous rassemble la synthèse de toutes les théories biologiques et directives architecturales exposées dans ce rapport. Il est conçu pour être directement exécutable.

### ---

**Prompt d'Architecture Écosystémique pour Copilot Agent (Mode Plan)**

**Contexte et Objectif :**

Je souhaite développer un prototype expérimental interactif en Python en utilisant la bibliothèque pygame. Il s'agit d'une simulation écologique et systémique complexe en vue de dessus (2D top-down), qui servira de moteur de fondation pour un futur jeu de gestion de guilde (Isekai Fantasy). L'objectif est de générer un écosystème autonome doté de comportements émergents, où des créatures naissent, chassent, s'organisent socialement, évoluent génétiquement, et où de puissantes anomalies biologiques (des Bosses de Rang S) peuvent apparaître organiquement sans scripts prédéfinis.

**Rôle de l'IA :**

Tu vas agir en tant qu'Architecte Logiciel Senior. Rédige d'abord le plan détaillé des modules et des classes. Après mon approbation de ce plan, tu implémenteras itérativement le code. L'architecture doit être modulaire, hautement orientée objet (OOP) et respecter la séparation des préoccupations (principe SOLID). Utilise systématiquement un deltaTime fixe pour que la simulation mathématique soit indépendante du framerate.

**Cahier des Charges Algorithmiques et Biologiques :**

1. **Optimisation Spatiale (Quadtree) :**  
   * Implémente obligatoirement une classe Quadtree. À chaque *frame*, la structure doit être effacée et reconstruite. Tous les agents s'y enregistrent pour effectuer des recherches spatiales en $O(N \log N)$ (rayon de perception, collisions, distance des cibles). L'absence de Quadtree ruinera les performances de la simulation.  
2. **Navigation Émergente (Cartes Olfactives / Flow Fields) :**  
   * Implémente une grille sous-jacente représentant des champs vectoriels ou des cartes olfactives (Scent Maps).  
   * Les entités déposent des valeurs numériques (phéromones) sur la grille lors de leurs déplacements.  
   * À chaque tick, cette grille applique un calcul matriciel de dégradation (Decay) et de diffusion collaborative (répartition proportionnelle vers les cellules voisines).  
   * Les agents utiliseront la descente ou la montée de gradient de cette grille pour accomplir des tâches complexes (fuir des prédateurs, traquer des proies hors champ visuel, contourner les obstacles infranchissables de manière organique).  
3. **Le Modèle Centré sur l'Individu (ABM) et les Niveaux Trophiques :**  
   * **Producteurs :** Ressources passives générées par une croissance logistique respectant une capacité de charge maximale du terrain.  
   * **Proies (Stratégie r) :** Herbivores faibles, reproduction très rapide, maturation courte. Soumis aux équations de Lotka-Volterra. Comportement régi par une Machine à États (Errance, Fuite, Reproduction, Nourrissage).  
   * **Prédateurs (Stratégie K) :** Carnivores nécessitant l'absorption de proies pour restaurer leur jauge de faim. Reproduction lente.  
   * **Dynamique de Meute et Lignées :** Implémente un identifiant familial (kin_id). Les prédateurs de la même lignée forment des meutes menées par un individu Alpha (le plus haut fitness). Si l'Alpha meurt de faim ou d'un conflit territorial, la meute peut se disloquer en entités solitaires.  
4. **Évolution Sélective et Algorithme Génétique :**  
   * Chaque monstre possède un dictionnaire d'allèles (Génome) modulant : sa vitesse maximale, son champ de vision, sa puissance d'attaque, son efficacité d'absorption calorique et son seuil de reproduction.  
   * Lors de la phase de REPRODUCE, le système croise les gènes des parents, mais applique une fonction de **Mutation** (ajout/soustraction aléatoire à la valeur du gène).  
   * **Effondrement Mutationnel et Création de Bosses :** Modélise la robustesse dérivationnelle et la Règle Insulaire. Si la population locale est très faible, les amplitudes de mutation augmentent. Si un agent accumule un nombre anormal de victoires ou si ses traits mutés dépassent un certain seuil de l'écart-type, il brise la symétrie. Le système le catégorise immédiatement comme "Anomalie de Rang S". Sa couleur change, il devient un prédateur territorial exclusif, créant une "zone d'influence" de forte répulsion olfactive autour de lui.  
5. **Interface, Visualisation et Débogage (Pygame) :**  
   * Le rendu sera purement symbolique : les entités sont représentées par des cercles de taille et de couleurs variables, la végétation par des carrés verts. Les anomalies/Bosses doivent être particulièrement distinctes (taille imposante, couleur noire ou pulsante).  
   * Intègre une interface Textuelle (HUD) en surimpression (FPS, Population Totale, Nombre d'Herbivores, Nombre de Carnivores, Liste des Bosses actifs).  
   * Ajoute des raccourcis clavier (Tab, S, Q) pour activer/désactiver des calques de débogage visuel : affichage des lignes de découpage du Quadtree, et affichage en carte thermique (Heatmap) des valeurs de la Scent Map.

**Méthodologie de travail :**

Génère d'abord l'arborescence des fichiers (ex: main.py, settings.py, quadtree.py, scent_map.py, entities.py, genetics.py). Demande-moi la permission de continuer, puis nous attaquerons les fichiers un par un pour garantir la propreté du code.

## ---

**Conclusion et Perspectives**

La création d'un écosystème fonctionnel pour un jeu vidéo outrepasse la simple programmation géométrique pour embrasser la complexité de l'écologie théorique. En substituant aux scripts arbitraires les équations de dynamique des populations, la théorie de la sélection r/K, les modélisations de dynamique de meute, et les algorithmes de génétique stochastique, le système acquiert une profondeur infinie. L'ingénierie logicielle s'aligne avec la modélisation biologique grâce à l'utilisation structurale des Quadtrees et des champs de diffusion collaborative, qui résolvent les impasses computationnelles de l'intelligence artificielle classique. L'univers généré n'est plus un décor statique attendant le joueur, mais un réseau trophique résilient, où les cascades écologiques provoquées par la guilde exigent une gouvernance stratégique constante. Le prototype issu du cahier des charges proposé validera expérimentalement ces synergies systémiques, ouvrant la voie à une expérience ludique où les actions du joueur façonnent l'évolution et le destin biologique de mondes virtuels complets.

#### **Sources des citations**

1. When Game Worlds Stop Following a Script | by FunVoke - Medium, consulté le mai 7, 2026, [https://medium.com/@funvoke/when-game-worlds-stop-following-a-script-63079cdbeb43](https://medium.com/@funvoke/when-game-worlds-stop-following-a-script-63079cdbeb43)  
2. The Most 'Alive' Game Ecosystems - YouTube, consulté le mai 7, 2026, [https://www.youtube.com/watch?v=NB0XmexIa5s](https://www.youtube.com/watch?v=NB0XmexIa5s)  
3. The Most Complex Ecosystems in Games - YouTube, consulté le mai 7, 2026, [https://www.youtube.com/watch?v=TbROFiFhUh0](https://www.youtube.com/watch?v=TbROFiFhUh0)  
4. Games with observable ecosystems and/or advanced animal behavior? - Reddit, consulté le mai 7, 2026, [https://www.reddit.com/r/gaming/comments/t9ledj/games_with_observable_ecosystems_andor_advanced/](https://www.reddit.com/r/gaming/comments/t9ledj/games_with_observable_ecosystems_andor_advanced/)  
5. Create Emergent Gameplay with Open Worlds - Ideas - GameDev.tv, consulté le mai 7, 2026, [https://community.gamedev.tv/t/create-emergent-gameplay-with-open-worlds/199093](https://community.gamedev.tv/t/create-emergent-gameplay-with-open-worlds/199093)  
6. Trophic cascade - Wikipedia, consulté le mai 7, 2026, [https://en.wikipedia.org/wiki/Trophic_cascade](https://en.wikipedia.org/wiki/Trophic_cascade)  
7. Vision, Mission, Principles - Forest Stewards Guild, consulté le mai 7, 2026, [https://foreststewardsguild.org/vision-mission-principles/](https://foreststewardsguild.org/vision-mission-principles/)  
8. (PDF) From individual behavior and pack dynamics to population ..., consulté le mai 7, 2026, [https://www.researchgate.net/publication/338830326_From_individual_behavior_and_pack_dynamics_to_population_responses_An_individual-based_approach_to_model_the_wolf_social_life_cycle](https://www.researchgate.net/publication/338830326_From_individual_behavior_and_pack_dynamics_to_population_responses_An_individual-based_approach_to_model_the_wolf_social_life_cycle)  
9. Quantitative genetics of body size evolution on islands: an individual-based simulation approach - PMC, consulté le mai 7, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6832192/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6832192/)  
10. Emergent Gameplay (Introductory Guide) - Game Design Skills, consulté le mai 7, 2026, [https://gamedesignskills.com/game-design/emergent-gameplay/](https://gamedesignskills.com/game-design/emergent-gameplay/)  
11. Investigating Genetic Algorithm Optimization Techniques in Video Games - Digital Commons@ETSU, consulté le mai 7, 2026, [https://dc.etsu.edu/cgi/viewcontent.cgi?article=1788&context=honors](https://dc.etsu.edu/cgi/viewcontent.cgi?article=1788&context=honors)  
12. How do animal territories form and change? Lessons from 20 years ..., consulté le mai 7, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4043092/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4043092/)  
13. The Ecosystem Safari Simulator: Technical Manual - Conceptual Agent-Based Model (ABM) - Conservation Mag, consulté le mai 7, 2026, [https://conservationmag.org/games/documents/ecosystem_simulator_technical_manual.pdf](https://conservationmag.org/games/documents/ecosystem_simulator_technical_manual.pdf)  
14. Using AI enhanced agent-based models to support management of wild populations, consulté le mai 7, 2026, [https://www.researchgate.net/publication/393249300_Using_AI_enhanced_agent-based_models_to_support_management_of_wild_populations](https://www.researchgate.net/publication/393249300_Using_AI_enhanced_agent-based_models_to_support_management_of_wild_populations)  
15. Predicting Ecosystem Resilience Using Multi-Agent Reinforcement Learning | bioRxiv, consulté le mai 7, 2026, [https://www.biorxiv.org/content/10.1101/2025.06.07.658424v1.full](https://www.biorxiv.org/content/10.1101/2025.06.07.658424v1.full)  
16. Lotka–Volterra equations - Wikipedia, consulté le mai 7, 2026, [https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations)  
17. The biology of small, introduced populations, with special reference to biological control, consulté le mai 7, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3407862/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3407862/)  
18. Integrating Lotka-Volterra dynamics and gravity modeling for regional population forecasting, consulté le mai 7, 2026, [https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2025.1469890/full](https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2025.1469890/full)  
19. Intraspecific variation stabilizes classic predator-prey dynamics - bioRxiv, consulté le mai 7, 2026, [https://www.biorxiv.org/content/10.1101/2021.09.27.461947v1.full-text](https://www.biorxiv.org/content/10.1101/2021.09.27.461947v1.full-text)  
20. Joining or opting out of a Lotka–Volterra game between predators and prey: does the best strategy depend on modelling energy lost and gained? - PMC, consulté le mai 7, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3915850/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3915850/)  
21. r/K selection theory - Wikipedia, consulté le mai 7, 2026, [https://en.wikipedia.org/wiki/R/K_selection_theory](https://en.wikipedia.org/wiki/R/K_selection_theory)  
22. Genetic Algorithm: Complete Guide With Python Implementation - DataCamp, consulté le mai 7, 2026, [https://www.datacamp.com/tutorial/genetic-algorithm-python](https://www.datacamp.com/tutorial/genetic-algorithm-python)  
23. Genetic Algorithm in action! - DEV Community, consulté le mai 7, 2026, [https://dev.to/kavinbharathi/genetic-algorithm-in-action-3ilj](https://dev.to/kavinbharathi/genetic-algorithm-in-action-3ilj)  
24. Genetic algorithms - What is a genetic algorithm? - Rock the Prototype, consulté le mai 7, 2026, [https://rock-the-prototype.com/en/algorithms/genetic-algorithms/](https://rock-the-prototype.com/en/algorithms/genetic-algorithms/)  
25. Featured Blog | Supporting game design with evolutionary algorithms, consulté le mai 7, 2026, [https://www.gamedeveloper.com/design/supporting-game-design-with-evolutionary-algorithms](https://www.gamedeveloper.com/design/supporting-game-design-with-evolutionary-algorithms)  
26. Monsters of Darwin: a strategic game based on Artificial Intelligence and Genetic Algorithms - CEUR-WS.org, consulté le mai 7, 2026, [https://ceur-ws.org/Vol-1956/GHItaly17_paper_05.pdf](https://ceur-ws.org/Vol-1956/GHItaly17_paper_05.pdf)  
27. Simple Genetic Algorithm From Scratch in Python - MachineLearningMastery.com, consulté le mai 7, 2026, [https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/](https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/)  
28. Simple Genetic Algorithm by a Simple Developer (in Python) | by Maciej S. - Medium, consulté le mai 7, 2026, [https://medium.com/data-science/simple-genetic-algorithm-by-a-simple-developer-in-python-272d58ad3d19](https://medium.com/data-science/simple-genetic-algorithm-by-a-simple-developer-in-python-272d58ad3d19)  
29. Genetic Algorithms in Games (Part 1) - Game Developer, consulté le mai 7, 2026, [https://www.gamedeveloper.com/design/genetic-algorithms-in-games-part-1-](https://www.gamedeveloper.com/design/genetic-algorithms-in-games-part-1-)  
30. Genetics Gameplay / Understanding puzzle design : r/gamedesign - Reddit, consulté le mai 7, 2026, [https://www.reddit.com/r/gamedesign/comments/1ljhar8/genetics_gameplay_understanding_puzzle_design/](https://www.reddit.com/r/gamedesign/comments/1ljhar8/genetics_gameplay_understanding_puzzle_design/)  
31. Mutation load and the survival of small populations - Arizona State University, consulté le mai 7, 2026, [https://asu.elsevierpure.com/en/publications/mutation-load-and-the-survival-of-small-populations/](https://asu.elsevierpure.com/en/publications/mutation-load-and-the-survival-of-small-populations/)  
32. Two sides of the same coin: A population genetics perspective on lethal mutagenesis and mutational meltdown - PMC, consulté le mai 7, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6007402/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6007402/)  
33. Evolution of drift robustness in small populations - PMC - NIH, consulté le mai 7, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC5647343/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5647343/)  
34. How natural systems became biological agents through the generation - YouTube, consulté le mai 7, 2026, [https://www.youtube.com/watch?v=ETS-Gc46Ps4](https://www.youtube.com/watch?v=ETS-Gc46Ps4)  
35. From the origin of life to pandemics: emergent phenomena in complex systems - PMC, consulté le mai 7, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC9125231/](https://pmc.ncbi.nlm.nih.gov/articles/PMC9125231/)  
36. Islands give rise to evolutionary giants and dwarfs - Imperial College London, consulté le mai 7, 2026, [https://www.imperial.ac.uk/news/219453/islands-give-rise-evolutionary-giants-dwarfs/](https://www.imperial.ac.uk/news/219453/islands-give-rise-evolutionary-giants-dwarfs/)  
37. Gigantism & Dwarfism on Islands | NOVA - PBS, consulté le mai 7, 2026, [https://www.pbs.org/wgbh/nova/article/gigantism-and-dwarfism-islands/](https://www.pbs.org/wgbh/nova/article/gigantism-and-dwarfism-islands/)  
38. True story: island gigantism and dwarfism and the island rule | Radboud University, consulté le mai 7, 2026, [https://www.ru.nl/en/services/recharge/overview/true-story-island-gigantism-and-dwarfism-and-the-island-rule](https://www.ru.nl/en/services/recharge/overview/true-story-island-gigantism-and-dwarfism-and-the-island-rule)  
39. Island Gigantism and Dwarfism Explained | The Curious Current - YouTube, consulté le mai 7, 2026, [https://www.youtube.com/watch?v=QgLSbKbun88](https://www.youtube.com/watch?v=QgLSbKbun88)  
40. Pitfalls of creating a massive 2d topdown gameworld : r/gamedesign - Reddit, consulté le mai 7, 2026, [https://www.reddit.com/r/gamedesign/comments/1d6bgxw/pitfalls_of_creating_a_massive_2d_topdown/](https://www.reddit.com/r/gamedesign/comments/1d6bgxw/pitfalls_of_creating_a_massive_2d_topdown/)  
41. Territorial behavior may help animals flatten disease curve - The Wildlife Society, consulté le mai 7, 2026, [https://wildlife.org/territorial-behavior-may-help-animals-flatten-disease-curve/](https://wildlife.org/territorial-behavior-may-help-animals-flatten-disease-curve/)  
42. scent_map : Built with Processing, consulté le mai 7, 2026, [http://robotacid.com/PBeta/scent_map/index.html](http://robotacid.com/PBeta/scent_map/index.html)  
43. Utilizing Collaborative Diffusion (aka Flow Fields) for 2D pathfinding and enemy AI in my game prototype : r/gamedev - Reddit, consulté le mai 7, 2026, [https://www.reddit.com/r/gamedev/comments/z98wvh/utilizing_collaborative_diffusion_aka_flow_fields/](https://www.reddit.com/r/gamedev/comments/z98wvh/utilizing_collaborative_diffusion_aka_flow_fields/)  
44. Navigation Patterns and Scent Marking: Underappreciated Contributors to Hippocampal and Entorhinal Spatial Representations? - PMC, consulté le mai 7, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC5996749/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5996749/)  
45. Eco, consulté le mai 7, 2026, [https://play.eco/](https://play.eco/)  
46. Health factors that influence sustainable behaviour in a single-player resource management game - PMC, consulté le mai 7, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11061002/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11061002/)  
47. Activity II: Introduction or Review of Food Webs and Trophic Levels - Modeling Marine Ecosystems with Virtual Reality: NOAA's National Ocean Service, consulté le mai 7, 2026, [https://oceanservice.noaa.gov/education/marine-ecosystem-modeling-vr/ocean-food-webs/activity-2.html](https://oceanservice.noaa.gov/education/marine-ecosystem-modeling-vr/ocean-food-webs/activity-2.html)  
48. OpenStax Biology 2e, Ecology, Ecosystems, Energy Flow through Ecosystems | OhioLINK, consulté le mai 7, 2026, [https://ohiolink.oercommons.org/courseware/lesson/1719/overview](https://ohiolink.oercommons.org/courseware/lesson/1719/overview)  
49. Trophic Levels Relay Race | NYC.gov, consulté le mai 7, 2026, [https://www.nyc.gov/assets/dep/downloads/pdf/environment/education/trophic-levels-relay-race.pdf](https://www.nyc.gov/assets/dep/downloads/pdf/environment/education/trophic-levels-relay-race.pdf)  
50. 5 Creative Ways to Teach Trophic Levels - Labster, consulté le mai 7, 2026, [https://www.labster.com/blog/5-creative-ways-teach-trophic-levels](https://www.labster.com/blog/5-creative-ways-teach-trophic-levels)  
51. Trophic Levels Activities & Games - Study.com, consulté le mai 7, 2026, [https://study.com/academy/lesson/trophic-levels-activities-games.html](https://study.com/academy/lesson/trophic-levels-activities-games.html)  
52. Haunted ecosystems: Losing top predators - Science in the Classroom, consulté le mai 7, 2026, [https://www.scienceintheclassroom.org/research-papers/haunted-ecosystems-losing-top-predators](https://www.scienceintheclassroom.org/research-papers/haunted-ecosystems-losing-top-predators)  
53. Trophic cascade | Definition, Importance, & Examples - Britannica, consulté le mai 7, 2026, [https://www.britannica.com/science/trophic-cascade](https://www.britannica.com/science/trophic-cascade)  
54. What happens to ecosystems when you restore iconic top predators? It's more complicated than you might think. - UC Santa Cruz - News, consulté le mai 7, 2026, [https://news.ucsc.edu/2025/11/what-happens-to-ecosystems-when-you-restore-iconic-top-predators-its-more-complicated-than-you-might-think/](https://news.ucsc.edu/2025/11/what-happens-to-ecosystems-when-you-restore-iconic-top-predators-its-more-complicated-than-you-might-think/)  
55. What Happens to an Ecosystem When Its Top Predator Is Removed? | Scuba Diving, consulté le mai 7, 2026, [https://www.scubadiving.com/what-happens-ecosystem-when-its-top-predator-removed](https://www.scubadiving.com/what-happens-ecosystem-when-its-top-predator-removed)  
56. Conservation Mag's Ecosystem Simulator Game, consulté le mai 7, 2026, [https://conservationmag.org/en/kids-activities/conservation-mag-ecosystem-simulator-game](https://conservationmag.org/en/kids-activities/conservation-mag-ecosystem-simulator-game)  
57. Does this already exist? Collaborative game where players are native plants fending off invasive species. : r/tabletopgamedesign - Reddit, consulté le mai 7, 2026, [https://www.reddit.com/r/tabletopgamedesign/comments/16k0p30/does_this_already_exist_collaborative_game_where/](https://www.reddit.com/r/tabletopgamedesign/comments/16k0p30/does_this_already_exist_collaborative_game_where/)  
58. Using a Game to Teach Invasive Species Spread and Management - NSTA, consulté le mai 7, 2026, [https://www.nsta.org/journal-college-science-teaching/journal-college-science-teaching-januaryfebruary-2023/using-game](https://www.nsta.org/journal-college-science-teaching/journal-college-science-teaching-januaryfebruary-2023/using-game)  
59. Space Invaders 2.0? Games with Alien Species • Featured Stories - Freie Universität Berlin, consulté le mai 7, 2026, [https://www.fu-berlin.de/en/featured-stories/research/2023/invasive-species/index.html](https://www.fu-berlin.de/en/featured-stories/research/2023/invasive-species/index.html)  
60. Coevolution between native and invasive plant competitors: implications for invasive species management - PMC, consulté le mai 7, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3352482/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3352482/)  
61. Design Patterns That Shaped the World of Games: History and Practical Application, consulté le mai 7, 2026, [https://kokkugames.com/design-patterns-that-shaped-the-world-of-games-history-and-practical-application/](https://kokkugames.com/design-patterns-that-shaped-the-world-of-games-history-and-practical-application/)  
62. Level up your code with game programming patterns - Unity, consulté le mai 7, 2026, [https://unity.com/blog/games/level-up-your-code-with-game-programming-patterns](https://unity.com/blog/games/level-up-your-code-with-game-programming-patterns)  
63. what are some game design patterns that you wish you knew earlier? : r/gamedev - Reddit, consulté le mai 7, 2026, [https://www.reddit.com/r/gamedev/comments/10qtoe4/what_are_some_game_design_patterns_that_you_wish/](https://www.reddit.com/r/gamedev/comments/10qtoe4/what_are_some_game_design_patterns_that_you_wish/)  
64. Some ideas and small issues for 2D top-down RPG games - Unity Discussions, consulté le mai 7, 2026, [https://discussions.unity.com/t/some-ideas-and-small-issues-for-2d-top-down-rpg-games/938406](https://discussions.unity.com/t/some-ideas-and-small-issues-for-2d-top-down-rpg-games/938406)  
65. Spatial-Partitioning-Quadtree - GitHub Pages, consulté le mai 7, 2026, [https://carlosupc.github.io/Spatial-Partitioning-Quadtree/](https://carlosupc.github.io/Spatial-Partitioning-Quadtree/)  
66. The magic of quad trees (spatial partitioning) - Zach Thompson, consulté le mai 7, 2026, [https://www.zachmakesgames.com/node/22](https://www.zachmakesgames.com/node/22)  
67. Spatial Partition - Game Programming Patterns, consulté le mai 7, 2026, [https://gameprogrammingpatterns.com/spatial-partition.html](https://gameprogrammingpatterns.com/spatial-partition.html)  
68. An introduction to spatial partitioning (grids, quadtrees, and the like) - Reddit, consulté le mai 7, 2026, [https://www.reddit.com/r/programming/comments/1htfki/an_introduction_to_spatial_partitioning_grids/](https://www.reddit.com/r/programming/comments/1htfki/an_introduction_to_spatial_partitioning_grids/)  
69. Quadtree Space Partitioning with Python - YouTube, consulté le mai 7, 2026, [https://www.youtube.com/watch?v=J8CS2qi7jOA](https://www.youtube.com/watch?v=J8CS2qi7jOA)
