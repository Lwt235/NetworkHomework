<template>
  <div class="dashboard-content">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#409eff"><Monitor /></el-icon>
            <div class="stat-text">
              <div class="stat-value">{{ deviceCount }}</div>
              <div class="stat-label">设备数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#67c23a"><Upload /></el-icon>
            <div class="stat-text">
              <div class="stat-value">{{ uploadSpeed }} Mbps</div>
              <div class="stat-label">上传速度</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#e6a23c"><Download /></el-icon>
            <div class="stat-text">
              <div class="stat-value">{{ downloadSpeed }} Mbps</div>
              <div class="stat-label">下载速度</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#f56c6c"><Warning /></el-icon>
            <div class="stat-text">
              <div class="stat-value">{{ alertCount }}</div>
              <div class="stat-label">活动警报</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统状态</span>
            </div>
          </template>
          <div class="system-stats" v-if="systemStats">
            <div class="stat-item">
              <span>CPU 使用率:</span>
              <el-progress :percentage="systemStats.cpu?.percent || 0" />
            </div>
            <div class="stat-item">
              <span>内存使用率:</span>
              <el-progress :percentage="systemStats.memory?.percent || 0" :color="getProgressColor(systemStats.memory?.percent)" />
            </div>
            <div class="stat-item">
              <span>磁盘使用率:</span>
              <el-progress :percentage="systemStats.disk?.percent || 0" :color="getProgressColor(systemStats.disk?.percent)" />
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近警报</span>
            </div>
          </template>
          <el-timeline v-if="recentAlerts.length > 0">
            <el-timeline-item
              v-for="alert in recentAlerts"
              :key="alert.id"
              :timestamp="formatTime(alert.created_at)"
              :color="getAlertColor(alert.severity)"
            >
              {{ alert.message }}
            </el-timeline-item>
          </el-timeline>
          <el-empty v-else description="暂无警报" :image-size="80" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import {
  Monitor,
  Upload,
  Download,
  Warning
} from '@element-plus/icons-vue'
import { devicesAPI, monitoringAPI } from '@/services/api'

const deviceCount = ref(0)
const uploadSpeed = ref(0)
const downloadSpeed = ref(0)
const alertCount = ref(0)
const systemStats = ref(null)
const recentAlerts = ref([])
let refreshInterval = null

const loadData = async () => {
  try {
    // Load devices
    const devicesRes = await devicesAPI.getDevices()
    deviceCount.value = devicesRes.data.devices.length
    
    // Load system stats
    const systemRes = await monitoringAPI.getSystem()
    systemStats.value = systemRes.data.system
    
    // Load alerts
    const alertsRes = await monitoringAPI.getAlerts({ status: 'active' })
    recentAlerts.value = alertsRes.data.alerts.slice(0, 5)
    alertCount.value = alertsRes.data.count
    
    // Load speed test (simulated) - non-blocking
    try {
      const speedRes = await monitoringAPI.runSpeedTest()
      uploadSpeed.value = speedRes.data.results.upload_speed
      downloadSpeed.value = speedRes.data.results.download_speed
    } catch (speedError) {
      console.warn('Speed test failed:', speedError)
      // Keep default values (0) if speed test fails
    }
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  }
}

const getProgressColor = (percent) => {
  if (percent < 50) return '#67c23a'
  if (percent < 80) return '#e6a23c'
  return '#f56c6c'
}

const getAlertColor = (severity) => {
  const colors = {
    'info': '#909399',
    'warning': '#e6a23c',
    'error': '#f56c6c',
    'critical': '#f56c6c'
  }
  return colors[severity] || '#909399'
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString('zh-CN')
}

onMounted(() => {
  loadData()
  // Refresh data every 30 seconds
  refreshInterval = setInterval(loadData, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
}

.stat-card {
  margin-bottom: 20px;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  font-size: 40px;
}

.stat-text {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.card-header {
  font-weight: bold;
}

.system-stats {
  padding: 10px 0;
}

.stat-item {
  margin-bottom: 20px;
}

.stat-item span {
  display: block;
  margin-bottom: 8px;
  color: #606266;
}
</style>
