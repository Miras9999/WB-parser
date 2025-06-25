<template>
  <div class="q-pa-md">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Title
} from 'chart.js'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Title)

export default {
  props: {
    labels: {
      type: Array as () => string[],
      required: true
    },
    values: {
      type: Array as () => number[],
      required: true
    },
    title: {
      type: String,
      required: false,
      default: 'Bar Chart'
    }
  },
  setup(props) {
    const canvas = ref<HTMLCanvasElement | null>(null)
    let chartInstance: Chart | null = null

    const renderChart = () => {
      if (!canvas.value) return
      if (chartInstance) {
        chartInstance.destroy()
      }

      chartInstance = new Chart(canvas.value, {
        type: 'bar',
        data: {
          labels: props.labels,
          datasets: [
            {
              label: props.title,
              data: props.values,
              backgroundColor: '#C2185B',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: !!props.title,
              text: props.title
            },
            tooltip: {
              enabled: true
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

    onMounted(() => {
      renderChart()
    })

    onBeforeUnmount(() => {
      if (chartInstance) {
        chartInstance.destroy()
      }
    })

    watch(
      () => [props.labels, props.values],
      () => {
        renderChart()
      },
      { deep: true }
    )

    return {
      canvas
    }
  }
}
</script>
