-- Data set: https://www.kaggle.com/lava18/google-play-store-apps

-- 1.0 Setup. Delete tables after every build iteration.
--
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS app,category,content_rating,app_genre,genre,pay_type,android_versionnumbers,temp_app_genre,temp_app_genre_name,temp_app,numbers;
SET FOREIGN_KEY_CHECKS=1;



--
-- 2.0 ENTITIES
-- Serve as lookup tables
--

--
-- 2.1 genre table
--
CREATE TABLE IF NOT EXISTS genre (
  genre_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  genre_name VARCHAR(25) NOT NULL UNIQUE,
  PRIMARY KEY (genre_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/genres_unique.csv'
INTO TABLE genre
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (genre_name)

  SET genre_name = IF(genre_name = '', NULL, TRIM(genre_name));


--
-- 2.2 pay_type table
--
CREATE TABLE IF NOT EXISTS pay_type (
  pay_type_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  pay_type_name VARCHAR(10) NOT NULL UNIQUE,
  PRIMARY KEY (pay_type_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/type.csv'
INTO TABLE pay_type
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  (pay_type_name)

  SET pay_type_name = IF(pay_type_name = '', NULL, TRIM(pay_type_name));



--
-- 2.3 android_version table
--
CREATE TABLE IF NOT EXISTS android_version (
  android_version_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  android_version VARCHAR(20) NOT NULL UNIQUE,
  PRIMARY KEY (android_version_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/android_ver.csv'
INTO TABLE android_version
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  (android_version)

  SET android_version = IF(android_version = '', NULL, TRIM(android_version));


--
-- 2.4 category table
--
CREATE TABLE IF NOT EXISTS category (
  category_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  category_name VARCHAR(20) NOT NULL UNIQUE,
  PRIMARY KEY (category_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/category.csv'
INTO TABLE category
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  (category_name)

  SET category_name = IF(category_name = '', NULL, TRIM(category_name));


-- 2.5 content_rating table
--
CREATE TABLE IF NOT EXISTS content_rating (
  content_rating_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  content_rating VARCHAR(20) NOT NULL UNIQUE,
  PRIMARY KEY (content_rating_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/content_rating.csv'
INTO TABLE content_rating
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY '\t'
  ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  (content_rating)

  SET content_rating = IF(content_rating = '', NULL, TRIM(content_rating));


--
-- 3.0 CORE ENTITIES AND M2M TABLES 
--

--
-- 3.1 Temporary game table
-- Note: 10841 rows data set.
--
CREATE TABLE temp_app (
  app_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  app_name VARCHAR(255) NOT NULL,
  rating VARCHAR(10) NULL,
  reviews INTEGER NULL,
  size VARCHAR(20) NULL,
  install VARCHAR(20) NULL,
  price VARCHAR(10) NULL,
  updated_time VARCHAR(20) NULL,
  current_version VARCHAR(50) NULL,
  category VARCHAR(20) NULL,
  pay_type VARCHAR(10) NULL,
  content_rating VARCHAR(20) NULL,
  android_version VARCHAR(20) NULL,
  PRIMARY KEY (app_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/source_without_genre.csv'
INTO TABLE temp_app
  CHARACTER SET utf8mb4
  -- FIELDS TERMINATED BY '\t'
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (app_name, category, rating, reviews,
  size, install, pay_type, price, content_rating,
  updated_time, current_version, android_version)

  SET app_name = IF(app_name = '', NULL, TRIM(app_name)),
  category = IF(category = '', NULL, TRIM(category)),
  rating = IF(rating = '', NULL, TRIM(rating)),
  reviews = IF(reviews = '', NULL, reviews),
  size = IF(size = '', NULL, TRIM(size)),
  install = IF(install = '', NULL, TRIM(install)),
  pay_type = IF(pay_type = '', NULL, TRIM(pay_type)),
  price = IF(price = '', NULL, TRIM(price)),
  content_rating = IF(content_rating = '', NULL, TRIM(content_rating)),
  updated_time = IF(updated_time = '', NULL, TRIM(updated_time)),
  current_version = IF(current_version = '', NULL, TRIM(current_version)),
  android_version = IF(android_version = '', NULL, TRIM(android_version));


--
-- 3.2 app table
--

CREATE TABLE app (
    app_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    app_name VARCHAR(255) NOT NULL,
    rating VARCHAR(10) NULL,
    reviews INTEGER NULL,
    size VARCHAR(20) NULL,
    install VARCHAR(20) NULL,
    price VARCHAR(10) NULL,
    updated_time VARCHAR(20) NULL,
    current_version VARCHAR(50) NULL,
    category_id INTEGER NULL,
    pay_type_id INTEGER NULL,
    content_rating_id INTEGER NULL,
    android_version_id INTEGER NULL,
    PRIMARY KEY (app_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (pay_type_id) REFERENCES pay_type(pay_type_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (content_rating_id) REFERENCES content_rating(content_rating_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (android_version_id) REFERENCES android_version(android_version_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)
  ENGINE=InnoDB
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;



INSERT IGNORE INTO app
  (app_name, category_id, rating, reviews,
  size, install, pay_type_id, price, content_rating_id,
  updated_time, current_version, android_version_id)

SELECT ta.app_name, c.category_id, ta.rating, ta.reviews,ta.size,ta.install,p.pay_type_id,
        ta.price,cr.content_rating_id,ta.updated_time,ta.current_version,a.android_version_id
 FROM temp_app ta
      LEFT JOIN android_version a
             ON TRIM(ta.android_version) = TRIM(a.android_version)
      LEFT JOIN content_rating cr
             ON TRIM(ta.content_rating) = TRIM(cr.content_rating)
      LEFT JOIN category c
             ON TRIM(ta.category) = TRIM(c.category_name)
      LEFT JOIN pay_type p
             ON TRIM(ta.pay_type) = TRIM(p.pay_type_name)
WHERE ta.app_name IS NOT NULL AND ta.app_name != ''
ORDER BY ta.app_name;





--
-- 3.3 temporary app_genre_name table
--

CREATE TABLE temp_app_genre_name (
  app_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  app_name VARCHAR(255) NOT NULL,
  genre_name VARCHAR(255) NULL,
  rating VARCHAR(10) NULL,
  reviews INTEGER NULL,
  size VARCHAR(20) NULL,
  install VARCHAR(20) NULL,
  price VARCHAR(10) NULL,
  updated_time VARCHAR(20) NULL,
  current_version VARCHAR(50) NULL,
  category VARCHAR(20) NULL,
  pay_type VARCHAR(10) NULL,
  content_rating VARCHAR(20) NULL,
  android_version VARCHAR(20) NULL,
  PRIMARY KEY (app_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE './output/googleplaystore_trimmed.csv'
INTO TABLE temp_app_genre_name
  CHARACTER SET utf8mb4
  -- FIELDS TERMINATED BY '\t'
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 LINES
  (app_name, category, rating, reviews,
  size, install, pay_type, price, content_rating, genre_name,
  updated_time, current_version, android_version)

  SET app_name = IF(app_name = '', NULL, TRIM(app_name)),
  genre_name = IF(genre_name = '', NULL, TRIM(genre_name)),
  category = IF(category = '', NULL, TRIM(category)),
  rating = IF(rating = '', NULL, TRIM(rating)),
  reviews = IF(reviews = '', NULL, reviews),
  size = IF(size = '', NULL, TRIM(size)),
  install = IF(install = '', NULL, TRIM(install)),
  pay_type = IF(pay_type = '', NULL, TRIM(pay_type)),
  price = IF(price = '', NULL, TRIM(price)),
  content_rating = IF(content_rating = '', NULL, TRIM(content_rating)),
  updated_time = IF(updated_time = '', NULL, TRIM(updated_time)),
  current_version = IF(current_version = '', NULL, TRIM(current_version)),
  android_version = IF(android_version = '', NULL, TRIM(android_version));








--
-- 3.4 temporary numbers table
-- Split comma-delimited developer values in order to populate a developer table
-- and a M2M game_developer associative table
-- Create temporary numbers table that will be used to split out comma-delimited lists of states.
--
CREATE TABLE numbers
  (
    num_id INTEGER NOT NULL UNIQUE,
    PRIMARY KEY (num_id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO numbers (num_id) VALUES
  (1), (2), (3), (4), (5), (6), (7), (8), (9), (10), (11), (12), (13), (14), (15);


-- All the part below had to be run in mysql workbench or it will fail,which is very strange!!!!
CREATE TABLE temp_app_genre
  (
    id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    app_name VARCHAR(255) NOT NULL,
    genre_name VARCHAR(255) NULL,
    PRIMARY KEY (id)
  )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;



INSERT IGNORE INTO temp_app_genre (app_name, genre_name)

SELECT DISTINCT g.app_name, TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(g.genre_name, ';',n.num_id), ';', -1)) AS genre_name
  FROM temp_app_genre_name g
       INNER JOIN numbers n 
               ON CHAR_LENGTH(g.genre_name) - CHAR_LENGTH(REPLACE(g.genre_name, ';', ''))
                  >= n.num_id - 1
  ORDER BY g.app_name, genre_name;
  


-- create table app_genre
CREATE TABLE IF NOT EXISTS app_genre (
  app_genre_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  app_id INTEGER NOT NULL,
  genre_id INTEGER NOT NULL,
  PRIMARY KEY (app_genre_id),
  FOREIGN KEY (app_id) REFERENCES app(app_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
    ON DELETE CASCADE ON UPDATE CASCADE
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO app_genre (app_id, genre_id)
SELECT a.app_id, g.genre_id
  FROM temp_app_genre tag
       LEFT JOIN app a
               ON TRIM(tag.app_name) = TRIM(a.app_name)
       LEFT JOIN genre g
                ON TRIM(tag.genre_name) = TRIM(g.genre_name)
 ORDER BY a.app_id, g.genre_id;






--
-- 4.0 Clean up
--


--
-- 4.1 DROP temporary tables
--
DROP TABLE numbers;
DROP TABLE temp_app_genre;
DROP TABLE temp_app_genre_name;
DROP TABLE temp_app;
