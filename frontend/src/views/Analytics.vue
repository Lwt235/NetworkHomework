<template>
  <div class="analytics-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>网络负载分析</span>
              <el-select v-model="timeRange" @change="loadData" style="width: 150px;">
                <el-option label="最近1小时" :value="1" />
                <el-option label="最近6小时" :value="6" />
                <el-option label="最近24小时" :value="24" />
                <el-option label="最近7天" :value="168" />
              </el-select>
            </div>
          </template>
          
          <div class="summary-stats">
            <div class="summary-item">
              <div class="summary-label">总上传流量</div>
              <div class="summary-value">{{ formatBytes(totalBytesSent) }}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">总下载流量</div>
              <div class="summary-value">{{ formatBytes(totalBytesRecv) }}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">总数据包(发送)</div>
              <div class="summary-value">{{ totalPacketsSent }}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">总数据包(接收)</div>
              <div class="summary-value">{{ totalPacketsRecv }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>流量趋势对比图</span>
          </template>
          <div style="height: 400px; padding: 10px;">
            <TrafficChart :history-data="historyData" title="上传 vs 下载流量" />
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>系统资源趋势图</span>
          </template>
          <div style="height: 400px; padding: 10px;">
            <SystemResourceChart :history-data="systemHistoryData" title="CPU、内存、磁盘使用率" />
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>警报管理</span>
          </template>
          
          <el-tabs v-model="alertTab" @tab-change="loadAlerts">
            <el-tab-pane label="活动警报" name="active">
              <el-table :data="alerts" style="width: 100%" max-height="400">
                <el-table-column prop="created_at" label="时间" width="180">
                  <template #default="{ row }">
                    {{ formatTime(row.created_at) }}
                  </template>
                </el-table-column>
                <el-table-column prop="alert_type" label="类型" width="120">
                  <template #default="{ row }">
                    <el-tag>{{ row.alert_type }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="severity" label="严重程度" width="120">
                  <template #default="{ row }">
                    <el-tag :type="getSeverityType(row.severity)">
                      {{ getSeverityLabel(row.severity) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="message" label="消息" min-width="300" />
                <el-table-column label="操作" width="120">
                  <template #default="{ row }">
                    <el-button
                      v-if="row.status === 'active'"
                      size="small"
                      type="success"
                      @click="resolveAlert(row.id)"
                    >
                      解决
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
            
            <el-tab-pane label="已解决警报" name="resolved">
              <el-table :data="alerts" style="width: 100%" max-height="400">
                <el-table-column prop="created_at" label="创建时间" width="180">
                  <template #default="{ row }">
                    {{ formatTime(row.created_at) }}
                  </template>
                </el-table-column>
                <el-table-column prop="resolved_at" label="解决时间" width="180">
                  <template #default="{ row }">
                    {{ formatTime(row.resolved_at) }}
                  </template>
                </el-table-column>
                <el-table-column prop="alert_type" label="类型" width="120">
                  <template #default="{ row }">
                    <el-tag>{{ row.alert_type }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="severity" label="严重程度" width="120">
                  <template #default="{ row }">
                    <el-tag :type="getSeverityType(row.severity)">
                      {{ getSeverityLabel(row.severity) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="message" label="消息" min-width="300" />
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>阈值配置</span>
          </template>
          
          <el-form label-width="120px">
            <el-form-item label="CPU阈值 (%)">
              <el-slider v-model="thresholds.cpu" :min="50" :max="100" show-input />
            </el-form-item>
            <el-form-item label="内存阈值 (%)">
              <el-slider v-model="thresholds.memory" :min="50" :max="100" show-input />
            </el-form-item>
            <el-form-item label="磁盘阈值 (%)">
              <el-slider v-model="thresholds.disk" :min="50" :max="100" show-input />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveThresholds">保存设置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>系统状态</span>
          </template>
          
          <div v-if="systemStats" class="system-status">
            <div class="status-item">
              <div class="status-label">CPU使用率</div>
              <el-progress
                :percentage="systemStats.cpu?.percent || 0"
                :color="getProgressColor(systemStats.cpu?.percent || 0, thresholds.cpu)"
              />
            </div>
            <div class="status-item">
              <div class="status-label">内存使用率</div>
              <el-progress
                :percentage="systemStats.memory?.percent || 0"
                :color="getProgressColor(systemStats.memory?.percent || 0, thresholds.memory)"
              />
            </div>
            <div class="status-item">
              <div class="status-label">磁盘使用率</div>
              <el-progress
                :percentage="systemStats.disk?.percent || 0"
                :color="getProgressColor(systemStats.disk?.percent || 0, thresholds.disk)"
              />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { monitoringAPI } from '@/services/api'
import TrafficChart from '@/components/TrafficChart.vue'
import SystemResourceChart from '@/components/SystemResourceChart.vue'

const timeRange = ref(24)
const totalBytesSent = ref(0)
const totalBytesRecv = ref(0)
const totalPacketsSent = ref(0)
const totalPacketsRecv = ref(0)
const alertTab = ref('active')
const alerts = ref([])
const systemStats = ref(null)
const historyData = ref([])
const systemHistoryData = ref([])
const thresholds = ref({
  cpu: 80,
  memory: 80,
  disk: 90
})

let refreshInterval = null

const loadData = async () => {
  try {
    const response = await monitoringAPI.getHistory({ hours: timeRange.value })
    historyData.value = response.data.history
    const history = response.data.history
    
    totalBytesSent.value = history.reduce((sum, log) => sum + log.bytes_sent, 0)
    totalBytesRecv.value = history.reduce((sum, log) => sum + log.bytes_recv, 0)
    totalPacketsSent.value = history.reduce((sum, log) => sum + log.packets_sent, 0)
    totalPacketsRecv.value = history.reduce((sum, log) => sum + log.packets_recv, 0)
    
    // Load system resource history
    const systemResponse = await monitoringAPI.getSystemHistory({ hours: timeRange.value })
    systemHistoryData.value = systemResponse.data.history
  } catch (error) {
    console.error('Failed to load analytics data:', error)
  }
}

const loadAlerts = async () => {
  try {
    const response = await monitoringAPI.getAlerts({ status: alertTab.value })
    alerts.value = response.data.alerts
  } catch (error) {
    ElMessage.error('加载警报失败')
  }
}

const loadSystemStats = async () => {
  try {
    const response = await monitoringAPI.getSystem()
    systemStats.value = response.data.system
  } catch (error) {
    console.error('Failed to load system stats:', error)
  }
}

const resolveAlert = async (alertId) => {
  try {
    await monitoringAPI.resolveAlert(alertId)
    ElMessage.success('警报已解决')
    loadAlerts()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const saveThresholds = () => {
  localStorage.setItem('thresholds', JSON.stringify(thresholds.value))
  ElMessage.success('阈值设置已保存')
}

const getSeverityType = (severity) => {
  const types = {
    'info': 'info',
    'warning': 'warning',
    'error': 'danger',
    'critical': 'danger'
  }
  return types[severity] || 'info'
}

const getSeverityLabel = (severity) => {
  const labels = {
    'info': '信息',
    'warning': '警告',
    'error': '错误',
    'critical': '严重'
  }
  return labels[severity] || severity
}

const getProgressColor = (value, threshold) => {
  if (value < threshold * 0.8) return '#67c23a'
  if (value < threshold) return '#e6a23c'
  return '#f56c6c'
}

const formatBytes = (bytes) => {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const formatTime = (timestamp) => {
  if (!timestamp) return '-'
  return new Date(timestamp).toLocaleString('zh-CN')
}

onMounted(() => {
  const savedThresholds = localStorage.getItem('thresholds')
  if (savedThresholds) {
    thresholds.value = JSON.parse(savedThresholds)
  }
  
  loadData()
  loadAlerts()
  loadSystemStats()
  
  refreshInterval = setInterval(() => {
    loadSystemStats()
    loadAlerts()
  }, 10000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.analytics-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  padding: 20px;
}

.summary-item {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.summary-label {
  color: #909399;
  font-size: 14px;
  margin-bottom: 10px;
}

.summary-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.system-status {
  padding: 20px;
}

.status-item {
  margin-bottom: 30px;
}

.status-label {
  margin-bottom: 10px;
  color: #606266;
  font-weight: 500;
}
</style>
