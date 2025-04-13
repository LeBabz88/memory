import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QMainWindow,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,QCheckBox,
                             QGridLayout,QLineEdit,QComboBox,QSpinBox,QButtonGroup,QRadioButton,QFrame,QSizePolicy)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QCoreApplication

class Interface_regles(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 12px;
                background-color: #5A5A5A;
                color: white;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # Titre
        titre = QLabel("📘 Règles du jeu")
        titre.setFont(QFont("Arial", 24, QFont.Bold))
        titre.setAlignment(Qt.AlignCenter)
        layout.addWidget(titre)

        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Bloc de règles
        regles_box = QLabel()
        regles_box.setTextFormat(Qt.PlainText)
        regles_box.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        regles_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        regles_box.setWordWrap(True)
        regles_box.setStyleSheet("""
            background-color: #f8f8f8;
            border: 2px solid #ccc;
            border-radius: 12px;
            padding: 24px;
        """)

        regles_box.setText(
            "🧠 Memory est un jeu de mémoire.\n\n\n"
            "🎯 Objectif :\n\n"
            "Retrouver toutes les paires de cartes identiques le plus rapidement possible.\n\n"
            "🔄 Déroulement du tour :\n\n"
            "- À chaque tour, un joueur retourne deux cartes.\n\n"
            "- Si elles sont identiques : elles restent visibles et le joueur marque 1 point.\n\n"
            "- Si elles sont différentes : elles se retournent face cachée.\n\n\n"
            "👥 Fin de partie :\n\n"
            "Le joueur avec le plus de paires à la fin du jeu remporte la partie.\n\n\n"
            "🎉 Bonne chance et amuse-toi bien !"
        )

        layout.addWidget(regles_box,)

        # Bouton retour
        retour = QPushButton("⬅ Retour")
        retour.setFixedWidth(130)
        retour.clicked.connect(self.retour)
        layout.addWidget(retour, alignment=Qt.AlignLeft)

        self.setLayout(layout)

    def retour(self):
        self.parentWidget().setCurrentIndex(0)