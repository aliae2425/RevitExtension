-- CREATE TABLE IF NOT EXISTS Folder (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name varchar(150) NOT NULL UNIQUE,
--     parent_id INTEGER,
--     FOREIGN KEY (parent_id) REFERENCES Folder(id)
--     );

-- CREATE TABLE IF NOT EXISTS Item (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name varchar(150) NOT NULL UNIQUE,
--     description TEXT
--     url varchar(150) UNIQUE,
--     folder_id INTEGER,
--     FOREIGN KEY (folder_id) REFERENCES Folder(id)
--     );

-- -- insert into Folder (name) values ('root');
-- -- insert into Folder (name, parent_id) values ('folder1', 1);
-- -- insert into Folder (name, parent_id) values ('folder2', 1);
-- -- insert into Folder (name, parent_id) values ('folder3', 2);
-- -- INSERT into Item (name, folder_id) values ('item1', 3);

SELECT Item.name, Folder.name
FROM Item INNER JOIN Folder ON Item.folder_id = Folder.id;

