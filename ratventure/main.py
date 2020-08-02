from models import GameProgressModel
from views import ratventure, encounter, defeated, validated_option, validate_movement, interface
import os, json


with open('config.txt', 'r') as config_file:
    config = json.load(config_file)


if __name__ == "__main__":
    
    print('Welcome to Ratventure!\n1. New Game')
    
    if os.stat('data.txt').st_size != 0:
        print('2. Resume Game')
        
    print('3. Exit Game')
    
    game_option = validated_option('Enter your choice', 1 , 3)
    
    if game_option == 1:
        print('Characters:\nRaze is a self sufficient hero with her damage stacking with every consecutive kills she get.\nViper is a toxic hero that receives lesser damage from poisonous rats.\nJett is a unpredictable speedy hero that has a fewer chance of getting attacks from bugs, and a higher maximum damage.\n')
        game_option = validated_option('Show detailed statistics? 1 for yes and 0 for no', 0,1)
        
        if game_option == 1:
            print('Raze:\nMaximum initial damage: {}\nDamage stack: 1 for every consecutive kill\nMinimum initial damage: {}\nInitial health points: {}\nInitial defence: {}\n'.format(config['raze_max_damage'], config['raze_min_damage'], config['raze_health'], config['raze_defence']))
            print('Viper:\nMaximum initial damage: {}\nMinimum initial damage: {}\nReduced damage from rats: 1 to {}\nInitial health points: {}\nInitial defence: {}\n'.format(config['viper_max_damage'], config['viper_min_damage'], config['viper_reduced_rat_damage'], config['viper_health'], config['viper_defence']))
            print('Jett:\nMaximum initial damage: {}\nMinimum initial damage: {}\n{} more chance of dodging an attack from a bug\nInitial health points: {}\nInitial defence: {}\n'.format(config['jett_max_damage'], config['jett_min_damage'],  config['jett_reduced_bug_accuracy'], config['jett_health'], config['jett_defence']))
        
        game_option = validated_option('Choose your character: 1 for Raze, 2 for Viper, 3 for Jett', 1, 3)
        
        GameProgressModel.new_game(game_option-1)
        
        game_action = None
        
        
        while True:
            game_action = ratventure(game_action)
        
            if game_action == 'exit':
                break
        
        
        
    elif game_option == 2:
        print('Continuing from previous checkpoint')
        
        game_action = None
        
        while True:
            game_action = ratventure(game_action)
        
            if game_action == 'exit':
                break
    
    elif game_option == 3:
        print('Exited game')
        