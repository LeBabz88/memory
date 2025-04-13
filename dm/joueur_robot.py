from PyQt5.QtWidgets import  QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
import random
class Joueur(QFrame):
    def __init__(self, nom, couleur):
        super().__init__()
        self.nom = nom
        self.score = 0
        self.setStyleSheet(f"background-color: {couleur}; border-radius: 10px;") #mettre un cadre de couleur en fond 
        self.setMinimumSize(150, 100)
        self.setMaximumSize(400, 140)
        
        # Layout pour le joueur
        layout = QVBoxLayout()
        
        # Label pour le nom
        self.nom_label = QLabel(nom)
        self.nom_label.setStyleSheet("color: white; font-size: 14px;")
        self.nom_label.setAlignment(Qt.AlignCenter)
        
        # Label pour le score
        self.score_label = QLabel(f"Score: {self.score}")
        self.score_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.score_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.nom_label)
        layout.addWidget(self.score_label)
        self.setLayout(layout)
    
    def update_score(self, nouveau_score):
        self.score = nouveau_score
        self.score_label.setText(f"Score: {self.score}")

class Robot(Joueur):
    def __init__(self, nom,difficulte, couleur):
        super().__init__(nom, couleur)
        self.cartes_memorisees = {}  # Dictionnaire pour mémoriser les cartes vues {"zebre":[Carte(),Carte()]}
        self.difficulte = 100//difficulte #difficulte definie le pourcentage de reusite pour reunir 2 cartes  connues
        # Initialisation du dictionnaire avec les noms des cartes comme clés
        for i in range(23): #on prends toute la liste mais on pourrait recupérer le nombre de carte dans les boutons
            self.cartes_memorisees[liste_nom_image[i][0]] = []  # On utilise le nom de la carte comme clé
        
    def memoriser_carte(self, carte):
        """Mémorise une carte à une position donnée"""
        if carte not in self.cartes_memorisees[carte.nom] and random.randint(0,100)<=self.difficulte:
            self.cartes_memorisees[carte.nom].append(carte)
            print(self.cartes_memorisees)
            return True
        return False
        
    def choisir_carte(self,liste):
        """Choisit une carte à retourner de façon stratégique"""
        nbr_carte = len(liste)  # Utiliser la longueur de la liste des cartes
        for i,j in self.cartes_memorisees.items():
            if len(j)==2 and j[1].est_retournee==False:#on regarde si on a pas une paire en mémoire et qu'elle n'est pas retourné
                    return j[0],j[1]
        
        index=random.randint(0,nbr_carte-1)  # -1 car les index commencent à 0
        carte = liste[index]
        while carte in self.cartes_memorisees[carte.nom] or carte.est_retournee:#on prends forcement une carte non decouverte
            index=random.randint(0,nbr_carte-1)
            carte = liste[index]
        var=self.memoriser_carte(carte)
        if (len(self.cartes_memorisees[carte.nom])==2 and var) or (len(self.cartes_memorisees[carte.nom])==1 and var==False) :
            
            return carte,self.cartes_memorisees[carte.nom][0]
        else:
            index2=random.randint(0,nbr_carte-1)
            carte2 = liste[index2]
            while carte2 in self.cartes_memorisees[carte2.nom] or carte==carte2 or carte2.est_retournee:#on prends forcement une carte non decouverte
                index2=random.randint(0,nbr_carte-1)
                carte2 = liste[index2]
            self.memoriser_carte(carte2)
            
            return carte,carte2
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