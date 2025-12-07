from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, PacketCapture
from services.capture import start_packet_capture, get_protocol_stats, check_capture_permissions, get_packet_analysis
from datetime import datetime, timedelta

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/check-permissions', methods=['GET'])
@jwt_required()
def check_permissions():
    """Check if the application has packet capture permissions"""
    try:
        result = check_capture_permissions()
        status_code = 200 if result['has_permission'] else 403
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            'error': 'Permission check failed',
            'message': str(e)
        }), 500

@analysis_bp.route('/capture', methods=['POST'])
@jwt_required()
def capture_packets():
    """Start packet capture"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # Get capture parameters
    protocol = data.get('protocol', 'all')  # tcp, udp, ip, or all
    count = data.get('count', 100)
    timeout = data.get('timeout', 10)
    clear_previous = data.get('clear_previous', False)  # Whether to clear previous captures
    
    try:
        # Clear previous captures if requested
        if clear_previous:
            deleted_count = PacketCapture.query.filter_by(user_id=user_id).delete()
            db.session.commit()
        
        packets = start_packet_capture(protocol=protocol, count=count, timeout=timeout, user_id=user_id)
        
        return jsonify({
            'message': 'Packet capture completed',
            'packets': packets,
            'count': len(packets),
            'cleared_previous': clear_previous
        }), 200
    except PermissionError as e:
        return jsonify({
            'error': 'Permission denied',
            'message': str(e),
            'requires_elevated_privileges': True
        }), 403
    except RuntimeError as e:
        return jsonify({
            'error': 'Capture failed',
            'message': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'Unexpected error',
            'message': str(e)
        }), 500


@analysis_bp.route('/clear-packets', methods=['DELETE'])
@jwt_required()
def clear_packets():
    """Clear all captured packets for the current user"""
    user_id = int(get_jwt_identity())
    
    try:
        deleted_count = PacketCapture.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({
            'message': 'Packets cleared successfully',
            'deleted_count': deleted_count
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to clear packets',
            'message': str(e)
        }), 500


@analysis_bp.route('/packets', methods=['GET'])
@jwt_required()
def get_packets():
    """Get captured packets"""
    user_id = int(get_jwt_identity())
    
    # Get time range
    hours = request.args.get('hours', 1, type=int)
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    # Get protocol filter
    protocol = request.args.get('protocol')
    
    query = PacketCapture.query.filter(
        PacketCapture.user_id == user_id,
        PacketCapture.timestamp >= start_time
    )
    
    if protocol:
        query = query.filter(PacketCapture.protocol == protocol)
    
    packets = query.order_by(PacketCapture.timestamp.desc()).limit(500).all()
    
    return jsonify({
        'packets': [packet.to_dict() for packet in packets],
        'count': len(packets)
    }), 200


@analysis_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get network statistics and analysis"""
    user_id = int(get_jwt_identity())
    
    # Get time range
    hours = request.args.get('hours', 24, type=int)
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    # Get protocol statistics
    try:
        protocol_stats = get_protocol_stats(user_id, start_time)
        packet_analysis = get_packet_analysis(user_id, start_time)
        
        return jsonify({
            'stats': protocol_stats,
            'analysis': packet_analysis,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analysis_bp.route('/protocols', methods=['GET'])
@jwt_required()
def get_protocols():
    """Get available protocol types"""
    protocols = [
        {'value': 'tcp', 'label': 'TCP'},
        {'value': 'udp', 'label': 'UDP'},
        {'value': 'ip', 'label': 'IP'},
        {'value': 'icmp', 'label': 'ICMP'},
        {'value': 'all', 'label': 'All Protocols'}
    ]
    
    return jsonify({'protocols': protocols}), 200
