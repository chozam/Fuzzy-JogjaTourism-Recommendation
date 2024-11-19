class Fuzzy:
    def __init__(self) -> None:
        self.domain_variabel = {} # variabel : range
        self.himpunan_fuzzy = {} # domain_var : {himp fuzzy : range}

    def trimf(self, x, a, b, c):
        if a <= x <= b:
            return (x - a) / (b - a) if b - a != 0 else 0
        elif b <= x <= c:
            return (c - x) / (c - b) if c - b != 0 else 0
        else:
            return 0

    def trapmf(self, x, a, b, c, d):
        if x == a and x == b:
            return 1
        elif a <= x <= b:
            return (x - a) / (b - a) if b - a != 0 else 0
        elif b <= x <= c:
            return 1
        elif c <= x <= d:
            return (d - x) / (d - c) if d - c != 0 else 0
        else:
            return 0

    def linupmf(self, x, a, b):
        if a < x <= b:
            return (x - a) / (b - a) if b - a != 0 else 0
        else:
            return 0

    def lindownmf(self, x, a, b):
        if a < x <= b:
            return (b - x) / (b - a) if b - a != 0 else 0
        else:
            return 0

    def sigmupf(self, x, a, b, c):
        if x <= a:
            return 0
        elif a <= x <= b:
            return 2 * ((x - a) / (c - a)) ** 2 if c - a != 0 else 0
        elif b <= x <= c:
            return 1 - 2 * ((c - x) / (c - a)) ** 2 if c - a != 0 else 1
        elif x >= c:
            return 1

    def sigmdownf(self, x, a, b, c):
        if x <= a:
            return 0
        elif a <= x <= b:
            return 1 - 2 * ((x - a) / (c - a)) ** 2 if c - a != 0 else 1
        elif b <= x <= c:
            return 2 * ((c - x) / (c - a)) ** 2 if c - a != 0 else 0
        elif x >= c:
            return 1

    def smf(self, x, a, b):
        if x <= a:
            return 0
        elif a <= x <= (a + b) / 2:
            return 2 * ((x - a) / (b - a)) ** 2 if b - a != 0 else 0
        elif (a + b) / 2 <= x <= b:
            return 1 - 2 * ((x - b) / (b - a)) ** 2 if b - a != 0 else 1
        elif x >= b:
            return 1

    def zmf(self, x, a, b):
        if x <= a:
            return 1
        elif a <= x <= (a + b) / 2:
            return 1 - 2 * ((x - a) / (b - a)) ** 2 if b - a != 0 else 1
        elif (a + b) / 2 <= x <= b:
            return 2 * ((x - b) / (b - a)) ** 2 if b - a != 0 else 0
        elif x >= b:
            return 0