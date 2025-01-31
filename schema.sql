CREATE TABLE users (
   user_id SERIAL PRIMARY KEY,
   first_name VARCHAR(50),
   last_name VARCHAR(50),
   username VARCHAR(50) NOT NULL,
   email VARCHAR(100) UNIQUE NOT NULL,
   password_hash VARCHAR(255) NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TABLE transactions (
--    id SERIAL PRIMARY KEY,
--    user_id INTEGER REFERENCES users(id),
--    amount DECIMAL(10,2) NOT NULL,
--    category VARCHAR(50),
--    description TEXT,
--    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE TABLE budgets (
--    id SERIAL PRIMARY KEY,
--    user_id INTEGER REFERENCES users(id),
--    category VARCHAR(50) NOT NULL,
--    amount DECIMAL(10,2) NOT NULL,
--    period VARCHAR(20) NOT NULL,
--    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );