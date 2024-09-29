CREATE DATABASE "moviedb";
CREATE TABLE IF NOT EXISTS Directors (
    DirectorID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    BirthDate DATE CHECK (BirthDate < CURRENT_DATE),
    Nationality VARCHAR(50) NOT NULL,
    UNIQUE (FirstName, LastName)
);

CREATE TABLE IF NOT EXISTS Genres (
    GenreID SERIAL PRIMARY KEY,
    GenreName VARCHAR(30) NOT NULL UNIQUE,
    Description TEXT,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_genre_name CHECK (GenreName <> '')
);

CREATE TABLE IF NOT EXISTS Movies (
    MovieID SERIAL PRIMARY KEY,
    Title VARCHAR(100) NOT NULL,
    ReleaseYear INT CHECK (ReleaseYear >= 1888 AND ReleaseYear <= EXTRACT(YEAR FROM CURRENT_DATE)),
    DirectorID INT REFERENCES Directors(DirectorID) ON DELETE SET NULL ON UPDATE CASCADE,
    GenreID INT REFERENCES Genres(GenreID) ON DELETE CASCADE ON UPDATE CASCADE,
    Rating DECIMAL(3, 2) CHECK (Rating >= 0 AND Rating <= 10)
);

CREATE TABLE IF NOT EXISTS Actors (
                    ActorID SERIAL PRIMARY KEY,
                    FirstName VARCHAR(50) NOT NULL,
                    LastName VARCHAR(50) NOT NULL,
                    BirthDate DATE CHECK (BirthDate < CURRENT_DATE),
                    Nationality VARCHAR(50),
                    UNIQUE (FirstName, LastName)
                );

CREATE TABLE IF NOT EXISTS MovieActors (
                    MovieID INT REFERENCES Movies(MovieID) ON DELETE CASCADE ON UPDATE CASCADE,
                    ActorID INT REFERENCES Actors(ActorID) ON DELETE CASCADE ON UPDATE CASCADE,
                    Role VARCHAR(50),
                    BirthDate DATE CHECK (BirthDate < CURRENT_DATE),
                    Nationality VARCHAR(50),
                    PRIMARY KEY (MovieID, ActorID),
                    UNIQUE (MovieID, ActorID)
                );

CREATE TABLE IF NOT EXISTS Directors_backup AS TABLE Directors WITH NO DATA;
CREATE TABLE IF NOT EXISTS Genres_backup AS TABLE Genres WITH NO DATA;
CREATE TABLE IF NOT EXISTS Movies_backup AS TABLE Movies WITH NO DATA;
ALTER TABLE Directors ADD COLUMN Email VARCHAR(100);
ALTER TABLE Directors DROP COLUMN BirthDate;
ALTER TABLE Directors ALTER COLUMN Nationality SET DEFAULT 'Unknown';
CREATE TABLE IF NOT EXISTS Awards (
                    AwardID SERIAL PRIMARY KEY,
                    AwardName VARCHAR(100) NOT NULL,
                    Year INT CHECK (Year >= 1900 AND Year <= EXTRACT(YEAR FROM CURRENT_DATE))
                );
ALTER TABLE Awards ADD COLUMN Category VARCHAR(50);
ALTER TABLE Awards ADD COLUMN DirectorID INT REFERENCES Directors(DirectorID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Movies ALTER COLUMN Rating TYPE DECIMAL(4, 2);
ALTER TABLE Movies DROP COLUMN GenreID;
DROP TABLE IF EXISTS Genres CASCADE;