from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


class Device(db.Model):
    """Network device model"""
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    device_type = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'ip_address': self.ip_address,
            'device_type': self.device_type,
            'status': self.status,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'created_at': self.created_at.isoformat()
        }


class TrafficLog(db.Model):
    """Network traffic log model"""
    __tablename__ = 'traffic_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    bytes_sent = db.Column(db.BigInteger, default=0)
    bytes_recv = db.Column(db.BigInteger, default=0)
    packets_sent = db.Column(db.Integer, default=0)
    packets_recv = db.Column(db.Integer, default=0)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'bytes_sent': self.bytes_sent,
            'bytes_recv': self.bytes_recv,
            'packets_sent': self.packets_sent,
            'packets_recv': self.packets_recv,
            'device_id': self.device_id
        }


class Alert(db.Model):
    """Alert model for threshold violations"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(20), default='warning')
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    resolved_at = db.Column(db.DateTime)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'alert_type': self.alert_type,
            'message': self.message,
            'severity': self.severity,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'device_id': self.device_id
        }


class PacketCapture(db.Model):
    """Packet capture records"""
    __tablename__ = 'packet_captures'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    protocol = db.Column(db.String(10))
    src_ip = db.Column(db.String(45))
    dst_ip = db.Column(db.String(45))
    src_port = db.Column(db.Integer)
    dst_port = db.Column(db.Integer)
    length = db.Column(db.Integer)
    info = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'protocol': self.protocol,
            'src_ip': self.src_ip,
            'dst_ip': self.dst_ip,
            'src_port': self.src_port,
            'dst_port': self.dst_port,
            'length': self.length,
            'info': self.info
        }


class SystemResourceLog(db.Model):
    """System resource usage log model for historical tracking"""
    __tablename__ = 'system_resource_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    cpu_percent = db.Column(db.Float, default=0)
    memory_percent = db.Column(db.Float, default=0)
    memory_used = db.Column(db.BigInteger, default=0)
    memory_total = db.Column(db.BigInteger, default=0)
    disk_percent = db.Column(db.Float, default=0)
    disk_used = db.Column(db.BigInteger, default=0)
    disk_total = db.Column(db.BigInteger, default=0)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'memory_used': self.memory_used,
            'memory_total': self.memory_total,
            'disk_percent': self.disk_percent,
            'disk_used': self.disk_used,
            'disk_total': self.disk_total
        }
