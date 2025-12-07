from scapy.all import sniff, IP, TCP, UDP, ICMP
from models import db, PacketCapture
from datetime import datetime
import os


def check_capture_permissions():
    """
    Check if the application has permissions to capture packets
    
    Returns:
        dict with 'has_permission' (bool) and 'message' (str)
    """
    try:
        # Try to capture a single packet with a very short timeout
        sniff(count=1, timeout=1, store=False)
        return {
            'has_permission': True,
            'message': 'Packet capture permissions are available'
        }
    except PermissionError:
        return {
            'has_permission': False,
            'message': 'Insufficient permissions for packet capture',
            'instructions': get_permission_instructions()
        }
    except OSError as e:
        if 'Operation not permitted' in str(e) or e.errno == 1:
            return {
                'has_permission': False,
                'message': 'Insufficient permissions for packet capture',
                'instructions': get_permission_instructions()
            }
        else:
            return {
                'has_permission': False,
                'message': f'Error checking permissions: {str(e)}'
            }
    except Exception as e:
        return {
            'has_permission': False,
            'message': f'Error checking permissions: {str(e)}'
        }


def get_permission_instructions():
    """
    Get OS-specific instructions for granting packet capture permissions
    
    Returns:
        dict with OS-specific instructions
    """
    import platform
    import sys
    
    system = platform.system()
    python_executable = os.path.realpath(sys.executable)  # Resolve symlinks
    
    if system == 'Linux':
        return {
            'os': 'Linux',
            'methods': [
                {
                    'method': 'Grant capabilities to Python binary (recommended)',
                    'command': f'sudo setcap cap_net_raw,cap_net_admin=eip {python_executable}',
                    'description': 'This allows Python to capture packets without running as root'
                },
                {
                    'method': 'Run application as root (not recommended for production)',
                    'command': 'sudo python3 app.py',
                    'description': 'Run the entire application with root privileges'
                }
            ]
        }
    elif system == 'Darwin':  # macOS
        return {
            'os': 'macOS',
            'methods': [
                {
                    'method': 'Run application as root',
                    'command': 'sudo python3 app.py',
                    'description': 'macOS requires root privileges for packet capture'
                }
            ]
        }
    elif system == 'Windows':
        return {
            'os': 'Windows',
            'methods': [
                {
                    'method': 'Run Command Prompt as Administrator',
                    'command': 'python app.py',
                    'description': 'Right-click Command Prompt and select "Run as Administrator", then run the command'
                }
            ]
        }
    else:
        return {
            'os': system,
            'methods': [
                {
                    'method': 'Run with elevated privileges',
                    'command': 'Contact your system administrator',
                    'description': 'Packet capture requires elevated privileges on this system'
                }
            ]
        }


def format_permission_instructions():
    """
    Format permission instructions as a user-friendly string
    
    Returns:
        str: Formatted instructions for granting permissions
    """
    instructions = get_permission_instructions()
    lines = [f"Insufficient permissions for packet capture on {instructions['os']}."]
    lines.append("Please use one of the following methods:")
    
    for i, method in enumerate(instructions['methods'], 1):
        lines.append(f"\n{i}. {method['method']}")
        lines.append(f"   Command: {method['command']}")
        lines.append(f"   {method['description']}")
    
    return '\n'.join(lines)


def packet_callback(packet, user_id, captured_packets):
    """Callback function to process captured packets"""
    try:
        if IP in packet:
            protocol = None
            src_port = None
            dst_port = None
            info = ""
            
            if TCP in packet:
                protocol = 'TCP'
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                info = f"Flags: {packet[TCP].flags}"
            elif UDP in packet:
                protocol = 'UDP'
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
            elif ICMP in packet:
                protocol = 'ICMP'
                info = f"Type: {packet[ICMP].type}"
            else:
                protocol = 'IP'
            
            packet_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'protocol': protocol,
                'src_ip': packet[IP].src,
                'dst_ip': packet[IP].dst,
                'src_port': src_port,
                'dst_port': dst_port,
                'length': len(packet),
                'info': info
            }
            
            # Save to database
            capture = PacketCapture(
                protocol=protocol,
                src_ip=packet[IP].src,
                dst_ip=packet[IP].dst,
                src_port=src_port,
                dst_port=dst_port,
                length=len(packet),
                info=info,
                user_id=user_id
            )
            db.session.add(capture)
            
            captured_packets.append(packet_data)
            
    except Exception as e:
        print(f"Error processing packet: {e}")


def start_packet_capture(protocol='all', count=100, timeout=10, user_id=None):
    """
    Start capturing network packets
    
    Args:
        protocol: Protocol filter (tcp, udp, ip, icmp, or all)
        count: Number of packets to capture
        timeout: Capture timeout in seconds
        user_id: User ID for database storage
    
    Returns:
        List of captured packet data
        
    Raises:
        PermissionError: If the process doesn't have sufficient permissions
        RuntimeError: If packet capture fails for other reasons
    """
    captured_packets = []
    
    # Build filter string
    filter_str = None
    if protocol.lower() == 'tcp':
        filter_str = 'tcp'
    elif protocol.lower() == 'udp':
        filter_str = 'udp'
    elif protocol.lower() == 'icmp':
        filter_str = 'icmp'
    elif protocol.lower() == 'ip':
        filter_str = 'ip'
    
    try:
        # Capture packets
        # Note: This requires root/admin privileges
        sniff(
            filter=filter_str,
            prn=lambda pkt: packet_callback(pkt, user_id, captured_packets),
            count=count,
            timeout=timeout,
            store=False
        )
        
        # Commit all captured packets to database
        db.session.commit()
        
    except PermissionError as e:
        # Permission error - need elevated privileges
        import logging
        logging.error(f"Packet capture permission denied: {e}")
        raise PermissionError(format_permission_instructions())
    except OSError as e:
        if 'Operation not permitted' in str(e) or e.errno == 1:
            # This is also a permission error
            import logging
            logging.error(f"Packet capture permission denied (OSError): {e}")
            raise PermissionError(format_permission_instructions())
        else:
            raise RuntimeError(f"Packet capture failed: {str(e)}")
    except Exception as e:
        # Other errors
        import logging
        logging.error(f"Packet capture error: {e}")
        raise RuntimeError(f"Packet capture failed: {str(e)}")
    
    return captured_packets



def get_protocol_stats(user_id, start_time):
    """Get statistics about captured packets by protocol"""
    from sqlalchemy import func
    
    # Query packet counts by protocol
    protocol_counts = db.session.query(
        PacketCapture.protocol,
        func.count(PacketCapture.id).label('count'),
        func.sum(PacketCapture.length).label('total_bytes')
    ).filter(
        PacketCapture.user_id == user_id,
        PacketCapture.timestamp >= start_time
    ).group_by(PacketCapture.protocol).all()
    
    stats = {
        'protocols': [],
        'total_packets': 0,
        'total_bytes': 0
    }
    
    for proto, count, total_bytes in protocol_counts:
        stats['protocols'].append({
            'protocol': proto,
            'count': count,
            'bytes': total_bytes or 0
        })
        stats['total_packets'] += count
        stats['total_bytes'] += total_bytes or 0
    
    return stats
