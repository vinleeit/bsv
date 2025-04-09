from typing import Optional

from PyQt6.QtWidgets import QWidget, QMessageBox


def show_information_dialog(message: str,
                            parent: Optional[QWidget] = None):
    dlg = QMessageBox(parent)
    dlg.setWindowTitle('Information')
    dlg.setIcon(QMessageBox.Icon.Information)
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    dlg.setText(message)
    dlg.exec()


def show_error_dialog(message: str,
                      parent: Optional[QWidget] = None):
    dlg = QMessageBox(parent)
    dlg.setWindowTitle('Error')
    dlg.setIcon(QMessageBox.Icon.Critical)
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    dlg.setText(message)
    dlg.exec()
