# API 文档 / API Documentation

## 基础信息 / Base Information

**Base URL**: `http://localhost:5000/api`

**认证方式 / Authentication**: JWT Bearer Token

所有需要认证的端点都需要在请求头中包含:
```
Authorization: Bearer <access_token>
```

## 认证端点 / Authentication Endpoints

### 注册用户 / Register User

**POST** `/auth/register`

创建新用户账号。

**请求体 / Request Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**响应 / Response** (201 Created):
```json
{
  "message": "User registered successfully",
  "access_token": "string",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### 用户登录 / User Login

**POST** `/auth/login`

用户登录并获取访问令牌。

**请求体 / Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**响应 / Response** (200 OK):
```json
{
  "message": "Login successful",
  "access_token": "string",
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### 获取当前用户信息 / Get Current User

**GET** `/auth/me`

获取当前登录用户的信息。

**需要认证 / Requires Authentication**: Yes

**响应 / Response** (200 OK):
```json
{
  "user": {
    "id": 1,
    "username": "string",
    "email": "string",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

## 设备管理端点 / Device Management Endpoints

### 获取所有设备 / Get All Devices

**GET** `/devices`

获取当前用户的所有设备列表。

**需要认证 / Requires Authentication**: Yes

**响应 / Response** (200 OK):
```json
{
  "devices": [
    {
      "id": 1,
      "name": "Router 1",
      "ip_address": "192.168.1.1",
      "device_type": "router",
      "status": "active",
      "last_seen": "2024-01-01T00:00:00",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### 获取特定设备 / Get Specific Device

**GET** `/devices/{device_id}`

获取特定设备的详细信息。

**需要认证 / Requires Authentication**: Yes

**响应 / Response** (200 OK):
```json
{
  "device": {
    "id": 1,
    "name": "Router 1",
    "ip_address": "192.168.1.1",
    "device_type": "router",
    "status": "active",
    "last_seen": "2024-01-01T00:00:00",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### 添加设备 / Add Device

**POST** `/devices`

添加新的网络设备。

**需要认证 / Requires Authentication**: Yes

**请求体 / Request Body**:
```json
{
  "name": "Router 1",
  "ip_address": "192.168.1.1",
  "device_type": "router"
}
```

**响应 / Response** (201 Created):
```json
{
  "message": "Device added successfully",
  "device": {
    "id": 1,
    "name": "Router 1",
    "ip_address": "192.168.1.1",
    "device_type": "router",
    "status": "active",
    "last_seen": "2024-01-01T00:00:00",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### 更新设备 / Update Device

**PUT** `/devices/{device_id}`

更新设备信息。

**需要认证 / Requires Authentication**: Yes

**请求体 / Request Body**:
```json
{
  "name": "Updated Router",
  "ip_address": "192.168.1.2",
  "device_type": "router",
  "status": "active"
}
```

**响应 / Response** (200 OK):
```json
{
  "message": "Device updated successfully",
  "device": { /* device object */ }
}
```

### 删除设备 / Delete Device

**DELETE** `/devices/{device_id}`

删除设备。

**需要认证 / Requires Authentication**: Yes

**响应 / Response** (200 OK):
```json
{
  "message": "Device deleted successfully"
}
```

## 监控端点 / Monitoring Endpoints

### 获取网络流量 / Get Network Traffic

**GET** `/monitoring/traffic`

获取当前网络流量统计。

**需要认证 / Requires Authentication**: Yes

**响应 / Response** (200 OK):
```json
{
  "traffic": {
    "bytes_sent": 1000000,
    "bytes_recv": 2000000,
    "packets_sent": 1000,
    "packets_recv": 2000,
    "errin": 0,
    "errout": 0,
    "dropin": 0,
    "dropout": 0
  },
  "timestamp": "2024-01-01T00:00:00"
}
```

### 获取系统状态 / Get System Stats

**GET** `/monitoring/system`

获取系统资源使用情况。

**需要认证 / Requires Authentication**: Yes

**响应 / Response** (200 OK):
```json
{
  "system": {
    "cpu": {
      "percent": 45.5,
      "count": 4
    },
    "memory": {
      "total": 8589934592,
      "available": 4294967296,
      "used": 4294967296,
      "percent": 50.0
    },
    "disk": {
      "total": 500000000000,
      "used": 250000000000,
      "free": 250000000000,
      "percent": 50.0
    },
    "network_interfaces": [
      {
        "name": "eth0",
        "address": "192.168.1.100",
        "netmask": "255.255.255.0"
      }
    ]
  },
  "timestamp": "2024-01-01T00:00:00"
}
```

### 运行网速测试 / Run Speed Test

**POST** `/monitoring/speed-test`

运行网络速度测试。

**需要认证 / Requires Authentication**: Yes

**响应 / Response** (200 OK):
```json
{
  "results": {
    "download_speed": 100.5,
    "upload_speed": 50.2,
    "unit": "Mbps"
  },
  "timestamp": "2024-01-01T00:00:00"
}
```

### 获取历史数据 / Get History Data

**GET** `/monitoring/history`

获取历史流量数据。

**需要认证 / Requires Authentication**: Yes

**查询参数 / Query Parameters**:
- `hours` (integer): 时间范围(小时) / Time range in hours (default: 24)
- `device_id` (integer): 设备ID / Device ID (optional)

**响应 / Response** (200 OK):
```json
{
  "history": [
    {
      "id": 1,
      "timestamp": "2024-01-01T00:00:00",
      "bytes_sent": 1000000,
      "bytes_recv": 2000000,
      "packets_sent": 1000,
      "packets_recv": 2000,
      "device_id": 1
    }
  ],
  "count": 100
}
```

### 获取警报列表 / Get Alerts

**GET** `/monitoring/alerts`

获取警报列表。

**需要认证 / Requires Authentication**: Yes

**查询参数 / Query Parameters**:
- `status` (string): 警报状态 / Alert status ('active' or 'resolved', default: 'active')

**响应 / Response** (200 OK):
```json
{
  "alerts": [
    {
      "id": 1,
      "alert_type": "cpu",
      "message": "CPU usage is at 85%",
      "severity": "warning",
      "status": "active",
      "created_at": "2024-01-01T00:00:00",
      "resolved_at": null,
      "device_id": 1
    }
  ],
  "count": 5
}
```

### 解决警报 / Resolve Alert

**PUT** `/monitoring/alerts/{alert_id}/resolve`

标记警报为已解决。

**需要认证 / Requires Authentication**: Yes

**响应 / Response** (200 OK):
```json
{
  "message": "Alert resolved successfully",
  "alert": { /* alert object */ }
}
```

## 分析端点 / Analysis Endpoints

### 检查抓包权限 / Check Packet Capture Permissions

**GET** `/analysis/check-permissions`

检查应用是否有数据包捕获权限。

**需要认证 / Requires Authentication**: Yes

**响应 / Response** (200 OK - 有权限 / Has permissions):
```json
{
  "has_permission": true,
  "message": "Packet capture permissions are available"
}
```

**响应 / Response** (403 Forbidden - 无权限 / No permissions):
```json
{
  "has_permission": false,
  "message": "Insufficient permissions for packet capture",
  "instructions": {
    "os": "Linux",
    "methods": [
      {
        "method": "Grant capabilities to Python binary (recommended)",
        "command": "sudo setcap cap_net_raw,cap_net_admin=eip /usr/bin/python3",
        "description": "This allows Python to capture packets without running as root"
      },
      {
        "method": "Run application as root (not recommended for production)",
        "command": "sudo python3 app.py",
        "description": "Run the entire application with root privileges"
      }
    ]
  }
}
```

详细的权限设置说明请参阅 [PACKET_CAPTURE_PERMISSIONS.md](PACKET_CAPTURE_PERMISSIONS.md)

### 开始抓包 / Start Packet Capture

**POST** `/analysis/capture`

开始捕获网络数据包。

**需要认证 / Requires Authentication**: Yes

**需要权限 / Requires Permissions**: 需要网络抓包权限 / Network packet capture permissions required

**请求体 / Request Body**:
```json
{
  "protocol": "tcp",
  "count": 100,
  "timeout": 10
}
```

**响应 / Response** (200 OK):
```json
{
  "message": "Packet capture completed",
  "packets": [
    {
      "timestamp": "2024-01-01T00:00:00",
      "protocol": "TCP",
      "src_ip": "192.168.1.100",
      "dst_ip": "192.168.1.1",
      "src_port": 54321,
      "dst_port": 80,
      "length": 1500,
      "info": "Flags: S"
    }
  ],
  "count": 100
}
```

**响应 / Response** (403 Forbidden - 权限不足 / Insufficient permissions):
```json
{
  "error": "Permission denied",
  "message": "Insufficient permissions for packet capture. Please run the application with elevated privileges...",
  "requires_elevated_privileges": true
}
```

### 获取数据包列表 / Get Packets

**GET** `/analysis/packets`

获取已捕获的数据包列表。

**需要认证 / Requires Authentication**: Yes

**查询参数 / Query Parameters**:
- `hours` (integer): 时间范围(小时) / Time range in hours (default: 1)
- `protocol` (string): 协议过滤 / Protocol filter (optional)

**响应 / Response** (200 OK):
```json
{
  "packets": [ /* array of packet objects */ ],
  "count": 100
}
```

### 获取统计信息 / Get Statistics

**GET** `/analysis/stats`

获取网络统计信息。

**需要认证 / Requires Authentication**: Yes

**查询参数 / Query Parameters**:
- `hours` (integer): 时间范围(小时) / Time range in hours (default: 24)

**响应 / Response** (200 OK):
```json
{
  "stats": {
    "protocols": [
      {
        "protocol": "TCP",
        "count": 1000,
        "bytes": 1500000
      },
      {
        "protocol": "UDP",
        "count": 500,
        "bytes": 750000
      }
    ],
    "total_packets": 1500,
    "total_bytes": 2250000
  },
  "timestamp": "2024-01-01T00:00:00"
}
```

### 获取可用协议列表 / Get Available Protocols

**GET** `/analysis/protocols`

获取支持的协议类型列表。

**需要认证 / Requires Authentication**: Yes

**响应 / Response** (200 OK):
```json
{
  "protocols": [
    { "value": "tcp", "label": "TCP" },
    { "value": "udp", "label": "UDP" },
    { "value": "ip", "label": "IP" },
    { "value": "icmp", "label": "ICMP" },
    { "value": "all", "label": "All Protocols" }
  ]
}
```

## 错误响应 / Error Responses

所有错误响应遵循以下格式:

```json
{
  "error": "Error message description"
}
```

**重要说明 / Important Note**: 本应用不使用任何模拟数据。所有返回的数据都是真实的网络监控数据。如果功能因权限不足而无法使用，将返回明确的错误信息和解决方案，而不是返回模拟数据。

This application does NOT use mock or simulated data. All returned data is real network monitoring data. If a feature cannot be used due to insufficient permissions, a clear error message with solutions will be returned instead of mock data.

常见HTTP状态码:
- `200` OK - 成功 / Success
- `201` Created - 创建成功 / Created successfully
- `400` Bad Request - 请求参数错误 / Invalid request
- `401` Unauthorized - 未授权/需要登录 / Unauthorized
- `403` Forbidden - 权限不足 / Insufficient permissions (e.g., packet capture)
- `404` Not Found - 资源不存在 / Resource not found
- `422` Unprocessable Entity - 数据验证失败 / Validation failed
- `500` Internal Server Error - 服务器内部错误 / Server error

## 健康检查 / Health Check

**GET** `/health`

检查API服务器状态。

**需要认证 / Requires Authentication**: No

**响应 / Response** (200 OK):
```json
{
  "status": "healthy"
}
```
