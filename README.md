# Network Performance Monitoring Tool

A comprehensive network performance monitoring tool with user authentication, device management, real-time traffic monitoring, packet capture analysis, and alerting capabilities.

## Features

1. **User Authentication**
   - User registration and login
   - JWT-based authentication
   - Secure password hashing

2. **Network Device Management**
   - View network device information
   - Monitor device status
   - Track device performance

3. **Real-time Monitoring**
   - Data traffic collection
   - Network speed testing
   - Real-time status updates

4. **Packet Analysis**
   - TCP/UDP/IP packet capture
   - Protocol analysis
   - Traffic inspection

5. **Performance Analytics**
   - Historical data reports
   - Statistical analysis charts
   - Network load analysis
   - Threshold-based alerts

## Technology Stack

### Backend
- Python 3.8+
- Flask (Web Framework)
- Flask-SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- Flask-CORS (Cross-Origin Support)
- Scapy (Packet Capture)
- psutil (System Monitoring)

### Frontend
- Vue 3
- Vue Router
- Axios (HTTP Client)
- Chart.js (Data Visualization)
- Element Plus (UI Components)

## Project Structure

```
NetworkHomework/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── models.py           # Database models
│   ├── routes/
│   │   ├── auth.py         # Authentication routes
│   │   ├── devices.py      # Device management routes
│   │   ├── monitoring.py   # Monitoring routes
│   │   └── analysis.py     # Analysis routes
│   ├── services/
│   │   ├── capture.py      # Packet capture service
│   │   ├── monitor.py      # Monitoring service
│   │   └── analytics.py    # Analytics service
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Page views
│   │   ├── router/         # Vue router
│   │   ├── store/          # State management
│   │   └── main.js         # Entry point
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Build configuration
└── README.md               # This file
```

## Installation

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Start the backend server (default: http://localhost:5000)
2. Start the frontend development server (default: http://localhost:5173)
3. Open your browser and navigate to the frontend URL
4. Register a new account or login
5. Access the monitoring dashboard

## Configuration

Backend configuration can be modified in `backend/config.py`:
- Database URI
- JWT secret key
- Alert thresholds
- Capture settings

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Devices
- `GET /api/devices` - List all devices
- `GET /api/devices/:id` - Get device details
- `POST /api/devices` - Add new device

### Monitoring
- `GET /api/monitoring/traffic` - Get real-time traffic data
- `GET /api/monitoring/speed-test` - Run network speed test
- `GET /api/monitoring/history` - Get historical data

### Analysis
- `POST /api/analysis/capture` - Start packet capture
- `GET /api/analysis/packets` - Get captured packets
- `GET /api/analysis/stats` - Get network statistics

## Security Considerations

- All passwords are hashed using bcrypt
- JWT tokens are used for authentication
- CORS is configured for secure cross-origin requests
- Input validation on all endpoints

## Requirements

### System Requirements
- Python 3.8 or higher
- Node.js 14 or higher
- Administrator/root privileges for packet capture

### Python Packages
See `backend/requirements.txt`

### Node Packages
See `frontend/package.json`

## License

MIT License

## Contributing

Feel free to submit issues and pull requests.