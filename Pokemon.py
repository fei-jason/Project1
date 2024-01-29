class Pokemon:

    def __init__(self, name, type, hp, attack, defense, moves):
        self.name = name
        self.type = type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.moves = moves

class Moves:
    
    def __init__(self, name, type, pp, power, accuracy):
        self.name = name
        self.type = type
        self.pp = pp
        self.power = power
        self.accuracy = accuracy
