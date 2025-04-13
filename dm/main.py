import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QCoreApplication
from jouer_interface import FenetreJeu
from gagnant_interface import Interface_gagnant
from Interface_regles import Interface_regles
from option_jeu import Interface_de_Jeu


class FenetrePrincipale(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jeu de Memory")
        self.setGeometry(600, 150, 1000, 800)

        # Titre
        self.titre = QLabel("Bienvenue dans le jeu de Memory")
        self.titre.setFont(QFont("Arial", 24, QFont.Bold))
        self.titre.setAlignment(Qt.AlignCenter)

        # Boutons
        self.bt1 = QPushButton("📘 Règles")
        self.bt2 = QPushButton("🎮 Jouer")
        for btn in [self.bt1, self.bt2]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet("QPushButton { font-size: 18px; border-radius: 10px; padding: 10px; background-color: #A3C1DA; }"
                              "QPushButton:hover { background-color: #83A9C6; }")

        # Layout principal de l'accueil
        self.layoutAccueil = QVBoxLayout()
        self.layoutAccueil.setContentsMargins(100, 100, 100, 100)
        self.layoutAccueil.setSpacing(20)
        self.layoutAccueil.addWidget(self.titre)
        self.layoutAccueil.addStretch()
        self.layoutAccueil.addWidget(self.bt2)
        self.layoutAccueil.addWidget(self.bt1)
        self.layoutAccueil.addStretch()

        self.bt1.clicked.connect(self.regles)
        self.bt2.clicked.connect(self.jouer)

        self.stack = QStackedWidget()
        self.accueil = QWidget()
        self.accueil.setLayout(self.layoutAccueil)

        self.interface1 = Interface_regles() 
        self.interface4 = Interface_gagnant()
        self.interface3 = FenetreJeu(self.interface4)
        self.interface2 = Interface_de_Jeu(self.interface3)
        
        self.stack.addWidget(self.accueil)
        self.stack.addWidget(self.interface1)
        self.stack.addWidget(self.interface2)
        self.stack.addWidget(self.interface3)
        self.stack.addWidget(self.interface4)

        principalLayout = QVBoxLayout()
        principalLayout.addWidget(self.stack)
        self.setLayout(principalLayout)


    def regles(self):
        self.stack.setCurrentIndex(1)

    def jouer(self):
        self.stack.setCurrentIndex(2)



if __name__ == '__main__':
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Palette claire pour la fenêtre principale
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#F7FBFC"))
    app.setPalette(palette)

    window = FenetrePrincipale()
    window.show()
    app.exec_()