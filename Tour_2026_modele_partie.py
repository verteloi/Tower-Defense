import Tour_2026_modele_creeps as fichierCreeps
import Tour_2026_modele_tours as fichierTours

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
        self.tours.append(fichierTours.Tour(self,pos))
        
    # dependament quel numero de self.creep creer creep de ce type
    def creeCreep(self):
        for i in self.creepsDuNivo:
            match i: 
                case 1 :
                    self.creeps.append(fichierCreeps.Creep_ours(self, i))
                case 2 :
                    self.creeps.append(fichierCreeps.Creep_renard(self, i))
                case 3 :
                    self.creeps.append(fichierCreeps.Creep_ecureuil(self, i))
                case 4 :
                    self.creeps.append(fichierCreeps.Creep_moufette(self, i))
                case 5 :
                    self.creeps.append(fichierCreeps.Creep_porcepique(self, i))
                
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
            if i.vie > 0:
                i.bouge()
            else:
                self.creepsEnCours.remove(i)
    
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
        self.vie = 1
        self.cash = 50000
        self.nivo = 0
        self.score = 0
        self.tagCreep = 0
        self.tagTours = 0
        self.tagProjectile = 0
        self.tourSelectionne = {}
        self.dictCreeps = {}
        self.toursEnJeu = {}
        self.projectiles = {}
        self.tousLesCreeps = [
            [1, 1, 1, 1, 2, 3, 4, 5],      # wave 0 - ours, ours         ------------------- J'ai enlevé un,
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
    
    def setTour(self,pos, type):
        print("TOUR",pos)
        
        match type:
            case 1:
                tour=fichierTours.Tour_classique(self,pos,1)
            case 2:
                tour=fichierTours.Tour_classique(self,pos,2) # tour feu
            case 3:
                tour=fichierTours.Tour_laser(self,pos,3)
            case 4:
                tour=fichierTours.Tour_poison(self,pos,4)
            case 5:
                tour=fichierTours.Tour_glace(self,pos,5)
         
        if(self.cash >= tour.cout):
            self.toursEnJeu[tour.tag] = tour
            self.cash -= tour.cout
            self.parent.parent.vue.afficherTours()
            self.parent.parent.vue.afficheInformationsPartie()   

    def vendreTour(self, tag):
        if tag in self.toursEnJeu:
            tour = self.toursEnJeu[tag]
            self.cash += tour.resellValue
            del self.toursEnJeu[tag]
            self.parent.parent.vue.afficherTours()
            self.parent.parent.vue.afficheInformationsPartie()   

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

    def changeTourSelectionne(self):
        match self.tourSelectionne:
            case None:
                self.noeuds=self.noeuds0
            case "feu":
                self.noeuds=self.noeuds1
            case "glace":
                self.noeuds=self.noeuds2