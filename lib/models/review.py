from models.__init__ import CURSOR, CONN
from models.game import Game


class Review:

    all = {}

    def __init__(self, title, summary, author, game_id, id=None):
        self.id = id
        self.title = title
        self.summary = summary
        self.author = author
        self.game_id = game_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.title} || {self.summary} || {self.author}, " +
            f"game ID: {self.game_id}>"
        )

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and len(title):
            self._title = title
        else:
            raise ValueError(
                "title must be a non-empty string"
            )

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, summary):
        if isinstance(summary, str) and len(summary):
            self._summary = summary
        else:
            raise ValueError(
                "summary must be a non-empty string"
            )

    @property
    def game_id(self):
        return self._game_id

    @game_id.setter
    def game_id(self, game_id):
        if type(game_id) is int and Game.find_by_id(game_id):
            self._game_id = game_id
        else:
            raise ValueError(
                "game_id must reference a game in the database")
        
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, author):
        if isinstance(author, str) and len(author):
            self._author = author
        else:
            raise ValueError(
                "Author must be a non-empty string"
            )

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            title TEXT,
            summary TEXT,
            author TEXT,
            game_id INTEGER,
            FOREIGN KEY (game_id) REFERENCES games(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
                INSERT INTO reviews (title, summary, author, game_id)
                VALUES (?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.title, self.summary, self.author, self.game_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        sql = """
            UPDATE reviews
            SET title = ?, summary = ?, author = ?, game_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.title, self.summary,
                             self.author, self.game_id, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM reviews
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def create(cls, title, summary, author, game_id):
        review = cls(title, summary, author, game_id)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        review = cls.all.get(row[0])
        if review:
            review.title = row[1]
            review.summary = row[2]
            review.author = row[3]
            review.game_id = row[4]
        else:
            review = cls(row[1], row[2], row[3], row[4])
            review.id = row[0]
            cls.all[review.id] = review
        return review

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM reviews
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM reviews
            WHERE id = ?
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_title(cls, title):
        sql = """
            SELECT *
            FROM reviews
            WHERE title is ?
        """

        row = CURSOR.execute(sql, (title,)).fetchone()
        return cls.instance_from_db(row) if row else None