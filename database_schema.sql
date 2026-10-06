CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME
);

CREATE TABLE transaction (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(150) NOT NULL,
    amount FLOAT NOT NULL,
    type VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    transaction_date DATE NOT NULL,
    note VARCHAR(300),
    created_at DATETIME,
    FOREIGN KEY(user_id) REFERENCES user(id)
);