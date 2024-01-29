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
    Cette fonction permet d'initialiser des objets de classes AS et Router du fichier classes.py à partir
    des informations contenues dans l'intent file. Ces classes permettent par exemple de pouvoir facilement réaccéder 
    aux caractéristiques et paramètres d'un router à partir de son numéro.
    Elle retourne une liste d'objets de type AS correspondant aux AS du intent file.
    """

    liste_as = [] # liste qui va être retournée contenant les AS

    #Cette première boucle permet d'initialiser chaque routeur avec son numéro et l'AS auxquels ils appartiennent
    for (as_n,value) in dico_as.items():

        num_as = f"as_{as_n}"                   #nom de la variable de type AS créée
        globals()[num_as] = AS(as_n)
        globals()[num_as].igp = value["IGP"]
        globals()[num_as].ip += value["ip_range"]
        globals()[num_as].loopback += value["loopback_range"]
        for as_voisin,relation in value["relationships"].items():
            globals()[num_as].rel[as_voisin]=relation   
        liste_as.append(globals()[num_as])      #ajout de l'AS à la liste des AS créés

        for (router_n,attributs) in value["routers"].items():
            Ri = f"R{router_n}" #nom de la variable de type router créée
            globals()[Ri] = Router(as_n)
            globals()[Ri].numero = router_n
            (globals()[num_as].routers).append(globals()[Ri])
          
            
    return liste_as


def init_routeur_adresses(dico_as):
    """
    Cette fonction permet d'attribuer un sous-réseau de sa plage IP à chaque lien interne à un AS,
    et donc d'attribuer les adresses correspondantes à ses routeurs.
    Elle s'occupe aussi de paramétrer le coût du lien s'il est en OSPF.
    Pour les routeurs liens entre deux AS, elle prend en compte des adresses données dans le intent file.
    """

    for as_n,value in dico_as.items():
        compteur_loopback = 1
        compteur_ip = 0

        num_as = f"as_{as_n}"                   #nom de la variable de type AS créée
        as_courant=globals()[num_as]

        for router_n,connexions in value["routers"].items(): 
            Ri = f"R{router_n}"
            routeur_courant = globals()[Ri]
            loopback_temp = loopback(ipaddress.IPv6Address(as_courant.loopback[0]),compteur_loopback)

            if loopback_temp > ipaddress.IPv6Address(as_courant.loopback[1]):
                print("Erreur, plage d'adresses loopback débordée")
                return -1
            
            routeur_courant.loopback = loopback_temp
            compteur_loopback+=1
            
            if connexions["e_interfaces"] !=None:
                routeur_courant.border = True

            for interface,valeur in connexions["e_interfaces"].items():
                voisin=valeur[0]
                ip=valeur[1]
                routeur_courant.interfaces[interface]=[ip,globals()[voisin]]


            for interface,valeur in connexions["i_interfaces"].items():
                if as_courant.igp == "OSPF":
                    voisin,cost = valeur    #dans ce cas valeur est une liste
                else:
                    voisin = valeur         #si on est en rip valeur est un string

                routeur_voisin = globals()[voisin]

                #On commence par vérifier que le lien n'a pas déjà été configuré
                if (routeur_voisin,routeur_courant) not in as_courant.lienslocaux.keys():
                    subnet = ipaddress.IPv6Address(as_courant.ip[0])
                    subnet+=compteur_ip*(2**64)

                    if subnet > ipaddress.IPv6Address(as_courant.ip[1]):
                        print("Erreur, plage d'adresses ip débordée")
                        return -1
                    
                    as_courant.lienslocaux[(routeur_courant,routeur_voisin)] = subnet
                    ip_1= ip_def(subnet,1)
                    ip_2= ip_def(subnet,2)

                    #On paramètre le coût OSPF si nécessaire
                    if as_courant.igp == "OSPF":
                        routeur_courant.interfaces[interface]=[ip_1,routeur_voisin,cost]
                        routeur_voisin.interfaces[interface]=[ip_2,routeur_courant,cost]
                    else:
                        routeur_courant.interfaces[interface]=[ip_1,routeur_voisin]
                        routeur_voisin.interfaces[interface]=[ip_2,routeur_courant]

                    compteur_ip+=1

            #print(f"Paramétrage du routeur R{routeur_courant.numero} :\n{routeur_courant.interfaces}\nLoopback:{routeur_courant.loopback}")        



def loopback(range_ip,compteur):
    ip = range_ip + compteur
    return ip

def ip_def(subnet,n):
    ip = subnet + n
    return ip

# #lignes de test des fonctions
# dico_json = load_intent("intent_old.json")
# liste_AS = init_as(dico_json)
# init_routeur_adresses(dico_json)
