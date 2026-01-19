

CREATE TABLE students (
    Student_ID VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(50),
    Email VARCHAR(50),
    Department VARCHAR(50),
    Personality_type VARCHAR(50)
);
CREATE TABLE Skills (
    Student_ID VARCHAR(10),
    Skill VARCHAR(255),
    PRIMARY KEY (student_id , skill)
);
CREATE TABLE Users (
    User_Email VARCHAR(50) PRIMARY KEY,
    Password VARCHAR(255),
    Account_Created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE Event_Registration (
    Registration_ID VARCHAR(10) PRIMARY KEY,
    Student_ID VARCHAR(10),
    Event_ID VARCHAR(10),
    Attendance_code BLOB,
    Attendance ENUM('Absent', 'Present') DEFAULT 'Absent',
    Attendance_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    Rating TINYINT UNSIGNED CHECK (rating >= 1 AND rating <= 5),
    Comment VARCHAR(255),
    Payment_status ENUM('Unpaid', 'Success') DEFAULT 'Unpaid'
);
CREATE TABLE Events (
    Event_ID VARCHAR(10) PRIMARY KEY,
    Event_Name VARCHAR(50),
    Event_Date DATETIME,
    Event_details VARCHAR(255),
    Event_type VARCHAR(50),
    Event_fee INT,
    Venue VARCHAR(50),
    Budget INT
);
CREATE TABLE Volunteers (
    Volunteer_ID VARCHAR(10) PRIMARY KEY,
    Event_ID VARCHAR(10),
    Student_ID VARCHAR(10),
    Role VARCHAR(255),
    Budget_allocated INT
);
CREATE TABLE Expenses (
    Expenses_ID VARCHAR(10) PRIMARY KEY,
    Volunteer_ID VARCHAR(10),
    Description VARCHAR(255),
    Amount INT
);
CREATE TABLE Clubs (
    Club_ID VARCHAR(10) PRIMARY KEY,
    Club_Name VARCHAR(50),
    Club_Funds INT,
    Reg_fee INT,
    Advisor_Name VARCHAR(50),
    Advisor_Email VARCHAR(50),
    Advisor_Initial VARCHAR(50),
    Founded_Year YEAR
);
CREATE TABLE Clubs_Members (
    Club_ID VARCHAR(10),
    Student_ID VARCHAR(10),
    Role_ID VARCHAR(10),
    Joining_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (Club_Id , Student_ID)
);
CREATE TABLE Roles (
    Role_ID VARCHAR(10) PRIMARY KEY,
    Role VARCHAR(50) NOT NULL
);
CREATE TABLE Clubs_Registration (
    Club_ID VARCHAR(10),
    Student_ID VARCHAR(10),
    Payment_status ENUM('Unpaid', 'Success') DEFAULT 'Unpaid',
    PRIMARY KEY (Club_Id , Student_ID)
);
CREATE TABLE Clubs_Events (
    Club_ID VARCHAR(10),
    Event_ID VARCHAR(10),
    Role VARCHAR(50),
    Budget_share INT,
    PRIMARY KEY (Club_Id , Event_ID)
);
CREATE TABLE Assets (
    Asset_ID VARCHAR(10) PRIMARY KEY,
    Club_ID VARCHAR(10),
    Asset_Name VARCHAR(50),
    Category VARCHAR(50)
);
CREATE TABLE Loans (
    Loan_ID VARCHAR(10) PRIMARY KEY,
    Asset_ID VARCHAR(10),
    Lender_Club_ID VARCHAR(10),
    Lender_Student_ID VARCHAR(10),
    Borrower_Club_ID VARCHAR(10),
    Borrower_Student_ID VARCHAR(10),
    Borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    return_date TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE Alert (
    Alert_ID VARCHAR(10) PRIMARY KEY,
    Club_ID VARCHAR(10),
    Message VARCHAR(255),
    Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 

# Foreign Keys:
Alter table students
add constraint fk_students_users
foreign key(Email) references users(User_Email) on delete cascade;

Alter table skills
add constraint fk_skills_students
foreign key(student_id) references students(Student_id) on delete cascade;

Alter table volunteers
add constraint fk_volunteer_students
foreign key(student_id) references students(Student_id) on delete cascade;

Alter table volunteers
add constraint fk_volunteer_events
foreign key(event_id) references events(event_id) on delete cascade;

Alter table event_registration
add constraint fk_event_registrationr_students
foreign key(student_id) references students(Student_id) on delete cascade;


Alter table event_registration
add constraint fk_event_registrationr_events
foreign key(event_id) references events(event_id) on delete cascade;

Alter table expenses
add constraint fk_expenses_volunteer
foreign key(Volunteer_ID) references volunteers(Volunteer_ID) on delete set null;

Alter table Clubs_Events
add constraint fk_Clubs_Events_events
foreign key(event_id) references events(event_id) on delete cascade;

Alter table Alert
add constraint fk_Alert_club
foreign key(Club_ID) references Clubs(Club_ID) on delete cascade;

Alter table Loans
add constraint fk_Loans_Assets
foreign key (asset_id) references assets(Asset_id) on delete cascade;

alter table clubs_members
add constraint fk_club_mem_clubs
foreign key(Club_ID) references clubs(Club_ID) on delete cascade;

alter table clubs_members
add constraint fk_club_mem_role
foreign key(Role_ID) references roles(Role_ID) on delete cascade;

alter table clubs_members
add constraint fk_club_mem_students
foreign key(Student_ID) references students(Student_ID) on delete cascade;

alter table clubs_registration
add constraint fk_club_reg_student
foreign key(Student_ID) references students(Student_ID) on delete cascade;

alter table clubs_registration
add constraint fk_club_reg_clubs
foreign key(Club_ID) references clubs(Club_ID) on delete cascade;

alter table assets
add constraint fk_asset_clubs
foreign key(Club_ID) references clubs(Club_ID) on delete cascade;

alter table loans
add constraint fk_loan_lender_club_member
foreign key(lender_club_id,lender_student_id) references clubs_members(Club_id,Student_id) on delete set null;

alter table loans
add constraint fk_loan_borrower_club_member
foreign key(borrower_club_id,borrower_student_id) references clubs_members(Club_id,Student_id) on delete set null;

ALTER TABLE Users ADD COLUMN last_login DATETIME NULL;

