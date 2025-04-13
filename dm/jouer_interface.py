from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,QPushButton
from PyQt5.QtCore import  QTimer
from PyQt5.QtGui import  QIcon
import numpy as np
import random
from joueur_robot import Joueur,Robot

class Carte:
    def __init__(self, nom, image):
        self.nom = nom
        self.image = image
        self.est_retournee = False
        
    def retourner(self):
        self.est_retournee = not self.est_retournee
    def __str__(self):
        return f"{self.nom}"

liste_nom_image = [
    ("image_1", "images/1.png"),
    ("image_2", "images/2.png"),
    ("image_3", "images/3.png"),
    ("image_4", "images/4.png"),
    ("image_5", "images/5.png"),
    ("image_6", "images/6.png"),
    ("image_7", "images/7.png"),
    ("image_9", "images/9.png"),
    ("image_10", "images/10.png"),
    ("image_11", "images/11.png"),
    ("image_12", "images/12.png"),
    ("image_13", "images/13.png"),
    ("image_14", "images/14.png"),
    ("image_15", "images/15.png"),
    ("image_16", "images/16.png"),
    ("image_17", "images/17.png"),
    ("image_18", "images/18.png"),
    ("image_19", "images/19.png"),
    ("image_20", "images/20.png"),
    ("image_21", "images/21.png"),
    ("image_22", "images/22.png"),
    ("image_23", "images/23.png"),
    ("image_24", "images/24.png")
]



