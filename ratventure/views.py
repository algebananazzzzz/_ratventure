import os
from models import GameProgressModel


def ratventure(action=None):

    progress_model = GameProgressModel.model()
    
    print('\nDay {}'.format(progress_model.day_number))
    
    town_name = progress_model.in_town()
    
    if town_name:
        print('You are in {}'.format(town_name))
    else:
        print('You are out in the open.')
        
        if action != 'defeated':
        
            if action != 'run':
                return encounter(initial=True)
        
            
    print('1. View Character\n2. View Map\n3. Move\n4. Sense orb\n5. Exit Game')
    
    if town_name:
        print('6. Rest')
        max_limit = 6
    else:
        max_limit = 5
    
    user_action = validated_option('Your choice: ', 1, max_limit)
    
    
    if user_action == 1:
        char_stats = progress_model.char_stats()
        print('Name: {}'.format(char_stats['name']))
        print('Minimum damage: {}'.format(char_stats['min_damage']))
        print('Maximum damage: {}'.format(char_stats['max_damage']))
        print('Health: {}'.format(char_stats['health']))
        print('Defence: {}'.format(char_stats['defence']))
    elif user_action == 2:
        map_data = progress_model.map_data()
        interface(map_data)
        
    elif user_action == 3:
        map_data = progress_model.map_data()
        interface(map_data)
        
        while True:
            direction = validate_movement('Your move: ')

            char_position = progress_model.char_position

            x_axis = char_position[0]
            y_axis = char_position[1]

            if direction == 'w':
                if y_axis > 0:
                    char_position = [x_axis, y_axis - 1]
                    progress_model.day_past()
                    progress_model.char_position = char_position
                    progress_model.save()
                    print('You moved to the North')
                    break

            elif direction == 's':
                if y_axis < 7:
                    char_position = [x_axis, y_axis + 1]
                    progress_model.day_past()
                    progress_model.char_position = char_position
                    progress_model.save()
                    print('You moved to the South')
                    break

            elif direction == 'd':
                if x_axis < 7:
                    char_position = [x_axis + 1, y_axis]
                    progress_model.day_past()
                    progress_model.char_position = char_position
                    progress_model.save()
                    print('You moved to the East')
                    break

            elif direction == 'a':
                if x_axis > 0:
                    char_position = [x_axis - 1, y_axis]
                    progress_model.day_past()
                    progress_model.char_position = char_position
                    progress_model.save()
                    print('You moved to the West')
                    break

            print("You can't move out of the map!")

    elif user_action == 4:
        progress_model.sense_orb()
    elif user_action == 5:
        print('Exiting game')
        return 'exit'
    
    elif user_action == 6:
        progress_model.rest()
        
    if action == 'run':
        return encounter()
        
    if action == 'defeated' and user_action != 3:
        return 'defeated'
        
    return None


def encounter(initial=None):
    progress_model = GameProgressModel.model()
    
    if initial:
        enemy_encounter = progress_model.enemy_encounter(initial=True)
    else:
        enemy_encounter = progress_model.enemy_encounter()
        
    print('You encountered a {}'.format(enemy_encounter['enemy_type']))
    print('Enemy damage: {} to {}'.format(enemy_encounter['enemy_damage'][0], enemy_encounter['enemy_damage'][1]))
    print('Enemy health: {}'.format(enemy_encounter['enemy_health']))
    print('Enemy defence: {}'.format(enemy_encounter['enemy_defence']))
    
    print('\n1. Attack\n2. Run')
    
    action = validated_option('Your choice', 1,2)
    
    if action == 1:
        char_stats = progress_model.char_stats()
        damage = [char_stats['min_damage'], char_stats['max_damage']]
        attack = progress_model.attack(damage)
        
        if attack['enemy_data'] == None:
            char_data = attack['char_data']
            print('\nYou dealt {} damage to the enemy'.format(char_data['damage']))
            print('You defeated the enemy')
            
            if progress_model.enemy_type == 3:
                defeated(won=True)
        
                
        elif attack['char_data'] == None:
            defeated()
            return 'exit'
        else:
            if attack['immune']:
                print('\nYou do not have the Orb of Power - the Rat King is immune!')
                
            enemy_data = attack['enemy_data']
            char_data = attack['char_data']
            print('\nYou dealt {} damage to the enemy'.format(char_data['damage']))
            
            if enemy_data['hit']:
                print('\nOuch! The enemy dealt {} damage to you'.format(enemy_data['damage']))
                encounter()
            else:
                print('\nHA! The enemy missed his attack!')
            
        
        return 'defeated'
    
    elif action == 2:
        progress_model.run()
        return 'run'
    

def defeated(won=None):
    if won:
        print('\nThe Rat King is dead! You are victorious!\nCongratulations, you have defeated the Rat King!\nThe world is saved! You win!')

    else:
        open('data.txt', 'w')
        print('\nOOF! You dieded.\nGame over')
        return 'exit'
        
        
def validated_option(message, min_limit , max_limit):
    tries = 3
    
    while tries > 0:
        try:
            option = int(input(message))
            if min_limit <= option and option <= max_limit:
                return option
            else:
                raise
        except:
            print('Please choose within the range. Tries left: {}'.format(tries))
            tries -= 1
    
    raise KeyboardInterrupt
    
    
def validate_movement(message):
    tries = 3
    while tries > 0:
        try:
            option = input(message)
            if option in ['w', 'a', 's', 'd']:
                return option
            else:
                raise
        except:
            print('Please choose either w, a, s or d. Tries left: {}'.format(tries))
            tries -= 1
    
    raise KeyboardInterrupt
    
    
def interface(data):
    hero_position = data['hero_position']
    town_locations = data['town_locations']

    
    print('+---+---+---+---+---+---+---+---+')
    
    for y in range(8):
        row_string = '|'
        for x in range(8):
            if x == hero_position['x'] and y == hero_position['y']:
                hero_here = True
            else:
                hero_here = False
                
                
            if [x,y] == [7,7]:
                
                if hero_here:
                    row_string += 'H/K|'
                else:
                    row_string += ' K |'
            
            else:
                
                if {'x':x, 'y':y} in town_locations.values():
                    town_here = True
                else:
                    town_here = False


                if hero_here and not town_here:
                    row_string += ' H |'


                elif town_here and not hero_here:

                    for i in town_locations.keys():
                        if town_locations[i] == {'x':x, 'y':y}:
                            town_name = i[0]

                    row_string += ' {} |'.format(town_name)


                elif hero_here and town_here:

                    for i in town_locations.keys():
                        if town_locations[i] == {'x':x, 'y':y}:
                            town_name = i[0]

                    row_string += 'H/{}|'.format(town_name)


                else:
                    row_string += '   |'
            
        print(row_string)
        print('+---+---+---+---+---+---+---+---+')
