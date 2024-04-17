CREATE TABLE SimpleBet (
    ID INT NOT NULL UNIQUE,
    ParticipantSpan VARCHAR,
    MarketDescription VARCHAR,
    FixtureName VARCHAR,
    MultipleBetID INT NOT NULL,
    FOREIGN KEY (MultipleBetID) REFERENCES MultipleBet(ID)
    PRIMARY KEY (ID)
);

CREATE TABLE MultipleBet (
    ID INT NOT NULL UNIQUE,
    StakeDesc VARCHAR,
    HeaderText VARCHAR,
    BetInformationText VARCHAR,
    PRIMARY KEY (ID)
);

--CREATE TABLE SimpleBetList (
--    ID INT NOT NULL UNIQUE,
--    SimpleBetID INT NOT NULL,
--    MultipleBetID INT NOT NULL,
--    FOREIGN KEY (SimpleBetID) REFERENCES SimpleBet(ID),
--    FOREIGN KEY (MultipleBetID) REFERENCES MultipleBet(ID)
--);

--DROP TABLE SimpleBet;
--DROP TABLE MultipleBet;
--DROP TABLE SimpleBetList;
