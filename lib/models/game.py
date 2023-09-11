from models.__init__ import CURSOR, CONN


class Game:

    all = {}

    def __init__(self, name, genre, publisher, id=None):
        self.id = id
        self.name = name
        self.genre = genre
        self.publisher = publisher

    def __repr__(self):
        return f"<Game {self.id}: {self.name}, {self.genre}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, genre):
        if isinstance(genre, str) and len(genre):
            self._genre = genre
        else:
            raise ValueError(
                "Genre must be a non-empty string"
            )

    @property
    def publisher(self):
        return self._publisher
    
    @publisher.setter
    def publisher(self, publisher):
        if isinstance(publisher, str) and len(publisher):
            self._publisher = publisher
        else:
            raise ValueError(
                "publisher must be a non-empty string"
            )

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            name TEXT,
            genre TEXT,
            publisher TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS games;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO games (name, genre, publisher)
            VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.genre, self.publisher))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, genre, publisher):
        game = cls(name, genre, publisher)
        game.save()
        return game

    def update(self):
        sql = """
            UPDATE games
            SET name = ?, genre = ?, publisher = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.genre, self.publisher, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM games
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        game = cls.all.get(row[0])
        if game:
            game.name = row[1]
            game.genre = row[2]
            game.publisher = row[3]
        else:
            game = cls(row[1], row[2], row[3])
            game.id = row[0]
            cls.all[game.id] = game
        return game

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM games
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM games
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM games
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    @classmethod
    def find_by_publisher(cls, publisher):
        sql = """
            SELECT *
            FROM games
            WHERE publisher is ?
        """

        rows = CURSOR.execute(sql, (publisher,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def reviews(self):
        from models.review import Review
        sql = """
            SELECT * FROM reviews
            WHERE game_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Review.instance_from_db(row) for row in rows
        ]