from fonctions import *
from init_classes import *


fin_config = ["!", "!", "!", "control-plane", "!", "!", "line con 0", " exec-timeout 0 0", " privilege level 15", " logging synchronous", " stopbits 1", "line aux 0", " exec-timeout 0 0", " privilege level 15", " logging synchronous", " stopbits 1", "line vty 0 4", " login", "!", "!", "end"]


jason = str(input("Quel fichier intent (.json) utilisé: "))
dico_json = load_intent(jason)
liste_AS = init_as(dico_json)
init_routeur_adresses(dico_json)

for AS_courant in liste_AS:
    for routeur_courant in AS_courant.routers:
        
        initConfigList(routeur_courant)
        routeur_courant.configList += initInterface(routeur_courant,AS_courant)
        routeur_courant.configList += initBGP(routeur_courant,AS_courant)
        routeur_courant.configList += initAddressFamily(routeur_courant,AS_courant)
        routeur_courant.configList += initProtocole(routeur_courant,AS_courant)
        if routeur_courant.border:
            routeur_courant.configList+= route_map_rules(routeur_courant,AS_courant)
        routeur_courant.configList += fin_config
        creationConfigFinal(routeur_courant)
        print(f"Routeur {routeur_courant.numero} : AS [{routeur_courant.AS_n}]")
        print("--> ADDRESSES IP <--")
        print(f"Interface Loopback: {routeur_courant.loopback} ")
        for i,c in routeur_courant.interfaces.items():
            print(f"Interface {i}: {c[0]}")
        print("-------------------------------------------")
print("Fin de création des fichiers .cfg.")
print("Déplacement des fichiers...")
drag_and_drop()
print("------------------FIN------------------")

