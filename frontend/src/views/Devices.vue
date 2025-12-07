<template>
  <div class="devices-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>设备管理</span>
          <el-button type="primary" @click="showAddDialog = true">添加设备</el-button>
        </div>
      </template>
      
      <el-table :data="devices" style="width: 100%" v-loading="loading">
        <el-table-column prop="name" label="设备名称" />
        <el-table-column prop="ip_address" label="IP地址" />
        <el-table-column prop="device_type" label="设备类型" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '在线' : '离线' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_seen" label="最后在线时间">
          <template #default="{ row }">
            {{ formatTime(row.last_seen) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="editDevice(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteDevice(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- Add/Edit Dialog -->
    <el-dialog
      v-model="showAddDialog"
      :title="editingDevice ? '编辑设备' : '添加设备'"
      width="500px"
    >
      <el-form :model="deviceForm" :rules="rules" ref="deviceFormRef" label-width="100px">
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="deviceForm.name" />
        </el-form-item>
        <el-form-item label="IP地址" prop="ip_address">
          <el-input v-model="deviceForm.ip_address" />
        </el-form-item>
        <el-form-item label="设备类型" prop="device_type">
          <el-select v-model="deviceForm.device_type" style="width: 100%">
            <el-option label="路由器" value="router" />
            <el-option label="交换机" value="switch" />
            <el-option label="服务器" value="server" />
            <el-option label="电脑" value="computer" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="saveDevice" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { devicesAPI } from '@/services/api'

const devices = ref([])
const loading = ref(false)
const showAddDialog = ref(false)
const saving = ref(false)
const editingDevice = ref(null)
const deviceFormRef = ref(null)

const deviceForm = reactive({
  name: '',
  ip_address: '',
  device_type: 'router'
})

const rules = {
  name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
  ip_address: [
    { required: true, message: '请输入IP地址', trigger: 'blur' },
    { pattern: /^(\d{1,3}\.){3}\d{1,3}$/, message: '请输入有效的IP地址', trigger: 'blur' }
  ],
  device_type: [{ required: true, message: '请选择设备类型', trigger: 'change' }]
}

const loadDevices = async () => {
  loading.value = true
  try {
    const response = await devicesAPI.getDevices()
    devices.value = response.data.devices
  } catch (error) {
    ElMessage.error('加载设备列表失败')
  } finally {
    loading.value = false
  }
}

const editDevice = (device) => {
  editingDevice.value = device
  deviceForm.name = device.name
  deviceForm.ip_address = device.ip_address
  deviceForm.device_type = device.device_type
  showAddDialog.value = true
}

const saveDevice = async () => {
  if (!deviceFormRef.value) return
  
  await deviceFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        if (editingDevice.value) {
          await devicesAPI.updateDevice(editingDevice.value.id, deviceForm)
          ElMessage.success('设备更新成功')
        } else {
          await devicesAPI.addDevice(deviceForm)
          ElMessage.success('设备添加成功')
        }
        showAddDialog.value = false
        resetForm()
        loadDevices()
      } catch (error) {
        ElMessage.error(error.response?.data?.error || '操作失败')
      } finally {
        saving.value = false
      }
    }
  })
}

const deleteDevice = async (device) => {
  try {
    await ElMessageBox.confirm('确定要删除这个设备吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await devicesAPI.deleteDevice(device.id)
    ElMessage.success('设备删除成功')
    loadDevices()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const resetForm = () => {
  editingDevice.value = null
  deviceForm.name = ''
  deviceForm.ip_address = ''
  deviceForm.device_type = 'router'
}

const formatTime = (timestamp) => {
  if (!timestamp) return '-'
  return new Date(timestamp).toLocaleString('zh-CN')
}

onMounted(() => {
  loadDevices()
})
</script>

<style scoped>
.devices-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
