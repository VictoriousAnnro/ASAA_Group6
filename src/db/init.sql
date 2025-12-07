-- This script should initialize the MySQL DB, the tables and insert some data
-- create DB if not exists
CREATE DATABASE IF NOT EXISTS mysqlDatabase;

USE mysqlDatabase;

-- create tables if not exist
CREATE TABLE IF NOT EXISTS Cars (
    model varchar(100) PRIMARY KEY,
    engine varchar(100),
    color varchar(50),
    price int
);

CREATE TABLE IF NOT EXISTS Orders (
    orderID int PRIMARY KEY,
    model varchar(100),
    engine varchar(100),
    color varchar(50),
    price int
);

CREATE TABLE IF NOT EXISTS OrderStatus (
    orderID varchar(150) PRIMARY KEY,
    status varchar(50), -- add check bc can only be in 3 states (ready, inProcess, done)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- This will automatically create a timestamp with the current time, for any newly inserted row. You only need to specify OrderID and Status when inserting
);


/*CREATE TABLE IF NOT EXISTS Cars (
    chassisID int PRIMARY KEY,
    carName varchar(50), -- string is not a valid type, must be varchar
    ImageID varchar(250)
);

CREATE TABLE IF NOT EXISTS Engines (
    engineID int PRIMARY KEY,
    size int,
    horsepower int
);

CREATE TABLE IF NOT EXISTS Interior (
    interiorID int PRIMARY KEY,
    coverMaterial varchar(100),
    color varchar(100)
);

CREATE TABLE IF NOT EXISTS Paint (
    paintID int PRIMARY KEY,
    color varchar(20), 
    finish varchar(100)
);

CREATE TABLE IF NOT EXISTS Orders (
    orderID int PRIMARY KEY,
    chassisID int REFERENCES Cars(chassisID),
    engineID int REFERENCES Engines(engineID),
    interiorID int REFERENCES Interior(interiorID),
    paintID int REFERENCES Paint(paintID)
);

CREATE TABLE IF NOT EXISTS OrderStatus (
    orderID int PRIMARY KEY,
    status varchar(50), -- add check bc can only be in 3 states (ready, inProcess, done)
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- This will automatically create a timestamp with the current time, for any newly inserted row. You only need to specify OrderID and Status when inserting
);

-- populate with data
INSERT INTO Cars VALUES (1, "toy-yoda", "path");
INSERT INTO Cars VALUES (2, "niisan", "path");
INSERT INTO Cars VALUES (3, "cungadero", "path");

INSERT INTO Engines VALUES (1, 10, 20);
INSERT INTO Engines VALUES (2, 5, 30);
INSERT INTO Engines VALUES (3, 2, 11);

INSERT INTO Interior VALUES (1, "leather", "rust");
INSERT INTO Interior VALUES (2, "velvet", "green");
INSERT INTO Interior VALUES (3, "cotton", "grey");

INSERT INTO Paint VALUES (1, "green", "glossy");
INSERT INTO Paint VALUES (2, "blue", "metallic");
INSERT INTO Paint VALUES (3, "red", "matte");
INSERT INTO Paint VALUES (4, "yellow", "clearcoat");
INSERT INTO Paint VALUES (5, "black", "clearcoat");*/