DROP VIEW IF EXISTS vstatus;
DROP TABLE IF EXISTS Manufacturer;
DROP TABLE IF EXISTS Vaccine;
DROP TABLE IF EXISTS manufacturedBy;
DROP TABLE IF EXISTS Batch;
DROP TABLE IF EXISTS Transportation;
DROP TABLE IF EXISTS Organization;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS Shift;
DROP TABLE IF EXISTS Vaccination;
DROP TABLE IF EXISTS Attendance;
DROP TABLE IF EXISTS Patient;
DROP TABLE IF EXISTS Diagnose;
DROP TABLE IF EXISTS Symptom;


CREATE TABLE Manufacturer(
    manufID TEXT NOT NULL,
    country TEXT NOT NULL,
    phone TEXT NOT NULL,
    PRIMARY KEY (manufID)
);
        
CREATE TABLE Vaccine(
    ID TEXT NOT NULL,
    name TEXT NOT NULL,
    doses INT NOT NULL,
    tempMin REAL NOT NULL,
    tempMax REAL NOT NULL,
    PRIMARY KEY (id),
    CHECK(doses>=1)
);

CREATE TABLE manufacturedBy(
    manufID TEXT NOT NULL,
    vaccID TEXT NOT NULL,
    PRIMARY KEY (manufID, vaccID)
);

CREATE TABLE Batch(
    batchID TEXT NOT NULL,
    amount INT NOT NULL,
    vaccID TEXT NOT NULL,
    manufID TEXT NOT NULL,
    prodDate DATE NOT NULL,
    expirDate DATE NOT NULL,
    org TEXT NOT NULL,
    PRIMARY KEY (batchID),
    CHECK(amount>=1)
);

CREATE TABLE Transportation(
    batchID TEXT NOT NULL,
    depDate DATE NOT NULL,
    arrDate DATE NOT NULL,
    depOrg TEXT NOT NULL,
    arrOrg TEXT NOT NULL,
    PRIMARY KEY (batchID, depOrg)
);

CREATE TABLE Organization(
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    telephone TEXT NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE Staff(
    ssNo TEXT NOT NULL,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    phone TEXT NOT NULL,
    status INT NOT NULL,
    role TEXT NOT NULL, 
    org TEXT NOT NULL,
    PRIMARY KEY (ssNo),
    CHECK(role IN ('nurse','doctor'))
);

CREATE TABLE Shift(
    org TEXT NOT NULL,
    weekday INT NOT NULL,
    ssNo TEXT NOT NULL,
    PRIMARY KEY (org, weekday, ssNo),
    CHECK(weekday>=0 AND weekday<=7)
);

CREATE TABLE Vaccination(
    eventDate DATE NOT NULL,
    organization TEXT NOT NULL,
    batchID TEXT NOT NULL,
    PRIMARY KEY (eventDate, organization)
);

CREATE TABLE Attendance(
    ssNo TEXT NOT NULL,
    eventDate DATE NOT NULL,
    org TEXT NOT NULL,
    PRIMARY KEY (ssNo, eventDate, org)
);

CREATE TABLE Patient(
    ssNo TEXT NOT NULL,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    gender TEXT NOT NULL,
    PRIMARY KEY (ssNo),
    CHECK(gender IN ('F','M'))
);

CREATE TABLE Diagnose(
    patient TEXT NOT NULL,
    symptom TEXT NOT NULL,
    reportDate DATE NOT NULL,
    PRIMARY KEY (patient, symptom, reportDate)
);

CREATE TABLE Symptom(
    name TEXT NOT NULL,
    critical BOOLEAN NOT NULL,
    PRIMARY KEY (name)
);

