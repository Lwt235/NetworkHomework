from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Device
from datetime import datetime

devices_bp = Blueprint('devices', __name__)

@devices_bp.route('', methods=['GET'])
@jwt_required()
def get_devices():
    """Get all devices for current user"""
    user_id = int(get_jwt_identity())
    devices = Device.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'devices': [device.to_dict() for device in devices]
    }), 200


@devices_bp.route('/<int:device_id>', methods=['GET'])
@jwt_required()
def get_device(device_id):
    """Get specific device"""
    user_id = int(get_jwt_identity())
    device = Device.query.filter_by(id=device_id, user_id=user_id).first()
    
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    return jsonify({'device': device.to_dict()}), 200


@devices_bp.route('', methods=['POST'])
@jwt_required()
def add_device():
    """Add a new device"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('ip_address'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    device = Device(
        name=data['name'],
        ip_address=data['ip_address'],
        device_type=data.get('device_type', 'unknown'),
        user_id=user_id
    )
    
    db.session.add(device)
    db.session.commit()
    
    return jsonify({
        'message': 'Device added successfully',
        'device': device.to_dict()
    }), 201


@devices_bp.route('/<int:device_id>', methods=['PUT'])
@jwt_required()
def update_device(device_id):
    """Update device information"""
    user_id = int(get_jwt_identity())
    device = Device.query.filter_by(id=device_id, user_id=user_id).first()
    
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        device.name = data['name']
    if 'ip_address' in data:
        device.ip_address = data['ip_address']
    if 'device_type' in data:
        device.device_type = data['device_type']
    if 'status' in data:
        device.status = data['status']
    
    device.last_seen = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Device updated successfully',
        'device': device.to_dict()
    }), 200


@devices_bp.route('/<int:device_id>', methods=['DELETE'])
@jwt_required()
def delete_device(device_id):
    """Delete a device"""
    user_id = int(get_jwt_identity())
    device = Device.query.filter_by(id=device_id, user_id=user_id).first()
    
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    db.session.delete(device)
    db.session.commit()
    
    return jsonify({'message': 'Device deleted successfully'}), 200
