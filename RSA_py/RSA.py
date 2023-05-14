import random
import base64


def isPrime(n):
    """
    判断质数
    :param n:
    :return: 返回true则代表可能为质数, false则一定不为质数
    """
    # 利用费马算法进行判断
    for i in range(20):
        # 100为检测次数, 次数越多准确性越大.
        print("第{}次检测n:{}".format(i, n))
        a = random.randint(1, n - 1)
        if montgomery(a, n - 1, n) != 1:
            return False
    return True


def montgomery(a, k, m):
    """
    蒙哥马利算法, 逐次平方法快速计算a^k(mod m)
    :param a: 底数
    :param k: 指数
    :param m: 取余的模
    :return: 余数
    """
    p = 1
    a %= m  # 防止n过大, 先取余
    while k != 1:
        if k & 1 != 0:
            p = (p * a) % m
        a = (a * a) % m
        k >>= 1
    return (k * a) % m


def modularLinearEquation(a, b, n):
    """
    利用扩展欧几里得算法求解线性同余方程ax===1(mod n)
    :param a:
    :param b:
    :param n:
    :return: 返回线性同余方程ax===1(mod n)的解
    """
    r = []
    d, x, y = exgcd(a, n)
    if b % d != 0:
        return r

    x0 = x * (b // d) % n
    r.append(x0)
    for i in range(d):
        r.append((x0 + i * (n - d)) % n)
    return r


def exgcd(a, b):
    """
    计算方程gcd(a, b) = ax + by的一个解
    :param a:
    :param b:
    :return: 返回方程的一个解
    """
    x0, y0 = 1, 0
    x1, y1 = 0, 1
    x, y = 0, 1
    r = a % b  # 余数
    q = (a - r) // b  # 商
    while r != 0:  # 余数不等于0
        x = x0 - q * x1
        y = y0 - q * y1
        x0, y0 = x1, y1
        x1, y1 = x, y
        a = b  # 除数赋给被除数
        b = r  # 余数赋给除数
        r = a % b
        q = (a - r) // b
    return b, x, y


def primeSieve(bits):
    1 << (bits - 1)
    n = (1 << bits) - 1
    index = 0
    primes = []
    isVisit = [True] * (n + 5)
    for i in range(2, n + 1):
        if isVisit[i]:
            primes.append(i)
        for j in range(len(primes)):
            if primes[j] * i > n:
                break
            isVisit[primes[j] * i] = False
            if i % primes[j] == 0:
                break

    a = random.randint(index, len(primes))
    b = random.randint(index, len(primes))
    while a == b:
        b = random.randint(index, len(primes))

    return primes[a], primes[b]


def randomPrimeBits(bits):
    """
    随机生成大质数
    :param bits: 位数
    :return: 质数
    """
    base1 = 1 << (bits - 1)
    base2 = (1 << bits) - 1
    i = random.randint(base1, base2)
    if i % 2 == 0:
        i += 1
    while True:
        i += 2
        if i > base2:
            i = base1
        if isPrime(i):
            return i


class RSA(object):
    P = 0
    Q = 0
    n = 0
    e = 0
    d = 0
    privateKey = (n, d)
    publicKey = (n, e)

    def __init__(self, bits: int):
        self.getKeys()

    def getPnQ(self):
        """
        生成质数P和Q
        :return: 元组形式的PQ
        """
        self.P, self.Q = primeSieve(20)

    def getNnEnD(self):
        """
        根据p和q的值计算n,e,d
        :return: n,e,d的元组
        """
        m = (self.P - 1) * (self.Q - 1)
        self.n = self.Q * self.Q
        self.e = 65537
        self.d = modularLinearEquation(self.e, 1, m)[0]

    def getKeys(self):
        """
        生成公钥与私钥
        :return 元组形式的公钥和私钥
        """
        self.getPnQ()
        self.getNnEnD()
        self.publicKey = (self.n, self.e)
        self.privateKey = (self.n, self.d)

    def encrypt(self, data):
        """
        字符串逐字符加密
        :param data: 字符串
        :return:
        """
        ciphertext = ""
        for x in data:
            byte = ord(x)
            cipher = (byte ** self.e) % self.n
            ciphertext += str(cipher)

        ciphertext = ciphertext.encode("utf-8")
        base64Ciphertext = base64.b64encode(bytes(ciphertext)).decode()
        return base64Ciphertext


if __name__ == '__main__':
    rsa = RSA(40)
    print("私钥对为:", rsa.privateKey)
    print("秘钥对为:", rsa.publicKey)
    plaintext = "物联网001朱志鑫"
    print("明文为:", plaintext)
    print("密文为:", str(rsa.encrypt(plaintext)))
