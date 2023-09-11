# lib/cli.py

from helpers import (
    exit_program,
    list_games,
    find_game_by_name,
    list_games_by_producer,
    find_game_by_id,
    create_game,
    update_game,
    delete_game,
    list_reviews_by_game,
    list_reviews,
    find_review_by_title,
    find_review_by_id,
    create_review,
    update_review,
    delete_review
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            helper_1()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Some useful function")


if __name__ == "__main__":
    main()
