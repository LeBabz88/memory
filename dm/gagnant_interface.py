from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout ,QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
class Interface_gagnant(QWidget):
    def __init__(self):
        super().__init__()
        self.gagnant_text = ""  # Renommé pour éviter le conflit
        
        # Titre
        self.titre = QLabel("Résultat")  # Texte par défaut
        self.titre.setFont(QFont("Arial", 24, QFont.Bold))
        self.titre.setAlignment(Qt.AlignCenter)

        # Boutons
        self.bt1 = QPushButton("Rejouer")
        self.bt2 = QPushButton("Quitter")
        for btn in [self.bt1, self.bt2]:
            btn.setMinimumHeight(50)
            btn.setStyleSheet("QPushButton { font-size: 18px; border-radius: 10px; padding: 10px; background-color: #A3C1DA; }"
                              "QPushButton:hover { background-color: #83A9C6; }")

        # Layout principal 
        layout = QVBoxLayout()
        layout.setContentsMargins(100, 100, 100, 100)
        layout.setSpacing(20)
        layout.addWidget(self.titre)
        layout.addStretch()
        layout.addWidget(self.bt1)
        layout.addWidget(self.bt2)
        layout.addStretch()

        self.bt1.clicked.connect(self.retour)
        self.bt2.clicked.connect(self.quitter)

        # Appliquer directement le layout au widget
        self.setLayout(layout)
    
    def definir_gagnant(self, texte):  # Méthode renommée pour éviter le conflit
        self.titre.setText(texte)

    def retour(self):
        self.parentWidget().setCurrentIndex(2)

    def quitter(self):
        QApplication.quit()