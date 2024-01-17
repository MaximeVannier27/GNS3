from fonctions import *
from init_classes import *

# dictionnaire qui stocke les correspondances entre les noms de dossier et les routeurs
correspondances = {"R1": "dossier1", "R2": "dossier2", "R3": "dossier3", "R4": "dossier4", "R5": "dossier5", "R6": "dossier6"}

fin_config = ["!", "!", "!", "control-plane", "!", "!", "line con 0", " exec-timeout 0 0", " privilege level 15", " logging synchronous", " stopbits 1", "line aux 0", " exec-timeout 0 0", " privilege level 15", " logging synchronous", " stopbits 1", "line vty 0 4", " login", "!", "!", "end"]

dico_json = load_intent("intent.json")
liste_AS = init_as(dico_json)
init_routeur_adresses(dico_json)

for AS_courant in liste_AS:
    for routeur_courant in AS_courant.routers:

        print(f"Début routeur {routeur_courant.numero} de l'AS {routeur_courant.AS_n}")

        initConfigList(routeur_courant)
        routeur_courant.configList += initInterface(routeur_courant,AS_courant)
        routeur_courant.configList += initBGP(routeur_courant,AS_courant)
        routeur_courant.configList += initAddressFamily(routeur_courant,AS_courant)
        routeur_courant.configList += initProtocole(routeur_courant,AS_courant)
        routeur_courant.configList += fin_config
        creationConfigFinal(routeur_courant)
        #drag_and_drop("projet_GNS3",correspondances,routeur_courant.numero)
        print(f"Fin routeur {routeur_courant.numero} de l'AS {routeur_courant.AS_n}")


