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
    def __init__(self, parcourChoisi):
        self.parcourChoisi=parcourChoisi
        self.noeuds1=[[0,10],
                     [50,10],
                     [50,80],
                     [100,80]]
        self.noeuds2=[[0,10],
                     [20,10],
                     [20,40],
                     [50,40],
                     [50,20],
                     [80,20],
                     [80,60],
                     [30,60],
                     [30,80],
                     [100,80]]
        self.noeuds = [[0, 10],
                       [20, 40],
                       [50, 40],
                       [50, 20],
                       [80, 20],
                       [80, 60],
                       [30, 60],
                       [30, 80],
                       [100, 80]]

class Tour():
    def __init__(self,parent,pos):
        self.parent=parent
        self.pos=pos
        self.cible=[0,0]
        self.niveauTour = 1


class Tour_de_glace(Tour):
    def __init__(self,parent):
        Tour.__init__(self,parent)
        self.vitesseTir = 1
        self.force = 1
        self.cout = 125

class Projectile():
    def __init__(self, parent, pos, cible):
        self.parent = parent
        self.pos = pos
        self.cible = cible
             

class Creep():
    def __init__(self,parent):
        self.parent=parent
        self.pos=self.parent.parcours.noeuds[0][:]
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

class Creep_lent(Creep):
    def __init__(self,parent):
        Tour.__init__(self,parent)
        self.degat = 5
        self.vitesse = 1
        self.argent = 50
        self.vie = 100

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
        print("une vie de moins")
        
class Nivo():
    def __init__(self,parent, numero):
        self.parent = parent
        self.wave_active = True
        self.parcours = parent.parcourChoisi
        self.densiteCreep = 3
        self.creeps = [[1, 1, 1, 1, 1],[1, 1, 1, 2, 2, 2]]
        self.creepsEnCours = []
        self.numeroVague = numero
        self.creeCreep()
        
    def ajouteTour(self,pos):
        self.tours.append(Tour(self,pos))
        
    # dependament quel numero de self.creep creer creep de ce type
    def creeCreep(self):
        for i in range(self.parent.creepparnivo):
            self.creeps.append(Creep(self))
            
    def bougeCreep(self):
        if self.creeps:
            ajoute=0
            c=self.creeps[0]
            if self.creepsEnCours:
                cPrecedent=self.creepsEnCours[0]
                if cPrecedent.cible==1: # onverifie si le dernier creep parti est assez loin seulement s'il est sur le m�me tron�on
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
            
    def setTour(self,pos):
        print("NIVO",pos)
        self.tours.append(Tour(self,pos))

class Partie():
    def __init__(self, parent, parcour):
        self.parent=parent
        self.vie = 100
        self.cash = 500
        self.nivo = 0
        self.score = 0
        self.nivoActif = None
        self.listeTourEnJeu = []
        self.parcourChoisi = Parcours(self, parcour)

    def demarrerVague(self):
        self.nivo = self.nivo + 1
        self.nivoActif = Nivo(self, self.nivo)

        
class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.partieCourante = None
        self.parcourChoisi = 0
        self.difficulteChoisi = 0
        self.previewTours = [Tour_de_glace(self, (0,0))]
        
    def demarrePartie(self):
        self.partieCourante = Partie(self.parcourChoisi)

    def parcourCliquer(self, numero):
        self.parcourChoisi=numero

    def setTour(self,pos):
        print("MODELE",pos)
        self.nivoActif.setTour(pos)

if __name__ == '__main__':
    m=Modele(1)
    m.demarrePartie()
    print(m.nivo.creeps)
    print("FIN")