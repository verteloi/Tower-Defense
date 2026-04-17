# -*- coding: ISO-8859-1 -*-
'''
Jeu de defense de Tours_2026
 deux patrons de parcours
 les niveaux incremente la difficult�
    en augmentant la force des creeps
    en augmentant le nombre de creeps

les Tours_2026 peuvent b�n�ficier d'ameliorations
   en terme de morts occasion�es
   et d'argent disponible
'''

import random
from helper import *
class Parcours():
    def __init__(self, parent, parcourChoisi):
        self.parcourChoisi=parcourChoisi
        self.noeuds1=[[0,50],
                     [15,50],
                     [15,20],
                     [30,20],
                     [30,80],
                     [45,80],
                     [45,30],
                     [60,30],
                     [60,70],
                     [70,70],
                     [70,40],
                     [85,40],
                     [85,60],
                     [100,60]]
        self.noeuds2=[[0,30],
                     [40,30],
                     [50,20],
                     [90,20],
                     [90,50],
                     [20,50],
                     [20,90],
                     [50,90],
                     [60,70],
                     [100,70]]
        self.noeuds0 = [[0, 20],
                       [20, 48], 
                       [51, 48],
                       [51, 27],
                       [84, 27],
                       [84, 70],
                       [30, 70],
                       [30, 91],
                       [100, 91]]
        match parcourChoisi:
            case 0:
                self.noeuds=self.noeuds0
            case 1:
                self.noeuds=self.noeuds1
            case 2:
                self.noeuds=self.noeuds2

class Projectile():                                  
    def __init__(self, parent, cible): #la cible est passée en param, puis on calcule la direction 
        self.tag = parent.parent.getTagProjectile()
        self.largeur = 15
        self.hauteur = 20
        self.y = parent.pos[1]
        self.x = parent.pos[0]
        self.speed = 3
        self.degat = parent.force * 25

        dx = cible.pos[0] - parent.pos[0]
        dy = cible.pos[1] - parent.pos[1]
        angleRad = math.atan2(dy, dx)
        self.aimX = math.cos(angleRad) * self.speed
        self.aimY = math.sin(angleRad) * self.speed

    def deplacer(self):
        self.x += self.aimX
        self.y += self.aimY


class Tour():
    def __init__(self,parent,pos, vitesseTir):
        self.parent=parent
        self.pos=pos
        self.cible=[0,0]
        self.niveauTour = 1
        self.range = 15
        self.tag=parent.getTagTour()
        self.vitesseTir = vitesseTir               #à modif quand tour upgrade
        self.compteurTir = 11 - vitesseTir    # à modif quand tour upgrade
        print(self.tag)

    def scan(self):
        for creep in self.parent.nivoActif.creepsEnCours:
            #les if sont à recheck
            if creep.pos[0] > (self.pos[0]-self.range) and creep.pos[0] < (self.pos[0]+self.range): #si le x du creep est dans le range
                if creep.pos[1] > (self.pos[1]-self.range) and creep.pos[1] < (self.pos[1]+self.range): #si le y du creep est dans le range
                    self.compteurTir-=1
                    if self.compteurTir == 0: #le compteur compte jusqu'à 10 et tire 
                        projectile = Projectile(self,creep)
                        self.parent.projectiles[projectile.tag] = projectile
                        self.compteurTir = 10



class Tour_glace(Tour):
    def __init__(self, parent, pos):
        self.vitesseTir = 1 # 1 le plus lent, 10 le plus rapide 
        Tour.__init__(self, parent, pos, self.vitesseTir)
        self.force = 1      # 1 le plus faible (25 vies) 10 le plus fort (1000) 
        self.cout = 250
        self.effet = "ralentir"

class Tour_poison(Tour):
    def __init__(self, parent, pos):
        self.vitesseTir = 1
        Tour.__init__(self, parent, pos, self.vitesseTir)
        self.force = 1
        self.cout = 250
        self.effet = "poison"  

class Tour_laser(Tour):
    def __init__(self, parent, pos):
        self.vitesseTir = 1
        Tour.__init__(self, parent, pos, self.vitesseTir)
        self.force = 1
        self.cout = 300
        self.effet = "none"

class Tour_classique(Tour):
    def __init__(self, parent, pos):
        self.vitesseTir = 1    # 1 le plus lent, 10 le plus rapide 
        Tour.__init__(self, parent, pos, self.vitesseTir)   
        self.force = 1        # 1 le plus faible (25 vies) 10 le plus fort (1000) 
        self.cout = 150
        self.effet = "none"

class Creep():
    def __init__(self,parent, type):
        self.parent=parent
        self.pos=self.parent.parcours.noeuds[0][:]
        self.tag=parent.parent.getTagCreep()
        self.type = type
        print(self.tag)
        self.cible=1 #indice du noeud de parcours a atteindre
        if self.pos[0]!=self.parent.parcours.noeuds[1][0]: # on simplifie le mouvement en verifiant uniquement l'axe de deplacement
            self.axe=0
            if self.pos[0]<self.parent.parcours.noeuds[1][0]:
                self.dir=1
            else:
                self.dir=-1
        else:
            self.axe=1
            if self.pos[1]<self.parent.parcours.noeuds[1][1]:
                self.dir=1
            else:
                self.dir=-1
        self.vitesse=2
        self.force=10

    def bouge(self):
        # 1. V�rifier si on a fini le parcours (S�curit�)
        if self.cible >= len(self.parent.parcours.noeuds):
            self.perdre_vie_joueur()
            return

        # 2. Identifier le point de destination imm�diat
        cible_x, cible_y = self.parent.parcours.noeuds[self.cible]
        curr_x, curr_y = self.pos

        # 3. Calculer la distance restante vers ce point
        # (Utilise votre nouveau Helper ou l'alias)
        dist_restante = Helper.calcDistance(curr_x, curr_y, cible_x, cible_y)

        # 4. Logique de mouvement
        if dist_restante <= self.vitesse:
            # CAS A : On d�passe ou on atteint la cible ce tour-ci
            self.pos = [cible_x, cible_y]  # On se "snap" exactement sur le point
            self.cible += 1  # On passe au prochain noeud

            # Si c'�tait le dernier noeud, on blesse le joueur
            if self.cible >= len(self.parent.parcours.noeuds):
                self.perdre_vie_joueur()
                
        else:
            # CAS B : On est encore en chemin
            # On calcule l'angle vers la cible
            angle = Helper.calcAngle(curr_x, curr_y, cible_x, cible_y)
            # On avance exactement de "vitesse" dans cette direction
            nouv_x, nouv_y = Helper.getAngledPoint(angle, self.vitesse, curr_x, curr_y)
            self.pos = [nouv_x, nouv_y]

    def perdre_vie_joueur(self):
        for creep in self.parent.creepsEnCours:
            if (creep.pos[0] >= 100):
                self.parent.parent.vie -= creep.degat 
                self.parent.creepsEnCours.remove(creep)
                print(str(creep.tag) + " was deleted")  

    def scan_pour_projectiles(self):
        a_supprimer = []

        for projectile in self.parent.parent.projectiles.values():
            if (projectile.x >= (self.pos[0]-4) and projectile.x <= (self.pos[0] + 4)): #projectile est dans le x du creep
                if (projectile.y >= (self.pos[1]-4) and projectile.y <= (self.pos[1] + 4)): #projectile est dans le y du creep
                    a_supprimer.append(projectile.tag)
                    self.vie -= projectile.degat
                
        for tag in a_supprimer:
                del self.parent.parent.projectiles[tag]

# LENT ET FORT
class Creep_ours(Creep):
    def __init__(self,parent, type):
        Creep.__init__(self,parent, type)
        self.degat = 25
        self.vitesse = 0.5
        self.argent = 100 * 3
        self.vie = 1000

# MOYEN VITE ET MOYEN FORT
class Creep_renard(Creep):
    def __init__(self,parent, type):
        Creep.__init__(self,parent, type)
        self.degat = 15
        self.vitesse = 1.2
        self.argent = 100 * 2
        self.vie = 200

# VITE ET FAIBLE
class Creep_ecureuil(Creep):
    def __init__(self,parent, type):
        Creep.__init__(self,parent, type)
        self.degat = 5
        self.vitesse = 2
        self.argent = 100 * 1.5
        self.vie = 50

# VITESSE NORMALE ET VIE NORMALE
class Creep_moufette(Creep):
    def __init__(self,parent, type):
        Creep.__init__(self,parent, type)
        self.degat = 5
        self.vitesse = 1
        self.argent = 100
        self.vie = 100

# VITESSE NORMALE ET VIE NORMALE
class Creep_porcepique(Creep):
    def __init__(self,parent, type):
        Creep.__init__(self,parent, type)
        self.degat = 5
        self.vitesse = 1
        self.argent = 100
        self.vie = 100
        
