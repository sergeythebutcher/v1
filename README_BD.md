CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id VARCHAR(255) UNIQUE NOT NULL,    -- Telegram ID пользователя
    email VARCHAR(255),                          -- Электронная почта пользователя
    google_token TEXT,                           -- Access-токен Google
    google_refresh_token TEXT,                   -- Refresh-токен Google
    facebook_token TEXT,                         -- Access-токен Facebook
    facebook_refresh_token TEXT,                 -- Refresh-токен Facebook
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Дата создания записи
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Дата обновления
);


CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    user_id INT NOT NULL, -- Владелец проекта
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE ad_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL, -- Проект, к которому привязан кабинет
    platform ENUM('google', 'facebook') NOT NULL, -- Платформа кабинета
    account_id VARCHAR(255) NOT NULL, -- Уникальный ID кабинета на платформе
    account_name VARCHAR(255) NOT NULL, -- Название кабинета
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);
CREATE TABLE budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT, -- Проект, к которому привязан бюджет
    ad_account_id INT, -- Рекламный кабинет (NULL для общего бюджета проекта)
    campaign_id VARCHAR(255), -- Рекламная кампания (NULL, если бюджет уровня кабинета или проекта)
    amount DECIMAL(10, 2) NOT NULL, -- Сумма бюджета
    operation_period_id INT NOT NULL, -- Операционный период
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (ad_account_id) REFERENCES ad_accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (operation_period_id) REFERENCES operation_periods(id) ON DELETE CASCADE
);

CREATE TABLE operation_periods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name ENUM('weekly', 'monthly', 'custom_2_weeks', 'custom_month', 'custom_weeks') NOT NULL, -- Тип периода
    start_date DATE NOT NULL, -- Дата начала (только для кастомных)
    end_date DATE NOT NULL,   -- Дата окончания (только для кастомных)
    project_id INT NOT NULL,  -- Проект, к которому относится период
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

);
CREATE TABLE ad_accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,                  -- ID связанного проекта
    platform ENUM('google', 'facebook') NOT NULL, -- Платформа (Google или Facebook)
    account_id VARCHAR(255) NOT NULL,         -- ID рекламного кабинета
    token TEXT NOT NULL,                      -- Токен доступа к API
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Дата создания записи
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Дата обновления
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE -- Связь с таблицей проектов
);
CREATE TABLE ad_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,                  -- ID рекламного кабинета
    campaign_id VARCHAR(255) NOT NULL,        -- ID рекламной кампании
    campaign_name VARCHAR(255),               -- Название кампании
    spend DECIMAL(10, 2),                     -- Затраты
    clicks INT,                               -- Количество кликов
    impressions INT,                          -- Количество показов
    date DATE NOT NULL,                       -- Дата данных
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Дата создания записи
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Дата обновления
    FOREIGN KEY (account_id) REFERENCES ad_accounts(id) ON DELETE CASCADE -- Связь с таблицей кабинетов
);
