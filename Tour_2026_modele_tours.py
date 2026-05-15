from helper import *

class Tour():
    def __init__(self,parent,pos, type, vitesseTir, cout):
        self.parent=parent
        self.pos=pos
        self.type = type
        self.cible=[0,0]
        self.range = 20
        self.tag=parent.getTagTour()
        self.vitesseTir = vitesseTir               #à modif quand tour upgrade
        self.compteurTir = 11 - vitesseTir    # à modif quand tour upgrade
        self.resellValue = cout*0.7

    def scan(self):
        #pour que la tour compte régulièrement et non pas par creep
        self.compteurTir-=1
        for creep in self.parent.nivoActif.creepsEnCours:
            #les if sont à recheck
            if creep.pos[0] > (self.pos[0]-self.range) and creep.pos[0] < (self.pos[0]+self.range): #si le x du creep est dans le range
                if creep.pos[1] > (self.pos[1]-self.range) and creep.pos[1] < (self.pos[1]+self.range): #si le y du creep est dans le range                
                    if self.compteurTir == 0: #le compteur compte jusqu'à 10 et tire 
                        projectile = Projectile(self,creep)
                        self.parent.projectiles[projectile.tag] = projectile 
                        self.compteurTir = 50               
        if self.compteurTir == 0:
            self.compteurTir = 50

    def ameliorer(self):
        self.niveau += 1
        self.resellValue = round((self.cout*0.7),2)
        self.cout = round((self.cout + 100 )*1.3, 2)
    

class Tour_glace(Tour):
    def __init__(self, parent, pos, type):
        self.vitesseTir = 1 # 1 le plus lent, 10 le plus rapide 
        self.niveau = 1
        self.cout = 250
        Tour.__init__(self, parent, pos, type, self.vitesseTir, self.cout)
        self.force = 1      # 1 le plus faible (25 vies) 10 le plus fort (1000) 
        self.effet = "ralentir"

class Tour_poison(Tour):
    def __init__(self, parent, pos, type):
        self.vitesseTir = 1
        self.niveau = 1
        self.cout = 250
        Tour.__init__(self, parent, pos, type, self.vitesseTir, self.cout)        
        self.force = 1
        self.effet = "poison"

class Tour_laser(Tour):
    def __init__(self, parent, pos, type):
        self.vitesseTir = 1
        self.niveau = 1
        self.cout = 300
        Tour.__init__(self, parent, pos, type, self.vitesseTir, self.cout)        
        self.force = 1
        self.effet = "none"    

class Tour_classique(Tour):
    def __init__(self, parent, pos, type):
        self.vitesseTir = 1    # 1 le plus lent, 10 le plus rapide 
        self.niveau = 1
        self.cout = 150 * self.niveau
        Tour.__init__(self, parent, pos, type, self.vitesseTir, self.cout)        
        self.force = 1        # 1 le plus faible (25 vies) 10 le plus fort (1000) 
        self.effet = "none"

class Tour_bombe(Tour):
    def __init__(self, parent, pos, type):
        self.vitesseTir = 1    # 1 le plus lent, 10 le plus rapide 
        self.niveau = 1
        self.cout = 200 * self.niveau
        Tour.__init__(self, parent, pos, type, self.vitesseTir, self.cout)        
        self.force = 1        # 1 le plus faible (25 vies) 10 le plus fort (1000) 
        self.effet = "none"

class Projectile():                                  
    def __init__(self, parent, cible): #la cible est passée en param, puis on calcule la direction 
        self.tag = parent.parent.getTagProjectile()
        self.type = parent.type
        self.largeur = 25
        self.hauteur = 25
        self.y = parent.pos[1]
        self.x = parent.pos[0]
        self.speed = 1
        self.degat = parent.force * 25

        dx = cible.pos[0] - parent.pos[0]
        dy = cible.pos[1] - parent.pos[1]
        angleRad = math.atan2(dy, dx)
        self.aimX = math.cos(angleRad) * self.speed
        self.aimY = math.sin(angleRad) * self.speed

    def deplacer(self):
        self.x += self.aimX
        self.y += self.aimY