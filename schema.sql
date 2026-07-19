CREATE TABLE persons (
    sanction_id VARCHAR(20) PRIMARY KEY,
    first_name TEXT,
    second_name TEXT,
    third_name TEXT,
    fourth_name TEXT,
    full_name TEXT,
    dob TEXT,
    pob TEXT,
    nationality TEXT,
    listed_on TEXT
);

CREATE TABLE aliases (
    id SERIAL PRIMARY KEY,
    sanction_id VARCHAR(20),
    alias_type VARCHAR(20),
    alias_name TEXT
);

CREATE TABLE passports (
    id SERIAL PRIMARY KEY,
    sanction_id VARCHAR(20),
    passport_detail TEXT
);

CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    sanction_id VARCHAR(20),
    address TEXT
);

CREATE TABLE amendments (
    id SERIAL PRIMARY KEY,
    sanction_id VARCHAR(20),
    amendment_date TEXT
);