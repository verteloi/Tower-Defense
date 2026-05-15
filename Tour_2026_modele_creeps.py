from helper import *

class Creep():
    def __init__(self,parent, type):
        self.parent=parent
        self.pos=self.parent.parcours.noeuds[0][:]
        self.tag=parent.parent.getTagCreep()
        self.type = type
        self.diffMulti = parent.parent.diffMulti
        self.empoisone = False
        self.glace = False
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

        #si on est empoisoné ou figé dans la glace
        if self.glace:
            if self.compteurGlace>0:
                self.compteurGlace-=1
            else:
                self.glace = False
                self.vitesse = self.vitesseBase
        if self.empoisone:
            if self.compteurEmpoisone>0:
                self.compteurEmpoisone-=1
            else:
                self.empoisone = False
                self.vitesse = self.vitesseBase

    def perdre_vie_joueur(self):
        for creep in self.parent.creepsEnCours: #quand le creep arrive à la fin, le joueur perd une vie et on le delete de la liste
            if (creep.pos[0] >= 100):
                self.parent.parent.vie -= creep.degat 
                self.parent.creepsEnCours.remove(creep)
                if (self.parent.parent.vie <= 0):
                    self.parent.parent.parent.parent.partie_perdu()
                print(str(creep.tag) + " was deleted")  

    def scan_pour_projectiles(self):
        a_supprimer = []

        for projectile in self.parent.parent.projectiles.values():
            if (projectile.x >= (self.pos[0]-3) and projectile.x <= (self.pos[0] + 3)): #projectile est dans le x du creep
                if (projectile.y >= (self.pos[1]-3) and projectile.y <= (self.pos[1] + 3)): #projectile est dans le y du creep
                    
                    match projectile.type:
                        case 1: #feu
                            a_supprimer.append(projectile.tag)
                        case 2 : #bombe
                            a_supprimer.append(projectile.tag) 
                            self.parent.parent.lancerBombe(self)         
                        case 3 : #laser
                            pass
                        case 4 : #poison
                            a_supprimer.append(projectile.tag) 
                            self.parent.parent.lancerPoison(self)
                            self.empoisone = True
                            self.vitesse /=2
                            self.compteurEmpoisone = 100
                        case 5 : #glace
                            a_supprimer.append(projectile.tag) 
                            self.parent.parent.lancerGlace(self)
                            self.glace = True
                            self.vitesse =0
                            self.compteurGlace = 100
                    self.vie -= projectile.degat
        for tag in a_supprimer:
                del self.parent.parent.projectiles[tag]

# LENT ET FORT
class Creep_ours(Creep):
    def __init__(self,parent, type):
        Creep.__init__(self,parent, type)
        self.degat = 25 * self.diffMulti
        self.vitesse = 0.05
        self.vitesseBase = 0.05
        self.argent = 100
        self.vie = 1000 * self.diffMulti

# MOYEN VITE ET MOYEN FORT
class Creep_renard(Creep):
    def __init__(self,parent, type):
        Creep.__init__(self,parent, type)
        self.degat = 15 * self.diffMulti
        self.vitesseBase = 0.15
        self.vitesse = self.vitesseBase
        self.argent = 100
        self.vie = 300 * self.diffMulti

# VITE ET FAIBLE
class Creep_ecureuil(Creep):
    def __init__(self,parent, type):
        Creep.__init__(self,parent, type)
        self.degat = 5 * self.diffMulti
        self.vitesseBase = 0.2
        self.vitesse = self.vitesseBase
        self.argent = 100
        self.vie = 100 * self.diffMulti

# VITESSE NORMALE ET VIE NORMALE
class Creep_moufette(Creep):
    def __init__(self,parent, type):
        Creep.__init__(self,parent, type)
        self.degat = 5 * self.diffMulti
        self.vitesseBase = 0.1
        self.vitesse = self.vitesseBase
        self.argent = 100
        self.vie = 200 * self.diffMulti

# VITESSE NORMALE ET VIE NORMALE
class Creep_porcepique(Creep):
    def __init__(self,parent, type):
        Creep.__init__(self,parent, type)
        self.degat = 5 * self.diffMulti
        self.vitesseBase = 0.1
        self.vitesse = self.vitesseBase
        self.argent = 100
        self.vie = 200 * self.diffMulti
