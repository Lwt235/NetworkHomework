<template>
  <div class="monitoring-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>实时流量监控</span>
              <el-button type="primary" @click="refreshData">刷新</el-button>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="traffic-stat">
                <h4>上传流量</h4>
                <div class="value">{{ formatBytes(trafficData.bytes_sent) }}</div>
                <div class="sub-value">数据包: {{ trafficData.packets_sent }}</div>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="traffic-stat">
                <h4>下载流量</h4>
                <div class="value">{{ formatBytes(trafficData.bytes_recv) }}</div>
                <div class="sub-value">数据包: {{ trafficData.packets_recv }}</div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>流量趋势图</span>
              <el-select v-model="chartHours" @change="loadHistory" style="width: 150px;">
                <el-option label="最近1小时" :value="1" />
                <el-option label="最近6小时" :value="6" />
                <el-option label="最近24小时" :value="24" />
              </el-select>
            </div>
          </template>
          <div style="height: 350px; padding: 10px;">
            <TrafficChart :history-data="historyData" :title="''" />
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>网络负载</span>
              <el-button type="primary" @click="refreshNetworkLoad" size="small">刷新</el-button>
            </div>
          </template>
          <div v-if="networkLoad" class="network-load">
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="load-stat">
                  <h4>上传速率</h4>
                  <div class="value">{{ formatBytes(networkLoad.bytes_sent_per_sec) }}/s</div>
                  <el-progress :percentage="networkLoad.upload_utilization_percent" :color="getLoadColor(networkLoad.upload_utilization_percent)" />
                </div>
              </el-col>
              <el-col :span="8">
                <div class="load-stat">
                  <h4>下载速率</h4>
                  <div class="value">{{ formatBytes(networkLoad.bytes_recv_per_sec) }}/s</div>
                  <el-progress :percentage="networkLoad.download_utilization_percent" :color="getLoadColor(networkLoad.download_utilization_percent)" />
                </div>
              </el-col>
              <el-col :span="8">
                <div class="load-stat">
                  <h4>总体利用率</h4>
                  <div class="value">{{ networkLoad.total_utilization_percent }}%</div>
                  <el-progress :percentage="networkLoad.total_utilization_percent" :color="getLoadColor(networkLoad.total_utilization_percent)" />
                </div>
              </el-col>
            </el-row>
            <el-row :gutter="20" style="margin-top: 20px;">
              <el-col :span="12">
                <div class="sub-stat">
                  <span>发送数据包速率:</span>
                  <strong>{{ networkLoad.packets_sent_per_sec.toFixed(2) }} 包/秒</strong>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="sub-stat">
                  <span>接收数据包速率:</span>
                  <strong>{{ networkLoad.packets_recv_per_sec.toFixed(2) }} 包/秒</strong>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>网速测试</span>
          </template>
          <div class="speed-test">
            <el-button type="primary" @click="runSpeedTest" :loading="testingSpeed">
              {{ testingSpeed ? '测试中...' : '开始测速' }}
            </el-button>
            <div v-if="speedTestError" class="error-message">
              <el-alert type="error" :closable="false" style="margin-top: 10px;">
                {{ speedTestError }}
              </el-alert>
            </div>
            <div v-if="speedTestResult" style="margin-top: 20px;">
              <div class="speed-result">
                <div class="speed-item">
                  <span>下载速度:</span>
                  <strong>{{ speedTestResult.download_speed }} Mbps</strong>
                </div>
                <div class="speed-item">
                  <span>上传速度:</span>
                  <strong>{{ speedTestResult.upload_speed }} Mbps</strong>
                </div>
                <div class="speed-item" v-if="speedTestResult.ping">
                  <span>延迟(Ping):</span>
                  <strong>{{ speedTestResult.ping }} ms</strong>
                </div>
                <div class="speed-item" v-if="speedTestResult.server_location">
                  <span>测速服务器:</span>
                  <strong class="server-location">{{ speedTestResult.server_location }}</strong>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>系统资源</span>
          </template>
          <div v-if="systemData" class="system-info">
            <div class="info-item">
              <span>CPU核心数:</span>
              <strong>{{ systemData.cpu?.count || 0 }}</strong>
            </div>
            <div class="info-item">
              <span>总内存:</span>
              <strong>{{ formatBytes(systemData.memory?.total) }}</strong>
            </div>
            <div class="info-item">
              <span>可用内存:</span>
              <strong>{{ formatBytes(systemData.memory?.available) }}</strong>
            </div>
            <div class="info-item">
              <span>磁盘总空间:</span>
              <strong>{{ formatBytes(systemData.disk?.total) }}</strong>
            </div>
            <div class="info-item">
              <span>磁盘剩余:</span>
              <strong>{{ formatBytes(systemData.disk?.free) }}</strong>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>历史数据</span>
              <el-select v-model="historyHours" @change="loadHistory" style="width: 150px;">
                <el-option label="最近1小时" :value="1" />
                <el-option label="最近6小时" :value="6" />
                <el-option label="最近24小时" :value="24" />
                <el-option label="最近7天" :value="168" />
              </el-select>
            </div>
          </template>
          
          <el-table :data="historyData" style="width: 100%" max-height="400">
            <el-table-column prop="timestamp" label="时间" width="200">
              <template #default="{ row }">
                {{ formatTime(row.timestamp) }}
              </template>
            </el-table-column>
            <el-table-column label="上传" width="150">
              <template #default="{ row }">
                {{ formatBytes(row.bytes_sent) }}
              </template>
            </el-table-column>
            <el-table-column label="下载" width="150">
              <template #default="{ row }">
                {{ formatBytes(row.bytes_recv) }}
              </template>
            </el-table-column>
            <el-table-column label="发送数据包" width="150">
              <template #default="{ row }">
                {{ row.packets_sent }}
              </template>
            </el-table-column>
            <el-table-column label="接收数据包" width="150">
              <template #default="{ row }">
                {{ row.packets_recv }}
              </template>
            </el-table-column>
          </el-table>
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

