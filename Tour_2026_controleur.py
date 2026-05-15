# -*- coding: ISO-8859-1 -*-
import Tour_2026_modele as mod
import Tour_2026_vue as vue

class Controleur():
    def __init__(self):
        self.modele = mod.Modele(self)
        self.vue = vue.Vue(self)
        self.actif = 0
        self.delai = 11  # Vitesse du jeu

    def demarrePartie(self):
        if self.actif == 0:
            self.actif = 1
            self.modele.partieCourante.demarrerVague()
            self.vue.demarrerPartie()
            self.continuePartie() 
        else:
            self.actif = 0

    def continuePartie(self):
        if self.actif and self.modele.partieCourante:
            self.modele.partieCourante.continuerPartie()
            self.vue.afficheCreepTourBombe()    
            self.vue.root.after(self.delai, self.continuePartie)
            if self.modele.partieCourante.nivoActif:
                if not self.modele.partieCourante.nivoActif.creepsEnCours:
                    self.modele.partieCourante.nivoActif = None
                    self.actif = 0
                    self.vue.boutonLancerVague.config(state="normal")

    def setTour(self, pos, type):
        return self.modele.partieCourante.setTour(pos, type)

    def changerDifficulte(self, difficulte):
        self.modele.difficulteChoisi = difficulte
        match difficulte:
            case 0:
                self.modele.tempArgent = 500
                self.modele.tempDiff = 1
                self.modele.tempVie = 100
            case 1:
                self.modele.tempArgent = 750
                self.modele.tempDiff = 1.25
                self.modele.tempVie = 50
            case 2:
                self.modele.tempArgent = 1000
                self.modele.tempDiff = 1.5
                self.modele.tempVie = 10
        self.vue.actualiser_info_difficulte()

    def changerParcour(self, parcour):
        self.modele.parcourChoisi = parcour
        self.vue.actualiserPreviewParcour()
        self.vue.actualiser_info_map()

    def partie_perdu(self):
        self.actif = 0
        self.vue.afficherGameover()
        
if __name__ == '__main__':
    c = Controleur()
    c.vue.root.mainloop()
