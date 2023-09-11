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
            list_games()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. List all Games")
    print("2. Find a Game by its name")
    print("3. List Games by Producer")
    print("4. Find a Game by its ID")
    print("5. Add new Game to database")
    print("6. Update an existing Game")
    print("7. Delete an existing Game")
    print("8. List all Reviews")
    print("9. Find a Review by its title")
    print("10. Find a Review by its ID")
    print("11. Create a new Review")
    print("12. Update an existing Review")
    print("13. Delete an existing Review")
    print("14. List Reviews by Game ID")


if __name__ == "__main__":
    main()
