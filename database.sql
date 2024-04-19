CREATE TABLE Criminal(
	Criminal_ID NUMERIC(6),
	Last VARCHAR(15),
	First VARCHAR(10),
	Street VARCHAR(30),
	City VARCHAR(20),
	State CHAR(2),
	Zip CHAR(5),
	Phone CHAR(10),
	V_status CHAR(1) DEFAULT ‘N’,
	P_status CHAR(1) DEFAULT ‘N’,
	PRIMARY KEY(Criminal_ID)
);

CREATE TABLE Alias(
	Alias_ID NUMERIC(6),
	Criminal_ID NUMERIC(6) REFERENCES Criminal(Criminal_ID),
	Alias VARCHAR(20),
	PRIMARY KEY(Alias_ID)
);

CREATE TABLE Crime(
	Crime_ID NUMERIC(9),
	Criminal_ID NUMERIC(6) REFERENCES Criminal(Criminal_ID),
	Classification CHAR(1) DEFAULT ‘U’,
	Date_charged DATE,
	Status CHAR(2) NOT NULL,
Hearing_date DATE CHECK (Hearing_date > Date_charged),
	Appeal_out_date DATE,
	PRIMARY KEY(Crime_ID)
	);

CREATE TABLE Prob_officer(
	Prob_ID NUMERIC(5),
	Last VARCHAR(15),
	First VARCHAR(10),
	Street VARCHAR(30),
	City VARCHAR(20),
	State CHAR(2),
	Zip CHAR(5),
	Phone CHAR(10),
	Email VARCHAR(30),
	Status CHAR(1) NOT NULL,
	PRIMARY KEY(Prob_ID)
);

CREATE TABLE Sentences(
	Sentence_ID NUMERIC(6),
	Criminal_ID NUMERIC(6) REFERENCES Criminal(Criminal_ID),
	Type CHAR(1),
	Prob_ID NUMERIC(5) REFERENCES Prob_officer(Prob_ID),
	Start_date DATE, 
	End_date DATE CHECK (End_date > Start_date),
	Violations NUMERIC(3) NOT NULL,
	PRIMARY KEY(Sentence_ID)
);

CREATE TABLE Crime_code(
	Crime_code NUMERIC(3) NOT NULL,
	Code_description VARCHAR(30) NOT NULL UNIQUE,
	PRIMARY KEY (Crime_code)
);

CREATE TABLE Crime_charges(
	Charge_ID NUMERIC(10),
	Crime_ID NUMERIC(9) REFERENCES Crime(Crime_ID),
	Crime_code NUMERIC(3) REFERENCES Crime_code(Crime_code),
	Charge_status CHAR(2),
	Fine_amount NUMERIC(7),
	Court_fee NUMERIC(7),
	Amount_paid NUMERIC(7),
	Pay_due_date DATE,
	PRIMARY KEY(Charge_ID)
);

CREATE TABLE Officer(
	Officer_ID NUMERIC(8),
	Last VARCHAR(15),
	First VARCHAR(10),
	Precinct CHAR(4) NOT NULL,
	Badge VARCHAR(14) UNIQUE,
	Phone VARCHAR (10),
	Status CHAR(1) DEFAULT ‘A’, 
	PRIMARY KEY (Officer_ID)
);

CREATE TABLE Crime_officers(
	Crime_ID NUMERIC(9) REFERENCES Crime(Crime_ID),
	Officer_ID NUMERIC(8) REFERENCES Officer(Officer_ID),
	PRIMARY KEY(Crime_ID, Officer_ID)
);

CREATE TABLE Appeals(
	Appeal_ID NUMERIC(5),
	Crime_ID NUMERIC(9) REFERENCES Crime(Crime_ID),
	Filing_date DATE, 
	Hearing_date DATE,
	Status CHAR(1) DEFAULT ‘P’,
	PRIMARY KEY (Appeal_ID)
);

CREATE TABLE users(
	username VARCHAR(20),
	password NUMERIC(8),
	id NUMERIC(8),
	User_type  VARCHAR(20),
	PRIMARY KEY (username, id)
);

