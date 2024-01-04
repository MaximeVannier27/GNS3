from fonctions import *


fin_config = ["!", "!", "!", "control-plane", "!", "!", "line con 0", " exec-timeout 0 0", " privilege level 15", " logging synchronous", " stopbits 1", "line aux 0", " exec-timeout 0 0", " privilege level 15", " logging synchronous", " stopbits 1", "line vty 0 4", " login", "!", "!", "end"]


liste_AS = init_as("json")

for AS_courant in liste_AS:
    for routeur_courant in AS_courant.routers:

        print(f"Début routeur {routeur_courant.numero} de l'AS {routeur_courant.AS_n}")

        initConfigList(routeur_courant)
        routeur_courant.config_list += initInterface(routeur_courant,AS_courant)
        routeur_courant.config_list += initBGP(routeur_courant,AS_courant)
        routeur_courant.config_list += initAddressFamily(routeur_courant,AS_courant)
        routeur_courant.config_list += initProtocole(routeur_courant,AS_courant)
        routeur_courant.config_list += fin_config
        creationConfigFinal(routeur_courant)
        print(f"Fin routeur {routeur_courant.numero} de l'AS {routeur_courant.AS_n}")


