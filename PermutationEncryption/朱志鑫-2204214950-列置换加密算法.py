# encryption为所有加密算法的基类, 声明了不同加密算法类中共有的部分
import encryption
# 正则表达式
import re


class ColTransEncryption(encryption.Encryption):
    # 劣种子换矩形的尺寸, 行*列
    size = []
    # 列读取顺序
    key = ""

    def __init__(self, strSize: str, strKey: str):
        super(ColTransEncryption, self).__init__()
        self.key = strKey
        strPattern = "\\D+"
        self.size = re.split(strPattern, strSize)

    def encipher(self, plaintext: str):
        if int(self.size[0]) * int(self.size[1]) < len(plaintext):
            print("输入数据有误")
            exit(0)
        if plaintext not in self.plaintextTable:
            self.plaintextTable.append(plaintext)
        k = 0
        ciphertext = ""
        # 将字符填入列置换矩形(self.table)中
        for i in range(int(self.size[0])):
            lst = []
            for j in range(int(self.size[1])):
                lst.append(plaintext[k])
                k += 1
                if k >= len(plaintext):
                    break
            self.table.append(lst)
        # 按列读取顺序读
        for x in self.key:
            row = int(x) - 1
            for col in range(int(self.size[0])):
                ciphertext += self.table[col][row]
        if ciphertext not in self.ciphertextTable:
            self.ciphertextTable.append(ciphertext)


if __name__ == '__main__':
    colTranEncry = ColTransEncryption("5x4", "4123")
    colTranEncry.encipher("encryptionalgorithms".strip())
    print(colTranEncry.plaintextTable)
    print(colTranEncry.ciphertextTable)
