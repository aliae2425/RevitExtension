-- DROP TABLE IF EXISTS User;
-- DROP TABLE IF EXISTS Folder;
-- DROP TABLE IF EXISTS Familly;
-- DROP TABLE IF EXISTS tag;
-- DROP TABLE IF EXISTS Favoris;
-- DROP TABLE IF EXISTS ItemTag;
-- DROP TABLE IF EXISTS ProjetItem;
-- DROP TABLE IF EXISTS Feedback;
-- DROP TABLE IF EXISTS Tag;
-- DROP TABLE IF EXISTS Projet;

-- item tables
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username varchar(150) NOT NULL UNIQUE,
    password varchar(150) NOT NULL,
    role BOOLEAN DEFAULT False,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

CREATE TABLE IF NOT EXISTS Folder (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(150) NOT NULL UNIQUE,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES Folder(id)
    );

CREATE TABLE IF NOT EXISTS Familly (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(150) NOT NULL UNIQUE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    url varchar(150) UNIQUE,
    description TEXT,
    sum_vote INTEGER DEFAULT 0,
    nb_vote INTEGER DEFAULT 0,
    Folder_id INTEGER,
    FOREIGN KEY (Folder_id) REFERENCES Folder(id)
    );


CREATE TABLE IF NOT EXISTS Projet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title varchar(150) NOT NULL UNIQUE
    );

CREATE TABLE IF NOT EXISTS Tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name varchar(150) NOT NULL UNIQUE
    );

CREATE TABLE IF NOT EXISTS Feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    _create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    post TEXT NOT NULL,
    image varchar(150),
    item_id INTEGER not NULL,
    responce_to INTEGER,
    FOREIGN KEY (item_id) REFERENCES Item(id),
    FOREIGN KEY (responce_to) REFERENCES Feedback(id)
    );



-- -- table de relation
CREATE TABLE IF NOT EXISTS Favoris (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    item_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (item_id) REFERENCES Item(id)
    );

CREATE TABLE IF NOT EXISTS ItemTag (
    item_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (item_id, tag_id),
    FOREIGN KEY (item_id) REFERENCES Item(id),
    FOREIGN KEY (tag_id) REFERENCES Tag(id)
    );

CREATE TABLE IF NOT EXISTS ProjetItem (
    projet_id INTEGER,
    item_id INTEGER,
    PRIMARY KEY (projet_id, item_id),
    FOREIGN KEY (projet_id) REFERENCES Projet(id),
    FOREIGN KEY (item_id) REFERENCES Item(id)
    );



