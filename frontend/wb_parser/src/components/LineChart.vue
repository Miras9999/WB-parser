<template>
  <div class="q-pa-md">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Title,
  Filler
} from 'chart.js'

Chart.register(LineController, LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Title, Filler)

export default {
  props: {
    labels: {
      type: Array as () => number[],
      required: true
    },
    values: {
      type: Array as () => number[],
      required: true
    },
    title: {
      type: String,
      default: 'Скидка vs Рейтинг'
    }
  },
  setup(props) {
    const canvas = ref<HTMLCanvasElement | null>(null)
    let chartInstance: Chart | null = null

    const renderChart = () => {
      if (!canvas.value) return
      if (chartInstance) chartInstance.destroy()

      chartInstance = new Chart(canvas.value, {
        type: 'line',
        data: {
          labels: props.labels,
          datasets: [
            {
              label: props.title,
              data: props.values,
              borderColor: '#C2185B',
              backgroundColor: 'rgba(194, 24, 91, 0.2)',
              fill: true,
              tension: 0.3,
              pointRadius: 3
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: props.title
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }

    onMounted(renderChart)
    onBeforeUnmount(() => chartInstance?.destroy())
    watch(() => [props.labels, props.values], renderChart, { deep: true })

    return { canvas }
  }
}
</script>
