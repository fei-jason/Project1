import Pokemon, csv, ast, random, math, time
from collections import deque

def load_pokemons_from_csv(pokemon_csv_file):
    moves_list = load_moves_from_csv('moves-data.csv')
    pokemons = []
    with open(pokemon_csv_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip header
        for row in reader:
            # pokemon moves into Pokemon.Moves objects to be added to Pokemon.Pokemon moves
            moves_data = ast.literal_eval(row[7])
            moves_data_list = [Pokemon.Moves(
                name = move.name,
                type = move.type,
                pp = move.pp,
                power = move.power,
                accuracy = move.accuracy
            ) for move in moves_list if move.name in moves_data]

            pokemon = Pokemon.Pokemon(
                name = row[0],
                type = row[1],
                hp = int(row[2]),
                attack = int(row[3]),
                defense = int(row[4]),
                moves = moves_data_list
                # moves = ast.literal_eval(row[7])
            )
            pokemons.append(pokemon)
    return pokemons

def load_moves_from_csv(moves_csv_file):
    moves = []
    with open(moves_csv_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # Skip header
        for row in reader:
            move = Pokemon.Moves(
                name = row[0],
                type = row[1],
                pp = int(row[4]),
                power = int(row[5]),
                accuracy = row[6]
            )
            moves.append(move)
    return moves

pokemon_list = load_pokemons_from_csv('pokemon-data.csv')

def assign_pokemon(pokemon_list):
    queue = []
    for i in range (0, 3): 
        random_index = random.randint(0, len(pokemon_list) - 1)
        queue.append(pokemon_list.pop(random_index))
    return queue  

player_pokemons = assign_pokemon(pokemon_list)
enemy_pokemons = assign_pokemon(pokemon_list)

#test below with professor's pokemon
# player_pokemons = [pokemon_list[21], pokemon_list[11], pokemon_list[0]]
# enemy_pokemons = [pokemon_list[66], pokemon_list[42], pokemon_list[31]]

type_chart = [ 
    #normal fire    water  elec    grass
    [1.0,   1.0,    1.0,   1.0,    1.0],  # normal
    [1.0,   0.5,    0.5,   1.0,    2.0],  # fire
    [1.0,   2.0,    0.5,   1.0,    0.5],  # water
    [1.0,   1.0,    2.0,   0.5,    0.5],  # electric
    [1.0,   0.5,    2.0,   1.0,    0.5],  # grass
    [1.0,   1.0,    1.0,   1.0,    1.0]   # others
    #indexes at 0
]

def match_type_int(type):
    match type:
        case 'Normal':
            return 0
        case 'Fire':
            return 1
        case 'Water':
            return 2
        case 'Electric':
            return 3
        case 'Grass':
            return 4
        case default:
            return 5
    
def get_type_matchup(attacker_index, defender_index):
    return type_chart[attacker_index][defender_index]

# move will be the base power of move
# attacker is the attack stat
# defender will be the defense stat
def get_damage(move, attacker, defender):
    STAB = 1
    if move.type == attacker.type:
        STAB = 1.5
    move_type = match_type_int(move.type)
    defender_type = match_type_int(defender.type)
    damage = move.power * (attacker.attack / defender.defense) * STAB * get_type_matchup(move_type, defender_type) * random.uniform(0.5, 1.0)
    return math.ceil(damage)

# --------------------------- GAME ----------------------------
winning_flag = 0

print("Welcome to Pokemon Colosseum!\n")
player_name = input("Enter player name: \n")
print(" ")
print(f"Team Rocket enters with {", ".join(items.name for items in enemy_pokemons[::-1])}")
print(f"Team {player_name} enters with {", ".join(items.name for items in player_pokemons[::-1])}")
print(" ")
print("Let the battle begin!")
current_player = random.choice([player_name, "Rocket"])
print(f"Coin toss goes to ---- Team {current_player} to start the attack!")
print("")

curr_pokemon = player_pokemons.pop()
curr_enemy = enemy_pokemons.pop()

# used a list to keep track of which moves have been used, backup_moves is used to restore the list once everything is used.
available_moves = []
backup_moves = []
for item in curr_pokemon.moves:
    available_moves.append(item)
    backup_moves.append(item)

# --------------------------- BATTLE ---------------------------
while True:
    # enemy attacks
    if current_player is not player_name:
        curr_enemy_move = random.sample(curr_enemy.moves, 1)
        print("\n")
        print(f"Team Rocket's {curr_enemy.name} cast '{curr_enemy_move[0].name}' to {curr_pokemon.name}")
        damage = get_damage(curr_enemy_move[0], curr_enemy, curr_pokemon)
        curr_pokemon.hp -= damage
        time.sleep(1)
        print(f"Damage to {curr_pokemon.name} is {damage} points")
        time.sleep(1)
        if curr_pokemon.hp <= 0:
            curr_pokemon.hp = 0
            print(f"Now {curr_enemy.name} has {curr_enemy.hp} HP and {curr_pokemon.name} faints back into pokeball")
            time.sleep(1)
            if not player_pokemons:
                # you lose
                break
            # player pokemon dies and resets the avaiable moves 
            curr_pokemon = player_pokemons.pop()
            available_moves = []
            backup_moves = []
            for item in curr_pokemon.moves:
                available_moves.append(item)
                backup_moves.append(item)

            print(f"\nNext for Team {player_name}, {curr_pokemon.name} enters battle!")
            time.sleep(1)
        else:
            print(f"Now {curr_enemy.name} has {curr_enemy.hp} HP and {curr_pokemon.name} has {curr_pokemon.hp} HP")
            time.sleep(1)
        current_player = player_name

    # player side attacks
    else:
        print("")
        time.sleep(1)
        print(f"Choose the moves for {curr_pokemon.name}:")
        
        for index, move in enumerate(available_moves):
            print(f"{index}. {move.name}")
        # for index, move in enumerate(curr_pokemon.moves):
        #     print(f"{index}. {move.name}")
        #     available_moves.append(move)
        #     backup_moves.append(move)

        while True:
            curr_move_index = input(f"Team {player_name}'s choice: ")
            if not curr_move_index.isdigit():
                print("Not valid choice try again.")
                continue
            curr_move_index = int(curr_move_index)
            if 0 <= curr_move_index < len(available_moves):
                break
            print("Not valid choice try again.")

        damage = get_damage(available_moves[curr_move_index], curr_pokemon, curr_enemy)
        print("")
        time.sleep(1)
        print(f"Team {player_name}'s {curr_pokemon.name} cast '{available_moves[curr_move_index].name}' to {curr_enemy.name}")
        time.sleep(1)
        print(f"Damage to {curr_enemy.name} is {damage} points")
        time.sleep(1)
        available_moves.pop(curr_move_index)
        curr_enemy.hp -= damage

        # once the available moves list is empty, restore using backup list
        if not available_moves:
            available_moves = backup_moves

        if curr_enemy.hp <= 0:
            curr_enemy.hp = 0
            print(f"Now {curr_pokemon.name} has {curr_pokemon.hp} HP and {curr_enemy.name} faints back into pokeball")
            time.sleep(1)
            if not enemy_pokemons:
                # you win
                winning_flag = 1
                break
            curr_enemy = enemy_pokemons.pop()
            print(f"\nNext for Team Rocket, {curr_enemy.name} enters battle!")
            time.sleep(1)
        else:
            # print(f"Now {curr_pokemon.name} has {curr_pokemon.hp} HP and {curr_enemy.name} has {curr_enemy.hp} HP")
            print(f"Now {curr_enemy.name} has {curr_enemy.hp} HP and {curr_pokemon.name} has {curr_pokemon.hp} HP")
            time.sleep(1)
        current_player = "Rocket"
        
    if (not player_pokemons or not enemy_pokemons) and (curr_pokemon.hp < 0 or curr_enemy.hp < 0):
        break

if winning_flag:
    print("\n")
    print(f"All of Team Rocket's Pokemon fainted, and Team {player_name} prevails!")
else:
    print("\n")
    print(f"All of Team {player_name}'s Pokemon fainted, and Team Rocket wins!")