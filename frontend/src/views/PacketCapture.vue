<template>
  <div class="packet-capture-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据包抓取分析</span>
        </div>
      </template>
      
      <el-form :inline="true" :model="captureForm">
        <el-form-item label="协议类型">
          <el-select v-model="captureForm.protocol" style="width: 150px;">
            <el-option label="所有协议" value="all" />
            <el-option label="TCP" value="tcp" />
            <el-option label="UDP" value="udp" />
            <el-option label="ICMP" value="icmp" />
            <el-option label="IP" value="ip" />
          </el-select>
        </el-form-item>
        <el-form-item label="数据包数量">
          <el-input-number v-model="captureForm.count" :min="10" :max="1000" />
        </el-form-item>
        <el-form-item label="超时时间(秒)">
          <el-input-number v-model="captureForm.timeout" :min="5" :max="60" />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="captureForm.clearPrevious">清除之前的抓包</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="startCapture" :loading="capturing">
            {{ capturing ? '抓取中...' : '开始抓包' }}
          </el-button>
          <el-button type="danger" @click="clearAllPackets" :loading="clearing">
            清除所有抓包
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>捕获的数据包 ({{ packets.length }})</span>
          <div>
            <el-select v-model="filterProtocol" @change="loadPackets" style="width: 150px; margin-right: 10px;">
              <el-option label="所有协议" value="" />
              <el-option label="TCP" value="TCP" />
              <el-option label="UDP" value="UDP" />
              <el-option label="ICMP" value="ICMP" />
              <el-option label="IP" value="IP" />
            </el-select>
            <el-button @click="loadPackets">刷新</el-button>
          </div>
        </div>
      </template>
      
      <el-table :data="packets" style="width: 100%" max-height="500" v-loading="loading">
        <el-table-column prop="timestamp" label="时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.timestamp) }}
          </template>
        </el-table-column>
        <el-table-column prop="protocol" label="协议" width="80">
          <template #default="{ row }">
            <el-tag :type="getProtocolType(row.protocol)">{{ row.protocol }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="src_ip" label="源IP" width="150" />
        <el-table-column prop="dst_ip" label="目标IP" width="150" />
        <el-table-column prop="src_port" label="源端口" width="100" />
        <el-table-column prop="dst_port" label="目标端口" width="100" />
        <el-table-column prop="length" label="长度" width="100">
          <template #default="{ row }">
            {{ row.length }} bytes
          </template>
        </el-table-column>
        <el-table-column prop="info" label="信息" min-width="200" show-overflow-tooltip />
      </el-table>
    </el-card>
    
    <el-card style="margin-top: 20px;">
      <template #header>
        <span>协议统计</span>
      </template>
      
      <div v-if="stats && stats.protocols && stats.protocols.length > 0" class="stats-grid">
        <div v-for="proto in stats.protocols" :key="proto.protocol" class="stat-item">
          <div class="stat-protocol">{{ proto.protocol }}</div>
          <div class="stat-count">数据包: {{ proto.count }}</div>
          <div class="stat-bytes">字节: {{ formatBytes(proto.bytes) }}</div>
        </div>
      </div>
      <el-empty v-else description="暂无统计数据" :image-size="80" />
    </el-card>
    
    <el-card style="margin-top: 20px;" v-if="analysis">
      <template #header>
        <span>深度分析</span>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <h4>Top 源IP地址</h4>
          <el-table :data="analysis.top_source_ips" style="width: 100%" max-height="300" size="small">
            <el-table-column prop="ip" label="IP地址" />
            <el-table-column prop="packet_count" label="包数" width="80" />
            <el-table-column label="字节数" width="100">
              <template #default="{ row }">
                {{ formatBytes(row.total_bytes) }}
              </template>
            </el-table-column>
          </el-table>
        </el-col>
        
        <el-col :span="8">
          <h4>Top 目标IP地址</h4>
          <el-table :data="analysis.top_destination_ips" style="width: 100%" max-height="300" size="small">
            <el-table-column prop="ip" label="IP地址" />
            <el-table-column prop="packet_count" label="包数" width="80" />
            <el-table-column label="字节数" width="100">
              <template #default="{ row }">
                {{ formatBytes(row.total_bytes) }}
              </template>
            </el-table-column>
          </el-table>
        </el-col>
        
        <el-col :span="8">
          <h4>Top 目标端口</h4>
          <el-table :data="analysis.top_destination_ports" style="width: 100%" max-height="300" size="small">
            <el-table-column prop="port" label="端口" width="80" />
            <el-table-column prop="service" label="服务" />
            <el-table-column prop="packet_count" label="包数" width="80" />
          </el-table>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { analysisAPI } from '@/services/api'
import { formatBytes, formatTime } from '@/utils/formatters'

const captureForm = ref({
  protocol: 'all',
  count: 100,
  timeout: 10,
  clearPrevious: true
})
const capturing = ref(false)
const clearing = ref(false)
const loading = ref(false)
const packets = ref([])
const filterProtocol = ref('')
const stats = ref(null)
const analysis = ref(null)

const startCapture = async () => {
  capturing.value = true
  try {
    const response = await analysisAPI.capturePackets({
      protocol: captureForm.value.protocol,
      count: captureForm.value.count,
      timeout: captureForm.value.timeout,
      clear_previous: captureForm.value.clearPrevious
    })
    packets.value = response.data.packets
    const message = captureForm.value.clearPrevious 
      ? `成功捕获 ${response.data.count} 个数据包（已清除旧数据）`
      : `成功捕获 ${response.data.count} 个数据包`
    ElMessage.success(message)
    loadStats()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '数据包捕获失败')
  } finally {
    capturing.value = false
  }
}

const clearAllPackets = async () => {
  clearing.value = true
  try {
    const response = await analysisAPI.clearPackets()
    ElMessage.success(`已清除 ${response.data.deleted_count} 个数据包`)
    packets.value = []
    stats.value = null
    analysis.value = null
  } catch (error) {
    ElMessage.error('清除数据包失败')
  } finally {
    clearing.value = false
  }
}

const loadPackets = async () => {
  loading.value = true
  try {
    const params = { hours: 1 }
    if (filterProtocol.value) {
      params.protocol = filterProtocol.value
    }
    const response = await analysisAPI.getPackets(params)
    packets.value = response.data.packets
  } catch (error) {
    ElMessage.error('加载数据包失败')
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    const response = await analysisAPI.getStats({ hours: 24 })
    stats.value = response.data.stats
    analysis.value = response.data.analysis
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

const getProtocolType = (protocol) => {
  const types = {
    'TCP': 'primary',
    'UDP': 'success',
    'ICMP': 'warning',
    'IP': 'info'
  }
  return types[protocol] || 'info'
}

onMounted(() => {
  loadPackets()
  loadStats()
})
</script>

<style scoped>
.packet-capture-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.stat-item {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 4px;
  text-align: center;
}

.stat-protocol {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 10px;
}

.stat-count,
.stat-bytes {
  color: #606266;
  font-size: 14px;
  margin: 5px 0;
}
</style>
