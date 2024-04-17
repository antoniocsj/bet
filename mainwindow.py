import os.path

from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QAbstractItemView, QPushButton,
                               QMessageBox, QTableWidget, QTableWidgetItem, QLabel)
from PySide6.QtCore import Qt
from parse_html_ops import extract_bets_from_html
from database_ops import create_database, query_db_01
from utils import read_json, tuple_parameters_ok


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.listas = None
        self.ParticipantSpan = ''
        self.MarketDescription = ''
        self.FixtureName = ''
        self.multiple_id_selected = ''
        self.query_result = None

        self.setWindowTitle("Apostas Múltiplas")

        self.ParticipantSpanList_widget = QListWidget(self)
        self.ParticipantSpanList_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ParticipantSpanList_widget.currentItemChanged.connect(self.ParticipantSpanList_widget_current_item_changed)
        self.ParticipantSpanList_widget.setMaximumHeight(250)

        self.MarketDescriptionList_widget = QListWidget(self)
        self.MarketDescriptionList_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.MarketDescriptionList_widget.currentItemChanged.connect(
            self.MarketDescriptionList_widget_current_item_changed)
        self.MarketDescriptionList_widget.setMaximumHeight(250)

        self.FixtureNameList_widget = QListWidget(self)
        self.FixtureNameList_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.FixtureNameList_widget.currentItemChanged.connect(self.FixtureNameList_widget_current_item_changed)
        self.FixtureNameList_widget.setMaximumHeight(250)

        self.button_extract = QPushButton("Extrair")
        self.button_extract.clicked.connect(self.extract)

        self.button_load = QPushButton("Carregar listas")
        self.button_load.clicked.connect(self.load_lists)

        self.button_query = QPushButton("Consultar")
        self.button_query.clicked.connect(self.query_db)

        h_layout1 = QHBoxLayout()
        h_layout1.addWidget(self.button_extract)
        h_layout1.addWidget(self.button_load)
        h_layout1.addWidget(self.button_query)

        h_layout2 = QHBoxLayout()
        h_layout2.addWidget(self.ParticipantSpanList_widget)
        h_layout2.addWidget(self.MarketDescriptionList_widget)
        h_layout2.addWidget(self.FixtureNameList_widget)

        self.multipleIDsList_widget = QListWidget(self)
        self.multipleIDsList_widget.setMaximumWidth(100)
        self.multipleIDsList_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.multipleIDsList_widget.currentItemChanged.connect(self.multipleIDsList_widget_current_item_changed)

        self.table_widget = QTableWidget()

        h_layout3 = QHBoxLayout()
        h_layout3.addWidget(self.multipleIDsList_widget)

        self.label_mbet_stake = QLabel()
        self.label_mbet_name = QLabel()
        self.label_mbet_ret = QLabel()

        h_layout4 = QHBoxLayout()
        h_layout4.addWidget(self.label_mbet_stake)
        h_layout4.addWidget(self.label_mbet_name)
        h_layout4.addWidget(self.label_mbet_ret)

        v_layout0 = QVBoxLayout()
        v_layout0.addLayout(h_layout4)
        v_layout0.addWidget(self.table_widget)

        h_layout3.addLayout(v_layout0)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout1)
        v_layout.addLayout(h_layout2)
        v_layout.addLayout(h_layout3)

        self.setLayout(v_layout)
        self.check_files()

    def ParticipantSpanList_widget_current_item_changed(self, item):
        if item:
            print("ParticipantSpanList_widget_current_item_changed. Current item : ", item.text())
            self.ParticipantSpan = item.text()
        else:
            self.ParticipantSpan = ''

    def MarketDescriptionList_widget_current_item_changed(self, item):
        if item:
            print("MarketDescriptionList_widget_current_item_changed. Current item : ", item.text())
            self.MarketDescription = item.text()
        else:
            self.MarketDescription = ''

    def FixtureNameList_widget_current_item_changed(self, item):
        if item:
            print("FixtureNameList_widget_current_item_changed. Current item : ", item.text())
            self.FixtureName = item.text()
        else:
            self.FixtureName = ''

    def multipleIDsList_widget_current_item_changed(self, item):
        if item:
            print("multipleIDsList_widget_current_item_changed. Current item : ", item.text())
            self.multiple_id_selected = item.text()

            if self.query_result:
                self.reset_table_widget()

                result = self.query_result[self.multiple_id_selected]

                # atualiza as informações gerais sobre a múltipla
                info = result['info']
                mbet_stake, mbet_name, mbet_ret = info[0], info[1], info[2]
                self.label_mbet_stake.setText(mbet_stake)
                self.label_mbet_name.setText(mbet_name)
                self.label_mbet_ret.setText(mbet_ret)

                # atualiza a tabela que contém os detalhes da aposta múltipla
                rows = result['rows']
                n_rows = len(rows)
                n_columns = len(rows[0])

                self.table_widget.setRowCount(n_rows)
                self.table_widget.setColumnCount(n_columns)

                table_widget_width = self.table_widget.width()
                for i in range(n_columns):
                    self.table_widget.setColumnWidth(i, (table_widget_width - 100) // 3)

                for i, (a, b, c) in enumerate(rows):
                    item_a = QTableWidgetItem(a)
                    item_a.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                    item_b = QTableWidgetItem(b)
                    item_b.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                    item_c = QTableWidgetItem(c)
                    item_c.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

                    self.table_widget.setItem(i, 0, item_a)
                    self.table_widget.setItem(i, 1, item_b)
                    self.table_widget.setItem(i, 2, item_c)

        else:
            self.multiple_id_selected = ''

    def extract(self):
        if not os.path.exists('apostas.html'):
            QMessageBox.information(self, "Erro", "O arquivo apostas.html não foi encontrado.",
                                    QMessageBox.Ok)
            return

        extract_bets_from_html()

        if not os.path.exists('apostas.json'):
            QMessageBox.information(self, "Erro", "O arquivo apostas.json não foi encontrado.",
                                    QMessageBox.Ok)
            return

        create_database('apostas.json', 'database.db')

        QMessageBox.information(self, "Extração concluída", "A extração de apostas do arquivo html está completa.",
                                QMessageBox.Ok)

        if self.ParticipantSpanList_widget.count() > 0:
            self.ParticipantSpanList_widget.clear()

        if self.MarketDescriptionList_widget.count() > 0:
            self.MarketDescriptionList_widget.clear()

        if self.FixtureNameList_widget.count() > 0:
            self.FixtureNameList_widget.clear()

        self.check_files()

    def load_lists(self):
        if not os.path.exists('listas.json'):
            QMessageBox.information(self, "Erro", "O arquivo database.db não foi encontrado.",
                                    QMessageBox.Ok)
            return

        self.listas = read_json('listas.json')

        if self.ParticipantSpanList_widget.count() == 0:
            self.ParticipantSpanList_widget.addItems(self.listas['ParticipantSpanList'])

        if self.MarketDescriptionList_widget.count() == 0:
            self.MarketDescriptionList_widget.addItems(self.listas['MarketDescriptionList'])

        if self.FixtureNameList_widget.count() == 0:
            self.FixtureNameList_widget.addItems(self.listas['FixtureNameList'])

        if self.multipleIDsList_widget.count() > 0:
            self.multipleIDsList_widget.clear()

        # if self.table_widget.rowCount() > 0:
        self.reset_table_widget()

    def query_db(self):
        if not os.path.exists('database.db'):
            QMessageBox.information(self, "Erro", "O arquivo database.db não foi encontrado.",
                                    QMessageBox.Ok)
            return

        params = (self.ParticipantSpan, self.MarketDescription, self.FixtureName)
        if tuple_parameters_ok(params):
            self.query_result = query_db_01('database.db', params)
        else:
            self.query_result = None
            QMessageBox.information(self, "Atenção", "Selecione elementos das 3 listas",
                                    QMessageBox.Ok)

        if self.multipleIDsList_widget.count() > 0:
            self.multipleIDsList_widget.clear()

        self.reset_table_widget()

        if self.query_result:
            for multiple_id in self.query_result:
                self.multipleIDsList_widget.addItem(multiple_id)

    def reset_table_widget(self):
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(0)
        self.label_mbet_stake.clear()
        self.label_mbet_name.clear()
        self.label_mbet_ret.clear()

    def check_files(self):
        if os.path.exists('listas.json'):
            self.button_load.setEnabled(True)
        else:
            self.button_load.setEnabled(False)

        if os.path.exists('listas.json') and os.path.exists('database.db'):
            self.button_query.setEnabled(True)
        else:
            self.button_query.setEnabled(False)
