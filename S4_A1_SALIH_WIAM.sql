-- Task 2 - Create database by Wiam Salih
DROP DATABASE IF EXISTS SOCCER_LEAGUE_WS;
CREATE DATABASE SOCCER_LEAGUE_WS;
USE SOCCER_LEAGUE_WS;

-- Create tables for PLAYER, COACH, TEAM, PLAYER_TEAM, and COACH_TEAM
CREATE TABLE PLAYER (
    PLAYER_ID_WS INT AUTO_INCREMENT PRIMARY KEY,
    LAST_NAME_WS VARCHAR(17),
    FIRST_NAME_WS VARCHAR(17),
    MIDDLE_NAME_WS VARCHAR(17),
    BIRTH_YEAR_WS YEAR,
    JERSEY_WS INT,
    PARENT_PHONE_WS VARCHAR(14)
);

CREATE TABLE COACH (
    COACH_ID_WS INT AUTO_INCREMENT PRIMARY KEY,
    LAST_NAME_WS VARCHAR(17),
    FIRST_NAME_WS VARCHAR(17),
    MIDDLE_NAME_WS VARCHAR(17),
    BIRTH_YEAR_WS YEAR,
    START_YEAR_WS INT,
    EMAIL_WS VARCHAR(50)
);

CREATE TABLE TEAM (
    TEAM_ID_WS INT AUTO_INCREMENT PRIMARY KEY,
    NAME_WS VARCHAR(20)
);

CREATE TABLE PLAYER_TEAM (
    PLAYER_ID_WS INT,
    TEAM_ID_WS INT,
    SEASON_ID_WS INT,
    JERSEY_WS INT,
    PRIMARY KEY (PLAYER_ID_WS, SEASON_ID_WS),
    FOREIGN KEY (PLAYER_ID_WS) REFERENCES PLAYER (PLAYER_ID_WS),
    FOREIGN KEY (TEAM_ID_WS) REFERENCES TEAM (TEAM_ID_WS)
);

CREATE TABLE COACH_TEAM (
    COACH_ID_WS INT,
    TEAM_ID_WS INT,
    SEASON_ID_WS INT,
    PRIMARY KEY (COACH_ID_WS, TEAM_ID_WS, SEASON_ID_WS),
    FOREIGN KEY (COACH_ID_WS) REFERENCES COACH(COACH_ID_WS),
    FOREIGN KEY (TEAM_ID_WS) REFERENCES TEAM(TEAM_ID_WS)
);

-- Create tables for SEASON_WS, DIVISION_WS, CLUB_WS, and TEAM_WS
CREATE TABLE SEASON_WS (
    SEASON_ID_WS INT AUTO_INCREMENT PRIMARY KEY,
    NAME_WS VARCHAR(20),
    REGISTRATION_START_DATE_WS DATE,
    REGISTRATION_END_DATE_WS DATE,
    START_DATE_WS DATE,
    END_DATE_WS DATE
);

CREATE TABLE DIVISION_WS (
    DIVISION_ID_WS INT AUTO_INCREMENT PRIMARY KEY,
    SEASON_ID_WS INT,
    NAME_WS VARCHAR(20),
    AGE_GROUP_WS VARCHAR(5),
    SEX_WS VARCHAR(10),
    RANK_WS INT,
    CONTACT_EMAIL_WS VARCHAR(50),
    CONTACT_PHONE_WS VARCHAR(15),
    FOREIGN KEY (SEASON_ID_WS) REFERENCES SEASON_WS(SEASON_ID_WS)
);

CREATE TABLE CLUB_WS (
    CLUB_ID_WS INT AUTO_INCREMENT PRIMARY KEY,
    NAME_WS VARCHAR(23),
    CONTACT_EMAIL_WS VARCHAR(50),
    CONTACT_PHONE_WS VARCHAR(15),
    ABBREVIATION_WS VARCHAR(5) UNIQUE
);

