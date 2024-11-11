current_gold_balance = 0
def set_starting_gold(current_level):
    global current_gold_balance
    current_gold_balance = current_level.gold_balance
    return

def can_afford(turret_cost):
    global current_gold_balance
    return current_gold_balance >= turret_cost

def deduct_gold(turret_cost, current_level):
    global current_gold_balance
    if can_afford(turret_cost):
        current_gold_balance -= turret_cost
        current_level.gold_balance -= turret_cost
    return
