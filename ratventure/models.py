import json
import random

with open('config.txt', 'r') as config_file:
    config = json.load(config_file)


class GameProgressModel:

    # max damage stacks with enemies killed and resets when running
    RAZE = 0
    # reduced damage from poison elements (rats)
    VIPER = 1
    # reduced chance of damage from wind elements (bugs)
    JETT = 2

    HERO_CHOICES = (
        (RAZE, 'RAZE'),
        (VIPER, 'VIPER'),
        (JETT, 'JETT'),
    )

    NO_ENEMY = 0
    RAT = 1
    BUG = 2
    BOSS = 3

    ENEMY_CHOICES = (
        (NO_ENEMY, 'NO_ENEMY'),
        (RAT, 'RAT'),
        (BUG, 'BUG'),
        (BOSS, 'BOSS'),
    )
    
    def __init__(self, hero_name, enemy_locations, enemies_killed, consecutive_enemies_killed, day_number, char_position, orb_location, town_locations, char_health, char_defence, enemy_type, initial_enemy_health, enemy_health, enemy_defence, sense_orb_cooldown, orb_status):

        self.hero_name = hero_name

        self.enemy_locations = enemy_locations

        self.enemies_killed = enemies_killed

        self.consecutive_enemies_killed = consecutive_enemies_killed

        self.day_number = day_number

        # [x,y],  0>>8 (x),  8>>0 (y)
        self.char_position = char_position

        # {[x,y],[x,y]},  0>>8 (x),  8>>0 (y)
        self.orb_location = orb_location

        self.town_locations = town_locations

        self.char_health = char_health
        self.char_defence = char_defence

        self.enemy_type = enemy_type

        self.initial_enemy_health = initial_enemy_health

        self.enemy_health = enemy_health
        self.enemy_defence = enemy_defence

        self.sense_orb_cooldown = sense_orb_cooldown
        self.orb_status = orb_status

    def model():

        with open('data.txt', 'r') as datafile:
            data = json.load(datafile)

        return GameProgressModel(hero_name=data['hero_name'],
                                 enemy_locations=data['enemy_locations'],
                                 enemies_killed=data['enemies_killed'],
                                 consecutive_enemies_killed=data['consecutive_enemies_killed'],
                                 day_number=data['day_number'],
                                 char_position=data['char_position'],
                                 orb_location=data['orb_location'],
                                 town_locations=data['town_locations'],
                                 char_health=data['char_health'],
                                 char_defence=data['char_defence'],
                                 enemy_type=data['enemy_type'],
                                 initial_enemy_health=data['initial_enemy_health'],
                                 enemy_health=data['enemy_health'],
                                 enemy_defence=data['enemy_defence'],
                                 sense_orb_cooldown=data['sense_orb_cooldown'],
                                 orb_status=data['orb_status'])
    
    def save(self):

        data = {'hero_name': self.hero_name,
                'enemy_locations': self.enemy_locations,
                'enemies_killed': self.enemies_killed,
                'consecutive_enemies_killed': self.consecutive_enemies_killed,
                'day_number': self.day_number,
                'char_position': self.char_position,
                'orb_location': self.orb_location,
                'town_locations': self.town_locations,
                'char_health': self.char_health,
                'char_defence': self.char_defence,
                'enemy_type': self.enemy_type,
                'initial_enemy_health': self.initial_enemy_health,
                'enemy_health': self.enemy_health,
                'enemy_defence': self.enemy_defence,
                'sense_orb_cooldown': self.sense_orb_cooldown,
                'orb_status': self.orb_status}

        with open('data.txt', 'w') as datafile:
            json.dump(data, datafile)

        return True

    def new_game(character):
        town_names = ['Pochinki', 'Haven', 'Georgopol', 'Ascent', 'Gulag']

        town_locations = dict()

        positions = list()

        def new_position():
            position = [random.randint(0, 7), random.randint(0, 7)]

            while position in positions or position == [0, 0] or position == [7, 7]:
                position = [random.randint(0, 7), random.randint(0, 7)]

            positions.append(position)

            return position

        for i in town_names:
            # check if items

            position = new_position()

            town_locations[i] = position

        town_locations['Base'] = [0, 0]

        orb_location = new_position()

        def neighbouring(town, char):
            if abs(town[0] - char[0]) <= 1:
                return True
            elif abs(town[1] - char[1]) <= 1:
                return True
            else:
                return False

        enemy_locations = {'rats': [], 'bugs': []}

        for x in range(0, 8):
            for y in range(0, 8):

                position = [x, y]

                if position == [0, 0] or position == [7, 7]:
                    pass
                elif position in town_locations.values():
                    pass
                else:
                    enemy_random = random.random()

                    if neighbouring(town_locations['Pochinki'], position):
                        if enemy_random <= 0.8:
                            enemy_type = 1
                        else:
                            enemy_type = 2

                    elif neighbouring(town_locations['Ascent'], position):
                        if enemy_random <= 0.8:
                            enemy_type = 2
                        else:
                            enemy_type = 1

                    else:
                        if enemy_random <= 0.5:
                            enemy_type = 1
                        else:
                            enemy_type = 2

                    if enemy_type == 1:
                        enemy_locations['rats'].append(position)
                    else:
                        enemy_locations['bugs'].append(position)

        if character == 0:
            char_health = config['raze_health']
            char_defence = config['raze_defence']
            
        elif character == 1:
            char_health = config['viper_health']
            char_defence = config['viper_defence']
            
        elif character == 2:
            char_health = config['jett_health']
            char_defence = config['jett_defence']

            
        model = GameProgressModel(hero_name=character,
                                  enemy_locations=enemy_locations,
                                  enemies_killed=0,
                                  consecutive_enemies_killed=0,
                                  day_number=1,
                                  char_position=[0, 0],
                                  orb_location=orb_location,
                                  town_locations=town_locations,
                                  char_health=char_health,
                                  char_defence=char_defence,
                                  enemy_type=0,
                                  initial_enemy_health=0,
                                  enemy_health=0,
                                  enemy_defence=0,
                                  sense_orb_cooldown=0,
                                  orb_status=0
                                  )

        model.save()

        return model

    def char_stats(self):
        hero_name = self.hero_name
        
        if self.orb_status:
            
            if hero_name == 0:
                consecutive_enemies_killed = self.consecutive_enemies_killed
                enemies_killed = self.enemies_killed

                min_damage = config["raze_min_damage"] + 5 + consecutive_enemies_killed + enemies_killed
                max_damage = config["raze_max_damage"] + 5 + consecutive_enemies_killed + enemies_killed

            elif hero_name == 1:
                enemies_killed = self.enemies_killed
                min_damage = config["viper_min_damage"] + 5 + enemies_killed
                max_damage = config["viper_max_damage"] + 5 + enemies_killed

            elif hero_name == 2:
                enemies_killed = self.enemies_killed
                min_damage = config["jett_min_damage"] + 5 + enemies_killed
                max_damage = config["jett_max_damage"] + 5 + enemies_killed

        else:
            if hero_name == 0:
                consecutive_enemies_killed = self.consecutive_enemies_killed
                enemies_killed = self.enemies_killed

                min_damage = config["raze_min_damage"] + consecutive_enemies_killed + enemies_killed
                max_damage = config["raze_max_damage"] + consecutive_enemies_killed + enemies_killed

            elif hero_name == 1:
                enemies_killed = self.enemies_killed
                min_damage = config["viper_min_damage"] + enemies_killed
                max_damage = config["viper_max_damage"] + enemies_killed

            elif hero_name == 2:
                enemies_killed = self.enemies_killed
                min_damage = config["jett_min_damage"] + enemies_killed
                max_damage = config["jett_max_damage"] + enemies_killed


        return {'name': self.HERO_CHOICES[self.hero_name][1], 'min_damage': min_damage, 'max_damage': max_damage, 'health': self.char_health, 'defence': self.char_defence}

    
    
    def enemy_encounter(self, initial=None):
        enemy_locations = self.enemy_locations

        if initial:

            if self.char_position in enemy_locations['rats']:
                enemy_type = 1
            elif self.char_position == [7, 7]:
                enemy_type = 3
            else:
                enemy_type = 2

            if enemy_type == 1:
                self.enemy_type = 1
                initial_enemy_health = random.randint(
                    config['rat_min_health'] + self.enemies_killed, config['rat_max_health'] + self.enemies_killed)
                self.enemy_health = initial_enemy_health
                self.initial_enemy_health = initial_enemy_health
                self.enemy_defence = config['rat_defence']

            elif enemy_type == 2:
                self.enemy_type = 2
                initial_enemy_health = random.randint(
                    config['bug_min_health'] + self.enemies_killed, config['bug_max_health'] + self.enemies_killed)
                self.enemy_health = initial_enemy_health
                self.initial_enemy_health = initial_enemy_health

                self.enemy_defence = config['bug_defence']

            elif enemy_type == 3:
                self.enemy_type = 3
                self.enemy_health = config['king_health']
                self.initial_enemy_health = config['king_health']

                self.enemy_defence = config['king_defence']

            self.save()
            
        else:
            enemy_type = self.enemy_type

        enemies_killed = self.enemies_killed

        if self.enemy_type == 1:
            damage = [config['rat_min_damage'] + enemies_killed, config['rat_max_damage'] + enemies_killed]

            if self.hero_name == 1:
                damage[0] -= config['viper_reduced_rat_damage']
                if damage[0] < 0:
                    damage[0] = 0

                damage[1] -= 1

        elif self.enemy_type == 2:

            damage = [config['bug_min_damage'] + enemies_killed, config['bug_max_damage'] + enemies_killed]

        elif self.enemy_type == 3:

            damage = config['king_damage']
            
            

        return {'enemy_damage': damage, 'enemy_type': ['Rat', 'Bug', 'Rat king'][enemy_type - 1], 'enemy_health': self.enemy_health, 'enemy_defence': self.enemy_defence}

    
    
    def enemy_damage(self):
        enemies_killed = self.enemies_killed

        if self.enemy_type == 1:
            damage = random.randint(config['rat_min_damage'] + enemies_killed, config['rat_max_damage'] + enemies_killed)

            if self.hero_name == 1:
                damage -= random.randint(1, config['viper_reduced_rat_damage'])

            if damage < 0:
                damage = 0

            return {'health': self.enemy_health, 'defence': self.enemy_defence, 'damage': damage, 'hit': 1}

        elif self.enemy_type == 2:

            hit = random.random()

            if self.hero_name == 3:

                if hit <= config['bug_accuracy']:
                    hit = 1
                else:
                    hit = 0

            else:

                if hit <= (config['bug_accuracy'] - config['jett_reduced_bug_accuracy']):
                    hit = 1
                else:
                    hit = 0

            damage = random.randint(config['bug_min_damage'] + enemies_killed, config['bug_max_damage'] + enemies_killed)

        elif self.enemy_type == 3:
            hit = 1
            damage = random.randint(config['king_damage'][0], config['king_damage'][1])

        return {'health': self.enemy_health, 'defence': self.enemy_defence, 'damage': damage, 'hit': hit}

    def attack(self, damage):
        initial_char_damage = random.randint(damage[0], damage[1])
        char_damage = initial_char_damage

        enemy_defence = self.enemy_defence
        enemy_health = self.enemy_health

        if self.enemy_type == 3 and self.orb_status == False:
            immune = True
        else:
            immune = False

        if not immune:
            while char_damage > 0:
                if enemy_defence > 0:
                    enemy_defence -= 1
                elif enemy_health > 0:
                    enemy_health -= 1
                char_damage -= 1

        self.enemy_defence = enemy_defence
        self.enemy_health = enemy_health

        if enemy_health > 0:

            enemy_data = self.enemy_damage()
            damage = enemy_data['damage']

            char_defence = self.char_defence
            char_health = self.char_health

            if enemy_data['hit'] == 1:

                while damage > 0:
                    if char_defence > 0:
                        char_defence -= 1
                    elif char_health > 0:
                        char_health -= 1
                    damage -= 1

                self.char_defence = char_defence
                self.char_health = char_health

            if char_health > 0:
                self.save()
                return {'immune': immune, 'enemy_data': enemy_data, 'char_data': {'defence': char_defence, 'health': char_health, 'damage': initial_char_damage}}
            
            else:
                self.save()
                return {'immune': immune, 'char_data': None, 'enemy_data': enemy_data}
        else:
            self.consecutive_enemies_killed += 1
            self.enemies_killed += 1
            self.save()
            return {'immune': immune, 'enemy_data': None, 'char_data': {'damage': initial_char_damage}}

    # town_options

    def day_past(self):
        if self.sense_orb_cooldown:
            self.sense_orb_cooldown = False

        self.day_number += 1
        self.save()

    def in_town(self):
        char_position = self.char_position
        town_locations = self.town_locations

        for key, value in enumerate(town_locations):
            if town_locations[value] == char_position:
                if value == 'Haven':
                    if self.char_health < 20:
                        self.char_health += 5
                        self.save()
                    print('Your health increased by 5, if your health is below 20')
                if value == 'Gulag':
                    if self.char_health > 2:
                        self.char_health -= 2
                        self.save()
                    print('Your health decreased by 2, if your health is above 2')

                return value
        return False

    def rest(self):
        print('Resting...')
        
        if self.hero_name == 0:
            self.char_health = config['raze_health']
        elif self.hero_name == 1:
            self.char_health = config['viper_health']
        elif self.hero_name == 2:
            self.char_health = config['jett_health']

        self.save()
        self.day_past()
        print('You are fully healed.')

    def sense_orb(self):
        
        if self.sense_orb_cooldown:
            print('This ability is still on cooldown. Return tomorrow!')
            return True

        else:
            self.sense_orb_cooldown = True
            self.save()

        char_position = self.char_position
        orb_location = self.orb_location

        if char_position == orb_location:
            self.orb_status = True
            self.save()
            print(
                'You found the Orb of Power!\nYour attack increases by 5!\nYour defence increases by 5!')
        else:
            # sense which direction to nearest orb
            x_diff = orb_location[0] - char_position[0]
            y_diff = orb_location[1] - char_position[1]

            if abs(x_diff) >= abs(y_diff):
                if x_diff > 0:
                    direction = 'West'
                else:
                    direction = 'East'
            else:
                if y_diff > 0:
                    direction = 'South'
                else:
                    direction = 'North'

            print('The orb is to your {}'.format(direction))

    # enemy_options

    def run(self):
        self.day_past()
        self.enemy_health = self.initial_enemy_health
        self.consecutive_enemies_killed = 0
        self.save()

    # order of code:
    # enemy_encounter > town options > enemy_data > map_data

    def map_data(self):
        hero_position = self.char_position
        hero_position = {'x': hero_position[0], 'y': hero_position[1]}

        town_l = self.town_locations
        town_locations = dict()

        for key, item in enumerate(town_l):
            town_locations[item] = {'x': town_l[item]
                                    [0], 'y': town_l[item][1]}

        return {'hero_position': hero_position, 'town_locations': town_locations}

    # Create your models here.
