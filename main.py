from datetime import datetime


config_defaut = ["!", f"! Last configuration change at {datetime.now()}", "!", "version 15.2", "service timestamps debug datetime msec", "service timestamps log datetime msec", "!", "hostname ", "!", "boot-start-marker", "boot-end-marker", "!", "!", "!", "no aaa new-model", "no ip icmp rate-limit unreachable", "ip cef", "!", "!", "!", "!", "!", "!", "no ip domain lookup", "ipv6 unicast-routing", "ipv6 cef", "!", "!", "multilink bundle-name authenticated", "!", "!", "!", "!", "!", "!", "!", "!", "!", "ip tcp synwait-time 5", "!", "!", "!", "!", "!", "!", "!", "!", "!"]


def initConfigList(routerName):
    routerName.configList = config_defaut


def creationConfigFinal(routerName,configList):
    with open(f".configs/i{routerName.numero}_startup-config.cfg","w") as fichier:
        fichier.writelines(configList)

"""
Fonction pour initialiser les premières lignes du fichier config pour
chaque interface, avec la fonction de l'adressage IP qui, je suppose
modifie directement la classe routeurs à l'initialisation (self.interfaces)
On va traiter une liste par interface comme ça on rajoute directement les différentes
lignes (en fonction du protocole) et on concatène à la fin
"""
def initInterface(routeurName,interface):
    lignes_interface = []
    lignes_interface.append("interface",interface)
    lignes_interface.append(" no ip address")
    if "Loopback" not in interface:
        lignes_interface.append(" negotiation auto")
    lignes_interface.append(" ipv6 address",routeurName.interfaces[interface][0]) #routeurName.interfaces[interface][0] --> @ ip de l'interface précisée dans la classe du routeur concerné
    lignes_interface.append(" ipv6 enable")

    return lignes_interface
    
"""
Fonction pour écrire dans la liste config de l'interface les/la ligne(s) liés au protocole (elle écrit sur la liste/pas de return)
J'ai testé et c'est pas comme en C, la liste est bien modifiée
"""
def protInterface(routeurName,interface,lignes_interface):
    if routeurName.AS_n.igp == "rip" and routeurName.interface[interface][2]==routeurName.AS_n.num:  #test si protocole rip ET interface interne à l'AS (le test est un peu étrange je suis d'accord mais je voulais utiliser les classes et pas le json -->c'est plus clair dans le json vu qu'sépare interface interne et externe)
        lignes_interface.append(" ipv6 rip prot_RIP enable")
    elif routeurName.AS_n.igp == "ospf":
        lignes_interface.append(" ipv6 ospf 1 area 0")


        #on peut essayer de créer directement des bouts de listes avec les réglages des protocoles
        #qu'on ajoutera après à tout (autant utiliser les tests qui sont fait ici)
        #sûrement problématique pour BGP car pas lié à une interface (appeler une autre fonction ?)
        #PAS OUBLIER LES PASSIVES INTERFACES (GE2/0 sur R3 car ospf)





#autres fonctions pour écrire les lignes après la déclaration des interfaces
    # concaténer les listes interface dans la config_list du routeur




liste_AS = initAS("json")

for AS in liste_AS:
    if AS.igp == "rip":
        for R in AS.routers:
            initConfigList(R)
            R.configList.append()
