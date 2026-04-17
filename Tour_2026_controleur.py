# -*- coding: ISO-8859-1 -*-
import Tour_2026_modele as mod
import Tour_2026_vue as vue

class Controleur():
    def __init__(self):
        self.modele = mod.Modele(self)
        self.vue = vue.Vue(self)
        self.actif = 0
        self.delai = 10  # Vitesse du jeu

    def demarrePartie(self):
        if self.actif == 0:
            self.actif = 1
            self.modele.demarrePartie()
            self.vue.afficheModele()
            self.continuePartie()
        else:
            self.actif = 0

    def continuePartie(self):
        if self.actif:
            self.modele.partieCourante.nivoActif.bougeCreep()
            self.modele.partieCourante.nivoActif.tourScan()
            self.modele.partieCourante.nivoActif.creepScan()
            self.modele.partieCourante.bougeProjectile()
            self.vue.afficheCreepTourBombe()    
            self.vue.afficheInformationsPartie()
            self.vue.root.after(self.delai, self.continuePartie)

    def setTour(self, pos):
        self.modele.partieCourante.setTour(pos)

    def changerDifficulte(self, difficulte):
        self.modele.difficulteChoisi = difficulte

    def changerParcour(self, parcour):
        self.modele.parcourChoisi = parcour
        self.vue.actualiserPreviewParcour()

    def partie_perdu(self):
        self.actif = 0
        self.vue.afficherGameover()
        
if __name__ == '__main__':
    c = Controleur()
    c.vue.root.mainloop()
