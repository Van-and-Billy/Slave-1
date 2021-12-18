import random


class Casino:
    
    def __init__(self):
        self.error: bool = False
    
    @staticmethod
    def punch(bet: int, power: int) -> list:
        resulted: int = random.randint(1, 100)
        result = power - resulted
        if (result <= 10) and (result >= -10):
            multiplier = 1 + resulted / 100
            return [round((bet / 20) + (bet * multiplier)) - bet, resulted]
        else:
            return [-bet, resulted]
    
    @staticmethod
    def up(bet: int, multiplier: float) -> list:
        real_multiplier = round(random.uniform(0.5, 2.0), 1)
        if multiplier <= real_multiplier:
            return [round(bet * multiplier) - bet, real_multiplier]
        else:
            return [-bet, real_multiplier]
    
    @staticmethod
    def one_to_five(bet: int, number: int) -> list:
        real_number = random.randint(1, 5)
        if real_number == number:
            multiplier = 1 + (real_number * 20) / 100
            return [round(bet * multiplier) - bet, real_number]
        else:
            return [-bet, real_number]
    
    @staticmethod
    def slots(bet: int, value: int) -> list:
        n = [random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)]
        if n[0] == n[1] == n[2] and n[0] != 7:
            return [round(bet * 10) - bet, n]
        elif n[0] == 7 and n[0] == n[1] == n[2]:
            return [round(bet * 51.25) - bet, n]
        elif (n[0] == n[1] and n[0] != 7) or (n[0] == n[2] and n[0] != 7) or (n[1] == n[2] and n[1] != 7):
            return [round(bet * 1.25) - bet, n]
        elif (n[0] == n[1] and n[0] == 7) or (n[0] == n[2] and n[0] == 7) or (n[1] == n[2] and n[1] == 7):
            return [round(bet * 3.75) - bet, n]
        else:
            return [-bet, n]
