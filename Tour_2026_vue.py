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
        self.coefHeight = self.hight/100
        self.coefWidth = self.width/100
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
        self.img_tour_classique = PhotoImage(file="images\\tourfeu.png")

        self.frame_demarrage = tk.Frame(self.root, width=self.width, height=self.hight, bg="gray")
        self.frame_menu = tk.Frame(self.root, width=self.width, height=self.hight, bg="lightgray")
        self.frame_jeu = tk.Frame(self.root)
        self.frame_scores = tk.Frame(self.root, width=self.width, height=self.hight, bg="black")
        self.frame_gameover = tk.Frame(self.root, width=self.width, height=self.hight, bg="black")

        self.afficherEcranDemarrage()

    def afficherEcranDemarrage(self):
        self.frame_gameover.pack_forget()
        self.frame_menu.pack_forget()
        self.frame_jeu.pack_forget()
        self.frame_scores.pack_forget()
        
        self.frame_demarrage.pack()
        
        titre = tk.Label(self.frame_demarrage, text="Tower Defense", font=("Arial", 30))
        titre.pack(pady=50)

        bouton_demarrer = tk.Button(self.frame_demarrage, text="Demarrer", command=self.afficherMenu)
        bouton_demarrer.pack(pady=10)

        bouton_scores = tk.Button(self.frame_demarrage, text="Scores", command=self.afficherScores)
        bouton_scores.pack(pady=10)

    def afficherMenu(self):
        self.frame_gameover.pack_forget()
        self.frame_demarrage.pack_forget()
        self.frame_menu.pack()

        # sidebar
        sidebar_creer = tk.Frame(self.frame_menu, bg="white", width=300, height=self.hight)
        sidebar_creer.pack(side="right", fill="y")

        tk.Label(sidebar_creer, text="MENU", font=("Arial", 18, "bold"), bg="#AAAAAA").pack(pady=10, fill="x")

        # Map
        bouton_parcour_0 = tk.Button(sidebar_creer, text="Map 1", command=lambda:self.parent.changerParcour(0))
        bouton_parcour_0.pack(pady=5, padx=20)
        bouton_parcour_1 = tk.Button(sidebar_creer, text="Map 2", command=lambda:self.parent.changerParcour(1))
        bouton_parcour_1.pack(pady=5, padx=20)
        bouton_parcour_2 = tk.Button(sidebar_creer, text="Map 3", command=lambda:self.parent.changerParcour(2))
        bouton_parcour_2.pack(pady=5, padx=20)

        # Difficulté
        text_diff = tk.Label(sidebar_creer, text="difficulte", font=("Arial", 12, "bold"), bg="#AAAAAA")
        text_diff.pack(pady=(20, 0), fill="x")

        diff_frame = tk.Frame(sidebar_creer, bg="white")
        diff_frame.pack(pady=10)
        
        bouton_diff_facile = tk.Button(diff_frame, text="F", bg="lightgreen", command=lambda:self.parent.changerDifficulte(0))
        bouton_diff_facile.pack(side="left", padx=2)

        bouton_diff_moyenne = tk.Button(diff_frame, text="M", bg="orange", command=lambda:self.parent.changerDifficulte(1))
        bouton_diff_moyenne.pack(side="left", padx=2)
        
        bouton_diff_difficile = tk.Button(diff_frame, text="D", bg="red",  command=lambda:self.parent.changerDifficulte(2))
        bouton_diff_difficile.pack(side="left", padx=2)

        # Démarrer
        bouton_demarrer = tk.Button(sidebar_creer, text="Demarrer", font=("Arial", 14, "bold"), bg="#A0EC2C", command=self.afficherInterfaceJeu)
        bouton_demarrer.pack(side="bottom", pady=10, padx=10)

        # preview parcour
        conteneurPreviewParcours = tk.Frame(self.frame_menu, bg="gray", width=self.width, height=self.hight)
        conteneurPreviewParcours.pack(side="left", expand=True, fill="both")
        self.previewParcours = tk.Canvas(conteneurPreviewParcours, width=self.width, height=self.hight)
        self.previewParcours.pack(expand=True, fill="both")

        self.actualiserPreviewParcour()

    def actualiserPreviewParcour(self):
        self.previewParcours.delete("all")
        match self.parent.modele.parcourChoisi:
            case 0: self.previewParcours.create_image(0, 0, image=self.img_parcour1, anchor="nw")
            case 1: self.previewParcours.create_image(0, 0, image=self.img_parcour3, anchor="nw")
            case 2: self.previewParcours.create_image(0, 0, image=self.img_parcour2, anchor="nw")

    def afficherInterfaceJeu(self):
        self.frame_menu.pack_forget()        
        self.frame_jeu.pack()

        # Sidebar à droite dans frame_jeu
        self.sidebar = tk.Frame(self.frame_jeu, bg="white", width=250, height=self.hight)
        self.sidebar.pack(side="right", fill="y")
        tk.Button(self.sidebar, text="Lancer Vague", command=self.parent.demarrePartie).pack(pady=20)

        # Canva à gauche dans frame_jeu
        self.canevas = tk.Canvas(self.frame_jeu, width=self.width, height=self.hight, bg="black")
        self.canevas.pack(side="left")

        # Fond du canevas
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

    def afficherScores(self):
        return        

    def afficherGameover(self):
        self.frame_menu.pack_forget()
        self.frame_jeu.pack_forget()
        self.frame_scores.pack_forget()
        
        self.frame_gameover.pack()
        
        titre = tk.Label(self.frame_gameover, text="GAME OVER", font=("Arial", 30))
        titre.pack(pady=50)

        bouton_menu = tk.Button(self.frame_gameover, text="menu", command=self.afficherEcranDemarrage)
        bouton_menu.pack(pady=10)

        bouton_rejouer = tk.Button(self.frame_gameover, text="rejouer", command=self.afficherMenu)
        bouton_rejouer.pack(pady=10)

    def getPosTour(self, evt):
        x = evt.x / self.coefWidth
        y = evt.y / self.coefHeight
        # print ("POS",x,y)
        self.parent.setTour([x, y])

    def afficheModele(self):
        pos = []
        # On assume que nivoActif est initialis� au moment de l'affichage, pour aficher la ligne noire
        for i in self.parent.modele.partieCourante.parcourChoisi.noeuds:
            pos.append(i[0] * self.coefWidth)
            pos.append(i[1] * self.coefHeight)
        #self.canevas.create_line(pos, width=2, fill="black", tags=("chemin",))  # ------ on n'a pas besoin de la ligne noire

    def afficheCreepTourBombe(self):
        self.canevas.delete("creep")
        self.canevas.delete("tour")
        self.canevas.delete("bombe")

        # Logique originale pr�serv�e (via nivoActif)
        for i in self.parent.modele.partieCourante.nivoActif.creepsEnCours:
            x1 = i.pos[0] * self.coefWidth - 15
            y1 = i.pos[1] * self.coefHeight - 15
            #x2 = i.pos[0] * (self.width/100) + 15
            #y2 = i.pos[1] * (self.hight/100) + 15
            #self.canevas.create_oval(x1, y1, x2, y2, width=2, fill="red", tags=("creep",))
            match i.type :
                case 1 :
                     self.canevas.create_image(x1, y1, image=self.img_creep_ours, anchor="nw",tags=("creep",))
                case 2 :
                     self.canevas.create_image(x1, y1, image=self.img_creep_renard, anchor="nw",tags=("creep",))
                case 3 :
                     self.canevas.create_image(x1, y1, image=self.img_creep_ecur, anchor="nw",tags=("creep",))
                case 4 :
                     self.canevas.create_image(x1, y1, image=self.img_creep_raton, anchor="nw",tags=("creep",))
                case 5 :
                     self.canevas.create_image(x1, y1, image=self.img_creep_por, anchor="nw",tags=("creep",)) 

        # Logique originale pr�serv�e (via nivoActif)
        for i in self.parent.modele.partieCourante.toursEnJeu.values():
            x1 = i.pos[0] * self.coefWidth - 10
            y1 = i.pos[1] * self.coefHeight - 10
            x2 = i.pos[0] * self.coefWidth + 10
            y2 = i.pos[1] * self.coefHeight + 10
            # print("LOCtour",i.pos,x1,y1,x2,y2)
            #self.canevas.create_rectangle(x1, y1, x2, y2, width=1, fill="green", tags=("tour",))            
            self.canevas.create_image(x1, y1, image=self.img_tour_classique, anchor="nw",tags=("tour",)) 

            #def afficher_projectile(self, projectiles):
        if len(self.parent.modele.partieCourante.projectiles) > 0:
            self.canevas.delete("projectile")
            for i in self.parent.modele.partieCourante.projectiles.values():
                x1 = i.x * self.coefWidth - (i.largeur / self.coefWidth)
                x2 = i.x * self.coefWidth + (i.largeur / self.coefWidth)
                y1 = i.y * self.coefHeight - (i.hauteur / self.coefHeight)
                y2 = i.y * self.coefHeight + (i.hauteur / self.coefHeight)
                self.canevas.create_rectangle(x1, y1, x2, y2, fill="yellow", tags=("projectile",))

    def afficheInformationsPartie(self):
        self.canevas.delete("cash")
        self.canevas.delete("vie")
        self.canevas.delete("nivo")
        self.canevas.create_text(600, 10, fill="#FCA510", text= str(self.parent.modele.partieCourante.cash) + "$", font=("Cooper Black", 24), anchor="nw", tags=("cash",))
        self.canevas.create_text(15, 10, fill="#FF0000", text="health: " + str(self.parent.modele.partieCourante.vie), font=("Cooper Black", 24), anchor="nw", tags=("vie",))
        self.canevas.create_text(15, 650, fill="#000000", text="wave: " + str(self.parent.modele.partieCourante.nivo + 1), font=("Cooper Black", 24), anchor="nw", tags=("nivo",))
