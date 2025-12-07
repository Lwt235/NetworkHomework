import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add token
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  register: (data) => apiClient.post('/auth/register', data),
  login: (data) => apiClient.post('/auth/login', data),
  getCurrentUser: () => apiClient.get('/auth/me')
}

// Devices API
export const devicesAPI = {
  getDevices: () => apiClient.get('/devices'),
  getDevice: (id) => apiClient.get(`/devices/${id}`),
  addDevice: (data) => apiClient.post('/devices', data),
  updateDevice: (id, data) => apiClient.put(`/devices/${id}`, data),
  deleteDevice: (id) => apiClient.delete(`/devices/${id}`)
}

// Monitoring API
export const monitoringAPI = {
  getTraffic: () => apiClient.get('/monitoring/traffic'),
  getSystem: () => apiClient.get('/monitoring/system'),
  runSpeedTest: () => apiClient.post('/monitoring/speed-test'),
  getHistory: (params) => apiClient.get('/monitoring/history', { params }),
  getSystemHistory: (params) => apiClient.get('/monitoring/system-history', { params }),
  getAlerts: (params) => apiClient.get('/monitoring/alerts', { params }),
  resolveAlert: (id) => apiClient.put(`/monitoring/alerts/${id}/resolve`)
}

// Analysis API
export const analysisAPI = {
  capturePackets: (data) => apiClient.post('/analysis/capture', data),
  getPackets: (params) => apiClient.get('/analysis/packets', { params }),
  getStats: (params) => apiClient.get('/analysis/stats', { params }),
  getProtocols: () => apiClient.get('/analysis/protocols')
}

export default apiClient
