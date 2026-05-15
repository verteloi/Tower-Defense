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
import Tour_2026_modele_partie as fichierPartie

from helper import *


class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.partieCourante = None
        self.parcourChoisi = 0
        self.difficulteChoisi = 0
        self.tempDiff = 0
        self.tempArgent = 0
        self.tempVie = 0
        
    def demarrePartie(self):
        self.partieCourante = fichierPartie.Partie(self, self.parcourChoisi, self.tempVie, self.tempArgent, self.tempDiff)

    def parcourCliquer(self, numero):
        self.parcourChoisi=numero

if __name__ == '__main__':
    m=Modele(1)
    m.demarrePartie()
    print("FIN")
