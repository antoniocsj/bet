from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QAbstractItemView, QPushButton,
                               QMessageBox)
from parse_html_ops import extract_bets_from_html
from database_ops import create_database
from utils import read_json


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.listas = None

        self.setWindowTitle("Apostas Múltiplas")

        self.ParticipantSpanList_widget = QListWidget(self)
        self.ParticipantSpanList_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ParticipantSpanList_widget.currentItemChanged.connect(self.ParticipantSpanList_widget_current_item_changed)

        self.MarketDescriptionList_widget = QListWidget(self)
        self.MarketDescriptionList_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.MarketDescriptionList_widget.currentItemChanged.connect(self.MarketDescriptionList_widget_current_item_changed)

        self.FixtureNameList_widget = QListWidget(self)
        self.FixtureNameList_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.FixtureNameList_widget.currentItemChanged.connect(self.FixtureNameList_widget_current_item_changed)

        button_extract = QPushButton("Extrair")
        button_extract.clicked.connect(self.extract)

        button_load = QPushButton("Carregar listas")
        button_load.clicked.connect(self.load_lists)

        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(button_extract)
        h_layout1.addWidget(button_load)

        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(self.ParticipantSpanList_widget)
        h_layout2.addWidget(self.MarketDescriptionList_widget)
        h_layout2.addWidget(self.FixtureNameList_widget)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout1)
        v_layout.addLayout(h_layout2)

        self.setLayout(v_layout)

    def ParticipantSpanList_widget_current_item_changed(self, item):
        if item:
            print("ParticipantSpanList_widget_current_item_changed. Current item : ", item.text())

    def MarketDescriptionList_widget_current_item_changed(self, item):
        if item:
            print("MarketDescriptionList_widget_current_item_changed. Current item : ", item.text())

    def FixtureNameList_widget_current_item_changed(self, item):
        if item:
            print("FixtureNameList_widget_current_item_changed. Current item : ", item.text())

    def extract(self):
        extract_bets_from_html()
        create_database('apostas.json', 'database.db')

        QMessageBox.information(self, "Extração", "A extração de apostas do arquivo html está completa.", QMessageBox.Ok)

        if self.ParticipantSpanList_widget.count() > 0:
            self.ParticipantSpanList_widget.clear()

        if self.MarketDescriptionList_widget.count() > 0:
            self.MarketDescriptionList_widget.clear()

        if self.FixtureNameList_widget.count() > 0:
            self.FixtureNameList_widget.clear()

    def load_lists(self):
        self.listas = read_json('listas.json')

        if self.ParticipantSpanList_widget.count() == 0:
            self.ParticipantSpanList_widget.addItems(self.listas['ParticipantSpanList'])

        if self.MarketDescriptionList_widget.count() == 0:
            self.MarketDescriptionList_widget.addItems(self.listas['MarketDescriptionList'])

        if self.FixtureNameList_widget.count() == 0:
            self.FixtureNameList_widget.addItems(self.listas['FixtureNameList'])
