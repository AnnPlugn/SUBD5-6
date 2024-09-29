import psycopg2
from psycopg2 import sql
import tkinter.messagebox


class DataBase:
    def __init__(self, db):
        self.name_db = db

    def check_db(self):
        try:
            conn = psycopg2.connect(host="localhost",
                                     user="postgres",
                                     password="root",
                                     database=self.name_db,
                                     options="-c search_path=public")
            print("Вы подключились")
            tkinter.messagebox.showinfo("Вы подключились", self.name_db)
        except psycopg2.OperationalError:
            conn = psycopg2.connect(host="localhost",
                                    user="postgres",
                                    password="root",
                                    options="-c search_path=public")
            conn.autocommit = True  # Включаем автокоммит для создания базы данных
            cursor = conn.cursor()
            cursor.execute(sql.SQL("CREATE DATABASE {} WITH ENCODING 'UTF8'").format(sql.Identifier(self.name_db)))
            print("Вы создали БД")
            tkinter.messagebox.showinfo("Вы создали БД", self.name_db)
            cursor.close()
            conn.close()
            return self.check_db()

        return conn

    def con_db(self):
        return psycopg2.connect(host="localhost",
                                user="postgres",
                                password="root",
                                database=self.name_db)

    def create_tables(self):
        with self.con_db() as conn:
            with conn.cursor() as cursor:

                create_directors = """
                CREATE TABLE IF NOT EXISTS Directors (
                    DirectorID SERIAL PRIMARY KEY,
                    FirstName VARCHAR(50) NOT NULL,
                    LastName VARCHAR(50) NOT NULL,
                    BirthDate DATE CHECK (BirthDate < CURRENT_DATE),
                    Nationality VARCHAR(50) NOT NULL,
                    UNIQUE (FirstName, LastName)
                );
                """

                create_genres = """
                CREATE TABLE IF NOT EXISTS Genres (
                    GenreID SERIAL PRIMARY KEY,
                    GenreName VARCHAR(30) NOT NULL UNIQUE,
                    Description TEXT,
                    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT chk_genre_name CHECK (GenreName <> '')
                );
                """

                create_movies = """
                CREATE TABLE IF NOT EXISTS Movies (
                    MovieID SERIAL PRIMARY KEY,
                    Title VARCHAR(100) NOT NULL,
                    ReleaseYear INT CHECK (ReleaseYear >= 1888 AND ReleaseYear <= EXTRACT(YEAR FROM CURRENT_DATE)),
                    DirectorID INT REFERENCES Directors(DirectorID) ON DELETE SET NULL ON UPDATE CASCADE,
                    GenreID INT REFERENCES Genres(GenreID) ON DELETE CASCADE ON UPDATE CASCADE,
                    Rating DECIMAL(3, 2) CHECK (Rating >= 0 AND Rating <= 10)
                );
                """

                create_actors = """
                CREATE TABLE IF NOT EXISTS Actors (
                    ActorID SERIAL PRIMARY KEY,
                    FirstName VARCHAR(50) NOT NULL,
                    LastName VARCHAR(50) NOT NULL,
                    BirthDate DATE CHECK (BirthDate < CURRENT_DATE),
                    Nationality VARCHAR(50),
                    UNIQUE (FirstName, LastName)
                );
                """

                create_movie_actors = """
                CREATE TABLE IF NOT EXISTS MovieActors (
                    MovieID INT REFERENCES Movies(MovieID) ON DELETE CASCADE ON UPDATE CASCADE,
                    ActorID INT REFERENCES Actors(ActorID) ON DELETE CASCADE ON UPDATE CASCADE,
                    Role VARCHAR(50),
                    BirthDate DATE CHECK (BirthDate < CURRENT_DATE),
                    Nationality VARCHAR(50),
                    PRIMARY KEY (MovieID, ActorID),
                    UNIQUE (MovieID, ActorID)
                );
                """


                create_update_trigger_function = """
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.UpdatedAt = NOW();
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                """

                create_update_trigger = """
                CREATE TRIGGER update_genres_updated_at
                BEFORE UPDATE ON Genres
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
                """

                # Выполнение запросов
                try:
                    cursor.execute(create_directors)
                    cursor.execute(create_genres)
                    cursor.execute(create_movies)
                    cursor.execute(create_actors)
                    cursor.execute(create_movie_actors)

                    # Создание функции и триггера
                    cursor.execute(create_update_trigger_function)
                    cursor.execute(create_update_trigger)

                except Exception as e:
                    print(f"Ошибка при создании таблиц: {e}")
                    tkinter.messagebox.showerror("Ошибка", f"Не удалось создать таблицы: {e}")

    def backup_tables(self):
        with self.con_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS Directors_backup AS TABLE Directors WITH NO DATA;
                CREATE TABLE IF NOT EXISTS Genres_backup AS TABLE Genres WITH NO DATA;
                CREATE TABLE IF NOT EXISTS Movies_backup AS TABLE Movies WITH NO DATA;
                """)

    def add_email_column(self):
        with self.con_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                ALTER TABLE Directors ADD COLUMN Email VARCHAR(100);
                """)

    def drop_birthdate_column(self):
        with self.con_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                ALTER TABLE Directors DROP COLUMN BirthDate;
                """)

    def set_default_nationality(self):
        with self.con_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                ALTER TABLE Directors ALTER COLUMN Nationality SET DEFAULT 'Unknown';
                """)

    def create_awards_table(self):
        with self.con_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS Awards (
                    AwardID SERIAL PRIMARY KEY,
                    AwardName VARCHAR(100) NOT NULL,
                    Year INT CHECK (Year >= 1900 AND Year <= EXTRACT(YEAR FROM CURRENT_DATE))
                );
                """)

    def add_category_column(self):
        with self.con_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                ALTER TABLE Awards ADD COLUMN Category VARCHAR(50);
                """)

    def add_foreign_key_director(self):
        with self.con_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                ALTER TABLE Awards ADD COLUMN DirectorID INT REFERENCES Directors(DirectorID) ON DELETE CASCADE ON UPDATE CASCADE;
                """)

    def modify_rating_column(self):
        with self.con_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                ALTER TABLE Movies ALTER COLUMN Rating TYPE DECIMAL(4, 2);
                """)

    def drop_genre_id_column(self):
        with self.con_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                ALTER TABLE Movies DROP COLUMN GenreID;
                """)

    def drop_genres_table(self):
        with self.con_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                DROP TABLE IF EXISTS Genres CASCADE;
                """)

    def modify_database(self):
        self.backup_tables()
        self.add_email_column()
        self.drop_birthdate_column()
        self.set_default_nationality()
        self.create_awards_table()
        self.add_category_column()
        self.add_foreign_key_director()
        self.modify_rating_column()
        self.drop_genre_id_column()
        self.drop_genres_table()
