import encryption


class Caesar(encryption.Encryption):
    def __init__(self, index: int):
        super(Caesar, self).__init__()
        self.table = index

    def encipher(self, plaintext: str):
        if plaintext not in self.plaintextTable:
            self.plaintextTable.append(plaintext)
        ciphertext = ""
        for x in plaintext:
            if 65 <= ord(x) <= 90:
                ciphertext += chr((ord(x) - 65 + self.table) % 26 + 65)
            elif 97 <= ord(x) <= 122:
                ciphertext += chr((ord(x) - 97 + self.table) % 26 + 97)
        if ciphertext not in self.ciphertextTable:
            self.ciphertextTable.append(ciphertext)


if __name__ == '__main__':
    caecar = Caesar(4)
    caecar.encipher("y")
    print(caecar.plaintextTable)
    print(caecar.ciphertextTable)
