from models.__init__ import CURSOR, CONN


class Game:

    all = {}

    def __init__(self, name, genre, producer, id=None):
        self.id = id
        self.name = name
        self.genre = genre
        self.producer = producer

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
    def producer(self):
        return self._producer
    
    @producer.setter
    def producer(self, producer):
        if isinstance(producer, str) and len(producer):
            self._producer = producer
        else:
            raise ValueError(
                "Producer must be a non-empty string"
            )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of game instances """
        sql = """
            CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            name TEXT,
            genre TEXT,
            producer TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists game instances """
        sql = """
            DROP TABLE IF EXISTS games;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and genre values of the current game instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO games (name, genre, producer)
            VALUES (?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.genre, self.producer))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, genre, producer):
        """ Initialize a new game instance and save the object to the database """
        game = cls(name, genre, producer)
        game.save()
        return game

    def update(self):
        """Update the table row corresponding to the current game instance."""
        sql = """
            UPDATE games
            SET name = ?, genre = ?, producer = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.genre, self.producer, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current game instance,
        delete the dictionary entry, and reassign id attribute"""

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
        """Return a game object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        game = cls.all.get(row[0])
        if game:
            # ensure attributes match row values in case local instance was modified
            game.name = row[1]
            game.genre = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            game = cls(row[1], row[2])
            game.id = row[0]
            cls.all[game.id] = game
        return game

    @classmethod
    def get_all(cls):
        """Return a list containing a game object per row in the table"""
        sql = """
            SELECT *
            FROM games
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return a game object corresponding to the table row matching the specified primary key"""
        sql = """
            SELECT *
            FROM games
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return a game object corresponding to first table row matching specified name"""
        sql = """
            SELECT *
            FROM games
            WHERE name is ?
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def employees(self):
        """Return list of employees associated with current game"""
        from models.employee import Employee
        sql = """
            SELECT * FROM employees
            WHERE game_id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Employee.instance_from_db(row) for row in rows
        ]