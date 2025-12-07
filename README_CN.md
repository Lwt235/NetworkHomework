# 网络性能监测工具

一个全面的网络性能监测工具，具有用户认证、设备管理、实时流量监控、数据包捕获分析和警报功能。

[English](README.md) | 简体中文

## 功能特性

### 1. 用户认证系统
- ✅ 用户注册和登录
- ✅ 基于JWT的身份认证
- ✅ 安全的密码哈希加密
- ✅ 个性化用户界面

### 2. 网络设备管理
- ✅ 添加、编辑、删除网络设备
- ✅ 支持多种设备类型（路由器、交换机、服务器等）
- ✅ 实时设备状态监控
- ✅ 设备在线/离线状态追踪

### 3. 实时网络监控
- ✅ 实时数据流量采集
- ✅ 网速测试功能
- ✅ 上传/下载速度显示
- ✅ 系统资源监控（CPU、内存、磁盘）
- ✅ 自动刷新机制
- ✅ 历史数据记录和查询

### 4. 数据包捕获与分析
- ✅ TCP/UDP/IP/ICMP协议抓包
- ✅ 可配置的抓包参数（数量、超时）
- ✅ 详细的数据包信息展示
- ✅ 协议类型过滤
- ✅ 协议统计分析
- ✅ 源/目标IP和端口显示

### 5. 性能分析与统计
- ✅ 历史数据统计图表
- ✅ 网络负载分析
- ✅ 流量趋势可视化
- ✅ 可自定义时间范围
- ✅ 数据导出功能

### 6. 智能警报系统
- ✅ 基于阈值的自动警报
- ✅ CPU/内存/磁盘使用率监控
- ✅ 可配置的警报阈值
- ✅ 警报历史记录
- ✅ 警报状态管理（活动/已解决）
- ✅ 多级别严重程度（信息/警告/错误/严重）

## 技术栈

### 后端技术
- **Python 3.8+** - 主要编程语言
- **Flask** - 轻量级Web框架
- **Flask-SQLAlchemy** - ORM数据库操作
- **Flask-JWT-Extended** - JWT身份认证
- **Flask-CORS** - 跨域资源共享
- **Flask-Bcrypt** - 密码加密
- **Scapy** - 网络数据包捕获和分析
- **psutil** - 系统和网络信息收集
- **SQLite** - 默认数据库（可配置PostgreSQL/MySQL）

### 前端技术
- **Vue 3** - 渐进式JavaScript框架
- **Vue Router** - 单页应用路由
- **Axios** - HTTP客户端
- **Element Plus** - Vue 3 UI组件库
- **Chart.js** - 数据可视化（未来增强）
- **Vite** - 下一代前端构建工具

## 项目结构

```
NetworkHomework/
├── backend/                    # 后端目录
│   ├── app.py                 # Flask应用主文件
│   ├── config.py              # 配置文件
│   ├── models.py              # 数据库模型
│   ├── requirements.txt       # Python依赖
│   ├── init_db.py             # 数据库初始化脚本
│   ├── create_db_postgresql.sql # PostgreSQL数据库创建脚本
│   ├── create_db_mysql.sql    # MySQL数据库创建脚本
│   ├── DATABASE_SETUP.md      # 数据库设置指南
│   ├── DB_QUICK_REFERENCE.md  # 数据库快速参考
│   ├── routes/                # API路由
│   │   ├── auth.py           # 认证相关路由
│   │   ├── devices.py        # 设备管理路由
│   │   ├── monitoring.py     # 监控相关路由
│   │   └── analysis.py       # 分析相关路由
│   ├── services/              # 业务逻辑服务
│   │   ├── capture.py        # 数据包捕获服务
│   │   ├── monitor.py        # 监控服务
│   │   └── analytics.py      # 分析服务
│   ├── test_backend.py        # 后端测试脚本
│   └── .env.example           # 环境变量示例
├── frontend/                   # 前端目录
│   ├── index.html             # HTML入口
│   ├── package.json           # Node.js依赖
│   ├── vite.config.js         # Vite配置
│   └── src/                   # 源代码
│       ├── App.vue            # 根组件
│       ├── main.js            # 入口文件
│       ├── router/            # 路由配置
│       │   └── index.js
│       ├── services/          # API服务
│       │   └── api.js
│       └── views/             # 页面组件
│           ├── Login.vue      # 登录页面
│           ├── Register.vue   # 注册页面
│           ├── Dashboard.vue  # 仪表板
│           ├── Devices.vue    # 设备管理
│           ├── Monitoring.vue # 实时监控
│           ├── PacketCapture.vue # 抓包分析
│           └── Analytics.vue  # 统计分析
├── start.sh                    # 启动脚本
├── README.md                   # 英文文档
├── README_CN.md               # 中文文档（本文件）
├── API.md                      # API文档
└── DEPLOYMENT.md              # 部署指南
```

## 快速开始

### 前置要求
- Python 3.8 或更高版本
- Node.js 14 或更高版本
- 数据包捕获需要管理员权限

### 方法1: 使用启动脚本（推荐）

```bash
chmod +x start.sh
./start.sh
```

### 方法2: 手动启动

#### 步骤1: 初始化数据库

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 初始化数据库（创建表）
python init_db.py init

# 或查看数据库信息
python init_db.py info
```

详细的数据库设置指南请参阅 [DATABASE_SETUP.md](backend/DATABASE_SETUP.md)

#### 步骤2: 启动后端

```bash
python app.py
```

后端将在 `http://localhost:5000` 启动

