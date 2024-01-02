from datetime import datetime


config_defaut = ["!", f"! Last configuration change at {datetime.now()}", "!", "version 15.2", "service timestamps debug datetime msec", "service timestamps log datetime msec", "!", "hostname ", "!", "boot-start-marker", "boot-end-marker", "!", "!", "!", "no aaa new-model", "no ip icmp rate-limit unreachable", "ip cef", "!", "!", "!", "!", "!", "!", "no ip domain lookup", "ipv6 unicast-routing", "ipv6 cef", "!", "!", "multilink bundle-name authenticated", "!", "!", "!", "!", "!", "!", "!", "!", "!", "ip tcp synwait-time 5", "!", "!", "!", "!", "!", "!", "!", "!", "!"]


def initConfigList(routerName):
    routerName.configList = config_defaut


def creationConfigFinal(routerName,configList):
    with open(f"./resultats_configs/i{routerName.numero}_startup-config.cfg","w") as fichier:
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
    if routeurName.AS_n.igp == "rip" and routeurName.interface[interface][2]==routeurName.AS_n.num:  #test si protocole rip ET interface interne à l'AS (le test est un peu étrange je suis d'accord mais je voulais utiliser les classes et pas le json -->c'est plus clair dans le json vu qu'sépare interface interne et externe)
        lignes_interface.append(" ipv6 rip prot_RIP enable")
    elif routeurName.AS_n.igp == "ospf":
        lignes_interface.append(" ipv6 ospf 1 area 0")

    return lignes_interface
    

def initBGP(routeurName):

    lignes_bgp = []
    lignes_bgp.append("router bgp",routeurName.AS_n.num)
    lignes_bgp.append(f" bgp router-id {'.'.join(4*str(routeurName.numero))}")
    lignes_bgp.append(" bgp log-neighbor-changes")
    lignes_bgp.append(" no bgp default ipv4-unicast")
    for interface in routeurName.interfaces:
        routeur_voisin = interface[1]
        if routeur_voisin.AS_n.num == routeurName.AS_n.num:
            lignes_bgp.append(f" neighbor {routeur_voisin.loopback} remote-as {routeur_voisin.AS_n.num}")     #rajouter l'interface loopback au fichier d'intention
            lignes_bgp.append(f" neighbor {routeur_voisin.loopback} update-source Loopback0")
        else:
            for i,c in routeur_voisin.interfaces:
                if c[1] == routeurName:
                    tmp = i
                    break
            lignes_bgp.append(f" neighbor {tmp} remote-as {routeur_voisin.AS_n.num}")

    return lignes_bgp
 






        #PAS OUBLIER LES PASSIVES INTERFACES (GE2/0 sur R3 car ospf)





#autres fonctions pour écrire les lignes après la déclaration des interfaces
    # concaténer les listes interface dans la config_list du routeur




liste_AS = initAS("json")

for AS in liste_AS:
    if AS.igp == "rip":
        for R in AS.routers:
            initConfigList(R)
            R.configList.append()
