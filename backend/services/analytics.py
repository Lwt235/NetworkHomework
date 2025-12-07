from models import db, TrafficLog, Alert
from datetime import datetime
from sqlalchemy import func

def get_traffic_analytics(device_id=None, hours=24):
    """Get traffic analytics for visualization"""
    from datetime import timedelta
    
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    query = TrafficLog.query.filter(TrafficLog.timestamp >= start_time)
    if device_id:
        query = query.filter(TrafficLog.device_id == device_id)
    
    logs = query.order_by(TrafficLog.timestamp).all()
    
    # Calculate statistics
    total_sent = sum(log.bytes_sent for log in logs)
    total_recv = sum(log.bytes_recv for log in logs)
    total_packets_sent = sum(log.packets_sent for log in logs)
    total_packets_recv = sum(log.packets_recv for log in logs)
    
    # Group by hour for visualization
    hourly_data = []
    if logs:
        current_hour = logs[0].timestamp.replace(minute=0, second=0, microsecond=0)
        hour_sent = 0
        hour_recv = 0
        
        for log in logs:
            log_hour = log.timestamp.replace(minute=0, second=0, microsecond=0)
            
            if log_hour != current_hour:
                hourly_data.append({
                    'timestamp': current_hour.isoformat(),
                    'bytes_sent': hour_sent,
                    'bytes_recv': hour_recv
                })
                current_hour = log_hour
                hour_sent = 0
                hour_recv = 0
            
            hour_sent += log.bytes_sent
            hour_recv += log.bytes_recv
        
        # Add last hour
        if hour_sent > 0 or hour_recv > 0:
            hourly_data.append({
                'timestamp': current_hour.isoformat(),
                'bytes_sent': hour_sent,
                'bytes_recv': hour_recv
            })
    
    return {
        'summary': {
            'total_bytes_sent': total_sent,
            'total_bytes_recv': total_recv,
            'total_packets_sent': total_packets_sent,
            'total_packets_recv': total_packets_recv
        },
        'hourly_data': hourly_data
    }


def get_alert_statistics(user_id, days=7):
    """Get alert statistics"""
    from datetime import timedelta
    
    start_time = datetime.utcnow() - timedelta(days=days)
    
    # Count alerts by type
    alert_counts = db.session.query(
        Alert.alert_type,
        func.count(Alert.id).label('count')
    ).filter(
        Alert.user_id == user_id,
        Alert.created_at >= start_time
    ).group_by(Alert.alert_type).all()
    
    # Count by severity
    severity_counts = db.session.query(
        Alert.severity,
        func.count(Alert.id).label('count')
    ).filter(
        Alert.user_id == user_id,
        Alert.created_at >= start_time
    ).group_by(Alert.severity).all()
    
    return {
        'by_type': [{'type': t, 'count': c} for t, c in alert_counts],
        'by_severity': [{'severity': s, 'count': c} for s, c in severity_counts]
    }


def create_alert(alert_type, message, severity, user_id, device_id=None):
    """Create a new alert"""
    alert = Alert(
        alert_type=alert_type,
        message=message,
        severity=severity,
        user_id=user_id,
        device_id=device_id
    )
    
    db.session.add(alert)
    db.session.commit()
    
    return alert