#### 步骤3: 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端将在 `http://localhost:5173` 启动

## 数据库设置

本项目支持多种数据库系统：SQLite（默认）、PostgreSQL、MySQL。

### SQLite（默认，无需额外配置）

```bash
cd backend
python init_db.py init
```

### PostgreSQL（推荐用于生产环境）

```bash
# 1. 创建数据库
sudo -u postgres psql -f create_db_postgresql.sql

# 2. 配置环境变量（在 .env 文件中）
DATABASE_URL=postgresql://network_monitor_user:password@localhost:5432/network_monitor

# 3. 初始化表
python init_db.py init
```

### MySQL

```bash
# 1. 创建数据库
mysql -u root -p < create_db_mysql.sql

# 2. 配置环境变量（在 .env 文件中）
DATABASE_URL=mysql://network_monitor_user:password@localhost:3306/network_monitor

# 3. 初始化表
python init_db.py init
```

### 数据库管理命令

```bash
# 查看数据库信息
python init_db.py info

# 重置数据库（警告：删除所有数据）
python init_db.py reset

# 获取帮助
python init_db.py help
```

详细说明请参阅 [backend/DATABASE_SETUP.md](backend/DATABASE_SETUP.md)

## 使用指南

### 1. 访问应用
在浏览器中打开 `http://localhost:5173`

### 2. 创建账号
- 点击"立即注册"
- 填写用户名、邮箱和密码
- 提交注册表单

### 3. 登录系统
使用注册的账号登录系统

### 4. 添加设备
- 进入"设备管理"页面
- 点击"添加设备"按钮
- 填写设备信息（名称、IP地址、设备类型）
- 保存设备

### 5. 监控网络
- 在"实时监控"页面查看当前网络状态
- 运行网速测试
- 查看历史数据

### 6. 抓包分析
- 进入"抓包分析"页面
- 选择协议类型
- 设置抓包参数
- 点击"开始抓包"
- 查看捕获的数据包

### 7. 统计分析
- 在"统计分析"页面查看网络统计
- 配置警报阈值
- 管理警报状态

## API文档

详细的API文档请参阅 [API.md](API.md)

主要端点：
- **认证**: `/api/auth/register`, `/api/auth/login`
- **设备**: `/api/devices`
- **监控**: `/api/monitoring/traffic`, `/api/monitoring/system`
- **分析**: `/api/analysis/capture`, `/api/analysis/stats`

## 配置说明

### 后端配置

在 `backend/` 目录下创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件以自定义配置：
- 修改 `SECRET_KEY` 和 `JWT_SECRET_KEY`
- 配置数据库连接
- 设置警报阈值
- 调整抓包参数

### 前端配置

前端通过代理连接后端API，配置在 `vite.config.js` 中。

## 部署说明

详细的部署指南请参阅 [DEPLOYMENT.md](DEPLOYMENT.md)

### 生产环境建议
- 使用 Gunicorn 或 uWSGI 运行后端
- 使用 Nginx 托管前端静态文件
- 使用 PostgreSQL 或 MySQL 替代SQLite
- 启用HTTPS
- 配置防火墙规则
- 定期备份数据库

## 安全注意事项

1. **密码安全**: 所有密码使用bcrypt加密存储
2. **JWT令牌**: 访问令牌有24小时有效期
3. **数据包捕获**: 需要管理员权限，请谨慎授权
4. **环境变量**: 不要将 `.env` 文件提交到版本控制
5. **CORS配置**: 仅允许受信任的源访问API

## 数据包捕获权限

### Linux
```bash
# 方法1: 授予Python捕获权限
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)

# 方法2: 以root用户运行
sudo python app.py
```

### Windows
以管理员身份运行命令提示符或PowerShell

### macOS
```bash
sudo python app.py
```

**注意**: 如果没有足够权限，系统将使用模拟数据。

## 故障排除

### 后端无法启动
- 检查Python版本（需要3.8+）
- 确认端口5000未被占用
- 检查所有依赖是否正确安装

### 前端无法连接后端
- 确认后端正在运行
- 检查CORS配置
- 查看浏览器控制台错误

### 数据包捕获失败
- 确认有管理员权限
- 检查Scapy是否正确安装
- 系统将自动回退到模拟数据

### 数据库错误
- 删除 `network_monitor.db` 重新初始化
- 检查数据库文件权限
- 查看后端日志

## 测试

运行后端测试：
```bash
cd backend
source venv/bin/activate
python test_backend.py
```

## 开发路线图

### 已完成 ✅
- [x] 用户认证系统
- [x] 设备管理功能
- [x] 实时流量监控
- [x] 数据包捕获和分析
- [x] 警报系统
- [x] 历史数据统计

### 计划中 📋
- [ ] 数据可视化图表（Chart.js集成）
- [ ] 实时WebSocket推送
- [ ] 邮件/短信警报通知
- [ ] 多用户角色和权限
- [ ] 数据导出（CSV/Excel）
- [ ] 暗色主题
- [ ] 移动端响应式优化
- [ ] Docker容器化部署
- [ ] 性能优化和缓存
- [ ] 国际化（i18n）支持

## 贡献

欢迎贡献代码、报告问题和提出功能建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 致谢

- Flask 框架团队
- Vue.js 核心团队
- Element Plus UI库
- Scapy 网络分析工具
- 所有开源贡献者

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 查看项目文档
- 参与 Pull Request 讨论

---

**注意**: 本工具仅用于合法的网络监控和诊断目的。请遵守所有适用的法律和法规。
