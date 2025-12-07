# 部署指南 / Deployment Guide

## 快速开始 / Quick Start

### 后端部署 / Backend Deployment

#### 1. 安装依赖 / Install Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. 配置环境变量 / Configure Environment

创建 `.env` 文件 / Create `.env` file:
```bash
cp .env.example .env
```

编辑 `.env` 文件 / Edit `.env` file:
```bash
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///network_monitor.db
```

#### 3. 初始化数据库 / Initialize Database

```bash
# 查看数据库配置信息 / View database configuration
python init_db.py info

# 创建数据库表 / Create database tables
python init_db.py init
```

详细的数据库设置指南请参阅 [DATABASE_SETUP.md](backend/DATABASE_SETUP.md)
For detailed database setup instructions, see [DATABASE_SETUP.md](backend/DATABASE_SETUP.md)

#### 4. 启动后端服务器 / Start Backend Server

```bash
python app.py
```

后端服务器将在 `http://localhost:5000` 启动。
Backend server will start at `http://localhost:5000`.

#### 5. 测试后端 / Test Backend (可选 / Optional)

```bash
python test_backend.py
```

### 前端部署 / Frontend Deployment

#### 1. 安装依赖 / Install Dependencies

```bash
cd frontend
npm install
```

#### 2. 启动开发服务器 / Start Development Server

```bash
npm run dev
```

前端将在 `http://localhost:5173` 启动。
Frontend will start at `http://localhost:5173`.

#### 3. 构建生产版本 / Build for Production

```bash
npm run build
```

构建的文件将在 `dist/` 目录中。
Built files will be in the `dist/` directory.

## 使用说明 / Usage Instructions

### 1. 注册账号 / Register Account

访问 `http://localhost:5173/register` 注册新账号。
Visit `http://localhost:5173/register` to register a new account.

### 2. 登录系统 / Login

使用注册的账号登录系统。
Login with your registered credentials.

### 3. 功能说明 / Features

#### 仪表板 / Dashboard
- 查看系统概览和统计信息
- 监控设备状态
- 查看最近警报

#### 设备管理 / Device Management
- 添加新设备
- 编辑设备信息
- 删除设备
- 查看设备状态

#### 实时监控 / Real-time Monitoring
- 查看网络流量
- 运行网速测试
- 查看系统资源使用情况
- 查看历史数据

#### 抓包分析 / Packet Capture
- 选择协议类型 (TCP/UDP/IP/ICMP)
- 捕获网络数据包
- 查看数据包详情
- 协议统计分析

#### 统计分析 / Analytics
- 查看网络负载统计
- 管理警报
- 配置阈值
- 查看系统状态

## 生产环境部署 / Production Deployment

### 后端 / Backend

建议使用 Gunicorn 或 uWSGI:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

或使用 uWSGI:

```bash
pip install uwsgi
uwsgi --http 0.0.0.0:5000 --wsgi-file app.py --callable app --processes 4 --threads 2
```

### 前端 / Frontend

1. 构建生产版本:
```bash
npm run build
```

2. 使用 Nginx 或 Apache 托管 `dist/` 目录。

示例 Nginx 配置:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /path/to/frontend/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 注意事项 / Important Notes

### 数据包捕获权限 / Packet Capture Permissions

数据包捕获功能需要管理员/root权限。在Linux上:

```bash
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)
# 或以 root 用户运行
sudo python app.py
```

如果无法获取权限，系统将使用模拟数据。

### 安全建议 / Security Recommendations

1. 更改默认的 SECRET_KEY 和 JWT_SECRET_KEY
2. 使用 HTTPS 在生产环境中
3. 配置防火墙规则
4. 定期备份数据库
5. 限制数据包捕获功能的访问

### 数据库 / Database

默认使用 SQLite。对于生产环境，建议使用 PostgreSQL 或 MySQL。
SQLite is used by default. For production environments, PostgreSQL or MySQL is recommended.

#### SQLite (默认 / Default)
```bash
# 数据库文件将自动创建 / Database file will be created automatically
DATABASE_URL=sqlite:///network_monitor.db
```

#### PostgreSQL (推荐用于生产 / Recommended for Production)
```bash
# 1. 创建数据库 / Create database
sudo -u postgres psql -f create_db_postgresql.sql

# 2. 配置连接 / Configure connection
DATABASE_URL=postgresql://network_monitor_user:password@localhost:5432/network_monitor

# 3. 初始化表 / Initialize tables
python init_db.py init
```

#### MySQL
```bash
# 1. 创建数据库 / Create database
mysql -u root -p < create_db_mysql.sql

# 2. 安装 MySQL 驱动 / Install MySQL driver
pip install mysqlclient  # or PyMySQL

# 3. 配置连接 / Configure connection
DATABASE_URL=mysql://network_monitor_user:password@localhost:3306/network_monitor

# 4. 初始化表 / Initialize tables
python init_db.py init
```

#### 数据库管理 / Database Management
```bash
# 查看数据库信息 / View database info
python init_db.py info

# 重置数据库 / Reset database (WARNING: deletes all data)
python init_db.py reset

# 备份数据库 / Backup database
# SQLite
cp network_monitor.db network_monitor.db.backup

# PostgreSQL
pg_dump -U network_monitor_user network_monitor > backup.sql

# MySQL
mysqldump -u network_monitor_user -p network_monitor > backup.sql
```

详细说明请参阅 [backend/DATABASE_SETUP.md](backend/DATABASE_SETUP.md)
For detailed instructions, see [backend/DATABASE_SETUP.md](backend/DATABASE_SETUP.md)

## 故障排除 / Troubleshooting

### 后端启动失败 / Backend Fails to Start

1. 检查端口 5000 是否被占用
2. 确认所有依赖已安装
3. 检查 Python 版本 (需要 3.8+)

### 前端无法连接后端 / Frontend Cannot Connect to Backend

1. 确认后端正在运行
2. 检查 CORS 配置
3. 查看浏览器控制台错误

### 数据包捕获不工作 / Packet Capture Not Working

1. 确认有足够的权限
2. 检查 Scapy 是否正确安装
3. 系统将回退到模拟数据

## 技术支持 / Support

如有问题，请查看:
- README.md 文档
- GitHub Issues
- 项目文档

## 许可证 / License

MIT License
