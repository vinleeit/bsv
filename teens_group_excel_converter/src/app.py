import sys
import os
from datetime import datetime

from PyQt6 import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pandas as pd

from components.pandas_model import PandasModel
import utils.dialogs as dialogs
import services.converter as converter


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.original_workdir = ''
        self.target_workdir = ''
        self.filename = ''

        self.setWindowTitle('Teens Group Excel Converter - v1.0.0')

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
            df = converter.process_df(pandasModel.dataframe)
            save_path = f'{self.selectSaveDirField.text()}/{datetime.now().strftime('%y%m%d%H%M%S')
                                                            }_{self.filename}'
            df.to_csv(save_path)
            dialogs.show_information_dialog(
                f'Success!\nFile is saved at:\n{save_path}')
        except Exception as err:
            dialogs.show_error_dialog(f'Error:\n{err}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
