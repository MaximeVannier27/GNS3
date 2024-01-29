# GNS3

## Fonctionalités de notre programme
Le programme permet de créer des fichiers de configuration pour tous les routeurs des AS décrits dans un intent file au format JSON avec les fonctionalités suivantes : 
- Allocation automatisée des sous-réseaux et adresses IP sur chaque lien interne à une AS, ainsi que des adresses IP de loopback
- Paramétrage du coût OSPF d'un lien
- Tagging de communautés BGP et mise en place de route-map correspondants 
- Drag-and-Drop bot

## Détail sur les politiques BGP et les communautés
Les routes reçues d'un AS différent sont taguées par le routeur de bordure qui les reçoit selon le format standard suivant, numéro d'AS qui tague la communauté : numéro de communauté.
Les numéros de communautés ont pour tous les AS les correponsdances suivantes :
- AS:100 : cette route provient d'un provider
- AS:200 : cette route provient d'un client
- AS:300 : cette route provient d'un peer

Les routeurs de bordure appliquent à ces routes des règles afin de les retransmettre ou pas aux autres AS.
Les règles prédéfinies dans notre programme sont les suivantes : 

- frommyprovider : tague la communauté provider à la route entrante et met la localpref à 
- frommypeer : tague la communauté peer et met la localpref à
- frommyclient : tague la communauté client et met la localpref à 

- tomyprovider : empêche la transmission des routes taguées peer et provider
- tomypeer : empêche la transmission des routes taguées peer et provider

## Structure du JSON
Le premier niveau de clé du JSON correspond au numéro d'AS
pour chaque AS on a les clés associées aux valeurs suivantes  :

- IGP : associé à une chaîne de caractère correspondant au protocole interne à l'AS (OSPF ou RIP)
- relationships : contient un dictionnaire dont les clés sont les AS voisins et les valeurs une chaîne de caractère définissant leur position par rapport à l'AS parcouru (client, provider ou peer)
- ip_range : contient une liste de deux adresses IP définssant la plage d'adresses de l'AS
- loopback_range : similaire au paramètre précédent mais pour les adresses de loopback
- routers : dictionnaire dont les clés sont les numéros (stocké en chaine de caractère) des routers de l'AS et les valeurs des informations sur leurs interfaces

#### Détails du dictionnaire routers
Les clés du dictionnaire routers sont : 
- i_interface : un dictionnaire dont les clés sont les interfaces du routeur connectées à un routeur du même AS
La valeur associée est le nom du routeur auquelle l'interface est connectée.
Si l'AS utilise OSPF, cette valeur est une liste dont le deuxième élément est le coût du lien (0 si le coût par défaut doit être utilisé, le coût souhaité sinon)
- e_interface : similaire au précédent, ce dictionnaire a pour clés les interfaces du routeur connectées à un routeur d'un AS différent. La valeur associée est une liste dont le premier élément est le routeur voisin, le deuxième l'adresse qui doit être paramétrée sur l'interface et éventuellement en troisième une valeur par défaut à 0 afin de faciliter le traitement des coûts OSPF si nécessaire.
Les interfaces connectées entre deux AS ont une adresse IP prédéfinie car on estime que les coordinateurs des AS se sont mis d'accord entre eux pour mettre en place leurs sous-réseaux communs.
