import sqlite3

CONN = sqlite3.connect('games.db')
CURSOR = CONN.cursor()
