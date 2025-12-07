import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database - MySQL only
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://network_monitor_user:your_secure_password_here@localhost:3306/network_monitor'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # CORS
    CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']
    
    # Monitoring
    TRAFFIC_SAMPLE_INTERVAL = 1  # seconds
    MAX_HISTORY_RECORDS = 1000
    
    # Alerts
    CPU_THRESHOLD = 80  # percentage
    MEMORY_THRESHOLD = 80  # percentage
    DISK_THRESHOLD = 90  # percentage
    NETWORK_THRESHOLD = 90  # percentage
    
    # Packet Capture
    CAPTURE_TIMEOUT = 60  # seconds
    MAX_PACKETS = 1000
    # Network interface for packet capture (None = default interface)
    # Example: 'Intel(R) Wi-Fi 6E AX211 160MHz' on Windows, 'eth0' on Linux
    # Set to None or empty string to let scapy choose the default interface automatically
    CAPTURE_INTERFACE = os.environ.get('CAPTURE_INTERFACE') or None
