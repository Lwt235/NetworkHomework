from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, TrafficLog, Alert
from services.monitor import get_network_traffic, get_system_stats, run_speed_test
from datetime import datetime, timedelta

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/traffic', methods=['GET'])
@jwt_required()
def get_traffic():
    """Get current network traffic data"""
    try:
        traffic_data = get_network_traffic()
        return jsonify({
            'traffic': traffic_data,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@monitoring_bp.route('/system', methods=['GET'])
@jwt_required()
def get_system():
    """Get system statistics"""
    try:
        system_stats = get_system_stats()
        return jsonify({
            'system': system_stats,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@monitoring_bp.route('/speed-test', methods=['POST'])
@jwt_required()
def speed_test():
    """Run network speed test"""
    try:
        results = run_speed_test()
        return jsonify({
            'results': results,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@monitoring_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """Get historical traffic data"""
    from config import Config
    user_id = int(get_jwt_identity())
    
    # Get time range from query params
    hours = request.args.get('hours', 24, type=int)
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    # Get device_id if provided
    device_id = request.args.get('device_id', type=int)
    
    # Get limit from config
    limit = getattr(Config, 'MAX_HISTORY_RECORDS', 1000)
    
    query = TrafficLog.query.filter(TrafficLog.timestamp >= start_time)
    
    if device_id:
        query = query.filter(TrafficLog.device_id == device_id)
    
    logs = query.order_by(TrafficLog.timestamp.desc()).limit(limit).all()
    
    return jsonify({
        'history': [log.to_dict() for log in logs],
        'count': len(logs)
    }), 200


@monitoring_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    """Get alerts for current user"""
    user_id = int(get_jwt_identity())
    
    status = request.args.get('status', 'active')
    alerts = Alert.query.filter_by(user_id=user_id, status=status).order_by(Alert.created_at.desc()).limit(100).all()
    
    return jsonify({
        'alerts': [alert.to_dict() for alert in alerts],
        'count': len(alerts)
    }), 200


@monitoring_bp.route('/alerts/<int:alert_id>/resolve', methods=['PUT'])
@jwt_required()
def resolve_alert(alert_id):
    """Resolve an alert"""
    user_id = int(get_jwt_identity())
    alert = Alert.query.filter_by(id=alert_id, user_id=user_id).first()
    
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    alert.status = 'resolved'
    alert.resolved_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Alert resolved successfully',
        'alert': alert.to_dict()
    }), 200


@monitoring_bp.route('/system-history', methods=['GET'])
@jwt_required()
def get_system_history():
    """Get historical system resource data"""
    from models import SystemResourceLog
    
    # Get time range from query params
    hours = request.args.get('hours', 24, type=int)
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    # Get limit from config
    from config import Config
    limit = getattr(Config, 'MAX_HISTORY_RECORDS', 1000)
    
    logs = SystemResourceLog.query.filter(
        SystemResourceLog.timestamp >= start_time
    ).order_by(SystemResourceLog.timestamp.desc()).limit(limit).all()
    
    return jsonify({
        'history': [log.to_dict() for log in logs],
        'count': len(logs)
    }), 200
