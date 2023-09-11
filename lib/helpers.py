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

def find_game_by_id():
    id_ = input("Please enter game id: ")
    game = Game.find_by_id(id_)
    print(game) if game else print(
        f"No game found with id {id_}"
    )

def create_game():
    name = input("Please enter a name: ")
    genre = input("Please enter the genre: ")
    producer = input("Please enter the producer: ")
    try:
        game = Game.create(name, genre, producer)
        print(f"Game successfully created: {game}")
    except Exception as exc:
        print("Error creating game: ", exc)

def update_game():
    id_ = input("Please enter the game id: ")
    if game := Game.find_by_id(id_):
        try:
            name = input("Please enter the new name: ")
            game.name = name
            genre = input("Please enter the new genre")
            game.genre = genre
            producer = input("Please enter the new producer: ")
            game.producer = producer

            game.update()
            print(f"Game successfully updated: {game}")
        except Exception as exc:
            print("Error updating game: ", exc)
    else:
        print(f"No game found by id {id_}")

def delete_game():
    id_ = input("Please enter the game's id: ")
    if game := Game.find_by_id(id_):
        game.delete()
        print(f"Game: {game}, id: {id_} successfully deleted")
    else:
        print(f"No game found by id {id_}")

def list_reviews_by_game():
    id_ = input("Please enter game id: ")
    if game := Game.find_by_id(id_):
        for review in game.reviews():
            print(review)

def list_reviews():
    reviews = Review.get_all()
    for review in reviews:
        print(review)

def find_review_by_title():
    title = input("Please enter the review's title: ")
    review = Review.find_by_title(title)
    print(review) if review else print(f"{title} not found")

def find_review_by_id():
    id_ = input("Please enter the review id: ")
    review = Review.find_by_id(id_)
    print(review) if review else print(f"Review {id_} not found")

def create_review():
    title = input("Please enter a title: ")
    summary = input("Please enter the summary: ")
    author = input("Please enter the Author: ")
    game_id_ = input("Please enter the associated game's id: ")
    try:
        review = Review.create(title, summary, author, Game.find_by_id(game_id_).id)
        print("Review successfully created: ", review)
    except Exception as exc:
        print("Error occurred", exc)

def update_review():
    id_ = input("Please enter the review's id")
    if review := Review.find_by_id(id_):
        try:
            title = input("Please enter a title: ")
            review.title = title
            summary = input("Please enter the new summary: ")
            review.summary = summary
            author = input("Please enter the new Author: ")
            review.author = author
            game_id_ = input("Please enter the new associated game's id: ")
            review.game_id = game_id_
            review.update()
            print("Review successfully updated: ", review)
        except Exception as exc:
            print("Error occurred: ", exc)
    else:
        print(f"No review found by id {id}")

def delete_review():
    id_ = input("Please enter the review's id: ")
    if review := Review.find_by_id(id_):
        review.delete()
        print("Review successfully deleted.")
    else:
        print(f"Review {id} not found")


def exit_program():
    print("Goodbye!")
    exit()