CREATE TABLE TEAM_WS (
    TEAM_ID_WS INT AUTO_INCREMENT PRIMARY KEY,
    NAME_WS VARCHAR(20),
    SEASON_ID_WS INT,  
    BIRTH_YEAR_WS YEAR,
    SEX_WS VARCHAR(10),
    EMAIL_WS VARCHAR(50),
    PHONE_WS VARCHAR(15),
    FOREIGN KEY (SEASON_ID_WS) REFERENCES SEASON_WS(SEASON_ID_WS)
);

CREATE TABLE PLAYER_WS (
    PLAYER_ID_WS INT AUTO_INCREMENT PRIMARY KEY,
    TEAM_ID_WS INT,
    SEASON_ID_WS INT,
    LAST_NAME_WS VARCHAR(17),
    FIRST_NAME_WS VARCHAR(17),
    MIDDLE_NAME_WS VARCHAR(17),
    BIRTH_YEAR_WS DATE,
    JERSEY_WS INT,
    PARENT_PHONE_WS VARCHAR(14),
    FOREIGN KEY (TEAM_ID_WS) REFERENCES TEAM_WS (TEAM_ID_WS),
    FOREIGN KEY (SEASON_ID_WS) REFERENCES SEASON_WS (SEASON_ID_WS)
);

CREATE TABLE PLAYER_TEAM_WS (
    TEAM_ID_WS INT,
    SEASON_ID_WS INT,
    LAST_NAME_WS VARCHAR(17),
    FIRST_NAME_WS VARCHAR(17),
    MIDDLE_NAME_WS VARCHAR(17),
    BIRTH_YEAR_WS DATE,
    JERSEY_WS INT,
    PARENT_PHONE_WS VARCHAR(14),
    PRIMARY KEY (TEAM_ID_WS, SEASON_ID_WS)
);

CREATE TABLE COACH_WS (
    COACH_ID_WS INT AUTO_INCREMENT PRIMARY KEY,
    TEAM_ID_WS INT,
    SEASON_ID_WS INT,
    LAST_NAME_WS VARCHAR(17),
    FIRST_NAME_WS VARCHAR(17),
    MIDDLE_NAME_WS VARCHAR(17),
    BIRTH_YEAR_WS DATE,
    START_YEAR_WS INT,
    EMAIL_WS VARCHAR(50),
    FOREIGN KEY (TEAM_ID_WS) REFERENCES TEAM_WS (TEAM_ID_WS),
    FOREIGN KEY (SEASON_ID_WS) REFERENCES SEASON_WS (SEASON_ID_WS)
);

-- Task 4 - Add data by Wiam Salih
-- Add data to SEASON_WS table
INSERT INTO SEASON_WS (NAME_WS, REGISTRATION_START_DATE_WS, REGISTRATION_END_DATE_WS, START_DATE_WS, END_DATE_WS)
VALUES 
('FALL 2020', '2020-09-01', '2020-08-31', '2020-08-01', '2020-11-30'), 
('SPRING 2021', '2021-03-01', '2021-02-28', '2021-02-01', '2021-05-31'), 
('SUMMER 2019', '2019-06-01', '2019-05-31', '2019-05-01', '2019-08-31');

-- Add data to DIVISION_WS table
INSERT INTO DIVISION_WS (SEASON_ID_WS, NAME_WS, AGE_GROUP_WS, SEX_WS, RANK_WS, CONTACT_EMAIL_WS, CONTACT_PHONE_WS) 
VALUES 
(1, 'U14 Boys 1', 'U14', 'boys', 1, 'u14boys1@example.com', '1234567890'),
(1, 'U14 Boys 2', 'U14', 'boys', 2, 'u14boys2@example.com', '1234567891'),
(1, 'U14 Girls 1', 'U14', 'girls', 1, 'u14girls1@example.com', '1234567892'),
(1, 'U14 Girls 2', 'U14', 'girls', 2, 'u14girls2@example.com', '1234567893'),
(3, 'U12 Boys 1', 'U12', 'boys', 1, 'u12boys1@example.com', '1234567894'),
(3, 'U12 Boys 2', 'U12', 'boys', 2, 'u12boys2@example.com', '1234567895'),
(3, 'U12 Girls 1', 'U12', 'girls', 1, 'u12girls1@example.com', '1234567896'),
(3, 'U12 Girls 2', 'U12', 'girls', 2, 'u12girls2@example.com', '1234567897');