class FenetreJeu(QWidget):
    def __init__(self,interface4):
        super().__init__()
        self.interface4=interface4
        # Liste des couleurs pour les joueurs
        self.couleurs = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        
        # Liste des joueurs 
        self.joueurs = []
        
        # Liste des cartes
        self.cartes = []
        
        # Variables pour le jeu
        self.cartes_retournees = []  # Liste des cartes actuellement retournées
        self.joueur_actuel = 0       # Index du joueur actuel
        self.en_attente = False      # Pour empêcher de retourner plus de 2 cartes
        
        self.main_layout = QVBoxLayout()
        self.joueur_layout = QHBoxLayout()
        self.carte_layout = QGridLayout()
        
        # Bouton paramètres
        self.btn_retour = QPushButton("⬅")
        self.btn_retour.setFixedSize(40, 40)
        self.btn_retour.clicked.connect(self.retour)
        self.main_layout.addWidget(self.btn_retour)
        
        
        # Ajout des éléments au layout principal
        self.main_layout.addLayout(self.joueur_layout)
        self.main_layout.addLayout(self.carte_layout)
        self.setLayout(self.main_layout)
    def retour(self):
        self.parentWidget().setCurrentIndex(2)
    
    def creer_cartes(self, nombre_cartes):
        """Crée et affiche les cartes sur l'interface"""
        # Nettoyer le layout existant plus efficacement
        while self.carte_layout.count():
            item = self.carte_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Créer les cartes
        self.cartes = []
        cartes_a_creer = nombre_cartes // 2  # On crée des paires de cartes
        for i in range(cartes_a_creer):
            nom, image = liste_nom_image[i]
            # Créer deux cartes identiques
            carte1 = Carte(nom, image)
            carte2 = Carte(nom, image)
            self.cartes.extend([carte1, carte2])
        
        # Mélanger les cartes
        random.shuffle(self.cartes)
        
        # Calculer la disposition en grille
        nb_colonnes = int(np.ceil(np.sqrt(nombre_cartes)))
        nb_lignes = int(np.ceil(nombre_cartes / nb_colonnes))
        
        # Définir une taille fixe pour les boutons ou utiliser des proportions plus stables
        taille_disponible = min(self.parentWidget().width(), self.parentWidget().height() - 150)
        taille_bouton = min(
            (taille_disponible - 20) // nb_colonnes,
            (taille_disponible - 20) // nb_lignes
        )
        
        # Limiter la taille du bouton à une valeur raisonnable
        taille_bouton = min(taille_bouton, 100)  # Par exemple, maximum 100px
        
        # Réduire l'espacement entre les cartes
        self.carte_layout.setSpacing(5)
        
        # Afficher les cartes
        for i, carte in enumerate(self.cartes):
            btn = QPushButton()
            btn.setFixedSize(taille_bouton, taille_bouton)
            btn.setStyleSheet("background-color: #2C3E50; border-radius: 10px;")
            btn.clicked.connect(lambda checked, c=carte, b=btn: self.retourner_carte(c, b))
            self.carte_layout.addWidget(btn, i // nb_colonnes, i % nb_colonnes)
    
    def retourner_carte(self, carte, bouton):
        """Retourne une carte lorsqu'on clique dessus"""
        if self.en_attente or carte.est_retournee : #empeche de retourner plus de 2 cartes ou une carte déjà retournée 
            return
            
        carte.retourner()
        self.cartes_retournees.append((carte, bouton)) #ajoute les cartes à une liste
        
        # Afficher le nom de la carte
        icon = QIcon(carte.image)
        bouton.setIcon(icon)
        bouton.setIconSize(bouton.size())
        bouton.setStyleSheet("background-color: white; border-radius: 10px;")
        
        # Mémoriser la carte pour tous les robots
        for joueur in self.joueurs:
            if isinstance(joueur, Robot):
                joueur.memoriser_carte(carte)
        
        if len(self.cartes_retournees) == 2: #on attends d'avoir 2 cartes retournées
            self.en_attente = True
            self.verifier_paire()
    def verifier_paire(self):
        """Vérifie si les deux cartes retournées forment une paire"""
        carte1, bouton1 = self.cartes_retournees[0]
        carte2, bouton2 = self.cartes_retournees[1]
        
        if carte1.nom == carte2.nom:
            # Paire trouvée
            self.joueurs[self.joueur_actuel].update_score(self.joueurs[self.joueur_actuel].score + 1)
            # Les cartes restent retournées
            self.cartes_retournees = [] #on remets la liste des cartes retournées à 0
            self.en_attente = False
            # Vérifier si la partie est terminée
            bool=self.verifier_fin_partie()
            if isinstance(self.joueurs[self.joueur_actuel], Robot) and bool==False: #le robot rejoue si c'est son tour et que la partie n'est pas terminé
                QTimer.singleShot(1000, self.faire_jouer_robot)
        else:
            # Sinon on retourne les cartes après un délai
            QTimer.singleShot(1000, self.retourner_cartes)
    
    def retourner_cartes(self):
        """Retourne les cartes qui ne forment pas une paire"""
        for carte, bouton in self.cartes_retournees:
            carte.retourner()
            bouton.setIcon(QIcon())
            bouton.setStyleSheet("background-color: #2C3E50; border-radius: 10px;")
        
        self.cartes_retournees = []#on remets la liste des cartes retournées à 0
        self.en_attente = False
        
        # Passer au joueur suivant
        self.joueur_actuel = (self.joueur_actuel + 1) % len(self.joueurs)
        
        # Si c'est le tour d'un robot, le faire jouer
        if isinstance(self.joueurs[self.joueur_actuel], Robot):
            QTimer.singleShot(1000, self.faire_jouer_robot)
    
    def faire_jouer_robot(self):
        """Fait jouer le robot actuel"""
        if self.en_attente :
            return
        
        robot = self.joueurs[self.joueur_actuel]
        carte1, carte2 = robot.choisir_carte(self.cartes)
        
        # Retourner la première carte
        bouton1 = self.carte_layout.itemAt(self.cartes.index(carte1)).widget() # on recupere le bouton associé à la carte
        self.retourner_carte(carte1, bouton1)
        
        # Retourner la deuxième carte après un court délai
        QTimer.singleShot(1000, lambda: self.retourner_carte(carte2, self.carte_layout.itemAt(self.cartes.index(carte2)).widget()))
        
    
    def verifier_fin_partie(self):
        """Vérifie si toutes les cartes sont retournées"""
        if all(carte.est_retournee for carte in self.cartes):
            self.afficher_gagnant()
            return True
        return False
    
    def afficher_gagnant(self):
        global message
        """Affiche le gagnant et propose de rejouer ou d'aller à l'accueil"""
        # Trouver le joueur avec le score le plus élevé
        scores = [joueur.score for joueur in self.joueurs]
        score_max = max(scores)
        gagnants = [joueur for joueur in self.joueurs if joueur.score == score_max]
        
        # Créer le message
        if len(gagnants) == 1:
            message = f"Félicitations {gagnants[0].nom} ! Vous avez gagné avec {score_max} points !"
        else:
            noms_gagnants = ", ".join(j.nom for j in gagnants)
            message = f"Égalité entre {noms_gagnants} avec {score_max} points !"
        self.interface4.definir_gagnant(message)
        self.parentWidget().setCurrentIndex(4)
    
    def reinitialiser_jeu(self):
        """Réinitialise le jeu pour une nouvelle partie""" ##################################### retour aux options
        # Réinitialiser les scores
        for joueur in self.joueurs:
            joueur.update_score(0)
        
        # Réinitialiser les cartes
        self.creer_cartes(len(self.cartes))
        
        # Réinitialiser les variables de jeu
        self.cartes_retournees = []
        self.joueur_actuel = 0
        self.en_attente = False
    
    
    
    def ajouter_joueurs(self, noms_joueurs, robots=None):    
        # Nettoyer le layout existant
        for i in range(self.joueur_layout.count()): # on supprime les joueurs de l'ancienne partie 
            self.joueur_layout.itemAt(0).widget().setParent(None)
        
        # Créer et ajouter les nouveaux joueurs
        self.joueurs = []
        total_joueurs = 0
        
        # Ajouter les joueurs 
        for i, nom in enumerate(noms_joueurs):
            if total_joueurs < 4:  # Maximum 4 joueurs
                joueur = Joueur(nom, self.couleurs[total_joueurs])
                self.joueurs.append(joueur)
                self.joueur_layout.addWidget(joueur)
                total_joueurs += 1
        
        # Ajouter les robots
        if robots:
            for nom, difficulte in robots:
                if total_joueurs < 4:  # Maximum 4 joueurs
                    robot = Robot(nom, difficulte, self.couleurs[total_joueurs])
                    self.joueurs.append(robot)
                    self.joueur_layout.addWidget(robot)
                    total_joueurs += 1