-- MySQL Database Creation Script
-- MySQL 数据库创建脚本

-- Create database
-- 创建数据库
CREATE DATABASE IF NOT EXISTS network_monitor
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Create a database user (optional, but recommended)
-- 创建数据库用户（可选，但推荐）
-- IMPORTANT: Replace 'your_secure_password_here' with a strong password
-- 重要：将 'your_secure_password_here' 替换为强密码
-- Password requirements: At least 12 characters, including uppercase, lowercase, numbers, and special characters
-- 密码要求：至少12个字符，包括大写字母、小写字母、数字和特殊字符
CREATE USER IF NOT EXISTS 'network_monitor_user'@'localhost' 
    IDENTIFIED BY 'your_secure_password_here';

-- Grant privileges to the user
-- 授予用户权限
GRANT ALL PRIVILEGES ON network_monitor.* TO 'network_monitor_user'@'localhost';

-- If you need to allow remote connections, create another user
-- 如果需要允许远程连接，创建另一个用户
-- IMPORTANT: Replace 'your_secure_password_here' with a strong password
-- 重要：将 'your_secure_password_here' 替换为强密码
-- CREATE USER IF NOT EXISTS 'network_monitor_user'@'%' 
--     IDENTIFIED BY 'your_secure_password_here';
-- GRANT ALL PRIVILEGES ON network_monitor.* TO 'network_monitor_user'@'%';

-- Flush privileges to apply changes
-- 刷新权限以应用更改
FLUSH PRIVILEGES;

-- Use the database
-- 使用数据库
USE network_monitor;

-- Show database information
-- 显示数据库信息
SELECT 
    SCHEMA_NAME as 'Database',
    DEFAULT_CHARACTER_SET_NAME as 'Charset',
    DEFAULT_COLLATION_NAME as 'Collation'
FROM information_schema.SCHEMATA 
WHERE SCHEMA_NAME = 'network_monitor';

-- Note: The actual tables will be created automatically by Flask-SQLAlchemy
-- when you run the application or use init_db.py
-- 注意：实际的表将由 Flask-SQLAlchemy 在运行应用程序或使用 init_db.py 时自动创建
