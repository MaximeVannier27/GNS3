class AS:
    def __init__(self,numero):
        self.num = numero       #numéro de l'AS
        self.igp = None         #IGP utilisé au sein de l'AS
        self.routers = []       #liste d'élements de type routers.
        self.rel = {}           #dico AS : relations à cet AS
        self.ip  = None         #range ip
        self.loopback = None    #range ip loopback

    def __str__(self):
        return "AS : {self.numero}\nIGP : {self.igp}\nRouters : {self.routers}\nAS relationships : {self.rel}\nIP RANGE: {self.ip}\nLoopback IP range: {self.loopback}"

class Router: 
    def __init__(self,router_AS):
        """
        fonction qui définit comment créer un objet de type router
        """
        self.AS_n = router_AS       #AS auquel appartient le router
        self.loopback = None        #adresse de loopback du router
        self.numero = None          # numero du routeur
        self.interfaces = {}        #dico adresse : interface
        self.voisins_AS = []        #liste des voisins au sein du même AS
        self.voisins_ext = {}       #dico voisin dans un AS différent : numéro d'AS
        self.border = False         #permet de savoir si le router est en bordure de l'AS ou non
        self.configList = []        #liste de strings correspondant aux lignes du fichier config du routeur

    def __str__(self):
        """
        renvoie une liste des attributs de 
        utilisée pour le print 
        """
        return "ID : {self.ID}\nAS: {self.AS}\ninterfaces : {self.interfaces}\nloopback : {self.loopback}\nvoisins du même AS : {self.voisins_AS}\nvoisins d'un autre AS : {self.voisins_ext}"	
    