const trafficData = ref({
  bytes_sent: 0,
  bytes_recv: 0,
  packets_sent: 0,
  packets_recv: 0
})
const systemData = ref(null)
const speedTestResult = ref(null)
const speedTestError = ref(null)
const testingSpeed = ref(false)
const networkLoad = ref(null)
const historyData = ref([])
const chartHours = ref(6)
let refreshInterval = null

const refreshData = async () => {
  try {
    const trafficRes = await monitoringAPI.getTraffic()
    trafficData.value = trafficRes.data.traffic
    
    const systemRes = await monitoringAPI.getSystem()
    systemData.value = systemRes.data.system
  } catch (error) {
    console.error('Failed to refresh data:', error)
  }
}

const refreshNetworkLoad = async () => {
  try {
    const response = await monitoringAPI.getNetworkLoad()
    networkLoad.value = response.data.load
  } catch (error) {
    console.error('Failed to refresh network load:', error)
  }
}

const runSpeedTest = async () => {
  testingSpeed.value = true
  speedTestError.value = null
  speedTestResult.value = null
  try {
    const response = await monitoringAPI.runSpeedTest()
    speedTestResult.value = response.data.results
    ElMessage.success('测速完成')
  } catch (error) {
    const errorMsg = error.response?.data?.error || '测速失败，请检查网络连接'
    speedTestError.value = errorMsg
    ElMessage.error(errorMsg)
  } finally {
    testingSpeed.value = false
  }
}

const getLoadColor = (percentage) => {
  if (percentage < 50) return '#67c23a'
  if (percentage < 80) return '#e6a23c'
  return '#f56c6c'
}

const loadHistory = async () => {
  try {
    const response = await monitoringAPI.getHistory({ hours: chartHours.value })
    historyData.value = response.data.history
  } catch (error) {
    ElMessage.error('加载历史数据失败')
  }
}

const formatBytes = (bytes) => {
  if (!bytes || bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString('zh-CN')
}

onMounted(() => {
  refreshData()
  loadHistory()
  refreshNetworkLoad()
  refreshInterval = setInterval(() => {
    refreshData()
    refreshNetworkLoad()
  }, 5000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
.monitoring-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.traffic-stat {
  text-align: center;
  padding: 20px;
}

.traffic-stat h4 {
  margin: 0 0 10px 0;
  color: #606266;
}

.traffic-stat .value {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 5px;
}

.traffic-stat .sub-value {
  color: #909399;
  font-size: 14px;
}

.speed-test {
  padding: 20px;
  text-align: center;
}

.speed-result {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 4px;
}

.speed-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #e6e6e6;
}

.speed-item:last-child {
  border-bottom: none;
}

.speed-item .server-location {
  font-size: 12px;
}

.system-info {
  padding: 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #e6e6e6;
}

.info-item:last-child {
  border-bottom: none;
}

.network-load {
  padding: 20px;
}

.load-stat {
  text-align: center;
  padding: 10px;
}

.load-stat h4 {
  margin: 0 0 10px 0;
  color: #606266;
  font-size: 16px;
}

.load-stat .value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 10px;
}

.sub-stat {
  display: flex;
  justify-content: space-between;
  padding: 8px 10px;
  background: #f5f7fa;
  border-radius: 4px;
}

.error-message {
  margin-top: 10px;
}
</style>
