DROP TABLE IF EXISTS goal_history;
DROP TABLE IF EXISTS goals;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id CHAR(36) PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  role VARCHAR(255),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE goals (
  id CHAR(36) PRIMARY KEY,
  department VARCHAR(255) NOT NULL,
  statement TEXT NOT NULL,
  criteria TEXT NOT NULL,
  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 10),
  assessment TEXT NOT NULL,
  last_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_modified_by CHAR(36),
  comments TEXT,
  FOREIGN KEY (last_modified_by) REFERENCES users(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE goal_history (
  id CHAR(36) PRIMARY KEY,
  goal_id CHAR(36) NOT NULL,
  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 10),
  assessment TEXT NOT NULL,
  modified_by CHAR(36) NOT NULL,
  modified_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (goal_id) REFERENCES goals(id),
  FOREIGN KEY (modified_by) REFERENCES users(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS notifications (
  id CHAR(36) PRIMARY KEY,
  table_name VARCHAR(255) NOT NULL,
  action VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;