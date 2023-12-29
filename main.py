from datetime import datetime


config_defaut = ["!", f"! Last configuration change at {datetime.now()}", "!", "version 15.2", "service timestamps debug datetime msec", "service timestamps log datetime msec", "!", "hostname ", "!", "boot-start-marker", "boot-end-marker", "!", "!", "!", "no aaa new-model", "no ip icmp rate-limit unreachable", "ip cef", "!", "!", "!", "!", "!", "!", "no ip domain lookup", "ipv6 unicast-routing", "ipv6 cef", "!", "!", "multilink bundle-name authenticated", "!", "!", "!", "!", "!", "!", "!", "!", "!", "ip tcp synwait-time 5", "!", "!", "!", "!", "!", "!", "!", "!", "!"]


def initConfigList(routerName):
    routerName.configList = config_defaut


def creationConfigFinal(routerName,configList):
    with open(f".configs/i{routerName.numero}_startup-config.cfg","w") as fichier:
        fichier.writelines(configList)



liste_AS = initAS("json")

for AS in liste_AS:
    if AS.igp == "rip":
        for R in AS.routers:
            initConfigList(R)
            R.configList.append()
