from models.game import Game
from models.review import Review

def list_games():
    games = Game.get_all()
    print("List of games:")
    for game in games:
        print(game)

def find_game_by_name():
    name = input("Please enter the game's name: ")
    game = Game.find_by_name(name)
    print(game) if game else print(
        f"Game {name} not found"
    )

def list_games_by_producer():
    producer = input("Please enter a producer: ")
    games = Game.find_by_producer(producer)
    print(games) if games else print(
        f"No games found produced by {producer}"
    )

def exit_program():
    print("Goodbye!")
    exit()
