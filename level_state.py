class LevelState:
    def __init__(self, starting_gold):
        self.current_gold_balance = starting_gold

    def can_afford(self, turret_cost):
        return self.current_gold_balance >= turret_cost

    def deduct_gold(self, turret_cost):
        if self.can_afford(turret_cost):
            self.current_gold_balance -= turret_cost
            return True
        return False

