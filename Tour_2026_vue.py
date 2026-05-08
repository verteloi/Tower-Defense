# -*- coding: ISO-8859-1 -*-
from tkinter import *
import tkinter as tk

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Tk()
        self.root.title("Tower Defense")
        self.hight = 700
        self.width = 700
        self.coefHeight = self.hight/100
        self.coefWidth = self.width/100
        self.info_effet = tk.StringVar(value="-")
        self.info_prix = tk.StringVar(value="-")
        self.info_degat = tk.StringVar(value="-")
        self.info_vitesse = tk.StringVar(value="-")

        self.tourSelec = 1

        # --- Import des images ---
        try:
            self.img_parcour1 = PhotoImage(file="images\\img_parcour1.png")
            self.img_parcour2 = PhotoImage(file="images\\img_parcour2.png")
            self.img_parcour3 = PhotoImage(file="images\\img_parcour3.png")
            self.img_creep_ours = PhotoImage(file="images\\creep_ours.png")
            self.img_creep_por = PhotoImage(file="images\\creep_porcupine.png")
            self.img_creep_raton = PhotoImage(file="images\\creep_raton.png")
            self.img_creep_renard = PhotoImage(file="images\\creep_renard.png")
            self.img_creep_ecur = PhotoImage(file="images\\creep_squirrel.png")
            self.img_tour_classique = PhotoImage(file="images\\tour_feu.png")
            self.img_tour_bombe = PhotoImage(file="images\\tour_bombe.png")
            self.img_tour_poison = PhotoImage(file="images\\tour_poison.png")
            self.img_tour_glace = PhotoImage(file="images\\tour_glace.png")
            self.img_tour_electrique = PhotoImage(file="images\\tour_electrique.png")
        except Exception as e:
            print(f"Erreur chargement images : {e}")

        # --- Initialisation des Frames ---
        self.frame_demarrage = tk.Frame(self.root, width=self.width, height=self.hight, bg="gray")
        self.frame_menu = tk.Frame(self.root, width=self.width, height=self.hight, bg="lightgray")
        self.frame_jeu = tk.Frame(self.root)
        self.frame_scores = tk.Frame(self.root, width=self.width, height=self.hight, bg="black")
        self.frame_gameover = tk.Frame(self.root, width=self.width, height=self.hight, bg="black")

        self.frames = {
            "demarrage": self.frame_demarrage,
            "menu": self.frame_menu,
            "jeu": self.frame_jeu,
            "scores": self.frame_scores,
            "gameover": self.frame_gameover
        }
        
        self.frame_actuelle = None
        self.afficherEcranDemarrage()

    def changer_frame(self, cle_frame):
        if self.frame_actuelle is not None:
            self.frame_actuelle.pack_forget()
        self.frame_actuelle = self.frames[cle_frame]
        self.frame_actuelle.pack()

    def afficherEcranDemarrage(self):
        self.changer_frame("demarrage")
        if not self.frame_demarrage.winfo_children():
            titre = tk.Label(self.frame_demarrage, text="Tower Defense", font=("Arial", 30))
            titre.pack(pady=50)
            bouton_demarrer = tk.Button(self.frame_demarrage, text="Demarrer", command=self.afficherMenu)
            bouton_demarrer.pack(pady=10)
            bouton_scores = tk.Button(self.frame_demarrage, text="Scores", command=self.afficherScores)
            bouton_scores.pack(pady=10)

    def afficherMenu(self):
        self.changer_frame("menu")
        if not self.frame_menu.winfo_children():
            sidebar_creer = tk.Frame(self.frame_menu, bg="white", width=300, height=self.hight)
            sidebar_creer.pack(side="right", fill="y")


            tk.Label(sidebar_creer, text="MENU", font=("Arial", 18, "bold"), bg="#AAAAAA").pack(pady=10, fill="x")

            tk.Button(sidebar_creer, text="Map 1", command=lambda:self.parent.changerParcour(0)).pack(pady=5, padx=20)
            tk.Button(sidebar_creer, text="Map 2", command=lambda:self.parent.changerParcour(1)).pack(pady=5, padx=20)
            tk.Button(sidebar_creer, text="Map 3", command=lambda:self.parent.changerParcour(2)).pack(pady=5, padx=20)

            tk.Label(sidebar_creer, text="difficulte", font=("Arial", 12, "bold"), bg="#AAAAAA").pack(pady=(20, 0), fill="x")

            diff_frame = tk.Frame(sidebar_creer, bg="white")
            diff_frame.pack(pady=10)

            tk.Button(diff_frame, text="F", bg="lightgreen", command=lambda:self.parent.changerDifficulte(0)).pack(side="left", padx=2)
            tk.Button(diff_frame, text="M", bg="orange", command=lambda:self.parent.changerDifficulte(1)).pack(side="left", padx=2)
            tk.Button(diff_frame, text="D", bg="red", command=lambda:self.parent.changerDifficulte(2)).pack(side="left", padx=2)
            tk.Button(sidebar_creer, text="Jouer", font=("Arial", 14, "bold"), bg="#A0EC2C", command=self.afficherInterfaceJeu).pack(side="bottom", pady=10, padx=10)
            
            conteneurPreviewParcours = tk.Frame(self.frame_menu, bg="gray", width=self.width, height=self.hight)
            conteneurPreviewParcours.pack(side="left", expand=True, fill="both")

            self.previewParcours = tk.Canvas(conteneurPreviewParcours, width=self.width, height=self.hight)
            self.previewParcours.pack(expand=True, fill="both")
            
        self.actualiserPreviewParcour()

    def actualiserPreviewParcour(self):
        self.previewParcours.delete("all")
        choix = self.parent.modele.parcourChoisi
        imgs = {0: self.img_parcour1, 1: self.img_parcour3, 2: self.img_parcour2}
        if choix in imgs:
            self.previewParcours.create_image(0, 0, image=imgs[choix], anchor="nw")

    def actualiser_infos_tour(self, type=1, type_appel="jeu"):
        self.selecTour(type)
        tour = self.parent.modele.partieCourante.tourSelectionne
        if type_appel=="bouton":
            tour = self.parent.modele.partieCourante.toutesLesTours[(type-1)]
        if tour:
            self.info_prix.set(f"Prix: {tour.cout}$")
            self.info_degat.set(f"Degat: {tour.force}")
            self.info_effet.set(f"Effet: {tour.effet}")
            self.info_vitesse.set(f"Vitesse de Tir: {tour.vitesseTir}")
        else:
            self.info_prix.set("Aucune selection")
            self.info_degat.set("-")
            self.info_effet.set("-") 
            self.info_vitesse.set("-")

    def afficherInterfaceJeu(self):
        self.changer_frame("jeu")
        if not self.frame_jeu.winfo_children():
            self.sidebar = tk.Frame(self.frame_jeu, bg="white", width=250, height=self.hight)
            self.sidebar.pack(side="right", fill="y")

            tk.Label(self.sidebar, text="TOURS", font=("Arial", 12, "bold"), bg="#AAAAAA").pack(pady=(10, 0), fill="x")
            
            # Grilles boutiques
            self.panneau_tours_range_1 = tk.Frame(self.sidebar, bg="white", bd=1)
            self.panneau_tours_range_1.pack(pady=5)
            self.panneau_tours_range_2 = tk.Frame(self.sidebar, bg="white", bd=1)
            self.panneau_tours_range_2.pack(pady=5)
            self.panneau_tours_range_3 = tk.Frame(self.sidebar, bg="white", bd=1)
            self.panneau_tours_range_3.pack(pady=5)

            tk.Button(self.panneau_tours_range_1, image=self.img_tour_classique, command=lambda: self.actualiser_infos_tour(1, "bouton"), bd=1).pack(side="right", padx=5)
            tk.Button(self.panneau_tours_range_1, image=self.img_tour_bombe, command=lambda: self.actualiser_infos_tour(2, "bouton"), bd=1).pack(side="left", padx=5)

            tk.Button(self.panneau_tours_range_2, image=self.img_tour_electrique, command=lambda: self.actualiser_infos_tour(3, "bouton"), bd=1).pack(side="right", padx=5)
            tk.Button(self.panneau_tours_range_2, image=self.img_tour_poison, command=lambda: self.actualiser_infos_tour(4, "bouton"), bd=1).pack(side="left", padx=5)

            tk.Button(self.panneau_tours_range_3, image=self.img_tour_glace, command=lambda: self.actualiser_infos_tour(5, "bouton"), bd=1).pack(side="right", padx=5)
        


            # Zone Stats
            self.panneau_stats = tk.Frame(self.sidebar, bg="white")
            self.panneau_stats.pack(pady=10, fill="x")
            tk.Label(self.panneau_stats, text="STATISTIQUES", font=("Arial", 12, "bold"), bg="#AAAAAA").pack(fill="x")
            tk.Label(self.panneau_stats, textvariable=self.info_prix, font=("Arial", 10, "bold")).pack()
            tk.Label(self.panneau_stats, textvariable=self.info_degat, font=("Arial", 10, "bold")).pack()
            tk.Label(self.panneau_stats, textvariable=self.info_effet, font=("Arial", 10, "bold")).pack()
            tk.Label(self.panneau_stats, textvariable=self.info_vitesse, font=("Arial", 10, "bold")).pack()

            # Zone Controles
            self.panneau_actions = tk.Frame(self.sidebar, bg="white")
            self.panneau_actions.pack(side="bottom", pady=20)
            tk.Button(self.panneau_actions, text="Lancer Vague", command=self.parent.demarrePartie).pack(pady=5)
            tk.Button(self.panneau_actions, text="Menu Principal", command=self.afficherMenu).pack(pady=5)

            # Canvas
            self.canevas = tk.Canvas(self.frame_jeu, width=self.width, height=self.hight, bg="black")
            self.canevas.pack(side="left")
            self.canevas.bind("<Button-1>", self.getPosTour)
            # Bind unique ici pour éviter l'empilement
            self.canevas.tag_bind("tour", "<Button-1>", self.clickSurTour)

        self.canevas.delete("all")
        choix = self.parent.modele.parcourChoisi
        imgs = {0: self.img_parcour1, 1: self.img_parcour3, 2: self.img_parcour2}
        if choix in imgs:
            self.canevas.create_image(0, 0, image=imgs[choix], anchor="nw")
        self.parent.modele.demarrePartie()
        self.afficheInformationsPartie()

    def selecTour(self, type):
        self.tourSelec = type

    def afficherScores(self):
        self.changer_frame("scores")
        if not self.frame_scores.winfo_children():
            tk.Label(self.frame_scores, text="SCORES", font=("Arial", 30), fg="white", bg="black").pack(pady=50)
            tk.Button(self.frame_scores, text="Retour", command=self.afficherEcranDemarrage).pack()

    def afficherGameover(self):
        self.changer_frame("gameover")
        
        if not self.frame_gameover.winfo_children():
            tk.Label(self.frame_gameover, text="GAME OVER", font=("Arial", 30), fg="red", bg="black").pack(pady=50)
            tk.Button(self.frame_gameover, text="Menu Principal", command=self.afficherEcranDemarrage).pack(pady=10)
            tk.Button(self.frame_gameover, text="Rejouer", command=self.afficherMenu).pack(pady=10)

    def getPosTour(self, evt):
        item_under_mouse = self.canevas.find_withtag("current")  
        all_tags = self.canevas.gettags(item_under_mouse)
        if "tour" in all_tags:
            return
        x = evt.x / self.coefWidth
        y = evt.y / self.coefHeight
        print("type de tour selec ", self.tourSelec)
        self.parent.setTour([x, y], self.tourSelec)

    def clickSurTour(self, event):
        tour = self.canevas.find_withtag("current")
        all_tags = self.canevas.gettags(tour)
        id_tour = [t for t in all_tags if t not in ["tour", "current"]]
        if id_tour:
            self.parent.modele.partieCourante.tourSelectionne = self.parent.modele.partieCourante.toursEnJeu[id_tour[0]]
            self.actualiser_infos_tour()

    #def clickSurTour(self, event):             -----------------------Celle que Elina avait fait
    #    # get le tag de la tour 
    #    tour = self.canevas.find_withtag("current")
    #    all_tags = self.canevas.gettags(tour)
    #    id_tour = [t for t in all_tags if t != "tour" and t != "current"]

    #    vendre la tour
    #    self.parent.modele.partieCourante.vendreTour(id_tour[0])

    def afficheCreepTourBombe(self):
        self.canevas.delete("creep")
        self.canevas.delete("projectile")
        self.afficherTours()
        if (self.parent.modele.partieCourante.nivoActif.creepsEnCours):
            for i in self.parent.modele.partieCourante.nivoActif.creepsEnCours:
                x1 = i.pos[0] * self.coefWidth - 15
                y1 = i.pos[1] * self.coefHeight - 15
                img_creep = {1: self.img_creep_ours, 2: self.img_creep_renard, 3: self.img_creep_ecur, 4: self.img_creep_raton, 5: self.img_creep_por}
                if i.type in img_creep:
                    self.canevas.create_image(x1, y1, image=img_creep[i.type], anchor="nw", tags=("creep",))
        if len(self.parent.modele.partieCourante.projectiles) > 0:
            for i in self.parent.modele.partieCourante.projectiles.values():
                x1 = i.x * self.coefWidth - (i.largeur / self.coefWidth)
                y1 = i.y * self.coefHeight - (i.hauteur / self.coefHeight)
                x2 = i.x * self.coefWidth + (i.largeur / self.coefWidth)
                y2 = i.y * self.coefHeight + (i.hauteur / self.coefHeight)
                self.canevas.create_rectangle(x1, y1, x2, y2, fill="yellow", tags=("projectile",))

    def afficheInformationsPartie(self):
        self.canevas.delete("info")
        self.canevas.create_text(600, 10, fill="#FCA510", text= str(self.parent.modele.partieCourante.cash) + "$", font=("Cooper Black", 24), anchor="nw", tags=("info",))
        self.canevas.create_text(15, 10, fill="#FF0000", text="health: " + str(self.parent.modele.partieCourante.vie), font=("Cooper Black", 24), anchor="nw", tags=("info",))
        self.canevas.create_text(15, 650, fill="#000000", text="wave: " + str(self.parent.modele.partieCourante.nivo + 1), font=("Cooper Black", 24), anchor="nw", tags=("info",))

    def afficherTours(self):
        self.canevas.delete("tour")
        # Logique originale pr�serv�e (via nivoActif)
        for i in self.parent.modele.partieCourante.toursEnJeu.values():
            x1 = i.pos[0] * self.coefWidth - 10
            y1 = i.pos[1] * self.coefHeight - 10
            x2 = i.pos[0] * self.coefWidth + 10
            y2 = i.pos[1] * self.coefHeight + 10
            # print("LOCtour",i.pos,x1,y1,x2,y2)
            #self.canevas.create_rectangle(x1, y1, x2, y2, width=1, fill="green", tags=("tour",))

        if (self.parent.modele.partieCourante.toursEnJeu):
            for i in self.parent.modele.partieCourante.toursEnJeu.values():
                x1 = i.pos[0] * self.coefWidth - 10
                y1 = i.pos[1] * self.coefHeight - 10
                
                img_tour = {1: self.img_tour_classique, 2: self.img_tour_bombe, 
                             3: self.img_tour_electrique, 4: self.img_tour_poison, 5: self.img_tour_glace}
                
                if i.type in img_tour:
                    self.canevas.create_image(x1-10, y1-10, image=img_tour[i.type], anchor="nw", tags=("tour",i.tag))
            
        self.canevas.tag_bind("tour", "<Button-1>", self.clickSurTour)


    def afficherScores(self):
        self.changer_frame("scores")
        if not self.frame_scores.winfo_children():
            tk.Label(self.frame_scores, text="SCORES", font=("Arial", 30), fg="white", bg="black").pack(pady=50)
            tk.Button(self.frame_scores, text="Retour", command=self.afficherEcranDemarrage).pack()

    def afficherGameover(self):
        self.changer_frame("gameover")
        if not self.frame_gameover.winfo_children():
            tk.Label(self.frame_gameover, text="GAME OVER", font=("Arial", 30), fg="red", bg="black").pack(pady=50)
            tk.Button(self.frame_gameover, text="Menu Principal", command=self.afficherEcranDemarrage).pack(pady=10)
            tk.Button(self.frame_gameover, text="Rejouer", command=self.afficherMenu).pack(pady=10)