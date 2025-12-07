from scapy.all import sniff, IP, TCP, UDP, ICMP
from models import db, PacketCapture
from datetime import datetime

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
        
    except Exception as e:
        # If permission denied or scapy not available, return mock data
        import logging
        logging.warning(f"Packet capture error: {e}. Using mock data instead.")
        print(f"Warning: Packet capture failed ({e}). Using mock data for demonstration.")
        captured_packets = generate_mock_packets(count, protocol)
    
    return captured_packets


def generate_mock_packets(count, protocol):
    """Generate mock packet data for testing/demo purposes"""
    import random
    
    protocols = ['TCP', 'UDP', 'ICMP'] if protocol == 'all' else [protocol.upper()]
    mock_packets = []
    
    for i in range(min(count, 20)):
        proto = random.choice(protocols)
        packet_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'protocol': proto,
            'src_ip': f"192.168.1.{random.randint(1, 254)}",
            'dst_ip': f"192.168.1.{random.randint(1, 254)}",
            'src_port': random.randint(1024, 65535) if proto in ['TCP', 'UDP'] else None,
            'dst_port': random.randint(1, 1024) if proto in ['TCP', 'UDP'] else None,
            'length': random.randint(64, 1500),
            'info': f"Mock packet {i+1}"
        }
        mock_packets.append(packet_data)
    
    return mock_packets


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
