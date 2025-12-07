import psutil
import time
import socket
import speedtest

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
    Run network speed test using speedtest-cli package
    Returns download and upload speeds in Mbps
    """
    try:
        # Initialize speedtest
        st = speedtest.Speedtest()
        
        # Get best server based on ping
        st.get_best_server()
        
        # Perform download speed test
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        # Perform upload speed test
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        
        # Get ping
        ping = st.results.ping
        
        return {
            'download_speed': round(download_speed, 2),
            'upload_speed': round(upload_speed, 2),
            'ping': round(ping, 2),
            'unit': 'Mbps',
            'server': st.results.server.get('host', 'Unknown'),
            'server_location': f"{st.results.server.get('name', 'Unknown')}, {st.results.server.get('country', 'Unknown')}"
        }
    except Exception as e:
        # Fallback to network activity measurement if speedtest fails
        # This is a backup method and won't be as accurate but ensures functionality
        raise RuntimeError(f"Speed test failed: {str(e)}. Please check your internet connection.")


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
