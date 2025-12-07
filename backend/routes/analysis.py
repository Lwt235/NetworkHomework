from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, PacketCapture
from services.capture import start_packet_capture, get_protocol_stats
from datetime import datetime, timedelta

analysis_bp = Blueprint('analysis', __name__)

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
    
    try:
        packets = start_packet_capture(protocol=protocol, count=count, timeout=timeout, user_id=user_id)
        
        return jsonify({
            'message': 'Packet capture completed',
            'packets': packets,
            'count': len(packets)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
        
        return jsonify({
            'stats': protocol_stats,
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
