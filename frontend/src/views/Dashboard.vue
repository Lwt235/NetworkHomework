<template>
  <div class="dashboard-container">
    <el-container>
      <el-aside width="200px">
        <el-menu
          :default-active="activeView"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <div class="logo">
            <h3>网络监测</h3>
          </div>
          <el-menu-item index="dashboard">
            <el-icon><House /></el-icon>
            <span>仪表板</span>
          </el-menu-item>
          <el-menu-item index="devices">
            <el-icon><Monitor /></el-icon>
            <span>设备管理</span>
          </el-menu-item>
          <el-menu-item index="monitoring">
            <el-icon><DataLine /></el-icon>
            <span>实时监控</span>
          </el-menu-item>
          <el-menu-item index="packet-capture">
            <el-icon><Coin /></el-icon>
            <span>抓包分析</span>
          </el-menu-item>
          <el-menu-item index="analytics">
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
          <component :is="currentView" />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  House,
  Monitor,
  DataLine,
  Coin,
  TrendCharts
} from '@element-plus/icons-vue'
import DashboardContent from './DashboardContent.vue'
import Devices from './Devices.vue'
import Monitoring from './Monitoring.vue'
import PacketCapture from './PacketCapture.vue'
import Analytics from './Analytics.vue'

const router = useRouter()
const activeView = ref('dashboard')

const currentView = computed(() => {
  const views = {
    'dashboard': DashboardContent,
    'devices': Devices,
    'monitoring': Monitoring,
    'packet-capture': PacketCapture,
    'analytics': Analytics
  }
  return views[activeView.value] || DashboardContent
})

const username = computed(() => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  return user.username || 'User'
})

const handleMenuSelect = (index) => {
  activeView.value = index
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  ElMessage.success('已退出登录')
  router.push('/login')
}
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
</style>
