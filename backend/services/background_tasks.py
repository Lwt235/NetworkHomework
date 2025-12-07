"""
Background tasks for automatic monitoring and alert generation
"""
import threading
import time
from datetime import datetime
from services.monitor import get_network_traffic, get_system_stats
from services.analytics import create_alert
from models import db, TrafficLog, SystemResourceLog, User, Alert


class BackgroundMonitor:
    """Background monitor for automatic traffic logging and threshold checking"""
    
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.running = False
        self.thread = None
        self.log_interval = 60  # Log traffic every 60 seconds
        self.check_interval = 30  # Check thresholds every 30 seconds
    
    def start(self):
        """Start the background monitoring thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
            print("Background monitor started")
    
    def stop(self):
        """Stop the background monitoring thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
            print("Background monitor stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        last_log_time = time.time()
        last_check_time = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # Log traffic data periodically
                if current_time - last_log_time >= self.log_interval:
                    self._log_traffic_data()
                    last_log_time = current_time
                
                # Check thresholds periodically
                if current_time - last_check_time >= self.check_interval:
                    self._check_thresholds()
                    last_check_time = current_time
                
                # Sleep briefly to avoid busy waiting
                time.sleep(1)
                
            except Exception as e:
                print(f"Error in background monitor: {e}")
                time.sleep(5)  # Wait before retrying on error
    
    def _log_traffic_data(self):
        """Log current traffic data to database"""
        try:
            with self.app.app_context():
                traffic_data = get_network_traffic()
                
                # Create a new traffic log entry
                log_entry = TrafficLog(
                    timestamp=datetime.utcnow(),
                    bytes_sent=traffic_data['bytes_sent'],
                    bytes_recv=traffic_data['bytes_recv'],
                    packets_sent=traffic_data['packets_sent'],
                    packets_recv=traffic_data['packets_recv']
                )
                
                db.session.add(log_entry)
                
                # Also log system resource data
                system_stats = get_system_stats()
                
                resource_entry = SystemResourceLog(
                    timestamp=datetime.utcnow(),
                    cpu_percent=system_stats['cpu']['percent'],
                    memory_percent=system_stats['memory']['percent'],
                    memory_used=system_stats['memory']['used'],
                    memory_total=system_stats['memory']['total'],
                    disk_percent=system_stats['disk']['percent'],
                    disk_used=system_stats['disk']['used'],
                    disk_total=system_stats['disk']['total']
                )
                
                db.session.add(resource_entry)
                db.session.commit()
                
        except Exception as e:
            print(f"Error logging traffic data: {e}")
    
    def _check_thresholds(self):
        """Check system thresholds and create alerts if needed"""
        try:
            with self.app.app_context():
                system_stats = get_system_stats()
                
                # Get all users to create alerts for
                users = User.query.all()
                
                for user in users:
                    # Check CPU threshold
                    if system_stats['cpu']['percent'] > self.config.CPU_THRESHOLD:
                        self._create_threshold_alert(
                            user.id,
                            'cpu',
                            f"CPU usage is at {system_stats['cpu']['percent']}%",
                            'warning'
                        )
                    
                    # Check memory threshold
                    if system_stats['memory']['percent'] > self.config.MEMORY_THRESHOLD:
                        self._create_threshold_alert(
                            user.id,
                            'memory',
                            f"Memory usage is at {system_stats['memory']['percent']}%",
                            'warning'
                        )
                    
                    # Check disk threshold
                    if system_stats['disk']['percent'] > self.config.DISK_THRESHOLD:
                        self._create_threshold_alert(
                            user.id,
                            'disk',
                            f"Disk usage is at {system_stats['disk']['percent']}%",
                            'warning'
                        )
                
        except Exception as e:
            print(f"Error checking thresholds: {e}")
    
    def _create_threshold_alert(self, user_id, alert_type, message, severity):
        """Create an alert if one doesn't already exist for this threshold"""
        # Check if there's already an active alert of this type for this user
        existing_alert = Alert.query.filter_by(
            user_id=user_id,
            alert_type=alert_type,
            status='active'
        ).first()
        
        # Only create new alert if one doesn't exist
        if not existing_alert:
            create_alert(alert_type, message, severity, user_id)
            print(f"Created alert for user {user_id}: {message}")


# Global background monitor instance
background_monitor = None


def init_background_monitor(app, config):
    """Initialize and start the background monitor"""
    global background_monitor
    
    if background_monitor is None:
        background_monitor = BackgroundMonitor(app, config)
        background_monitor.start()
    
    return background_monitor


def stop_background_monitor():
    """Stop the background monitor"""
    global background_monitor
    
    if background_monitor:
        background_monitor.stop()
        background_monitor = None
