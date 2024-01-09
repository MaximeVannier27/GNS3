import json
from classes import Router, AS
import ipaddress

def load_intent(intent):
    # ouverture de l'intent file
    with open(intent,'r',encoding='utf-8') as fichier:
        dico_as = json.load(fichier)
    return dico_as

def init_as(dico_as):
    """
    Cette fonction fait beaucoup de choses..euh trop de choses aha
    elle prend toutes les informations du json déjà chargé au préalable (dico_as) pour
    les stocker dans des objets de classe AS et Routeur
    """

    liste_as = [] # liste qui va être retournée contenant les AS

    #Cette première boucle permet d'initialiser chaque routeur avec son numéro et l'AS auxquels ils appartiennent
    for (as_n,value) in dico_as.items():

        num_as = f"as_{as_n}"                   #nom de la variable de type AS créée
        globals()[num_as] = AS(as_n)
        globals()[num_as].igp = value["IGP"]
        globals()[num_as].ip = value["ip_range"]
        globals()[num_as].loopback = ipaddress.IPv6Address(value["loopback_range"])
        liste_as.append(globals()[num_as])      #ajout de l'AS à la liste des AS créés

        for (router_n,attributs) in value["routers"].items():
            Ri = f"R{router_n}" #nom de la variable de type router créée
            globals()[Ri] = Router(as_n)
            globals()[Ri].numero = router_n
            print(globals()[Ri])
            (globals()[num_as].routers).append(globals()[Ri])

    print(globals()[num_as])            
            
    return liste_as


def init_routeur_adresses(dico_as):
    """
    cette fonction permet d'initialiser les adresses des interfaces de tout les routeurs
    pour l'instant c'est du bullshit ça écrit juste un chiffre random incrémenté de 1 à chaque fois
    mais ça sera suffisant pour faire des tests,
    à la rentrée je pose des questions et je m'en occupe
    """

    for as_n,value in dico_as.items():
        compteur_loopback = 1
        compteur_ip = 0

        num_as = f"as_{as_n}"                   #nom de la variable de type AS créée
        as_courant=globals()[num_as]

        for router_n,connexions in value["routers"].items(): 
            Ri = f"R{router_n}"
            routeur_courant = globals()[Ri]
            routeur_courant.loopback = loopback(as_courant.loopback,compteur_loopback)
            compteur_loopback+=1
            
            if connexions["e_interfaces"] !=None:
                routeur_courant.border = True
            for interface,(voisin,ip) in connexions["e_interfaces"].items():
                routeur_courant.interfaces[interface]=[ip,globals()[voisin]]

            for interface,voisin in connexions["i_interfaces"].items():
                routeur_voisin = globals()[voisin]
                if (routeur_voisin,routeur_courant) not in as_courant.lienslocaux.keys():
                    as_courant.lienslocaux[(routeur_courant,routeur_voisin)] = "subnet" + str(compteur_ip)
                    routeur_courant.interfaces[interface]=[ip_def(as_courant.ip,compteur_ip),routeur_voisin]
                    compteur_ip+=1
                    routeur_voisin.interfaces[interface]=[ip_def(as_courant.ip,compteur_ip),routeur_courant]
                    compteur_ip+=1

            print(f"Paramétrage du routeur R{routeur_courant.numero} :\n{routeur_courant.interfaces}\nLoopback:{routeur_courant.loopback}")        

"""
ces deux fonctions sont absolument absurdes pour l'instant mdrrr c'est juste histoire de
"""

def loopback(range_ip,compteur):
    ip = range_ip + compteur
    return ip

def ip_def(range_ip,compteur):
    ip = str(range_ip) + str(compteur)
    return ip

#lignes de test des fonctions
dico_json = load_intent("intent.json")
liste_AS = init_as(dico_json)
init_routeur_adresses(dico_json)
