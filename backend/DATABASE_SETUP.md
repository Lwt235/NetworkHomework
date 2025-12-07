# Database Setup Guide / 数据库设置指南

This guide provides instructions for setting up the database for the Network Monitoring Tool.

本指南提供了为网络监控工具设置数据库的说明。

## Table of Contents / 目录

1. [SQLite Setup (Default)](#sqlite-setup-default--sqlite-设置默认)
2. [PostgreSQL Setup](#postgresql-setup--postgresql-设置)
3. [MySQL Setup](#mysql-setup--mysql-设置)
4. [Database Management Commands](#database-management-commands--数据库管理命令)

---

## SQLite Setup (Default) / SQLite 设置（默认）

SQLite is the default database and requires no additional setup. The database file will be created automatically when you first run the application.

SQLite 是默认数据库，不需要额外设置。首次运行应用程序时会自动创建数据库文件。

### Quick Start / 快速开始

```bash
cd backend

# Initialize database tables
# 初始化数据库表
python init_db.py init

# Or simply run the application (it will create tables automatically)
# 或者直接运行应用程序（它会自动创建表）
python app.py
```

The SQLite database file `network_monitor.db` will be created in the `backend/` directory.

SQLite 数据库文件 `network_monitor.db` 将在 `backend/` 目录中创建。

---

## PostgreSQL Setup / PostgreSQL 设置

PostgreSQL is recommended for production environments due to its robustness and performance.

PostgreSQL 因其稳健性和性能而推荐用于生产环境。

### Prerequisites / 前置要求

- PostgreSQL 12 or higher installed
- PostgreSQL 12 或更高版本已安装

### Step 1: Create Database / 步骤 1：创建数据库

#### Method 1: Using SQL Script / 方法 1：使用 SQL 脚本

```bash
# Run as postgres user
# 以 postgres 用户身份运行
sudo -u postgres psql -f create_db_postgresql.sql
```

#### Method 2: Using psql Command Line / 方法 2：使用 psql 命令行

```bash
# Connect to PostgreSQL as superuser
# 以超级用户身份连接到 PostgreSQL
sudo -u postgres psql

# Create database
# 创建数据库
CREATE DATABASE network_monitor
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8';

# Create user (optional but recommended)
# 创建用户（可选但推荐）
CREATE USER network_monitor_user WITH PASSWORD 'your_secure_password_here';

# Grant privileges
# 授予权限
GRANT ALL PRIVILEGES ON DATABASE network_monitor TO network_monitor_user;

# Exit psql
# 退出 psql
\q
```

### Step 2: Configure Environment / 步骤 2：配置环境

Create or edit `.env` file in the `backend/` directory:

在 `backend/` 目录中创建或编辑 `.env` 文件：

```bash
DATABASE_URL=postgresql://network_monitor_user:your_secure_password_here@localhost:5432/network_monitor
```

### Step 3: Initialize Tables / 步骤 3：初始化表

```bash
cd backend

# Initialize database tables
# 初始化数据库表
python init_db.py init
```

### Step 4: Verify Installation / 步骤 4：验证安装

```bash
# Check database info
# 检查数据库信息
python init_db.py info

# Connect to database to verify tables
# 连接到数据库以验证表
psql -U network_monitor_user -d network_monitor -c "\dt"
```

---

## MySQL Setup / MySQL 设置

MySQL is also supported for production environments.

MySQL 也支持用于生产环境。

### Prerequisites / 前置要求

- MySQL 8.0 or higher installed
- MySQL 8.0 或更高版本已安装

### Step 1: Create Database / 步骤 1：创建数据库

#### Method 1: Using SQL Script / 方法 1：使用 SQL 脚本

```bash
# Run the SQL script
# 运行 SQL 脚本
mysql -u root -p < create_db_mysql.sql
```

#### Method 2: Using MySQL Command Line / 方法 2：使用 MySQL 命令行

```bash
# Connect to MySQL as root
# 以 root 身份连接到 MySQL
mysql -u root -p

# Create database
# 创建数据库
CREATE DATABASE IF NOT EXISTS network_monitor
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

# Create user (optional but recommended)
# 创建用户（可选但推荐）
CREATE USER IF NOT EXISTS 'network_monitor_user'@'localhost' 
    IDENTIFIED BY 'your_secure_password_here';

# Grant privileges
# 授予权限
GRANT ALL PRIVILEGES ON network_monitor.* TO 'network_monitor_user'@'localhost';

# Flush privileges
# 刷新权限
FLUSH PRIVILEGES;

# Exit MySQL
# 退出 MySQL
EXIT;
```

### Step 2: Configure Environment / 步骤 2：配置环境

Create or edit `.env` file in the `backend/` directory:

在 `backend/` 目录中创建或编辑 `.env` 文件：

```bash
DATABASE_URL=mysql://network_monitor_user:your_secure_password_here@localhost:3306/network_monitor
```

**Note**: You may need to install the MySQL Python driver:

**注意**：您可能需要安装 MySQL Python 驱动程序：

```bash
pip install mysqlclient
# or
pip install PyMySQL
```

If using PyMySQL, update the DATABASE_URL:

如果使用 PyMySQL，请更新 DATABASE_URL：

```bash
DATABASE_URL=mysql+pymysql://network_monitor_user:your_secure_password_here@localhost:3306/network_monitor
```

### Step 3: Initialize Tables / 步骤 3：初始化表

```bash
cd backend

# Initialize database tables
# 初始化数据库表
python init_db.py init
```

### Step 4: Verify Installation / 步骤 4：验证安装

```bash
# Check database info
# 检查数据库信息
python init_db.py info

# Connect to database to verify tables
# 连接到数据库以验证表
mysql -u network_monitor_user -p network_monitor -e "SHOW TABLES;"
```

---

## Database Management Commands / 数据库管理命令

The `init_db.py` script provides several commands for managing the database:

`init_db.py` 脚本提供了几个管理数据库的命令：

### Initialize Database / 初始化数据库

Create all database tables:

创建所有数据库表：

```bash
python init_db.py init
```

### Show Database Information / 显示数据库信息

Display current database configuration and tables:

显示当前数据库配置和表：

```bash
python init_db.py info
```

### Reset Database / 重置数据库

Drop all tables and recreate them (WARNING: deletes all data):

删除所有表并重新创建它们（警告：删除所有数据）：

```bash
python init_db.py reset
```

### Drop Database Tables / 删除数据库表

Drop all tables (WARNING: deletes all data):

删除所有表（警告：删除所有数据）：

```bash
python init_db.py drop
```

### Help / 帮助

Show help message with all available commands:

显示包含所有可用命令的帮助信息：

```bash
python init_db.py help
```

---

## Database Tables / 数据库表

The application creates the following tables:

应用程序创建以下表：

1. **users** - User authentication information / 用户认证信息
2. **devices** - Network devices / 网络设备
3. **traffic_logs** - Network traffic logs / 网络流量日志
4. **alerts** - System alerts / 系统警报
5. **packet_captures** - Captured network packets / 捕获的网络数据包

---

## Troubleshooting / 故障排除

### SQLite Issues / SQLite 问题

**Problem**: Permission denied error

**问题**：权限被拒绝错误

**Solution**: Ensure the backend directory is writable:

**解决方案**：确保后端目录可写：

```bash
chmod 755 backend/
```

### PostgreSQL Issues / PostgreSQL 问题

**Problem**: Connection refused

**问题**：连接被拒绝

**Solution**: Ensure PostgreSQL is running:

**解决方案**：确保 PostgreSQL 正在运行：

```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

**Problem**: Authentication failed

**问题**：认证失败

**Solution**: Check your `.env` file has correct credentials and the user exists:

**解决方案**：检查 `.env` 文件具有正确的凭据并且用户存在：

```bash
sudo -u postgres psql -c "\du"
```

### MySQL Issues / MySQL 问题

**Problem**: Access denied for user

**问题**：用户访问被拒绝

**Solution**: Verify user credentials and privileges:

**解决方案**：验证用户凭据和权限：

```bash
mysql -u root -p -e "SELECT User, Host FROM mysql.user;"
mysql -u root -p -e "SHOW GRANTS FOR 'network_monitor_user'@'localhost';"
```

**Problem**: MySQL driver not installed

**问题**：MySQL 驱动未安装

**Solution**: Install the required driver:

**解决方案**：安装所需的驱动程序：

```bash
pip install mysqlclient
# or
pip install PyMySQL
```

---

## Security Recommendations / 安全建议

1. **Change Default Passwords**: Always use strong, unique passwords
   
   **更改默认密码**：始终使用强大、唯一的密码

2. **Limit Access**: Configure database to accept connections only from trusted hosts
   
   **限制访问**：配置数据库仅接受来自受信任主机的连接

3. **Use SSL/TLS**: Enable encrypted connections for remote database access
   
   **使用 SSL/TLS**：为远程数据库访问启用加密连接

4. **Regular Backups**: Set up automated database backups
   
   **定期备份**：设置自动数据库备份

5. **Keep Updated**: Regularly update database software with security patches
   
   **保持更新**：定期使用安全补丁更新数据库软件

---

## Backup and Restore / 备份和恢复

### SQLite Backup / SQLite 备份

```bash
# Backup
# 备份
cp backend/network_monitor.db backend/network_monitor.db.backup

# Restore
# 恢复
cp backend/network_monitor.db.backup backend/network_monitor.db
```

### PostgreSQL Backup / PostgreSQL 备份

```bash
# Backup
# 备份
pg_dump -U network_monitor_user network_monitor > network_monitor_backup.sql

# Restore
# 恢复
psql -U network_monitor_user network_monitor < network_monitor_backup.sql
```

### MySQL Backup / MySQL 备份

```bash
# Backup
# 备份
mysqldump -u network_monitor_user -p network_monitor > network_monitor_backup.sql

# Restore
# 恢复
mysql -u network_monitor_user -p network_monitor < network_monitor_backup.sql
```

---

## Additional Resources / 其他资源

- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

For more information, see the main [README.md](../README.md) and [DEPLOYMENT.md](../DEPLOYMENT.md) files.

有关更多信息，请参阅主要的 [README.md](../README.md) 和 [DEPLOYMENT.md](../DEPLOYMENT.md) 文件。
