from typing import override, Optional

from PyQt6 import QtCore
from PyQt6 import QtWidgets
import pandas as pd


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self,
                 dataframe: pd.DataFrame,
                 parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self.__dataframe = dataframe

    @property
    def dataframe(self) -> pd.DataFrame:
        return self.__dataframe.copy()

    @override
    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        if parent == QtCore.QModelIndex():
            return len(self.__dataframe)
        return 0

    @override
    def columnCount(self, parent=QtCore.QModelIndex()) -> int:
        if parent == QtCore.QModelIndex():
            return len(self.__dataframe.columns)
        return 0

    @override
    def data(self, index: QtCore.QModelIndex, role=QtCore.Qt.ItemDataRole):
        if not index.isValid():
            return None
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return str(self.__dataframe.iloc[index.row(), index.column()])
        return None

    @override
    def headerData(self, section, orientation, role=...):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return str(self.__dataframe.columns[section])
            if orientation == QtCore.Qt.Orientation.Vertical:
                return str(self.__dataframe.index[section])
        return None
