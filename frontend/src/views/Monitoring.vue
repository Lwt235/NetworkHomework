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
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>网速测试</span>
          </template>
          <div class="speed-test">
            <el-button type="primary" @click="runSpeedTest" :loading="testingSpeed">
              {{ testingSpeed ? '测试中...' : '开始测速' }}
            </el-button>
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
const testingSpeed = ref(false)
const historyData = ref([])
const historyHours = ref(24)
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

const runSpeedTest = async () => {
  testingSpeed.value = true
  try {
    const response = await monitoringAPI.runSpeedTest()
    speedTestResult.value = response.data.results
    ElMessage.success('测速完成')
  } catch (error) {
    ElMessage.error('测速失败')
  } finally {
    testingSpeed.value = false
  }
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
  refreshInterval = setInterval(refreshData, 5000)
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
</style>
