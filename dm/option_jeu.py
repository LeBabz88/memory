from PyQt5.QtWidgets import ( QWidget, QVBoxLayout,QHBoxLayout, QPushButton, QLabel,QLineEdit,QComboBox,QButtonGroup,QRadioButton,QFrame)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
class Interface_de_Jeu(QWidget):
    def __init__(self,interface3):
        super().__init__()

        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
            }
            QRadioButton {
                font-size: 16px;
            }
            QComboBox, QLineEdit {
                font-size: 16px;
                padding: 4px;
                border-radius: 6px;
                background-color: #f0f0f0;
            }
            QPushButton {
                font-size: 16px;
                padding: 8px 16px;
                border-radius: 12px;
            }
            QPushButton:enabled {
                background-color: #5A5A5A;
                color: white;
            }
            QPushButton:disabled {
                background-color: #888;
                color: white;
            }
            QPushButton:hover:enabled {
                background-color: #444;
            }
        """)
        self.interface3=interface3
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        titre = QLabel("🎯 Mode de jeu")
        titre.setFont(QFont("Arial", 24, QFont.Bold))
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)

        # Section des modes de jeu
        mode_layout = QHBoxLayout()

        self.mode_group = QButtonGroup(self)

        # --- Solo ---
        solo_layout = QVBoxLayout()
        self.solo_btn = QRadioButton("Solo")
        self.solo_btn.setChecked(True)
        self.mode_group.addButton(self.solo_btn)
        solo_layout.addWidget(self.solo_btn)

        self.solo_pseudo = QLineEdit()
        self.solo_pseudo.setPlaceholderText("Pseudonyme")
        solo_layout.addWidget(self.solo_pseudo)
        mode_layout.addLayout(solo_layout)

        # --- Ami(es) ---
        amis_layout = QVBoxLayout()
        self.ami_btn = QRadioButton("Ami(es)")
        self.mode_group.addButton(self.ami_btn)
        amis_layout.addWidget(self.ami_btn)

        amis_layout.addWidget(QLabel("Nombre de joueurs"))
        self.nb_joueurs_combo = QComboBox()
        self.nb_joueurs_combo.addItems(["2", "3", "4"])
        amis_layout.addWidget(self.nb_joueurs_combo)

        self.pseudo_inputs = []
        self.pseudo_layout = QVBoxLayout()
        amis_layout.addLayout(self.pseudo_layout)

        mode_layout.addLayout(amis_layout)

        # --- Ordinateur ---
        ordi_layout = QVBoxLayout()
        self.ordi_btn = QRadioButton("Ordinateur")
        self.mode_group.addButton(self.ordi_btn)
        ordi_layout.addWidget(self.ordi_btn)
        ordi_layout.addWidget(QLabel("Difficulté"))

        self.difficulte_combo = QComboBox()
        self.difficulte_combo.addItems(["Facile", "Normal", "Difficile"])
        ordi_layout.addWidget(self.difficulte_combo)
        mode_layout.addLayout(ordi_layout)

        layout.addLayout(mode_layout)

        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Choix du nombre de cartes
        cartes_layout = QVBoxLayout()
        nb_cartes_label = QLabel("Nombre de cartes")
        nb_cartes_label.setFont(QFont("Arial", 16, QFont.Bold))
        nb_cartes_label.setAlignment(Qt.AlignCenter)
        cartes_layout.addWidget(nb_cartes_label)

        self.cartes_combo = QComboBox()
        self.cartes_combo.addItems(["3*2", "4*3", "5*4", "8*7", "10*7"])
        cartes_layout.addWidget(self.cartes_combo, alignment=Qt.AlignCenter)

        layout.addLayout(cartes_layout)

        # Bouton "Lancer la partie"
        lancer = QPushButton("🎮 Lancer la partie")
        lancer.setFixedHeight(45)
        layout.addWidget(lancer, alignment=Qt.AlignCenter)
        lancer.clicked.connect(self.jeu)

        # Bouton "Retour"
        retour = QPushButton("⬅ Retour")
        retour.setFixedWidth(120)
        retour.clicked.connect(self.retour)
        layout.addWidget(retour, alignment=Qt.AlignLeft)

        self.setLayout(layout)

        # Connexions
        self.solo_btn.toggled.connect(self.mettre_a_jour_affichage)
        self.ami_btn.toggled.connect(self.mettre_a_jour_affichage)
        self.ordi_btn.toggled.connect(self.mettre_a_jour_affichage)
        self.nb_joueurs_combo.currentIndexChanged.connect(self.mettre_a_jour_pseudos)

        self.mettre_a_jour_affichage()

    def mettre_a_jour_affichage(self):
        self.solo_pseudo.setVisible(self.solo_btn.isChecked())
        self.nb_joueurs_combo.setVisible(self.ami_btn.isChecked())
        self.pseudo_layout.setEnabled(self.ami_btn.isChecked())
        self.mettre_a_jour_pseudos()
        self.difficulte_combo.setVisible(self.ordi_btn.isChecked())

    def mettre_a_jour_pseudos(self):
        if not self.ami_btn.isChecked():
            for widget in self.pseudo_inputs:
                widget.setParent(None)
            self.pseudo_inputs.clear()
            return

        nb_joueurs = int(self.nb_joueurs_combo.currentText())

        # Supprimer anciens champs
        for widget in self.pseudo_inputs:
            widget.setParent(None)
        self.pseudo_inputs.clear()

        for i in range(nb_joueurs):
            champ = QLineEdit()
            champ.setPlaceholderText(f"Pseudonyme joueur {i+1}")
            self.pseudo_layout.addWidget(champ)
            self.pseudo_inputs.append(champ)

    def retour(self):
        self.parentWidget().setCurrentIndex(0)
    def jeu(self):
        print(self.mode_group.checkedButton().text())
        x=self.cartes_combo.currentText().split("*")
        nbr_cartes=int(x[0])*int(x[1])
        print(nbr_cartes)
        noms_joueurs=[]
        if self.mode_group.checkedButton().text()=="Solo":
            if self.solo_pseudo.text()=="":
                noms_joueurs.append("Joueur 1")
            else:
                noms_joueurs.append(self.solo_pseudo.text())
            self.interface3.ajouter_joueurs(noms_joueurs)
            self.interface3.creer_cartes(nbr_cartes)
        elif self.mode_group.checkedButton().text()=="Ami(es)":
            var=0
            liste=self.pseudo_inputs
            for i in liste:
                var+=1
                if i.text()=="":
                    noms_joueurs.append("Joueur "+str(var))
                else:
                    noms_joueurs.append(i.text())
            self.interface3.ajouter_joueurs(noms_joueurs)
            self.interface3.creer_cartes(nbr_cartes)
        else:
            if self.difficulte_combo.currentText()=="Facile":
                difficulte=10
            elif self.difficulte_combo.currentText()=="Normal":
                difficulte=4
            else:
                difficulte=1
            noms_joueurs.append("Joueur 1")
            self.interface3.ajouter_joueurs(noms_joueurs,[("Robot",difficulte)])
            self.interface3.creer_cartes(nbr_cartes)
        self.parentWidget().setCurrentIndex(3)