INSERT INTO Criminal (Criminal_ID, Last, First, Street, City, State, Zip, Phone, V_status, P_status) VALUES
(000001, 'Nilay', 'Dey', '11 jacobs lane', 'Springfield', 'IL', '11110', '7181234567', 'Y', 'N'),
(000002, 'Steven', 'Lo', '21 jacobs lane', 'Riverside', 'CA', '11112', '7189876543', 'N', 'Y'),
(000003, 'Alex', 'Wu', '31 jacobs lane,', 'Philadelphia', 'PA', '11113', '7182345678', 'Y', 'Y'),
(000004, 'Brown', 'Jessica', '41 jacobs lane', 'Miami', 'FL', '11114', '7188765432', 'N', 'N'),
(000005, 'Jones', 'David', '51 jacobs lane', 'Portland', 'OR', '11115', '7183456789', 'Y', 'N'),
(000006, 'Matthew', 'Mary', '61 jacobs lane', 'San Diego', 'CA', '11116', '7184567890', 'Y', 'Y'),
(000007, 'Garcia', 'Daniel', '71 jacobs lane', 'New York', 'NY', '11117', '7185678901', 'N', 'N'),
(000008, 'Ror', 'Chris', '81 jacobs lane', 'Los Angeles', 'CA', '11118', '7186789012', 'Y', 'N'),
(000009, 'Her', 'Sarah', '91 jacobs lane', 'Chicago', 'IL', '11119', '7187890123', 'N', 'Y'),
(000010, 'Peters', 'Joe', '100 jacobs lane', 'Houston', 'TX', '10010', '7188901234', 'Y', 'N');

INSERT INTO Alias (Alias_ID, Criminal_ID, Alias) VALUES
(200001, 000001, 'Nils'),
(200002, 000002, 'Steve'),
(200003, 000003, 'Alexis'),
(200004, 000004, 'Browny'),
(200005, 000005, 'Jon'),
(200006, 000006, 'Mari'),
(200007, 000007, 'Gah'),
(200008, 000008, 'Chris'),
(200009, 000009, 'Sari'),
(200010, 000010, 'Joey');

INSERT INTO Crime (Crime_ID, Criminal_ID, Classification, Date_charged, Status, Hearing_date, Appeal_out_date) VALUES
(100000001, 000001, 'M', '2023-05-10', 'CL', '2023-06-20', '2023-07-15'),
(100000002, 000002, 'M', '2023-06-15', 'CA', '2023-07-01', '2023-07-15'),
(100000003, 000003, 'M', '2023-07-20', 'CA', '2023-08-25', '2023-09-20'),
(100000004, 000004, 'M', '2023-08-25', 'CL', '2023-09-10', '2023-09-20'),
(100000005, 000005, 'F', '2023-09-30', 'IA', '2023-10-20', '2023-11-15'),
(100000006, 000006, 'M', '2023-10-05', 'IA', '2023-11-01', '2023-11-15'),
(100000007, 000007, 'F', '2023-11-10', 'CL', '2023-12-15', '2024-01-10'),
(100000008, 000008, 'M', '2023-12-15', 'IA', '2024-01-01', '2024-01-10'),
(100000009, 000009, 'F', '2024-01-20', 'CL', '2024-02-25', '2024-03-20'),
(100000010, 000010, 'M', '2024-02-25', 'CA', '2024-03-15', '2024-04-01');



INSERT INTO Prob_officer (Prob_ID, Last, First, Street, City, State, Zip, Phone, Email, Status) VALUES
(30001, 'Patel', 'Pari', '01 Horse St', 'Springfield', 'IL', '11210', '5551234567', 'pari.patel@email.com', 'A'),
(30002, 'Patel', 'Priya', '11 Horse St', 'Riverside', 'CA', '11200', '5552345678', 'priya.patel@email.com', 'A'),
(30003, 'Moses', 'Mike', '12 Horse St', 'Seattle', 'WA', '11201', '5553456789', 'mike.moses@email.com', 'A'),
(30004, 'Nguyen', 'Linh', '13 Horse St', 'Miami', 'FL', '11202', '5554567890', 'linh.nguyen@email.com', 'A'),
(30005, 'Lee', 'Ji-Woo', '14 Horse St', 'Portland', 'OR', '11203', '5555678901', 'jiwoo.lee@email.com', 'A'),
(30006, 'Wong', 'Kai', '15 Horse St', 'San Diego', 'CA', '11204', '5556789012', 'kai.wong@email.com', 'A'),
(30007, 'Jackson', 'Malik', '16 Horse St', 'New York', 'NY', '11205', '5557890123', 'malik.jackson@email.com', 'A'),
(30008, 'Patel', 'Aisha', '17 Horse St', 'Los Angeles', 'CA', '11206', '5558901234', 'aisha.patel@email.com', 'A'),
(30009, 'Kim', 'Jin', '18 Horse St', 'Chicago', 'IL', '11207', '5559012345', 'jin.kim@email.com', 'A'),
(30010, 'Chen', 'Wei', '19 Horse St', 'Houston', 'TX', '11208', '5550123456', 'wei.chen@email.com', 'A');