-- Add data to CLUB_WS table
INSERT INTO CLUB_WS (NAME_WS, CONTACT_EMAIL_WS, CONTACT_PHONE_WS, ABBREVIATION_WS)
VALUES 
('Patriots', 'patriots@example.com', '9876543210', 'PATR'), 
('Barcelona', 'barcelona@example.com', '9876543211', 'BARC'), 
('Tigers', 'tigers@example.com', '9876543212', 'TIGR');

-- Add data to TEAM_WS table
INSERT INTO TEAM_WS (NAME_WS, SEASON_ID_WS, BIRTH_YEAR_WS, SEX_WS, EMAIL_WS, PHONE_WS) VALUES  
('Blue', 1, 2007, 'boys', 'blue@example.com', '1112223334'), 
('Red', 1, 2008, 'boys', 'red@example.com', '1112223335'), 
('White', 2, 2009, 'boys', 'white@example.com', '1112223336'), 
('Yellow', 2, 2007, 'girls', 'yellow@example.com', '1112223337'), 
('Green', 3, 2008, 'girls', 'green@example.com', '1112223338');

-- Add data to PLAYER_WS table
INSERT INTO PLAYER_WS (TEAM_ID_WS, SEASON_ID_WS, LAST_NAME_WS, FIRST_NAME_WS, MIDDLE_NAME_WS, BIRTH_YEAR_WS, JERSEY_WS, PARENT_PHONE_WS)
VALUES
(1, 1, 'Doe', 'John', 'A', '2005-05-20', 10, '1234567890'),
(2, 1, 'Smith', 'Alice', 'B', '2006-08-15', 22, '1234567891'),
(3, 1, 'Johnson', 'Michael', 'C', '2007-03-10', 33, '1234567892'),
(4, 2, 'Williams', 'Emily', 'D', '2005-10-25', 12, '1234567893'),
(5, 2, 'Brown', 'Sophia', 'E', '2006-12-30', 25, '1234567894');

-- Add data to COACH_WS table
INSERT INTO COACH_WS (TEAM_ID_WS, SEASON_ID_WS, LAST_NAME_WS, FIRST_NAME_WS, MIDDLE_NAME_WS, BIRTH_YEAR_WS, START_YEAR_WS, EMAIL_WS) VALUES 
(1, 1, 'Anderson', 'David', 'X', '1980-02-15', 2015, 'david@example.com'),
(2, 1, 'Martinez', 'Maria', 'Y', '1975-07-20', 2018, 'maria@example.com'),
(3, 2, 'Garcia', 'Carlos', 'Z', '1982-09-10', 2016, 'carlos@example.com'),
(4, 2, 'Taylor', 'Jessica', 'W', '1978-11-05', 2017, 'jessica@example.com'),
(5, 3, 'Lewis', 'Matthew', 'V', '1985-04-30', 2019, 'matthew@example.com');

-- Task 5 - Query the data by Wiam Salih
-- Count all the players registered for a team in Spring 2021
SELECT COUNT(*) AS TOTAL_PLAYERS
FROM PLAYER_TEAM_WS
WHERE SEASON_ID_WS = (SELECT SEASON_ID_WS FROM SEASON_WS WHERE NAME_WS = 'SPRING 2021');

-- Count all the coaches hired by a club in SPRING 2019
SELECT COUNT(*) AS TOTAL_COACHES
FROM COACH_WS
WHERE SEASON_ID_WS = (SELECT SEASON_ID_WS FROM SEASON_WS WHERE NAME_WS = 'SPRING 2019');

-- List the player(s) that have the biggest jersey number
SELECT *
FROM PLAYER_WS
WHERE JERSEY_WS = (SELECT MAX(JERSEY_WS) FROM PLAYER_WS);

-- List the most experienced coaches
SELECT *
FROM COACH_WS
WHERE START_YEAR_WS = (SELECT MIN(START_YEAR_WS) FROM COACH_WS);