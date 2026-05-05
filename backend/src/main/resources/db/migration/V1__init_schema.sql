-- I am creating the initial risk_items table
CREATE TABLE IF NOT EXISTS risk_items (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    ai_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
