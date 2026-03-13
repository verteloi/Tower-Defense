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
        self.img_parcour1 = PhotoImage(file="images\\img_parcour1.png")
        self.img_parcour2 = PhotoImage(file="images\\img_parcour2.png")
        self.img_parcour3 = PhotoImage(file="images\\img_parcour3.png")
        self.img_creep_ours = PhotoImage(file="images\\ours.png")
        self.img_creep_por = PhotoImage(file="images\\porcupine.png")
        self.img_creep_raton = PhotoImage(file="images\\raton.png")
        self.img_creep_renard = PhotoImage(file="images\\renard.png")
        self.img_creep_ecur = PhotoImage(file="images\\squirrel.png")
        # On garde votre logique de bouton
        b = tk.Button(self.root, text="Demarrer", command=self.parent.demarrePartie)
        b.pack()
        self.canevas = tk.Canvas(self.root, width=self.width, height=self.hight) 
        match self.parent.modele.parcourChoisi:
            case 0:
                self.canevas.create_image(0,0, image=self.img_parcour1, anchor="nw")
                #image=self.img_parcour1
            case 1:
                self.canevas.create_image(0,0, image=self.img_parcour3, anchor="nw")
                #image=self.img_parcour2
            case 2:
                self.canevas.create_image(0,0, image=self.img_parcour2, anchor="nw")
                #image=self.img_parcour3

        
        self.canevas.bind("<Button-1>", self.getPosTour)
        self.canevas.pack()
        #sidebar try
        #self.sidebar = tk.Frame(self.mainframe, bg="lightblue", width=300, height=self.hight)
        #self.sidebar.grid(column=1,row=0)

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
        #self.canevas.create_line(pos, width=2, fill="black", tags=("chemin",))  # ------ on n'a pas besoin de la ligne noire

    def afficheCreepTourBombe(self):
        self.canevas.delete("creep")
        self.canevas.delete("tour")
        self.canevas.delete("bombe")

        # Logique originale pr�serv�e (via nivoActif)
        for i in self.parent.modele.partieCourante.nivoActif.creepsEnCours:
            x1 = i.pos[0] * (self.width/100) - 15
            y1 = i.pos[1] * (self.hight/100) - 15
            x2 = i.pos[0] * (self.width/100) + 15
            y2 = i.pos[1] * (self.hight/100) + 15
            #self.canevas.create_oval(x1, y1, x2, y2, width=2, fill="red", tags=("creep",))
            self.canevas.create_image(x1, y1, image=self.img_creep_ours, anchor="nw",tags=("creep",))

        # Logique originale pr�serv�e (via nivoActif)
        for i in self.parent.modele.partieCourante.toursEnJeu.values():
            x1 = i.pos[0] * 5 - 10
            y1 = i.pos[1] * 5 - 10
            x2 = i.pos[0] * 5 + 10
            y2 = i.pos[1] * 5 + 10
            # print("LOCtour",i.pos,x1,y1,x2,y2)
            self.canevas.create_rectangle(x1, y1, x2, y2, width=1, fill="green", tags=("tour",))
