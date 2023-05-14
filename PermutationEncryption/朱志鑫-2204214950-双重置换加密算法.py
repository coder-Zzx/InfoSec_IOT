import encryption
from PySide6.QtWidgets import QApplication, QHeaderView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QTableWidgetItem


def spaceRemove(string: str):
    res = []
    newString = ""
    index = []
    for i in range(len(string)):
        if string[i] != " ":
            newString += string[i]
        elif string[i] == " ":
            index.append(i)
    res.append(newString)
    res.append(index)
    return res


class DoubleTransEncryption(encryption.Encryption):
    firstTableTable = []
    secondTableTable = []

    def __init__(self, seqList: str):
        super(DoubleTransEncryption, self).__init__()
        seqList = spaceRemove(seqList)[0]
        lst = list(seqList)
        lst.sort()
        for i in range(len(seqList)):
            index = lst.index(seqList[i]) + 1
            if index in self.table:
                index += 1
            self.table.append(index)

    def initTable(self, text: str, table: list):
        k = 0
        j = 0
        while True:
            lst = []
            for i in range(len(self.table)):
                lst.append(text[k])
                k += 1
                if k == len(text):
                    break
            table.append(lst)
            j += 1
            if k == len(text):
                break

    def readTable(self, originText: str, table: list, flag: bool):
        newText = ""
        for i in range(1, max(self.table) + 1):
            for j in range(len(table)):
                try:
                    newText += table[j][self.table.index(i)]
                    if len(newText) == len(originText):
                        break
                except:
                    pass
            if flag:
                newText += " "
        return newText

    def encipher(self, plaintext: str):
        firstTable = []
        secondTable = []
        if plaintext not in self.plaintextTable:
            self.plaintextTable.append(plaintext)
        l = spaceRemove(plaintext)
        plaintext = l[0]
        self.initTable(plaintext, firstTable)
        newText = self.readTable(plaintext, firstTable, False)
        self.initTable(newText, secondTable)
        ciphertext = self.readTable(newText, secondTable, True)

        self.ciphertextTable.append(ciphertext)
        self.firstTableTable.append(firstTable)
        self.secondTableTable.append(secondTable)


class MainWindow:
    encry: DoubleTransEncryption

    def __init__(self):
        self.ui = QUiLoader().load("doubleTransEncryption.ui")
        self.ui.setWindowTitle("双重换位加密法")
        self.ui.tableBtn.clicked.connect(self.getKey)
        self.ui.plaintextBtn.clicked.connect(self.getPlaintext)
        self.ui.plaintextList.itemSelectionChanged.connect(self.selectionChanged)
        self.ui.ciphertextList.itemSelectionChanged.connect(self.selectionChanged)

    def getKey(self):
        key = self.ui.tableLine.text()
        self.encry = DoubleTransEncryption(key)

    def getPlaintext(self):
        plaintext = self.ui.plaintextLine.text()
        self.encry.encipher(plaintext)
        plaintextListItem = self.encry.plaintextTable[-1]
        self.ui.plaintextList.addItem(plaintextListItem)
        ciphertextListItem = self.encry.ciphertextTable[-1]
        self.ui.ciphertextList.addItem(ciphertextListItem)

    def selectionChanged(self):
        index = self.ui.plaintextList.currentRow()
        QFirstTable = []
        QSecondTable = []
        QFirstTable.clear()
        QSecondTable.clear()
        QFirstTable = self.encry.firstTableTable[index]
        QSecondTable = self.encry.secondTableTable[index]
        self.ui.firstTable.setRowCount(len(QFirstTable) + 1)
        self.ui.secondTable.setRowCount(len(QFirstTable) + 1)
        self.ui.firstTable.setColumnCount(len(QFirstTable[0]))
        self.ui.secondTable.setColumnCount(len(QFirstTable[0]))
        for i in range(len(QFirstTable[0])):
            self.ui.firstTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
            self.ui.secondTable.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        for i in range(len(self.encry.table)):
            newItem = QTableWidgetItem(str(self.encry.table[i]))
            self.ui.firstTable.setItem(0, i, newItem)
        for i in range(len(self.encry.table)):
            newItem = QTableWidgetItem(str(self.encry.table[i]))
            self.ui.secondTable.setItem(0, i, newItem)
        for i in range(len(QFirstTable)):
            for j in range(len(QFirstTable[i])):
                newItem = QTableWidgetItem(str(QFirstTable[i][j]))
                self.ui.firstTable.setItem(i + 1, j, newItem)
        for i in range(len(QSecondTable)):
            for j in range(len(QSecondTable[i])):
                newItem = QTableWidgetItem(str(QSecondTable[i][j]))
                self.ui.secondTable.setItem(i + 1, j, newItem)
        self.ui.firstTable.viewport().update()
        self.ui.secondTable.viewport().update()


if __name__ == '__main__':
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.ui.show()
    app.exec()