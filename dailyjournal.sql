CREATE TABLE `Entry` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT NOT NULL,
    `entry` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL,
    `date` DATE NOT NULL,
    FOREIGN KEY (`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `Mood` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` TEXT NOT NULL
);

INSERT INTO `Entry` VALUES (null, 'Javascript', 'I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.', 1, "Wed Sep 15 2021 10:10:47 ");
INSERT INTO `Entry` VALUES (null, 'Python', "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake", 4,  "Wed Sep 15 2021 10:11:33 ");
INSERT INTO `Entry` VALUES (null, 'Javascript', "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.", 3, "Wed Sep 15 2021 10:14:05 ");

INSERT INTO `Mood` VALUES (null, "Happy");
INSERT INTO `Mood` VALUES (null, "Sad");
INSERT INTO `Mood` VALUES (null, "Angry");
INSERT INTO `Mood` VALUES (null, "Ok");

CREATE TABLE `Tags` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `subject` TEXT NOT NULL
);

CREATE TABLE `EntryTags` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id` INTEGER NOT NULL,
    `tag_id` INTEGER NOT NULL,
    FOREIGN KEY (`entry_id`) REFERENCES `Entry`(`id`),
    FOREIGN KEY (`tag_id`) REFERENCES `Tags`(`id`)
);

INSERT INTO `Tags` VALUES (null, 'API');
INSERT INTO `Tags` VALUES (null, 'components');
INSERT INTO `Tags` VALUES (null, 'fetch');

INSERT INTO `EntryTags` VALUES (null, 4, 2);
INSERT INTO `EntryTags` VALUES (null, 4, 3);
INSERT INTO `EntryTags` VALUES (null, 9, 2);
INSERT INTO `EntryTags` VALUES (null, 9, 1);

SELECT `entry` FROM `Entry` WHERE `entry` LIKE '%' + REPLACE(searchTerm, '%', '[%]') + '%';

SELECT * 
FROM Entry
LEFT OUTER JOIN EntryTags 
    ON Entry.id = EntryTags.entry_id
LEFT OUTER JOIN Tags
    ON EntryTags.tag_id = Tags.id

DELETE FROM EntryTags 
WHERE entry_id = 9

INSERT INTO `EntryTags` VALUES (null, 2, 2);
INSERT INTO `EntryTags` VALUES (null, 1, 1);

SELECT DISTINCT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            m.label mood_label,
            e.date,
            (
           SELECT GROUP_CONCAT(t.id)
    FROM EntryTags et
    JOIN Tags t ON et.tag_id = t.id
    WHERE et.entry_id = e.id) as tag_id
        FROM Entry e
        JOIN Mood m
            ON m.id = e.mood_id
        LEFT OUTER JOIN EntryTags et
                ON e.id = et.entry_id
        LEFT OUTER JOIN Tags t
                ON et.tag_id = t.id
        

    SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            m.label mood_label,
            e.date,
            t.id, tag_id,
            t.subject tag_subject
        FROM Entry e
        JOIN Mood m
            ON m.id = e.mood_id
        JOIN EntryTags et
                ON e.id = et.entry_id
        JOIN Tags t
                ON et.tag_id = t.id
        UNION
        SELECT e.id,
            e.concept,
            e.entry,
            e.mood_id,
            m.label mood_label,
            e.date,
            t.id, tag_id,
            t.subject tag_subject
        FROM Entry e
        JOIN Mood m
            ON m.id = e.mood_id
        JOIN EntryTags et
                ON e.id = et.entry_id
        JOIN Tags t
                ON et.tag_id = t.id
        WHERE  = e.id