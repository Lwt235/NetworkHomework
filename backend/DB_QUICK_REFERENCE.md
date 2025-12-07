# 数据库快速参考 / Database Quick Reference

本文件提供数据库设置的快速参考命令。
This file provides quick reference commands for database setup.

---

## 快速开始 / Quick Start

### MySQL

```bash
# 1. 创建数据库 / Create database
mysql -u root -p < create_db_mysql.sql

# 2. 安装 MySQL 驱动 / Install MySQL driver
pip install PyMySQL

# 3. 在 .env 文件中设置 / Set in .env file:
DATABASE_URL=mysql+pymysql://network_monitor_user:your_password@localhost:3306/network_monitor

# 4. 初始化表 / Initialize tables
python init_db.py init
```

---

## 数据库管理命令 / Database Management Commands

```bash
# 初始化数据库（创建表） / Initialize database (create tables)
python init_db.py init

# 查看数据库信息 / Show database information
python init_db.py info

# 重置数据库（警告：删除所有数据） / Reset database (WARNING: deletes all data)
python init_db.py reset

# 删除所有表（警告：删除所有数据） / Drop all tables (WARNING: deletes all data)
python init_db.py drop

# 显示帮助信息 / Show help
python init_db.py help
```

---

## 数据库表 / Database Tables

应用程序使用以下表：
The application uses the following tables:

- `users` - 用户认证信息 / User authentication
- `devices` - 网络设备 / Network devices
- `traffic_logs` - 网络流量日志 / Network traffic logs
- `alerts` - 系统警报 / System alerts
- `packet_captures` - 捕获的网络数据包 / Captured network packets

---

## 备份和恢复 / Backup and Restore

### MySQL
```bash
# 备份 / Backup
mysqldump -u network_monitor_user -p network_monitor > backup.sql

# 恢复 / Restore
mysql -u network_monitor_user -p network_monitor < backup.sql
```

---

## 文件说明 / File Descriptions

- `init_db.py` - 数据库管理脚本 / Database management script
- `create_db_mysql.sql` - MySQL 数据库创建脚本 / MySQL database creation script
- `DATABASE_SETUP.md` - 完整的数据库设置指南 / Complete database setup guide

---

详细说明请参阅 [DATABASE_SETUP.md](DATABASE_SETUP.md)
For detailed instructions, see [DATABASE_SETUP.md](DATABASE_SETUP.md)
