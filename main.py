from fonctions import *
from init_classes import *

# dictionnaire contenant les dossiers pour le projet BGP final
#correspondances = {"R3": "1e881116-929d-4076-9780-6bdc963d0202", "R1": "5f039341-2c15-47a3-9406-d2cc3b8c06e7", "R6": "6eac6bd0-eca0-4c0b-b4ba-7b47441b61fc", "R2": "023ac9b2-d321-4e15-b855-ffc6e39ca9c4", "R4": "28ce5862-c795-4f76-9fd6-c401fc91104f", "R10": "22120b25-686c-44d9-afbc-fcb8836c0591","R7":"7170521f-325e-447a-9aff-a5cac4082f6c","R9":"a0eb7a18-3bde-4b3a-85b5-202239a84bdf","R5":"b85e4e0b-9dec-4831-a14c-7f4459d3b70f","R12":"c58c629b-8a33-4026-851d-36bd822bf5e1","R8":"dffdb23d-d79d-48cb-807d-ad2d2e11de5a","R11":"ed2fbd8a-899e-444e-8242-97ec0d2fe4bd"}

fin_config = ["!", "!", "!", "control-plane", "!", "!", "line con 0", " exec-timeout 0 0", " privilege level 15", " logging synchronous", " stopbits 1", "line aux 0", " exec-timeout 0 0", " privilege level 15", " logging synchronous", " stopbits 1", "line vty 0 4", " login", "!", "!", "end"]

dico_json = load_intent("intent_16-routeurs_4-AS.json")
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
        #drag_and_drop("projet_GNS3",correspondances,routeur_courant.numero)
        print(f"Routeur {routeur_courant.numero} : AS [{routeur_courant.AS_n}]")
        print("--> ADDRESSES IP <--")
        print(f"Interface Loopback: {routeur_courant.loopback} ")
        for i,c in routeur_courant.interfaces.items():
            print(f"Interface {i}: {c[0]}")
        print("-------------------------------------------")