INSERT INTO Sentences (Sentence_ID, CriminalID, Type, Prob_ID, Start_date, End_date, Violations) VALUES
(500001, 000001, 'J', 30001, '2023-06-10', '2023-07-15', 3),
(500002, 000002, 'J', 30002, '2023-07-15', '2023-09-20', 2),
(500003, 000003, 'H', 30003, '2023-08-20', '2023-09-15', 4),
(500004, 000004, 'H', 30004, '2023-09-25', '2023-10-30', 1),
(500005, 000005, 'P', 30005, '2023-10-30', '2023-12-05', 2),
(500006, 000006, 'P', 30006, '2023-11-05', '2023-12-10', 3),
(500007, 000007, 'H', 30007, '2023-12-10', '2024-01-15', 2),
(500008, 000008, 'J', 30008, '2024-01-15', '2024-03-20', 4),
(500009, 000009, 'H', 30009, '2024-02-20', '2024-04-25', 1),
(500010, 000010, 'P', 30010, '2024-03-25', '2024-05-30', 3);


INSERT INTO Crime_code (Crime_code, Code_description) VALUES
(001, 'Theft'),
(002, 'Hit and Run'),
(003, 'Burglary'),
(004, 'Robbery'),
(005, 'Drug Trafficking'),
(006, 'Fraud'),
(007, 'Vandalism'),
(008, 'DUI'),
(009, 'Violence'),
(010, 'Kidnapping');

INSERT INTO Crime_charges (Charge_ID, Crime_ID, Crime_code, Charge_status, Fine_amount, Court_fee, Amount_paid, Pay_due_date) VALUES
(2000000001, 100000001, 001, 'PD', 1000, 200, 800, '2023-08-15'),
(2000000002, 100000002, 002, 'PD', 1500, 300, 1200, '2023-09-20'),
(2000000003, 100000003, 003, 'GL', 2000, 400, 1600, '2023-10-25'),
(2000000004, 100000004, 004, 'GL', 2500, 500, 2000, '2023-11-30'),
(2000000005, 100000005, 005, 'PD', 3000, 600, 2400, '2023-12-05'),
(2000000006, 100000006, 006, 'PD', 3500, 700, 2800, '2024-01-10'),
(2000000007, 100000007, 007, 'NG', 4000, 800, 3200, '2024-02-15'),
(2000000008, 100000008, 008, 'NG', 4500, 900, 3600, '2024-03-20'),
(2000000009, 100000009, 009, 'PD', 5000, 1000, 4000, '2024-04-25'),
(2000000010, 100000010, 010, 'PD', 5500, 1100, 4400, '2024-05-30');

INSERT INTO Officer (Officer_ID, Last, First, Precinct, Badge, Phone, Status) VALUES
(10000021, 'Patel', 'Tom', '1234', '12345', '8551234567', 'A'),
(10000022, 'Pant', 'Jane', '5678', '23456', '8222345678', 'A'),
(10000023, 'Li', 'Alex', '9012', '34567', '8333456789', 'A'),
(10000024, 'Lee', 'Liz', '3456', '45678', '8444567890', 'A'),
(10000025, 'Brown', 'Ben', '7890', '56789', '8775678901', 'A'),
(10000026, 'Lo', 'Sara', '9012', '67890', '8666789012', 'A'),
(10000027, 'Jackson', 'Mike', '3456', '78901', '8997890123', 'A'),
(10000028, 'Pat', 'Ana', '1234', '89012', '8888901234', 'A'),
(10000029, 'Kim', 'Ken', '5678', '90123', '8779012345', 'A'),
(10000030, 'Chen', 'Tina', '9012', '01234', '8440123456', 'A');


INSERT INTO Crime_officers (Crime_ID, Officer_ID) VALUES
(100000001, 10000021),
(100000002, 10000022),
(100000003, 10000023),
(100000004, 10000024),
(100000005, 10000025),
(100000006, 10000026),
(100000007, 10000027),
(100000008, 10000028),
(100000009, 10000029),
(100000010, 10000030);

INSERT INTO Appeals (Appeal_ID, Crime_ID, Filing_date, Hearing_date, Status) VALUES
(1, 100000001, '2023-07-16', '2023-08-01', 'P'),
(2, 100000002, '2023-07-01', '2023-08-15', 'A'),
(3, 100000003, '2023-08-30', '2023-09-15', 'P'),
(4, 100000004, '2023-09-01', '2023-10-01', 'D'),
(5, 100000005, '2023-10-25', '2023-11-05', 'P'),
(6, 100000006, '2023-10-15', '2023-11-20', 'D'),
(7, 100000007, '2023-12-01', '2024-01-05', 'P'),
(8, 100000008, '2023-12-20', '2024-01-15', 'A'),
(9, 100000009, '2024-03-01', '2024-03-20', 'P'),
(10, 100000010, '2024-03-05', '2024-03-25', 'A');





