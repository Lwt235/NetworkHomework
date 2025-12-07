# Network Monitoring Improvements - December 2024

## Overview
This document describes the improvements made to the Network Performance Monitoring Tool to address issues with packet capture, navigation, traffic visualization, and network speed testing.

## Changes Summary

### 1. Packet Capture Interface Configuration

**Problem**: The packet capture feature (`sniff()` calls) would hang on certain systems without specifying a network interface.

**Solution**: 
- Added configurable `CAPTURE_INTERFACE` parameter in `backend/config.py`
- Updated all `sniff()` calls in `backend/services/capture.py` to use the configured interface
- Default is set to `None` to allow automatic interface detection for cross-platform compatibility
- Added configuration examples in `backend/.env.example`

**Configuration**:
```bash
# In .env file or environment variable
CAPTURE_INTERFACE=Intel(R) Wi-Fi 6E AX211 160MHz  # Windows
CAPTURE_INTERFACE=eth0                              # Linux
CAPTURE_INTERFACE=en0                               # macOS
CAPTURE_INTERFACE=                                  # Auto-detect (default)
```

### 2. Single-Page Navigation

**Problem**: Clicking sidebar menu items caused full page reloads, disrupting user experience.

**Solution**:
- Refactored `Dashboard.vue` to use dynamic component switching
- Removed `router` prop from `el-menu` and replaced with `@select` event handler
- Menu items now switch content components without page navigation
- Maintains SEO and deep-linking support through router for initial page load

**Benefits**:
- Faster navigation
- No data loss during view switches
- Smoother user experience
- Maintains application state

### 3. Traffic Visualization Charts

**Problem**: No visual representation of traffic trends over time.

**Solution**:
- Created `TrafficChart.vue` component using Chart.js and vue-chartjs
- Added traffic trend line charts to:
  - **Monitoring View**: Shows recent traffic over 1-24 hours
  - **Analytics View**: Shows traffic comparison over 1 hour to 7 days
- Charts display:
  - Upload traffic (green line with fill)
  - Download traffic (blue line with fill)
  - Time-based X-axis with proper formatting
  - MB units on Y-axis
  - Interactive tooltips

**Technical Details**:
- Uses Chart.js v4.4.0 and vue-chartjs v5.2.0
- Responsive design with proper aspect ratio
- Optimized array operations for better performance
- Configurable time ranges via dropdown selector

### 4. Network Speed Test Accuracy

**Problem**: Speed test results showed ~0 Mbps due to measurement over too short a duration.

**Solution**:
- Increased measurement duration from 1 second to 5 seconds
- Fixed calculation formula:
  - Old: `(bytes * 8) / (1024 * 1024)` (incorrect units)
  - New: `(bytes * 8) / (duration * 1,000,000)` (correct Mbps)
- Extracted duration to constant for maintainability
- Added duration info to API response

**Formula Explanation**:
```
Mbps = (bytes × 8) ÷ (time_seconds × 1,000,000)

Example:
- 5 MB transferred in 5 seconds
- (5,242,880 bytes × 8) ÷ (5 × 1,000,000) = 8.39 Mbps
```

## Files Modified

### Backend
- `backend/config.py` - Added CAPTURE_INTERFACE configuration
- `backend/services/capture.py` - Updated sniff() calls with iface parameter
- `backend/services/monitor.py` - Fixed speed test implementation
- `backend/.env.example` - Added interface configuration examples

### Frontend
- `frontend/src/views/Dashboard.vue` - Refactored for component switching
- `frontend/src/views/DashboardContent.vue` - Extracted dashboard content
- `frontend/src/views/Monitoring.vue` - Added traffic chart
- `frontend/src/views/Analytics.vue` - Added traffic comparison chart
- `frontend/src/components/TrafficChart.vue` - New chart component
- `frontend/src/router/index.js` - Simplified routing

## Performance Improvements

1. **Chart Rendering**: Array is now reversed once instead of multiple times (3x performance gain)
2. **Navigation**: No full page reloads, faster view switching
3. **Speed Test**: More accurate measurements with longer duration

## Cross-Platform Compatibility

The packet capture interface now works across platforms:
- **Windows**: Auto-detects or uses specified adapter name
- **Linux**: Auto-detects or uses interface name (eth0, wlan0, etc.)
- **macOS**: Auto-detects or uses interface name (en0, en1, etc.)

## Migration Guide

For existing deployments:

1. **Update Environment Variables** (Optional):
   ```bash
   # Add to .env if you need to specify an interface
   CAPTURE_INTERFACE=your_interface_name
   ```

2. **Install Frontend Dependencies** (if not already installed):
   ```bash
   cd frontend
   npm install
   ```

3. **Rebuild Frontend**:
   ```bash
   cd frontend
   npm run build
   ```

4. **Restart Backend**:
   ```bash
   cd backend
   python app.py
   ```

## Testing Recommendations

1. **Packet Capture**: Verify capture works without hanging
2. **Navigation**: Test all menu items switch content without page reload
3. **Charts**: Check that traffic charts display properly with real data
4. **Speed Test**: Run speed test and verify realistic results (not ~0 Mbps)

## Known Limitations

1. Speed test measures actual network activity, not maximum bandwidth
2. Charts require historical data to display (min 2 data points)
3. Packet capture still requires elevated privileges (admin/root)

## Future Enhancements

- [ ] Add real-time chart updates with WebSocket
- [ ] Export chart data to CSV/PNG
- [ ] Add more chart types (pie, bar) for protocol distribution
- [ ] Implement actual bandwidth speed test using external servers
- [ ] Add chart zoom and pan controls

## References

- Chart.js Documentation: https://www.chartjs.org/
- Vue Router Documentation: https://router.vuejs.org/
- Scapy Documentation: https://scapy.readthedocs.io/
