CREATE TABLE users (
   user_id SERIAL PRIMARY KEY,
   first_name VARCHAR(50),
   last_name VARCHAR(50),
   email VARCHAR(100) UNIQUE NOT NULL,
   password_hash VARCHAR(255) NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TABLE budget_sections (
--    section_id SERIAL PRIMARY KEY,      
--    user_id INTEGER NOT NULL,
--    name VARCHAR(100) NOT NULL,
--    start_date DATE,
--    end_date DATE,
--    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

CREATE TABLE budget_items (
   item_id SERIAL PRIMARY KEY,
   section_name VARCHAR(100) NOT NULL,
   user_id INTEGER NOT NULL,
   name VARCHAR(100) NOT NULL,
   amount DECIMAL(10,2) NOT NULL,
   type VARCHAR(10) CHECK (type IN ('income', 'expense')) NOT NULL,
   start_date DATE NOT NULL,
   end_date DATE,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   CHECK (end_date IS NULL OR end_date >= start_date)
);

CREATE TABLE item_transactions (
   transaction_id SERIAL PRIMARY KEY,
   user_id INTEGER NOT NULL,
   item_id INTEGER NOT NULL,
   description VARCHAR(100) NOT NULL,
   amount DECIMAL(10,2) NOT NULL,
   type VARCHAR(10) CHECK (type IN ('income', 'expense')) NOT NULL,
   date DATE NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ALTER TABLE budget_sections
-- ADD CONSTRAINT fk_budget_sections_user
-- FOREIGN KEY (user_id) 
-- REFERENCES users(user_id) 
-- ON DELETE CASCADE;

ALTER TABLE budget_items
ADD CONSTRAINT fk_budget_items_user
FOREIGN KEY (user_id) 
REFERENCES users(user_id) 
ON DELETE CASCADE;

ALTER TABLE item_transactions
ADD CONSTRAINT fk_item_transactions_item
FOREIGN KEY (item_id) 
REFERENCES budget_items(item_id) 
ON DELETE CASCADE;