class Nivo():
    def __init__(self,parent, numero):
        self.parent = parent
        self.wave_active = True
        self.parcours = parent.parcourChoisi
        self.densiteCreep = 3
        self.creepsDuNivo = parent.tousLesCreeps[numero]
        self.creeps = []
        self.creepsEnCours = []
        self.numeroVague = numero
        self.creeCreep()
        
    def ajouteTour(self,pos):
        self.tours.append(Tour(self,pos))
        
    # dependament quel numero de self.creep creer creep de ce type
    def creeCreep(self):
        for i in self.creepsDuNivo:
            match i: 
                case 1 :
                    self.creeps.append(Creep_ours(self, 1))
                case 2 :
                    self.creeps.append(Creep_renard(self, 2))
                case 3 :
                    self.creeps.append(Creep_ecureuil(self, 3))
                case 4 :
                    self.creeps.append(Creep_moufette(self, 4))
                case 5 :
                    self.creeps.append(Creep_porcepique(self, 5))
                
    def bougeCreep(self):
        if self.creeps:
            ajoute=0
            c=self.creeps[0]
            if self.creepsEnCours:
                cPrecedent=self.creepsEnCours[0]
                if cPrecedent.cible==1: # on verifie si le dernier creep parti est assez loin seulement s'il est sur le m�me tron�on
                    if cPrecedent.pos[c.axe]>c.pos[c.axe]+c.parent.densiteCreep:
                        ajoute=1
            else:
                ajoute=1
            if ajoute:
                c=self.creeps.pop(0)
                c.pos=self.parcours.noeuds[0][:] # on positionne le creep sur le prmier noeud
                c.cible=1 #on vise le prochain noeud, le deuxieme
                self.creepsEnCours.insert(0,c)
        n=0
        for i in self.creepsEnCours:
            n=n+1
            i.bouge()
    
    def tourScan(self):
        if self.parent.toursEnJeu and self.creepsEnCours:
            for i in self.parent.toursEnJeu.values():
                i.scan()

    def creepScan(self):
        if self.creepsEnCours:
            for creep in self.creepsEnCours:
                creep.scan_pour_projectiles()



class Partie():
    def __init__(self, parent, parcour):
        self.parent=parent
        self.vie = 100
        self.cash = 500
        self.nivo = 0
        self.score = 0
        self.tagCreep = 0
        self.tagTours = 0
        self.tagProjectile = 0
        self.dictCreeps = {}
        self.toursEnJeu = {}
        self.projectiles = {}
        self.tousLesCreeps = [
            [1, 2, 3, 4, 5],      # wave 0 - ours, ours         ------------------- J'ai enlevé un
            [2, 2],      # wave 1 - renard, renard
            [1, 2],      # wave 2 - ours, renard
        ]
        self.parcourChoisi = Parcours(self, parcour)
        self.nivoActif = Nivo(self, self.nivo)

    def demarrerVague(self):
        self.nivo = self.nivo + 1
        self.nivoActif = Nivo(self, self.nivo)

    def getTagCreep(self):
        self.tagCreep = self.tagCreep + 1
        return "creep_"+str(self.tagCreep)
    
    def getTagTour(self):
        self.tagTours = self.tagTours + 1
        return "tour_"+str(self.tagTours)
    
    def getTagProjectile(self): 
        self.tagProjectile = self.tagProjectile + 1
        return "tour_"+str(self.tagProjectile)
    
    def setTour(self,pos):
        print("MODELE",pos)
        tour=Tour_classique(self,pos)
        self.toursEnJeu[tour.tag] = tour

    def bougeProjectile(self):
        a_supprimer = []
        if self.projectiles:
            for p in self.projectiles.values():
                #deplacer s'il est encore dans le cadre, sinon effacer
                if p.x > 0 and p.y > 0 and p.x < 100 and p.y < 100:
                    p.deplacer()
                else:
                    a_supprimer.append(p.tag)
            
            for tag in a_supprimer:
                del self.projectiles[tag]


        
class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.partieCourante = None
        self.parcourChoisi = 0
        self.difficulteChoisi = 0
        
    def demarrePartie(self):
        self.partieCourante = Partie(self, self.parcourChoisi)

    def parcourCliquer(self, numero):
        self.parcourChoisi=numero





if __name__ == '__main__':
    m=Modele(1)
    m.demarrePartie()
    print("FIN")
