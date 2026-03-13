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
        self.noeuds = [[0, 20],
                       [20, 48], 
                       [51, 48],
                       [51, 27],
                       [84, 27],
                       [84, 70],
                       [30, 70],
                       [30, 91],
                       [100, 91]]

class Tour():
    def __init__(self,parent,pos):
        self.parent=parent
        self.pos=pos
        self.cible=[0,0]
        self.niveauTour = 1
        self.tag=parent.getTagTour()
        print(self.tag)

class Tour_glace(Tour):
    def __init__(self, parent, pos):
        Tour.__init__(self, parent, pos)
        self.vitesseTir = 1
        self.force = 1
        self.cout = 250
        self.effet = "ralentir"

class Tour_poison(Tour):
    def __init__(self, parent, pos):
        Tour.__init__(self, parent, pos)
        self.vitesseTir = 1
        self.force = 1
        self.cout = 250
        self.effet = "poison"  

class Tour_laser(Tour):
    def __init__(self, parent, pos):
        Tour.__init__(self, parent, pos)
        self.vitesseTir = 1
        self.force = 1
        self.cout = 300
        self.effet = "none"

class Tour_classique(Tour):
    def __init__(self, parent, pos):
        Tour.__init__(self, parent, pos)
        self.vitesseTir = 1
        self.force = 1
        self.cout = 150
        self.effet = "none"

class Projectile():
    def __init__(self, parent, pos, cible):
        self.parent = parent
        self.pos = pos
        self.cible = cible

class Creep():
    def __init__(self,parent):
        self.parent=parent
        self.pos=self.parent.parcours.noeuds[0][:]
        self.tag=parent.parent.getTagCreep()
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

# LENT ET FORT
class Creep_ours(Creep):
    def __init__(self,parent):
        Creep.__init__(self,parent)
        self.degat = 25
        self.vitesse = 0.5
        self.argent = 100 * 3
        self.vie = 1000

# MOYEN VITE ET MOYEN FORT
class Creep_renard(Creep):
    def __init__(self,parent):
        Creep.__init__(self,parent)
        self.degat = 15
        self.vitesse = 1.2
        self.argent = 100 * 2
        self.vie = 200

# VITE ET FAIBLE
class Creep_ecureuil(Creep):
    def __init__(self,parent):
        Creep.__init__(self,parent)
        self.degat = 5
        self.vitesse = 2
        self.argent = 100 * 1.5
        self.vie = 50

# VITESSE NORMALE ET VIE NORMALE
class Creep_moufette(Creep):
    def __init__(self,parent):
        Creep.__init__(self,parent)
        self.degat = 5
        self.vitesse = 1
        self.argent = 100
        self.vie = 100

# VITESSE NORMALE ET VIE NORMALE
class Creep_porcepique(Creep):
    def __init__(self,parent):
        Creep.__init__(self,parent)
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
                    self.creeps.append(Creep_ours(self))
                case 2 :
                    self.creeps.append(Creep_renard(self))
                case 3 :
                    self.creeps.append(Creep_ecureuil(self))
                case 4 :
                    self.creeps.append(Creep_moufette(self))
                case 5 :
                    self.creeps.append(Creep_porcepique(self))
                
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

class Partie():
    def __init__(self, parent, parcour):
        self.parent=parent
        self.vie = 100
        self.cash = 500
        self.nivo = 0
        self.score = 0
        self.tagCreep = 0
        self.tagTours = 0
        self.dictCreeps = {}
        self.toursEnJeu = {}
        self.tousLesCreeps = [
            [1, 1],      # wave 0 - ours, ours
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
    
    def setTour(self,pos):
        print("MODELE",pos)
        tour=Tour(self,pos)
        self.toursEnJeu[tour.tag] = tour
        
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
