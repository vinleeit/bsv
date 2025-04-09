import sys
import os
from datetime import datetime

from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pandas as pd

from components.pandas_model import PandasModel
import utils.dialogs as dialogs


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.original_workdir = ''
        self.target_workdir = ''
        self.filename = ''

        self.setWindowTitle('Teens Group Excel Converter')

        self.pandasView = QTableView()
        self.pandasView.resize(800, 500)
        self.pandasView.horizontalHeader().setStretchLastSection(True)
        self.pandasView.setAlternatingRowColors(True)
        self.pandasView.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )

        # Layouts
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.pandasView)

        self.actionSectionLayout = self.__create_export_section_layout()

        self.l = QVBoxLayout()
        self.l.addLayout(self.mainLayout)
        self.l.addLayout(self.actionSectionLayout)

        widget = QWidget(self)
        widget.setLayout(self.l)
        self.setCentralWidget(widget)

    def __create_export_section_layout(self) -> QLayout:
        # Load CSV Section
        loadCSVSectionLayout = QHBoxLayout()

        loadCsvButton = QPushButton(self)
        loadCsvButton.setText('Load CSV File')
        loadCsvButton.clicked.connect(self.load_csv)
        loadCSVSectionLayout.addWidget(loadCsvButton)

        # Directory section
        directorySectionLayout = QHBoxLayout()

        selectSaveDirLabel = QLabel(self)
        selectSaveDirLabel.setText('Directory:')
        directorySectionLayout.addWidget(selectSaveDirLabel)

        selectSaveDirField = QLineEdit(self)
        selectSaveDirField.setReadOnly(True)
        self.selectSaveDirField = selectSaveDirField
        directorySectionLayout.addWidget(selectSaveDirField)

        resetDirButton = QPushButton(self)
        resetDirButton.setText('Reset')
        resetDirButton.setDisabled(True)
        resetDirButton.clicked.connect(self.reset_save_dir)
        self.resetDirButton = resetDirButton
        directorySectionLayout.addWidget(resetDirButton)

        selectSaveDirButton = QPushButton(self)
        selectSaveDirButton.setText('Choose')
        selectSaveDirButton.clicked.connect(self.choose_save_dir)
        directorySectionLayout.addWidget(selectSaveDirButton)

        # Export section
        exportSectionLayout = QHBoxLayout()

        exportCSVButton = QPushButton(self)
        exportCSVButton.setText('Export')
        exportCSVButton.clicked.connect(self.export)
        exportCSVButton.setDisabled(True)
        self.exportCSVButton = exportCSVButton
        exportSectionLayout.addWidget(exportCSVButton)

        # Layout
        actionLayout = QVBoxLayout()
        actionLayout.addLayout(loadCSVSectionLayout)
        actionLayout.addLayout(directorySectionLayout)
        actionLayout.addLayout(exportSectionLayout)

        return actionLayout

    @pyqtSlot()
    def load_csv(self):
        fullpath = QFileDialog.getOpenFileName(
            self,
            'Open File',
            '${HOME}',
            'CSV Files (*.csv)',
        )[0]
        if fullpath:
            self.pandasView.setModel(PandasModel(pd.read_csv(fullpath)))
            self.filename = os.path.basename(fullpath)
            self.original_workdir = os.path.dirname(fullpath)
            if not self.selectSaveDirField.text():
                self.selectSaveDirField.setText(self.original_workdir)

            self.exportCSVButton.setDisabled(False)

            self.resetDirButton.setDisabled(
                not self.original_workdir or self.original_workdir == self.selectSaveDirField.text(),
            )

    @pyqtSlot()
    def choose_save_dir(self):
        dirpath = QFileDialog.getExistingDirectory(
            parent=self,
            directory=self.selectSaveDirField.text(),
            caption='Select save directory',
            options=QFileDialog.Option.ShowDirsOnly,
        )
        if dirpath:
            self.selectSaveDirField.setText(dirpath)
            self.resetDirButton.setDisabled(
                not self.original_workdir or self.original_workdir == self.selectSaveDirField.text(),
            )

    @pyqtSlot()
    def reset_save_dir(self):
        if self.original_workdir and self.original_workdir != self.selectSaveDirField.text:
            self.selectSaveDirField.setText(self.original_workdir)
            self.resetDirButton.setDisabled(
                not self.original_workdir or self.original_workdir == self.selectSaveDirField.text(),
            )

    @pyqtSlot()
    def export(self):
        pandasModel: PandasModel = self.pandasView.model()
        if not pandasModel:
            return

        try:
            df_original = pandasModel.dataframe
            cols = list(df_original)
            cols = cols[24:31] + cols[:24] + cols[31:]
            df = df_original[cols]

            df.rename({
                'Address 1': 'Address',
                'Location': 'State',
                'First Name.1': 'Child First Name',
                'Last Name.1': 'Child Last Name',
                'Gender.1': 'Child Gender',
                'First Name': 'Membership First Name',
                'Last Name': 'Membership Last Name',
                'Gender': 'Membership Gender',
            }, axis=1, inplace=True)
            df['Address 3'] = df['Address 3'].astype(str)
            df[['Address', 'Address 2', 'Address 3']] = df[['Address',
                                                            'Address 2', 'Address 3']].fillna('').replace('nan', '')
            df['Address'] = df[['Address', 'Address 2', 'Address 3']].agg(
                ' '.join, axis=1).transform(str.strip)
            df = df.drop(['Address 2', 'Address 3'], axis=1)

            for i in ['Child First Name', 'Child Last Name', 'Child Gender', 'Date of Birth (DD/MM/YYYY)', 'Age', 'Did the child attend the BSV Dhamma School in 2024?']:
                df[i] = df[i].str.split(', ')
            df['Grade/Year Level at school at start of 2025'] = df.apply(lambda row: row['Grade/Year Level at school at start of 2025'].split(
                ', ') if len(row['Child First Name']) > 1 else [row['Grade/Year Level at school at start of 2025']], axis=1)
            df = df.explode(['Child First Name', 'Child Last Name', 'Child Gender', 'Date of Birth (DD/MM/YYYY)', 'Age',
                            'Grade/Year Level at school at start of 2025', 'Did the child attend the BSV Dhamma School in 2024?'])

            save_path = f'{self.selectSaveDirField.text()}/{datetime.now().strftime('%Y%m%d%H%M')
                                                            }_{self.filename}'
            df.to_csv(save_path)
            dialogs.show_information_dialog(
                f'Success!\nFile is saved at:\n{save_path}'
            )
        except Exception as err:
            dialogs.show_information_dialog(f'Error:\n{err}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
