import json
from classes import Router, AS

def init_as(intent):

    # ouverture de l'intent file
    with open(intent,'r',encoding='utf-8') as fichier:
        dico_as = json.load(fichier)

    liste_as = [] # liste qui va être retournée contenant les AS

    #création des variables de types AS et de type 
    for (as_n,value) in dico_as.items():

        num_as = f"as_{as_n}" #nom de la variable de type AS créée
        globals()[num_as] = AS(as_n)
        globals()[num_as].igp = value["IGP"]
        globals()[num_as].ip = value["ip_range"]
        globals()[num_as].loopback = value["loopback_range"]
        liste_as.append(globals()[num_as]) #ajout de l'AS à la liste des AS créés

        for (router_n,attributs) in value["routers"].items():
            Ri = f"R{router_n}" #nom de la variable de type router créée
            globals()[Ri] = Router(as_n)
            globals()[Ri].numero = router_n
            print(globals()[Ri])
            (globals()[num_as].routers).append(globals()[Ri])
        print(globals()[num_as])

    return liste_as