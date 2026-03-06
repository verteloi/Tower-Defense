# -*- coding: ISO-8859-1 -*-
from tkinter import *
import tkinter as tk

#liste de frames pour toutes les affaires que je veux dessiner
#frames = petites boites
#fonctionb pour créer chq frame (comme des inits)
#dictionnaire avedc les fenetres avec les tags

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Tk()
        self.hight = 700
        self.width = 700
        #self.mainframe = tk.Frame(self.root,bg="gray", width=self.width, height=self.hight, cursor="man") # **** main frame
        #import des images
        self.img_parcour1 = PhotoImage(file="images\img_parcour1.png")
        # On garde votre logique de bouton
        b = tk.Button(self.root, text="Demarrer", command=self.parent.demarrePartie)
        b.pack()
        self.canevas = tk.Canvas(self.root, width=self.width, height=self.hight) 
        #self.canevas.create_image(0,0, image=self.img_parcour1, anchor="nw")
        self.canevas.bind("<Button-1>", self.getPosTour)
        self.canevas.pack()
        self.parcour1()
        #sidebar try
        #self.sidebar = tk.Frame(self.mainframe, bg="lightblue", width=300, height=self.hight)
        #self.sidebar.grid(column=1,row=0)

    def parcour1(self):
        #import des images
        self.img_parcour1 = PhotoImage(file="images\img_parcour1.png")
        self.canevas.create_image(0,0, image=self.img_parcour1, anchor="nw")


    def getPosTour(self, evt):
        x = evt.x / 5
        y = evt.y / 5
        # print ("POS",x,y)
        self.parent.setTour([x, y])

    def afficheModele(self):
        pos = []
        # On assume que nivoActif est initialis� au moment de l'affichage
        for i in self.parent.modele.partieCourante.parcourChoisi.noeuds:
            pos.append(i[0] * (self.width/100))
            pos.append(i[1] * (self.hight/100))
        self.canevas.create_line(pos, width=2, fill="black", tags=("chemin",))  # ------ on n'a pas besoin de la ligne noire

    def afficheCreepTourBombe(self):
        self.canevas.delete("creep")
        self.canevas.delete("tour")
        self.canevas.delete("bombe")

        # Logique originale pr�serv�e (via nivoActif)
        for i in self.parent.modele.partieCourante.nivoActif.creepsEnCours:
            x1 = i.pos[0] * (self.width/100) - 3
            y1 = i.pos[1] * (self.hight/100) - 3
            x2 = i.pos[0] * (self.width/100) + 3
            y2 = i.pos[1] * (self.hight/100) + 3
            self.canevas.create_oval(x1, y1, x2, y2, width=2, fill="red", tags=("creep",))

        # Logique originale pr�serv�e (via nivoActif)
        for i in self.parent.modele.partieCourante.listeTourEnJeu:
            x1 = i.pos[0] * (self.width/100) - 3
            y1 = i.pos[1] * (self.hight/100) - 5
            x2 = i.pos[0] * (self.width/100) + 3
            y2 = i.pos[1] * (self.hight/100) + 5
            # print("LOCtour",i.pos,x1,y1,x2,y2)
            self.canevas.create_rectangle(x1, y1, x2, y2, width=1, fill="green", tags=("tour",))

