from models.game import Game
from models.review import Review

def seed_database():
    Review.drop_table()
    Game.drop_table()
    Game.create_table()
    Review.create_table()

    # Create seed data
    rust = Game.create("Rust", " Survival", "Facepunch Studios")
    dayz = Game.create("DayZ", "Survival", "Bohemia Interactive")
    portal = Game.create("Portal", "Puzzle/Platformer", "Valve")
    ittr = Game.create("Into The Radius", "Survival/VR", "CM Games")
    Review.create("Why I love Rust", "Rust is fun :)", "SurvivalGameLover421", rust.id)
    Review.create("Why I love DayZ", "DayZ is fun :]", "SurvivalGameLover421", dayz.id)
    Review.create("Love it but has a ways to go", "God how I wish it was co-op", "VR enthusiast", ittr.id)
    Review.create("Good Game But Half-Life is better", 
                  "Was fun now back to half-life", "AllHailValve", portal.id)
    Review.create("Best game ever", "I played portal 1 and 2 in one sitting because this is the best game", 
                  "BigBrainGamer", portal.id)


seed_database()
print("Seeded database")
