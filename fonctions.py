from datetime import datetime
from init_classes import init_as


def initConfigList(routerName):
    routerName.configList = ["!","","!",f"! Last configuration change at {datetime.now()}", "!", "version 15.2", "service timestamps debug datetime msec", "service timestamps log datetime msec", "!", f"hostname R{routerName.numero} ", "!", "boot-start-marker", "boot-end-marker", "!", "!", "!", "no aaa new-model", "no ip icmp rate-limit unreachable", "ip cef", "!", "!", "!", "!", "!", "!", "no ip domain lookup", "ipv6 unicast-routing", "ipv6 cef", "!", "!", "multilink bundle-name authenticated", "!", "!", "!", "!", "!", "!", "!", "!", "!", "ip tcp synwait-time 5", "!", "!", "!", "!", "!", "!", "!", "!", "!", "!", "!", "!"]


def creationConfigFinal(routerName):
    with open(f"i{routerName.numero}_startup-config.cfg","w") as fichier:
        for ligne in routerName.configList:
            fichier.write(ligne + '\n')




def initInterface(routeurName,asName):
    """
    Fonction pour initialiser les premières lignes du fichier config pour
    chaque interface, avec la fonction de l'adressage IP
    On retourne la liste de toutes les interfaces rédigées

    routerName est le router dont on traite les interfaces (classe routeur)
    asName est l'AS auquel il appartient (objet de classe AS)
    """
    
    lignes_interface = []           #initialisation du texte à ajouter à la config

    lignes_interface.append("interface Loopback0")
    lignes_interface.append(" no ip address")
    lignes_interface.append(f" ipv6 address {routeurName.loopback}/128")
    lignes_interface.append(" ipv6 enable")
    if asName.igp == "RIP":
        lignes_interface.append(" ipv6 rip prot_RIP enable")
    elif asName.igp == "OSPF":
        lignes_interface.append(" ipv6 ospf 1 area 0")
    lignes_interface.append("!")

    for interface,(ip,voisin) in routeurName.interfaces.items():
        lignes_interface.append(f"interface {interface}")  
        lignes_interface.append(" no ip address")
        lignes_interface.append(" negotiation auto")

        lignes_interface.append(f" ipv6 address {ip}/64") 
        lignes_interface.append(" ipv6 enable")
        if asName.igp == "RIP" and voisin.AS_n==asName.num:  #test si protocole rip ET interface interne à l'AS (le test est un peu étrange je suis d'accord mais je voulais utiliser les classes et pas le json -->c'est plus clair dans le json vu qu'sépare interface interne et externe)
            lignes_interface.append(" ipv6 rip prot_RIP enable")
        elif asName.igp == "OSPF":
            lignes_interface.append(" ipv6 ospf 1 area 0")
        lignes_interface.append("!")


    return lignes_interface




def initBGP(routeurName,asName):

    lignes_bgp = []
    lignes_bgp.append(f"router bgp {asName.num}")
    lignes_bgp.append(f" bgp router-id {'.'.join(4*str(routeurName.numero))}")
    lignes_bgp.append(" bgp log-neighbor-changes")
    lignes_bgp.append(" no bgp default ipv4-unicast")

    for routeur_AS in asName.routers:
        if routeur_AS != routeurName:
            print(routeur_AS.numero)
            lignes_bgp.append(f" neighbor {routeur_AS.loopback} remote-as {routeur_AS.AS_n}")     #rajouter l'interface loopback au fichier d'intention
            lignes_bgp.append(f" neighbor {routeur_AS.loopback} update-source Loopback0")

    for interface,valeur in routeurName.interfaces.items():
        routeur_voisin = valeur[1]
        #print(routeur_voisin)
        if routeur_voisin.AS_n != routeurName.AS_n:
            temp = None
            for i,c in routeur_voisin.interfaces.items():
                if c[1] == routeurName:
                    temp = c[0]
                    break
            lignes_bgp.append(f" neighbor {temp} remote-as {routeur_voisin.AS_n}")
    lignes_bgp.append(" !")
    return lignes_bgp




def initAddressFamily(routerName,asName):
    lignes_addressfamily = []
    lignes_addressfamily.append(" address-family ipv4")
    lignes_addressfamily.append(" exit-address-family")
    lignes_addressfamily.append(" !")
    
    lignes_addressfamily.append(" address-family ipv6")

    if routerName.border:
        for i in asName.lienslocaux.values(): #faut réussir à se balader parmis tous les liens de l'AS et on append le préfixe du sous-réseau
            lignes_addressfamily.append(f"  network {i}/64")

        for i,(ip,voisin) in routerName.interfaces.items(): #récupérer toutes les interfaces des routeurs d'AS voisines, connectées a routeurName 
            if voisin.AS_n != routerName.AS_n:
                tmp = None
                for j in voisin.interfaces.values():
                    if j[1] == routerName:
                        tmp = j[0]
                        break
                lignes_addressfamily.append(f"  neighbor {tmp} activate") #@ip de l'interface du routeur de l'AS voisine

    for r in asName.routers:
        if r != routerName:         #pas sûre que le test entre deux classes routeurs soit défini
            lignes_addressfamily.append(f"  neighbor {r.loopback} activate") #@ loopback des routeurs de l'AS

    lignes_addressfamily.append(" exit-address-family")
    lignes_addressfamily.append("!")
    
    return lignes_addressfamily



def initProtocole(routeurName,asName):
    lignes_protocole = []
    lignes_protocole.append("ip forward-protocol nd")
    lignes_protocole.append("!")
    lignes_protocole.append("!")
    lignes_protocole.append("no ip http server")
    lignes_protocole.append("no ip http secure-server")
    lignes_protocole.append("!")

    if asName.igp == "RIP":
        lignes_protocole.append("ipv6 router rip prot_RIP")
        lignes_protocole.append(" redistribute connected")
    elif asName.igp == "OSPF":
        lignes_protocole.append("ipv6 router ospf 1")
        lignes_protocole.append(f" router-id {'.'.join(4*str(routeurName.numero))}")
        if routeurName.border:
            for i,c in routeurName.interfaces.items():
                if c[1].AS_n != routeurName.AS_n:
                    lignes_protocole.append(" passive-interface {i}")
    
    return lignes_protocole
    