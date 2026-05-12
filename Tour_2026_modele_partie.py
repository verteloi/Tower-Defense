import Tour_2026_modele_creeps as fichierCreeps
import Tour_2026_modele_tours as fichierTours

class Partie():
    def __init__(self, parent, parcour):
        self.parent=parent
        self.vie = 1
        self.cash = 5000
        self.nivo = 1
        self.score = 0
        self.tagCreep = 0
        self.tagTours = 0
        self.tagProjectile = 0
        self.tourSelectionne = None
        self.nivoActif = None
        self.dictCreeps = {}
        self.toursEnJeu = {}
        self.toutesLesTours = [self.creerTour(self,1), self.creerTour(self,2), self.creerTour(self,3), self.creerTour(self,4), self.creerTour(self,5)]
        self.projectiles = {}
        self.tousLesCreeps = [ #1 ours,  #2 renard,  #3 ecureuil,  #4 moufette,  #5 porcepine
            [5, 5, 5, 5, 2, 3, 4, 5],      
            [2, 2, 2, 3, 3, 4, 4, 4],      
            [5, 5, 5, 1, 1, 3, 3, 3],      
        ]
        self.parcourChoisi = Parcours(self, parcour)
        self.nivoActif = Nivo(self, self.nivo-1)

    def demarrerVague(self):
        if(not self.nivoActif):
            self.nivo = self.nivo + 1
            self.nivoActif = Nivo(self, self.nivo-1)

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
        match type:
            case 1:
                tour=self.creerTour(self, 1,pos)
            case 2:
                tour=self.creerTour(self,2,pos) # tour feu
            case 3:
                tour=self.creerTour(self,3,pos)
            case 4:
                tour=self.creerTour(self,4,pos)
            case 5:
                tour=self.creerTour(self,5,pos)
        if(self.cash >= tour.cout):
            self.toursEnJeu[tour.tag] = tour
            self.cash -= tour.cout
            self.parent.parent.vue.afficherTours()
            self.parent.parent.vue.afficheInformationsPartie() 
            return self.toursEnJeu[tour.tag]

    def creerTour(self, parent, type, pos=(0,0)):
        tour=None
        match type:
            case 1:
                tour=fichierTours.Tour_classique(parent,pos,1)
            case 2:
                tour=fichierTours.Tour_classique(parent,pos,2) # tour feu
            case 3:
                tour=fichierTours.Tour_laser(parent,pos,3)
            case 4:
                tour=fichierTours.Tour_poison(parent,pos,4)
            case 5:
                tour=fichierTours.Tour_glace(parent,pos,5)
        return tour


    def vendreTour(self, tag):
        if tag in self.toursEnJeu:
            tour = self.toursEnJeu[tag]
            self.cash += tour.resellValue
            del self.toursEnJeu[tag]
            self.parent.parent.vue.afficherTours()
            self.tourSelectionne = None
            self.parent.parent.vue.actualiser_infos_tour()
            self.parent.parent.vue.afficheInformationsPartie()

    def ameliorerTour(self, tag):
        if tag in self.toursEnJeu:
            tour = self.toursEnJeu[tag]
            if self.cash >= tour.cout:
                self.cash -= tour.cout
                tour.ameliorer()
                self.parent.parent.vue.afficheInformationsPartie()
                self.parent.parent.vue.actualiser_infos_tour()

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

    def continuerPartie(self):
        self.nivoActif.bougeCreep()
        self.nivoActif.tourScan()
        self.nivoActif.creepScan()
        self.bougeProjectile()

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
        if self.creepsEnCours:
            for i in self.creepsEnCours:
                if i.vie > 0:
                    i.bouge()
                else:
                    self.creepsEnCours.remove(i)
        else:
            self.wave_active = False
    
    def tourScan(self):
        if self.parent.toursEnJeu and self.creepsEnCours:
            for i in self.parent.toursEnJeu.values():
                i.scan()

    def creepScan(self):
        if self.creepsEnCours:
            for creep in self.creepsEnCours:
                creep.scan_pour_projectiles()

class Parcours():
    def __init__(self, parent, parcourChoisi):
        self.parcourChoisi=parcourChoisi
        self.noeuds1=[[0,51],
                     [14,51],
                     [14,18],
                     [29,18],
                     [29,80],
                     [45,80],
                     [45,29],
                     [60,29],
                     [60,70],
                     [70,70],
                     [70,40],
                     [86,40],
                     [86,60],
                     [100,60]]
        self.noeuds2=[[0,27],
                     [40,27],
                     [50,16],
                     [92,16],
                     [92,48],
                     [20,48],
                     [20,90],
                     [50,90],
                     [62,68],
                     [100,68]]
        self.noeuds0 = [[0, 20],
                       [20, 48], 
                       [51, 48],
                       [51, 27],
                       [84, 27],
                       [84, 70],
                       [30, 70],
                       [30, 91],
                       [100, 91]]
        self.noeudsTours1=[[5,42], #fait
                     [10,55],
                     [5,22],
                     [20,10],
                     [33,23],
                     [20,33],
                     [35,73],
                     [49,73],
                     [50,34],
                     [63,58],
                     [75,32],
                     [90,48],
                     [92,65]]
        self.noeudsTours2=[[10,19],
                     [30,35],
                     [37,15],
                     [60,8],
                     [80,8],
                     [85,54],
                     [65,54],
                     [10,60],
                     [10,80],
                     [59,84],
                     [66,74],
                     [76,60],
                     [88,74],]
        self.noeudsTours0 = [[10,25], #fait
                       [5,45], 
                       [30,40],
                       [39,55],
                       [40,32],
                       [59,30],
                       [67,18],
                       [75,30],
                       [88,45],                        
                       [75,60],
                       [59,79],
                       [38,78],
                       [20,80],
                       [90,80]]
        match parcourChoisi:
            case 0:
                self.noeuds=self.noeuds0
            case 1:
                self.noeuds=self.noeuds1
            case 2:
                self.noeuds=self.noeuds2
        match parcourChoisi:
            case 0:
                self.noeudsTours=self.noeudsTours0
            case 1:
                self.noeudsTours=self.noeudsTours1
            case 2:
                self.noeudsTours=self.noeudsTours2