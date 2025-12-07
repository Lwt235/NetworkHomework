import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///network_monitor.db'
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
    NETWORK_THRESHOLD = 90  # percentage
    
    # Packet Capture
    CAPTURE_TIMEOUT = 60  # seconds
    MAX_PACKETS = 1000
