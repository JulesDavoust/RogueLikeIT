class classePJ:
    def __init__(self):
        self.x = -1
        self.classe = {0:"guerrier", 1:"archer", 2:"sorcier"}

    def classeChoice(self):
        while(self.x < 0 or self.x > 2):
            print("Choisis ta classe :\nGuerrier (tape 0)\nArcher (tape 1)\nSorcier (tape 2)")
            self.x = int(input())
        return self.x