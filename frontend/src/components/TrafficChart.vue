<template>
  <div class="chart-container">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  historyData: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: '流量趋势'
  },
  showLegend: {
    type: Boolean,
    default: true
  }
})

const chartData = computed(() => {
  // Reverse the array once at the beginning for efficiency
  const reversedData = [...props.historyData].reverse()
  
  const labels = reversedData.map(item => {
    const date = new Date(item.timestamp)
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  })

  const uploadData = reversedData.map(item => {
    // Convert bytes to MB
    return (item.bytes_sent / (1024 * 1024)).toFixed(2)
  })

  const downloadData = reversedData.map(item => {
    // Convert bytes to MB
    return (item.bytes_recv / (1024 * 1024)).toFixed(2)
  })

  return {
    labels,
    datasets: [
      {
        label: '上传 (MB)',
        data: uploadData,
        borderColor: '#67c23a',
        backgroundColor: 'rgba(103, 194, 58, 0.1)',
        tension: 0.4,
        fill: true
      },
      {
        label: '下载 (MB)',
        data: downloadData,
        borderColor: '#409eff',
        backgroundColor: 'rgba(64, 158, 255, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  }
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: props.showLegend,
      position: 'top'
    },
    title: {
      display: !!props.title,
      text: props.title
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      callbacks: {
        label: function(context) {
          return context.dataset.label + ': ' + context.parsed.y + ' MB'
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        callback: function(value) {
          return value + ' MB'
        }
      }
    },
    x: {
      ticks: {
        maxRotation: 45,
        minRotation: 45
      }
    }
  },
  interaction: {
    mode: 'nearest',
    axis: 'x',
    intersect: false
  }
}))
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
  position: relative;
}
</style>
