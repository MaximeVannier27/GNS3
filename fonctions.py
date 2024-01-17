from datetime import datetime
from init_classes import init_as
import os


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

    for interface,valeur in routeurName.interfaces.items():
        ip=valeur[0]
        voisin=valeur[1]
        lignes_interface.append(f"interface {interface}")  
        lignes_interface.append(" no ip address")
        lignes_interface.append(" negotiation auto")

        lignes_interface.append(f" ipv6 address {ip}/64") 
        lignes_interface.append(" ipv6 enable")
        if asName.igp == "RIP" and voisin.AS_n==asName.num:  #test si protocole rip ET interface interne à l'AS (le test est un peu étrange je suis d'accord mais je voulais utiliser les classes et pas le json -->c'est plus clair dans le json vu qu'sépare interface interne et externe)
            lignes_interface.append(" ipv6 rip prot_RIP enable")
        elif asName.igp == "OSPF":
            lignes_interface.append(" ipv6 ospf 1 area 0")
            if voisin.AS_n==asName.num:
                cost = valeur[2]
                if cost:
                    lignes_interface.append(f" ipv6 ospf cost {cost}")
        lignes_interface.append("!")


    return lignes_interface




def initBGP(routeurName,asName):

    lignes_bgp = []
    lignes_bgp.append(f"router bgp {asName.num}")
    lignes_bgp.append(f" bgp router-id {routeurName.numero}.{routeurName.numero}.{routeurName.numero}.{routeurName.numero}")
    lignes_bgp.append(" bgp log-neighbor-changes")
    lignes_bgp.append(" no bgp default ipv4-unicast")

    for routeur_AS in asName.routers:
        if routeur_AS != routeurName:
            #print(routeur_AS.numero)
            lignes_bgp.append(f" neighbor {routeur_AS.loopback} remote-as {routeur_AS.AS_n}")     #rajouter l'interface loopback au fichier d'intention
            lignes_bgp.append(f" neighbor {routeur_AS.loopback} update-source Loopback0")
            lignes_bgp.append(f" neighbor {routeur_AS.loopback} send-community")

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
            lignes_bgp.append(f" neighbor {temp} send-community")

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

        for i,valeur in routerName.interfaces.items(): #récupérer toutes les interfaces des routeurs d'AS voisines, connectées a routeurName 
            ip=valeur[0]
            voisin=valeur[1]
            if voisin.AS_n != routerName.AS_n:
                tmp = None
                for j in voisin.interfaces.values():
                    if j[1] == routerName:
                        tmp = j[0]
                        break
                lignes_addressfamily.append(f"  neighbor {tmp} activate") #@ip de l'interface du routeur de l'AS voisine
                if asName.rel[voisin.AS_n]=="client":
                    lignes_addressfamily.append(f"  neighbor {tmp} route-map frommyclient in")


                elif asName.rel[voisin.AS_n]=="provider":
                    lignes_addressfamily.append(f"  neighbor {tmp} route-map frommyprovider in")
                    lignes_addressfamily.append(f"  neighbor {tmp} route-map tomyprovider out")

                elif asName.rel[voisin.AS_n]=="peer":
                    lignes_addressfamily.append(f"  neighbor {tmp} route-map frommypeer in")
                    lignes_addressfamily.append(f"  neighbor {tmp} route-map tomypeer out")                    


    for r in asName.routers:
        if r != routerName:         #pas sûre que le test entre deux classes routeurs soit défini
            lignes_addressfamily.append(f"  neighbor {r.loopback} activate") #@ loopback des routeurs de l'AS

    lignes_addressfamily.append(" exit-address-family")
    lignes_addressfamily.append("!")
    lignes_addressfamily.append("ip classless")
    lignes_addressfamily.append("ip bgp-community new-format")
    lignes_addressfamily.append("!")
    lignes_addressfamily.append(f"ip community-list standard provider permit {routerName.AS_n}:100")
    lignes_addressfamily.append(f"ip community-list standard client permit {routerName.AS_n}:200")
    lignes_addressfamily.append(f"ip community-list standard peer permit {routerName.AS_n}:300")
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
        lignes_protocole.append(f" router-id {routeurName.numero}.{routeurName.numero}.{routeurName.numero}.{routeurName.numero}")
        if routeurName.border:
            for i,c in routeurName.interfaces.items():
                if c[1].AS_n != routeurName.AS_n:
                    lignes_protocole.append(f" passive-interface {i}")
    
    return lignes_protocole

def route_map_rules(routeurName,AsName):

    lignes_rules=[]
    connexions=[]     #type d'AS connecté sur ce routeur

    for valeur in routeurName.interfaces.values(): #récupérer toutes les interfaces des routeurs d'AS voisines, connectées a routeurName 
        voisin=valeur[1]

        if voisin.AS_n != routeurName.AS_n:
            connexions.append(AsName.rel[voisin.AS_n])

    if "provider" in connexions:
        lignes_rules.append("route-map frommyprovider permit 20")
        lignes_rules.append(" set local-preference 50")
        lignes_rules.append(f" set community {routeurName.AS_n}:100")
        lignes_rules.append("!")

        lignes_rules.append("route-map tomyprovider deny 20")
        lignes_rules.append(f" match community {routeurName.AS_n}:300")
        lignes_rules.append("!")

        lignes_rules.append("route-map tomyprovider deny 21")
        lignes_rules.append(f" match community {routeurName.AS_n}:100")
        lignes_rules.append("!")

        lignes_rules.append("route-map tomyprovider permit 30")
        lignes_rules.append("!")

    if "client" in connexions:
        lignes_rules.append("route-map frommyclient permit 20")
        lignes_rules.append(" set local-preference 150")
        lignes_rules.append(f" set community {routeurName.AS_n}:200")
        lignes_rules.append("!")
        
    if "peer" in connexions:
        lignes_rules.append("route-map frommypeer permit 20")
        lignes_rules.append(" set local-preference 120")
        lignes_rules.append(f" set community {routeurName.AS_n}:300")
        lignes_rules.append("!")

        lignes_rules.append("route-map tomypeer deny 20")
        lignes_rules.append(f" match community {routeurName.AS_n}:100")
        lignes_rules.append("!")

        lignes_rules.append("route-map tomypeer deny 21")
        lignes_rules.append(f" match community {routeurName.AS_n}:300")
        lignes_rules.append("!")

        lignes_rules.append("route-map tomypeer permit 30")
        lignes_rules.append("!")


    return lignes_rules




def drag_and_drop(projet,dico,num):
    """
    fonction qui déplace les fichiers configs dans les bons dossiers
    la variable projet correspond au nom du dossier de projet GNS3 et le dico est correspondances
    num est le numéro du routeur traité
    """
    cle = "R" + str(num)
    nom = f"i{num}_startup-config.cfg"
    relatif = projet
    ancien = os.path.join(os.getcwd(), nom)
    nouveau = os.path.join(os.getcwd(), projet, "project_files", dico[cle],"configs",nom)
    print(ancien)
    print(nouveau)
    os.rename(ancien,nouveau)
