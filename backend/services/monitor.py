import psutil
import time
import socket
import speedtest

# Store previous network stats for load calculation
_previous_net_io = None
_previous_timestamp = None

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


def get_network_load():
    """
    Calculate current network load based on recent traffic
    Returns load metrics including bytes/second and utilization percentage
    """
    global _previous_net_io, _previous_timestamp
    
    current_net_io = psutil.net_io_counters()
    current_timestamp = time.time()
    
    # If this is the first call, just store the values
    if _previous_net_io is None or _previous_timestamp is None:
        _previous_net_io = current_net_io
        _previous_timestamp = current_timestamp
        # Wait a bit to get meaningful data
        time.sleep(1)
        current_net_io = psutil.net_io_counters()
        current_timestamp = time.time()
    
    # Calculate time delta
    time_delta = current_timestamp - _previous_timestamp
    
    if time_delta == 0:
        time_delta = 1  # Avoid division by zero
    
    # Calculate bytes per second
    bytes_sent_per_sec = (current_net_io.bytes_sent - _previous_net_io.bytes_sent) / time_delta
    bytes_recv_per_sec = (current_net_io.bytes_recv - _previous_net_io.bytes_recv) / time_delta
    
    # Calculate packets per second
    packets_sent_per_sec = (current_net_io.packets_sent - _previous_net_io.packets_sent) / time_delta
    packets_recv_per_sec = (current_net_io.packets_recv - _previous_net_io.packets_recv) / time_delta
    
    # Estimate network utilization (assuming typical 100 Mbps network)
    # This is a rough estimate - actual capacity varies by network
    typical_capacity_bytes_per_sec = 100 * 1000 * 1000 / 8  # 100 Mbps in bytes/sec
    
    upload_utilization = min(100, (bytes_sent_per_sec / typical_capacity_bytes_per_sec) * 100)
    download_utilization = min(100, (bytes_recv_per_sec / typical_capacity_bytes_per_sec) * 100)
    total_utilization = min(100, ((bytes_sent_per_sec + bytes_recv_per_sec) / (2 * typical_capacity_bytes_per_sec)) * 100)
    
    # Update previous values
    _previous_net_io = current_net_io
    _previous_timestamp = current_timestamp
    
    return {
        'bytes_sent_per_sec': round(bytes_sent_per_sec, 2),
        'bytes_recv_per_sec': round(bytes_recv_per_sec, 2),
        'packets_sent_per_sec': round(packets_sent_per_sec, 2),
        'packets_recv_per_sec': round(packets_recv_per_sec, 2),
        'upload_utilization_percent': round(upload_utilization, 2),
        'download_utilization_percent': round(download_utilization, 2),
        'total_utilization_percent': round(total_utilization, 2),
        'timestamp': current_timestamp
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
    import logging
    try:
        # Initialize speedtest with timeout
        st = speedtest.Speedtest(secure=True)
        
        # Get best server based on ping
        logging.info("Getting best server for speed test...")
        st.get_best_server()
        
        # Perform download speed test
        logging.info("Running download speed test...")
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        
        # Perform upload speed test
        logging.info("Running upload speed test...")
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        
        # Get ping
        ping = st.results.ping
        
        logging.info(f"Speed test completed: Download={download_speed:.2f} Mbps, Upload={upload_speed:.2f} Mbps, Ping={ping:.2f} ms")
        
        return {
            'download_speed': round(download_speed, 2),
            'upload_speed': round(upload_speed, 2),
            'ping': round(ping, 2),
            'unit': 'Mbps',
            'server': st.results.server.get('host', 'Unknown'),
            'server_location': f"{st.results.server.get('name', 'Unknown')}, {st.results.server.get('country', 'Unknown')}"
        }
    except speedtest.ConfigRetrievalError as e:
        logging.error(f"Speed test configuration error: {str(e)}")
        raise RuntimeError("Failed to retrieve speedtest configuration. Please check your internet connection.")
    except speedtest.NoMatchedServers as e:
        logging.error(f"No speedtest servers found: {str(e)}")
        raise RuntimeError("No speedtest servers available. Please try again later.")
    except speedtest.SpeedtestException as e:
        logging.error(f"Speedtest exception: {str(e)}")
        raise RuntimeError(f"Speed test failed: {str(e)}")
    except Exception as e:
        # Log the detailed error for debugging
        logging.error(f"Speed test error: {str(e)}", exc_info=True)
        # Raise a user-friendly error
        raise RuntimeError("Speed test failed. Please check your internet connection and try again.")


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
