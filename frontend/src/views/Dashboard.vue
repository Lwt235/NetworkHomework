<template>
  <div class="dashboard-container">
    <el-container>
      <el-aside width="200px">
        <el-menu
          :default-active="activeMenu"
          router
          class="sidebar-menu"
        >
          <div class="logo">
            <h3>网络监测</h3>
          </div>
          <el-menu-item index="/">
            <el-icon><House /></el-icon>
            <span>仪表板</span>
          </el-menu-item>
          <el-menu-item index="/devices">
            <el-icon><Monitor /></el-icon>
            <span>设备管理</span>
          </el-menu-item>
          <el-menu-item index="/monitoring">
            <el-icon><DataLine /></el-icon>
            <span>实时监控</span>
          </el-menu-item>
          <el-menu-item index="/packet-capture">
            <el-icon><Coin /></el-icon>
            <span>抓包分析</span>
          </el-menu-item>
          <el-menu-item index="/analytics">
            <el-icon><TrendCharts /></el-icon>
            <span>统计分析</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header>
          <div class="header-content">
            <h2>网络性能监测工具</h2>
            <div class="user-info">
              <span>{{ username }}</span>
              <el-button type="danger" size="small" @click="handleLogout">退出</el-button>
            </div>
          </div>
        </el-header>
        
        <el-main>
          <div class="main-content">
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
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  House,
  Monitor,
  DataLine,
  Coin,
  TrendCharts,
  Upload,
  Download,
  Warning
} from '@element-plus/icons-vue'
import { devicesAPI, monitoringAPI } from '@/services/api'

const router = useRouter()
const route = useRoute()

const deviceCount = ref(0)
const uploadSpeed = ref(0)
const downloadSpeed = ref(0)
const alertCount = ref(0)
const systemStats = ref(null)
const recentAlerts = ref([])

const activeMenu = computed(() => route.path)
const username = computed(() => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  return user.username || 'User'
})

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
    
    // Load speed test (simulated)
    const speedRes = await monitoringAPI.runSpeedTest()
    uploadSpeed.value = speedRes.data.results.upload_speed
    downloadSpeed.value = speedRes.data.results.download_speed
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

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  ElMessage.success('已退出登录')
  router.push('/login')
}

onMounted(() => {
  loadData()
  // Refresh data every 30 seconds
  setInterval(loadData, 30000)
})
</script>

<style scoped>
.dashboard-container {
  height: 100vh;
}

.sidebar-menu {
  height: 100vh;
  border-right: 1px solid #e6e6e6;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #e6e6e6;
}

.logo h3 {
  margin: 0;
  color: #409eff;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content h2 {
  margin: 0;
  color: #333;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}

.main-content {
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
