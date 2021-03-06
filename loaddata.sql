CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');

INSERT INTO Tags ('label') VALUES ('JavaScript');
UPDATE Reactions SET image_url = "???? " WHERE label = "happy";

INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');
INSERT INTO Posts ("user_id", "category_id", "title", "publication_date", "image_url", "content", "approved") VALUES (1, 1, "works?", 01102022, "google.com", "ordered?", 1)

INSERT INTO Tags ('label') VALUES ('Python');

INSERT INTO PostTags ('post_id', 'tag_id') VALUES (2, 7);
INSERT INTO PostTags ('post_id', 'tag_id') VALUES (2, 16);

INSERT INTO Tags ('label') VALUES ('Python');
INSERT INTO Tags ('label') VALUES ('SQL');
INSERT INTO Tags ('label') VALUES ('JavaScript');

INSERT INTO Comments ('post_id', 'author_id', 'content') VALUES (1, 1, 'Science is pretty cool.');
SELECT
  ep.id,
  ep.post_id,
  ep.tag_id,
  t.id,
  t.label
FROM PostTags ep
Left Join Tags t
ON t.id = ep.tag_id   

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

INSERT INTO PostReactions ('user_id', 'reaction_id', 'post_id') VALUES (1,1,14);
INSERT INTO PostReactions ('user_id', 'reaction_id', 'post_id') VALUES (1,1,13);


            SELECT
                pr.id,
                pr.user_id,
                pr.reaction_id,
                pr.post_id,
                r.label,
                r.image_url
            FROM PostReactions pr
            Left Join Reactions r
            ON pr.reaction_id = r.id
            WHERE pr.post_id =1


INSERT INTO Reactions ('label', 'image_url') VALUES ('laugh', '????');
INSERT INTO Reactions ('label', 'image_url') VALUES ('love', '????');
INSERT INTO Reactions ('label', 'image_url') VALUES ('angry', '????');
INSERT INTO Reactions ('label', 'image_url') VALUES ('wow', '????');
INSERT INTO Reactions ('label', 'image_url') VALUES ('cry', '????');