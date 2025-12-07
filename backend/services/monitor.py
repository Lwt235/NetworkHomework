import psutil
import time
import socket

def get_network_traffic():
    """Get current network traffic statistics"""
    net_io = psutil.net_io_counters()
    
    return {
        'bytes_sent': net_io.bytes_sent,
        'bytes_recv': net_io.bytes_recv,
        'packets_sent': net_io.packets_sent,
        'packets_recv': net_io.packets_recv,
        'errin': net_io.errin,
        'errout': net_io.errout,
        'dropin': net_io.dropin,
        'dropout': net_io.dropout
    }


def get_system_stats():
    """Get system statistics"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Network interfaces
    net_if_addrs = psutil.net_if_addrs()
    interfaces = []
    
    for interface_name, addrs in net_if_addrs.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                interfaces.append({
                    'name': interface_name,
                    'address': addr.address,
                    'netmask': addr.netmask
                })
    
    return {
        'cpu': {
            'percent': cpu_percent,
            'count': psutil.cpu_count()
        },
        'memory': {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percent': memory.percent
        },
        'disk': {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        },
        'network_interfaces': interfaces
    }


def run_speed_test():
    """
    Run a simple network speed test
    Note: This measures current network activity over a longer period for better accuracy
    """
    # Measure over 5 seconds for more accurate results
    net_io_start = psutil.net_io_counters()
    time.sleep(5)
    net_io_end = psutil.net_io_counters()
    
    bytes_sent = net_io_end.bytes_sent - net_io_start.bytes_sent
    bytes_recv = net_io_end.bytes_recv - net_io_start.bytes_recv
    
    # Convert to Mbps (bits per second divided by 1,000,000)
    # Formula: (bytes * 8) / (time_in_seconds * 1,000,000)
    download_speed = (bytes_recv * 8) / (5 * 1000 * 1000)  # Mbps
    upload_speed = (bytes_sent * 8) / (5 * 1000 * 1000)  # Mbps
    
    return {
        'download_speed': round(download_speed, 2),
        'upload_speed': round(upload_speed, 2),
        'unit': 'Mbps',
        'measurement_duration': 5
    }


def check_thresholds(config):
    """Check system thresholds and return alerts"""
    alerts = []
    stats = get_system_stats()
    
    if stats['cpu']['percent'] > config.CPU_THRESHOLD:
        alerts.append({
            'type': 'cpu',
            'message': f"CPU usage is at {stats['cpu']['percent']}%",
            'severity': 'warning'
        })
    
    if stats['memory']['percent'] > config.MEMORY_THRESHOLD:
        alerts.append({
            'type': 'memory',
            'message': f"Memory usage is at {stats['memory']['percent']}%",
            'severity': 'warning'
        })
    
    if stats['disk']['percent'] > config.DISK_THRESHOLD:
        alerts.append({
            'type': 'disk',
            'message': f"Disk usage is at {stats['disk']['percent']}%",
            'severity': 'warning'
        })
    
    return alerts
