CREATE TABLE IF NOT EXISTS `users` (
  `id` integer PRIMARY KEY,
  `username` varchar(255),
  `role` varchar(255),
  `created_at` timestamp,
  `favoris` integer
);

CREATE TABLE IF NOT EXISTS `item`(
  `id` integer PRIMARY KEY,
  `name` varchar(255),
  `password` varchar(255),
  `url` varchar(255),
  `Folder_id` int,
  `sum_vote` int,
  `nb_vote` int,
  `_autor_id` int,
  `_changeBy_id` int,
  `_create_at` timestamp,
  `_lastup_date` timestamp
);

CREATE TABLE IF NOT EXISTS `Feedback` (
  `id` int PRIMARY KEY,
  `_create_at` timestamp,
  `post` text,
  `state` int,
  `item_id` int,
  `responce_to` int
);

CREATE TABLE IF NOT EXISTS `Folder` (
  `id` integer PRIMARY KEY,
  `title` varchar(255),
  `parent_id` int
);

CREATE TABLE IF NOT EXISTS `Favoris` (
  `id` int PRIMARY KEY,
  `user_id` int,
  `item_id` int
);

CREATE TABLE IF NOT EXISTS `Projet` (
  `id` int PRIMARY KEY,
  `item_id` int,
  `title` int
);

CREATE TABLE IF NOT EXISTS `Itemtags` (
  `id` int PRIMARY KEY,
  `item_id` int,
  `tag_id` int
);

CREATE TABLE IF NOT EXISTS `Tag` (
  `id` int PRIMARY KEY,
  `title` varchar(255),
  `color` eint
);

ALTER TABLE `Folder` ADD FOREIGN KEY (`id`) REFERENCES `Folder` (`parent_id`);

ALTER TABLE `item` ADD FOREIGN KEY (`Folder_id`) REFERENCES `Folder` (`id`);

ALTER TABLE `item` ADD FOREIGN KEY (`_autor_id`) REFERENCES `users` (`id`);

ALTER TABLE `item` ADD FOREIGN KEY (`_changeBy_id`) REFERENCES `users` (`id`);

ALTER TABLE `Favoris` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `Favoris` ADD FOREIGN KEY (`item_id`) REFERENCES `item` (`id`);

ALTER TABLE `Projet` ADD FOREIGN KEY (`item_id`) REFERENCES `item` (`id`);

ALTER TABLE `Itemtags` ADD FOREIGN KEY (`item_id`) REFERENCES `item` (`id`);

ALTER TABLE `Itemtags` ADD FOREIGN KEY (`tag_id`) REFERENCES `Tag` (`id`);

ALTER TABLE `Feedback` ADD FOREIGN KEY (`item_id`) REFERENCES `item` (`id`);

ALTER TABLE `Feedback` ADD FOREIGN KEY (`responce_to`) REFERENCES `Feedback` (`id`);
