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
        self.button = "none"
        self.info_effet = tk.StringVar(value="-")
        self.info_niveau = tk.StringVar(value="-")
        self.info_prix = tk.StringVar(value="-")
        self.info_degat = tk.StringVar(value="-")
        self.info_vitesse = tk.StringVar(value="-")
        self.info_vie = tk.StringVar(value="Vie: -")
        self.info_argent = tk.StringVar(value="Argent: -")
        self.info_vague = tk.StringVar(value="Vague: -")
        self.info_vente = tk.StringVar(value="-")
        self.map_selectionne = tk.StringVar(value="-")
        self.argent_depart = tk.StringVar(value="-")
        self.force_creep = tk.StringVar(value="-")
        self.vie_creep = tk.StringVar(value="-")

        self.tourSelec = 1
        self.zoneSelec = -1
        self.zonesTours = {}

        # --- Import des images ---
        try:
            #parcours
            self.img_parcour1 = PhotoImage(file="images\\img_parcour1.png")
            self.img_parcour2 = PhotoImage(file="images\\img_parcour2.png")
            self.img_parcour3 = PhotoImage(file="images\\img_parcour3.png")
            #creeps
            self.img_creep_ours = PhotoImage(file="images\\creep_ours.png")
            self.img_creep_por = PhotoImage(file="images\\creep_porcupine.png")
            self.img_creep_raton = PhotoImage(file="images\\creep_raton.png")
            self.img_creep_renard = PhotoImage(file="images\\creep_renard.png")
            self.img_creep_ecur = PhotoImage(file="images\\creep_squirrel.png")
            self.img_creep_ours_empoisone = PhotoImage(file="images\\creep_ours_empoisone.png")
            self.img_creep_por_empoisone = PhotoImage(file="images\\creep_porcupine_empoisone.png")
            self.img_creep_raton_empoisone = PhotoImage(file="images\\creep_raton_empoisone.png")
            self.img_creep_renard_empoisone = PhotoImage(file="images\\creep_renard_empoisone.png")
            self.img_creep_ecur_empoisone = PhotoImage(file="images\\creep_squirrel_empoisone.png")
            self.img_creep_ours_glace = PhotoImage(file="images\\creep_ours_frozen.png")
            self.img_creep_por_glace = PhotoImage(file="images\\creep_porcupine_frozen.png")
            self.img_creep_raton_glace = PhotoImage(file="images\\creep_raton_frozen.png")
            #self.img_creep_renard_glace = PhotoImage(file="images\\creep_renard_frozen.png")
            #self.img_creep_ecur_glace = PhotoImage(file="images\\creep_squirrel_frozen.png")
            #tours
            self.img_tour_classique = PhotoImage(file="images\\tour_feu.png")
            self.img_tour_bombe = PhotoImage(file="images\\tour_bombe.png")
            self.img_tour_poison = PhotoImage(file="images\\tour_poison.png")
            self.img_tour_glace = PhotoImage(file="images\\tour_glace.png")
            self.img_tour_electrique = PhotoImage(file="images\\tour_electrique.png")
            #config
            self.img_bg = tk.PhotoImage(file="images\\bg.png")
            self.img_title = tk.PhotoImage(file="images\\title.png")
            self.img_scores = tk.PhotoImage(file="images\\score.png")
            self.img_play = tk.PhotoImage(file="images\\play.png")
            self.img_game_play_button = tk.PhotoImage(file="images\\playbutton.png")
            self.img_pause = tk.PhotoImage(file="images\\pausebutton.png")
            self.img_speedup = tk.PhotoImage(file="images\\speedupbutton.png")
            self.img_speeddown = tk.PhotoImage(file="images\\speeddownbutton.png")
            
        except Exception as e:
            print(f"Erreur chargement images : {e}")

        # --- initialisation des frames ---
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

    def resetPartie(self):
        pass
    def reset(self):
        self.parent.modele.partieCourante = None
        self.tourSelec = 1
        self.zoneSelec = -1
        self.zonesTours = {}
        self.parent.actif = 0

    def afficherEcranDemarrage(self):
        self.changer_frame("demarrage")
        self.reset()
        if not self.frame_demarrage.winfo_children():
            self.canevas_menu = tk.Canvas(self.frame_demarrage, width=self.width, height=self.hight, highlightthickness=0)
            self.canevas_menu.pack()

            self.canevas_menu.create_image(self.width/2, self.hight/2, image=self.img_bg)
            self.canevas_menu.create_image(self.width/2, self.hight/4 - 30, image=self.img_title)

            btn_play = self.canevas_menu.create_image(self.width/2, self.hight/2 + 35, image=self.img_play); 
            self.canevas_menu.tag_bind(btn_play, "<Button-1>", lambda event:self.afficherMenu())

            btn_score = self.canevas_menu.create_image(self.width/2, self.hight/2 + 200, image=self.img_scores); 
            self.canevas_menu.tag_bind(btn_score, "<Button-1>", lambda event:self.afficherScores())

    def afficherMenu(self):
        self.reset()
        self.changer_frame("menu")
        if not self.frame_menu.winfo_children():

            self.sidebartopmenu = tk.Frame(self.frame_menu, bg="#4a3222", height=40, highlightbackground="black", highlightthickness=1)
            self.sidebartopmenu.pack(side="top", fill="x")

            sidebar_creer = tk.Frame(self.frame_menu, bg="#6f4e37", highlightbackground="black", highlightthickness=1)
            sidebar_creer.pack(side="right", fill="y")

            tk.Label(sidebar_creer, text="Options", font=("Arial", 14, "bold"), bg="#4a3222", fg="white", bd=2, pady=3, padx=10, relief="raised").pack(pady=(15, 5), padx=25)

            map_frame = tk.Frame(sidebar_creer, bg="#6f4e37", highlightbackground="black", highlightthickness=1)
            map_frame.pack(pady=20)

            tk.Label(map_frame, text="Choisir Carte", font=("Arial", 11, "bold"), bg="#4a3222", fg="white", padx=12).pack(fill="x")
            tk.Button(map_frame, text="Map 1", bg="#4a3222", fg="white", font=("Arial", 10, "bold"), command=lambda:self.parent.changerParcour(0)).pack(pady=5)
            tk.Button(map_frame, text="Map 2", bg="#4a3222", fg="white", font=("Arial", 10, "bold"), command=lambda:self.parent.changerParcour(1)).pack(pady=5)
            tk.Button(map_frame, text="Map 3", bg="#4a3222", fg="white", font=("Arial", 10, "bold"), command=lambda:self.parent.changerParcour(2)).pack(pady=5)

            diff_frame = tk.Frame(sidebar_creer, bg="#6f4e37", highlightbackground="black", highlightthickness=1)
            diff_frame.pack(pady=10)

            tk.Label(diff_frame, text="Choisir Difficulte", font=("Arial", 11, "bold"), bg="#4a3222", fg="white").pack(fill="x")
            tk.Button(diff_frame, text="Facile", bg="green", fg="white", font=("Arial", 10, "bold"), command=lambda:self.parent.changerDifficulte(0)).pack(side="top", pady=5)
            tk.Button(diff_frame, text="Moyen", bg="orange", fg="white", font=("Arial", 10, "bold"), command=lambda:self.parent.changerDifficulte(1)).pack(side="top", pady=5)
            tk.Button(diff_frame, text="Difficile", bg="red", fg="white", font=("Arial", 10, "bold"),command=lambda:self.parent.changerDifficulte(2)).pack(side="top", pady=5)

            info_frame = tk.Frame(sidebar_creer, bg="#6f4e37", highlightbackground="black", highlightthickness=1)
            info_frame.pack(pady=10)

            tk.Label(info_frame, text="Config. Partie", font=("Arial", 11, "bold"), bg="#4a3222", fg="white").pack(fill="x")
            tk.Label(info_frame, textvariable=self.map_selectionne, bg="#6f4e37", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
            tk.Label(info_frame, textvariable=self.argent_depart, bg="#6f4e37", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
            tk.Label(info_frame, textvariable=self.force_creep, bg="#6f4e37", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
            tk.Label(info_frame, textvariable=self.vie_creep, bg="#6f4e37", fg="white", font=("Arial", 10, "bold")).pack(pady=2)

            tk.Button(sidebar_creer, text="Jouer", font=("Arial", 14, "bold"), fg="white", bg="green", command=self.afficherInterfaceJeu).pack(side="top", pady=(20,30), padx=10)
            
            conteneurPreviewParcours = tk.Frame(self.frame_menu, bg="#6f4e37", width=self.width, height=self.hight)
            conteneurPreviewParcours.pack(side="left", expand=True, fill="both")

            self.previewParcours = tk.Canvas(conteneurPreviewParcours, width=self.width, height=self.hight, highlightbackground="black", highlightthickness=3)
            self.previewParcours.pack(expand=True, fill="both")
            
        self.actualiserPreviewParcour()

    def actualiserPreviewParcour(self):
        self.previewParcours.delete("all")
        choix = self.parent.modele.parcourChoisi
        imgs = {0: self.img_parcour1, 1: self.img_parcour3, 2: self.img_parcour2}
        if choix in imgs:
            self.previewParcours.create_image(0, 0, image=imgs[choix], anchor="nw")

    def actualiser_info_difficulte(self):
        self.map_selectionne.set(f"Map: {self.parent.modele.parcourChoisi + 1}")
        self.argent_depart.set(f"Argent: {self.parent.modele.tempArgent}$")
        self.force_creep.set(f"Vie: {self.parent.modele.tempVie}")
        self.vie_creep.set(f"Force Creep: {self.parent.modele.difficulteMultiplicateur}x")

    def actualiser_infos_tour(self, type=1, type_appel="jeu"):
        tour = self.parent.modele.partieCourante.tourSelectionne
        if type_appel=="bouton":
            self.selecTour(type)
            tour = self.parent.modele.partieCourante.toutesLesTours[(type-1)]
            self.disableBoutonsVendreAmeliorer()
        if tour:
            self.info_prix.set(f"Prix: {tour.cout}$")
            self.info_degat.set(f"Degat: {tour.force}")     
            self.info_niveau.set(f"Niveau: {tour.niveau}") 
            self.info_vitesse.set(f"Vitesse de Tir: {tour.vitesseTir}")
            self.info_effet.set(f"Effet: {tour.effet}")  
            self.info_vente.set(tour.resellValue)
        else:
            self.info_prix.set("-")
            self.info_vente.set("-")
            self.info_degat.set("-")
            self.info_effet.set("-") 
            self.info_niveau.set("-") 
            self.info_vitesse.set("-")

    def afficherInterfaceJeu(self):
        self.changer_frame("jeu")
        if not self.frame_jeu.winfo_children():
            # --- ZONE DU HAUT ---
            self.sidebartop = tk.Frame(self.frame_jeu, bg="#4a3222", height=60, highlightbackground="black", highlightthickness=2)
            self.sidebartop.pack(side="top", fill="x")
            
            tk.Label(self.sidebartop, textvariable=self.info_vie, fg="#ff4d4d", bg="#4a3222", font=("Cooper Black", 22)).pack(side="left", padx=20)
            tk.Label(self.sidebartop, textvariable=self.info_argent, fg="#FCA510", bg="#4a3222", font=("Cooper Black", 22)).pack(side="left", padx=20)
            tk.Label(self.sidebartop, textvariable=self.info_vague, fg="white", bg="#4a3222", font=("Cooper Black", 22)).pack(side="left", padx=20)

            tk.Button(self.sidebartop, image=self.img_speedup, bg="#4a3222", borderwidth=0, highlightthickness=0, command=lambda: self.changer_etat_partie("speedup")).pack(side="right", padx=2)
            tk.Button(self.sidebartop, image=self.img_game_play_button, bg="#4a3222", borderwidth=0, highlightthickness=0, command=lambda: self.changer_etat_partie("play")).pack(side="right", padx=2)
            tk.Button(self.sidebartop, image=self.img_pause, bg="#4a3222", borderwidth=0, highlightthickness=0, command=lambda: self.changer_etat_partie("pause")).pack(side="right", padx=2)
            tk.Button(self.sidebartop, image=self.img_speeddown, bg="#4a3222", borderwidth=0, highlightthickness=0, command=lambda: self.changer_etat_partie("speeddown")).pack(side="right", padx=2)


            # --- SIDEBAR DROITE ---
            self.sidebar = tk.Frame(self.frame_jeu, bg="#6f4e37", width=250, highlightbackground="black", highlightthickness=2)
            self.sidebar.pack(side="right", fill="y")

            # BOUTIQUE DE TOURS

            tk.Label(self.sidebar, text="BOUTIQUE", font=("Arial", 14, "bold"), bg="#4a3222", fg="white", bd=2, relief="raised").pack(pady=5, fill="x")
            
            self.panneau_tours_range_1 = tk.Frame(self.sidebar, bg="#6f4e37")
            self.panneau_tours_range_1.pack(pady=5)
            self.panneau_tours_range_2 = tk.Frame(self.sidebar, bg="#6f4e37")
            self.panneau_tours_range_2.pack(pady=5)
            self.panneau_tours_range_3 = tk.Frame(self.sidebar, bg="#6f4e37")
            self.panneau_tours_range_3.pack(pady=5)

            tk.Button(self.panneau_tours_range_1, image=self.img_tour_classique, bg="#8b5a2b", activebackground="#a0522d", command=lambda: self.actualiser_infos_tour(1, "bouton"), bd=3, relief="ridge").pack(side="right", padx=5)
            tk.Button(self.panneau_tours_range_1, image=self.img_tour_bombe, bg="#8b5a2b", activebackground="#a0522d", command=lambda: self.actualiser_infos_tour(2, "bouton"), bd=3, relief="ridge").pack(side="left", padx=5)

            tk.Button(self.panneau_tours_range_2, image=self.img_tour_electrique, bg="#8b5a2b", activebackground="#a0522d", command=lambda: self.actualiser_infos_tour(3, "bouton"), bd=3, relief="ridge").pack(side="right", padx=5)
            tk.Button(self.panneau_tours_range_2, image=self.img_tour_poison, bg="#8b5a2b", activebackground="#a0522d", command=lambda: self.actualiser_infos_tour(4, "bouton"), bd=3, relief="ridge").pack(side="left", padx=5)

            tk.Button(self.panneau_tours_range_3, image=self.img_tour_glace, bg="#8b5a2b", activebackground="#a0522d", command=lambda: self.actualiser_infos_tour(5, "bouton"), bd=3, relief="ridge").pack(side="right", padx=5)

            # STATITSIQUE DE LA TOUR SELECTIONNER

            self.panneau_stats = tk.Frame(self.sidebar, bg="#6f4e37", highlightbackground="black", highlightthickness=1)
            self.panneau_stats.pack(pady=10, padx=10, fill="x")
            
            tk.Label(self.panneau_stats, text="STATISTIQUES", font=("Arial", 11, "bold"), bg="#4a3222", fg="white").pack(fill="x")
            tk.Label(self.panneau_stats, textvariable=self.info_prix, bg="#6f4e37", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
            tk.Label(self.panneau_stats, textvariable=self.info_degat, bg="#6f4e37", fg="#e0e0e0", font=("Arial", 10)).pack()
            tk.Label(self.panneau_stats, textvariable=self.info_niveau, bg="#6f4e37", fg="#e0e0e0", font=("Arial", 10)).pack(pady=1)
            tk.Label(self.panneau_stats, textvariable=self.info_vitesse, bg="#6f4e37", fg="#e0e0e0", font=("Arial", 10)).pack(pady=(0, 5))
            tk.Label(self.panneau_stats, textvariable=self.info_effet, bg="#6f4e37", fg="#e0e0e0", font=("Arial", 10)).pack()

            self.panneau_actions_tours = tk.Frame(self.sidebar, bg="#6f4e37", highlightbackground="black", highlightthickness=1)
            self.panneau_actions_tours.pack(pady=10, padx=10, fill="x")

            # ACTIONS POUR TOURS 
            tk.Label(self.panneau_actions_tours, text="ACTIONS", font=("Arial", 11, "bold"), bg="#4a3222", fg="white").pack(fill="x")

            tk.Label(self.panneau_actions_tours, text="Upgrade", bg="#6f4e37", fg="white", font=("Arial", 10, "bold")).pack(pady=2)
            self.boutonAmeliorer = tk.Button(self.panneau_actions_tours, textvariable=self.info_prix, command=lambda: self.parent.modele.partieCourante.ameliorerTour(self.parent.modele.partieCourante.tourSelectionne.tag), bg="#177245", fg="white", font=("Arial", 10, "bold"),state="disabled", width=10, bd=3)
            self.boutonAmeliorer.pack(pady=5)
            
            tk.Label(self.panneau_actions_tours, text="Sell", bg="#6f4e37", fg="#e0e0e0", font=("Arial", 10, "bold")).pack()
            self.boutonVente = tk.Button(self.panneau_actions_tours, textvariable=self.info_vente, command=lambda: self.parent.modele.partieCourante.vendreTour(self.parent.modele.partieCourante.tourSelectionne.tag), bg="#ff4d4d", fg="white", font=("Arial", 10, "bold"), state="disabled", width=10, bd=3)
            self.boutonVente.pack(pady=5)

            self.panneau_actions = tk.Frame(self.sidebar, bg="#6f4e37")
            self.panneau_actions.pack(side="bottom", pady=20)
            
            # ACTION PARTIE (LANCER VAGUE ET MENU)
            
            self.boutonLancerVague = tk.Button(self.panneau_actions, text="Lancer Vague", command=self.parent.demarrePartie, bg="grey", fg="white", font=("Arial", 10, "bold"), width=15, bd=3)
            self.boutonLancerVague.pack(pady=5)
            tk.Button(self.panneau_actions, text="Menu Principal", command=self.afficherMenu, bg="grey", fg="white", font=("Arial", 10, "bold"), width=15, bd=3).pack(pady=5)

            self.canevas = tk.Canvas(self.frame_jeu, width=self.width, height=self.hight, bg="black", highlightbackground="black", highlightthickness=2)
            self.canevas.pack(side="left")
            self.canevas.bind("<Button-1>", self.getPosTour)
            self.canevas.tag_bind("tour", "<Button-1>", self.clickSurTour)

        self.boutonLancerVague.config(state="normal")
        self.canevas.delete("all")
        choix = self.parent.modele.parcourChoisi
        imgs = {0: self.img_parcour1, 1: self.img_parcour3, 2: self.img_parcour2}
        if choix in imgs:
            self.canevas.create_image(0, 0, image=imgs[choix], anchor="nw")
        self.parent.modele.demarrePartie()
        self.afficheNoeudsTours()
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
        if "zoneTour" in all_tags:   
            id_zone = [t for t in all_tags if t not in ["zoneTour", "current"]]
            if id_zone and self.tourSelec:                   
                self.zoneSelec = int(id_zone[0])
                pos = self.parent.modele.partieCourante.parcourChoisi.noeudsTours[self.zoneSelec]
                self.parent.modele.partieCourante.tourSelectionne = self.parent.setTour(pos, self.tourSelec)
                self.zonesTours[self.parent.modele.partieCourante.tourSelectionne] = self.zoneSelec
                self.ableBoutonsVendreAmeliorer()
        elif "tour" in all_tags:
            self.ableBoutonsVendreAmeliorer()
            self.clickSurTour(evt)
        else:
            print("apuye ailleurs")
            self.zoneSelec = -1
            self.selecTour(0)
            self.parent.modele.partieCourante.tourSelectionne = None
            self.disableBoutonsVendreAmeliorer()
        self.afficheNoeudsTours()
        self.afficherTours()
        self.actualiser_infos_tour()
    
    def clickSurTour(self, event):
        tour = self.canevas.find_withtag("current")
        all_tags = self.canevas.gettags(tour)
        id_tour = [t for t in all_tags if t not in ["tour", "current"]]
        if id_tour:
            self.parent.modele.partieCourante.tourSelectionne = self.parent.modele.partieCourante.toursEnJeu[id_tour[0]]
            self.zoneSelec = self.zonesTours[self.parent.modele.partieCourante.tourSelectionne]
            

    def afficheCreepTourBombe(self):
        self.canevas.delete("creep")
        self.canevas.delete("projectile")
        self.afficherTours()
        #afficher creeps
        if(self.parent.modele.partieCourante.nivoActif):
            if (self.parent.modele.partieCourante.nivoActif.creepsEnCours):
                for i in self.parent.modele.partieCourante.nivoActif.creepsEnCours:
                    
                    x1 = i.pos[0] * self.coefWidth - 15
                    y1 = i.pos[1] * self.coefHeight - 15
                    if i.empoisone:
                        img_creep = {1: self.img_creep_ours_empoisone, 2: self.img_creep_renard_empoisone, 3: self.img_creep_ecur_empoisone, 4: self.img_creep_raton_empoisone, 5: self.img_creep_por_empoisone}
                    elif i.glace: #manquent images pour ecureuil et renard
                        img_creep = {1: self.img_creep_ours_glace, 2: self.img_creep_renard, 3: self.img_creep_ecur, 4: self.img_creep_raton_glace, 5: self.img_creep_por_glace}
                    else:
                        img_creep = {1: self.img_creep_ours, 2: self.img_creep_renard, 3: self.img_creep_ecur, 4: self.img_creep_raton, 5: self.img_creep_por}
                    if i.type in img_creep:
                        self.canevas.create_image(x1, y1, image=img_creep[i.type], anchor="nw", tags=("creep",))

        #afficher projectiles
        if len(self.parent.modele.partieCourante.projectiles) > 0:
            for i in self.parent.modele.partieCourante.projectiles.values():
                x1 = i.x * self.coefWidth - (i.largeur / self.coefWidth)
                y1 = i.y * self.coefHeight - (i.hauteur / self.coefHeight)
                x2 = i.x * self.coefWidth + (i.largeur / self.coefWidth)
                y2 = i.y * self.coefHeight + (i.hauteur / self.coefHeight)
                type_projectile = {1: "OrangeRed2", 2: "black", 3: "deep sky blue", 4: "green", 5: "powder blue"}
                if i.type in type_projectile:
                    self.canevas.create_oval(x1, y1, x2, y2, fill=type_projectile[i.type], tags=("projectile"))

    def afficheNoeudsTours(self):
        i=0
        self.canevas.delete("zoneSelec")
        for tuple in self.parent.modele.partieCourante.parcourChoisi.noeudsTours:
            if i == self.zoneSelec:
                self.canevas.create_rectangle((tuple[0]* self.coefWidth)-8, (tuple[1]* self.coefHeight)-8, ((tuple[0]+5)* self.coefWidth)+8, ((tuple[1]+5)* self.coefHeight)+8, fill="#a0522d", tags=("zoneSelec"))
            else :
                self.canevas.create_rectangle(tuple[0]* self.coefWidth, tuple[1]* self.coefHeight, (tuple[0]+5)* self.coefWidth, (tuple[1]+5)* self.coefHeight, fill="#CC9767", tags=("zoneTour",i))
            i=i+1

    def afficheInformationsPartie(self):
        partie = self.parent.modele.partieCourante
        self.info_vie.set(f"{partie.vie} hp")
        self.info_argent.set(f"{partie.cash}$")
        self.info_vague.set(f"{partie.nivo} / 10")
        
    def afficherTours(self):
        self.canevas.delete("tour")
        if (self.parent.modele.partieCourante.toursEnJeu):
            for i in self.parent.modele.partieCourante.toursEnJeu.values():
                x1 = i.pos[0] * self.coefWidth - 10
                y1 = i.pos[1] * self.coefHeight - 10
                
                img_tour = {1: self.img_tour_classique, 2: self.img_tour_bombe, 
                             3: self.img_tour_electrique, 4: self.img_tour_poison, 5: self.img_tour_glace}
                
                if i.type in img_tour:
                    self.canevas.create_image(x1+8, y1+6, image=img_tour[i.type], anchor="nw", tags=("tour",i.tag))
            
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

    def demarrerPartie(self):
        self.afficheCreepTourBombe()
        self.afficheInformationsPartie()
        self.disableBoutonsVendreAmeliorer()
        self.boutonLancerVague.config(state="disabled")

    def disableBoutonsVendreAmeliorer(self):
        self.boutonVente.config(state="disabled")
        self.boutonAmeliorer.config(state="disabled")

    def ableBoutonsVendreAmeliorer(self):
        self.boutonVente.config(state="normal")
        self.boutonAmeliorer.config(state="normal")

    def changer_etat_partie(self, button):
        match button:
            case "play":
                if (not self.parent.actif):
                    self.parent.actif = 1
                    self.parent.continuePartie()
            case "pause":
                self.parent.actif = 0
            case "speedup":
                if (self.parent.delai > 2):
                    self.parent.delai -= 10
            case "speeddown":
                if (self.parent.delai < 50):
                    self.parent.delai += 10
