class AS:
    def __init__(self,numero):
        self.num = numero       #numéro de l'AS
        self.igp = None         #IGP utilisé au sein de l'AS
        self.routers = []       #liste d'élements de type routers.
        self.rel = {}           #dico AS : relations de cet AS (les valeurs sont client provider ou peer)
        self.ip  = []           #plage d'adresses ip disponibles pour cet AS
        self.loopback = []      #plage d'adresses de loopback disponibles AS
        self.lienslocaux = {}   # dico (r1,r2) : "subnet ip"


    def __str__(self):
        """
        Fonction pour pouvoir obtenir les attributs d'un AS paramétré à partir d'un print
        """
        return f"AS : {self.num}\nIGP : {self.igp}\nRouters : {self.routers}\nAS relationships : {self.rel}\nIP RANGE: {self.ip}\nLoopback IP range: {self.loopback}\n"

class Router: 
    def __init__(self,router_AS):
        """
        fonction qui définit comment créer un objet de type router
        """
        self.AS_n = router_AS       #AS auquel appartient le router
        self.loopback = None        #adresse de loopback du router
        self.numero = None          # numero du routeur
        self.interfaces = {}        #dico interface : [adresse ip, voisin (objet de type routeur),*coût si ospf]
        self.border = False         #permet de savoir si le router est en bordure de l'AS ou non 
        self.configList = []        #liste de strings correspondant aux lignes du fichier config du routeur

    def __repr__(self):
        """
        représentation compacte, retourne le nom du router
        """
        return f"R{self.numero}"
    

    def __str__(self):
        """
        renvoie une liste des attributs de 
        utilisée pour le print 
        """
        return f"Router : R{self.numero}\nAS: {self.AS_n}\ninterfaces : {self.interfaces}\nloopback : {self.loopback}\n"
    
