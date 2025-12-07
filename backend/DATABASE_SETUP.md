# Database Setup Guide / 数据库设置指南

This guide provides instructions for setting up the MySQL database for the Network Monitoring Tool.

本指南提供了为网络监控工具设置 MySQL 数据库的说明。

## Table of Contents / 目录

1. [MySQL Setup](#mysql-setup--mysql-设置)
2. [Database Management Commands](#database-management-commands--数据库管理命令)
3. [Troubleshooting](#troubleshooting--故障排除)
4. [Security Recommendations](#security-recommendations--安全建议)
5. [Backup and Restore](#backup-and-restore--备份和恢复)

---

## MySQL Setup / MySQL 设置

MySQL is the database for this project.

MySQL 是本项目的数据库。

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

### Step 2: Install MySQL Driver / 步骤 2：安装 MySQL 驱动程序

**Note**: The MySQL Python driver is required for the application to connect to MySQL.

**注意**：应用程序需要 MySQL Python 驱动程序才能连接到 MySQL。

```bash
pip install PyMySQL
```

### Step 3: Configure Environment / 步骤 3：配置环境

Create or edit `.env` file in the `backend/` directory:

在 `backend/` 目录中创建或编辑 `.env` 文件：

```bash
DATABASE_URL=mysql+pymysql://network_monitor_user:your_secure_password_here@localhost:3306/network_monitor
```

### Step 4: Initialize Tables / 步骤 4：初始化表

```bash
cd backend

# Initialize database tables
# 初始化数据库表
python init_db.py init
```

### Step 5: Verify Installation / 步骤 5：验证安装

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
pip install PyMySQL
```

**Problem**: Connection refused

**问题**：连接被拒绝

**Solution**: Ensure MySQL is running:

**解决方案**：确保 MySQL 正在运行：

```bash
# On Linux
sudo systemctl status mysql
sudo systemctl start mysql

# On macOS
brew services list
brew services start mysql

# On Windows
# Check MySQL service in Services Manager
```

**Problem**: Character encoding issues

**问题**：字符编码问题

**Solution**: Ensure database uses utf8mb4:

**解决方案**：确保数据库使用 utf8mb4：

```bash
mysql -u root -p -e "ALTER DATABASE network_monitor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
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

6. **Remove Test Users**: Delete any test or anonymous MySQL users
   
   **删除测试用户**：删除任何测试或匿名 MySQL 用户

---

## Backup and Restore / 备份和恢复

### MySQL Backup / MySQL 备份

```bash
# Backup database
# 备份数据库
mysqldump -u network_monitor_user -p network_monitor > network_monitor_backup.sql

# Backup with timestamp
# 带时间戳的备份
mysqldump -u network_monitor_user -p network_monitor > network_monitor_backup_$(date +%Y%m%d_%H%M%S).sql
```

### MySQL Restore / MySQL 恢复

```bash
# Restore database
# 恢复数据库
mysql -u network_monitor_user -p network_monitor < network_monitor_backup.sql
```

### Automated Backup Script / 自动备份脚本

Create a cron job for regular backups:

为定期备份创建 cron 作业：

```bash
# Edit crontab
# 编辑 crontab
crontab -e

# Add this line to backup daily at 2 AM
# 添加此行以在凌晨 2 点每天备份
0 2 * * * /usr/bin/mysqldump -u network_monitor_user -p'your_password' network_monitor > /path/to/backups/network_monitor_$(date +\%Y\%m\%d).sql
```

---

## Additional Resources / 其他资源

- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)

---

For more information, see the main [README.md](../README.md) and [DEPLOYMENT.md](../DEPLOYMENT.md) files.

有关更多信息，请参阅主要的 [README.md](../README.md) 和 [DEPLOYMENT.md](../DEPLOYMENT.md) 文件。
