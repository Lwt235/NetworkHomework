-- PostgreSQL Database Creation Script
-- PostgreSQL 数据库创建脚本

-- Create database (run as postgres superuser)
-- 创建数据库（以 postgres 超级用户身份运行）
CREATE DATABASE network_monitor
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Create a database user (optional, but recommended)
-- 创建数据库用户（可选，但推荐）
-- IMPORTANT: Replace 'your_secure_password_here' with a strong password
-- 重要：将 'your_secure_password_here' 替换为强密码
-- Password requirements: At least 12 characters, including uppercase, lowercase, numbers, and special characters
-- 密码要求：至少12个字符，包括大写字母、小写字母、数字和特殊字符
CREATE USER network_monitor_user WITH PASSWORD 'your_secure_password_here';

-- Grant privileges to the user
-- 授予用户权限
GRANT ALL PRIVILEGES ON DATABASE network_monitor TO network_monitor_user;

-- Connect to the database
-- 连接到数据库
\c network_monitor;

-- Grant schema privileges
-- 授予模式权限
GRANT ALL ON SCHEMA public TO network_monitor_user;

-- Note: The actual tables will be created automatically by Flask-SQLAlchemy
-- when you run the application or use init_db.py
-- 注意：实际的表将由 Flask-SQLAlchemy 在运行应用程序或使用 init_db.py 时自动创建

-- Verify database creation
-- 验证数据库创建
SELECT datname, encoding, datcollate, datctype FROM pg_database WHERE datname = 'network_monitor';
