<template>
  <q-page class="q-pa-xl column items-center">
    <div style="max-width: 1100px; width: 100%">

      <q-input
        v-model="category"
        label="🔍 Категория"
        outlined
        rounded
        dense
        color="pink-10"
        class="q-mb-md"
        @keyup.enter="search"
      >
        <template v-slot:append>
          <q-icon name="search" class="cursor-pointer" @click="search" />
        </template>
      </q-input>

      <q-card flat bordered class="q-pa-md q-mb-md">
        <q-card-section class="text-subtitle1 text-bold">
          Фильтры
        </q-card-section>
        <q-card-section class="q-pt-none">
          <div class="row q-col-gutter-md items-center">

            <div class="col-12 col-md-4">
              <q-range
                v-model="priceRange"
                :min="0"
                :max="100000"
                @update:model-value="search"
                color="pink-10"
              />
              <div class="text-caption text-grey text-center">
                Цена: {{ priceRange.min }} ₸ — {{ priceRange.max }} ₸
              </div>
            </div>

            <div class="col-12 col-md-4">
              <q-slider
                v-model="minRating"
                :min="0"
                :max="5"
                :step="1"
                @update:model-value="search"
                color="pink-10"
              />
              <div class="text-caption text-grey text-center">
                Мин. рейтинг: {{ minRating.toFixed(1) }} ★
              </div>
            </div>

            <div class="col-12 col-md-4">
              <q-input
                v-model.number="minReviews"
                type="number"
                outlined
                dense
                placeholder="100"
                @update:model-value="search"
                color="pink-10"
              />
              <div class="text-caption text-grey text-center">
                Мин. отзывов
              </div>
            </div>

          </div>
        </q-card-section>
      </q-card>

      <q-table
        :rows="products"
        :columns="columns"
        row-key="id"
        dense
        bordered
        flat
        :pagination="{ rowsPerPage: 10 }"
        no-data-label="Нет информации"
      />

      <BarChart
        :labels="bucketLabels"
        :values="bucketCounts"
        title="Распределение товаров по цене"
      />

      <LineChart
        :labels="discountRatingsLabels"
        :values="discountValues"
        title="Скидка vs Рейтинг товара"
      />
    </div>
  </q-page>
</template>

<script lang="ts">
import { ref, watch } from 'vue';
import {api} from "src/boot/axios";
import type {Product} from 'components/models';
import type {QTableColumn} from "quasar";
import {Notify} from "quasar";
import BarChart from 'components/BarChart.vue'
import LineChart from 'components/LineChart.vue'

const columns: QTableColumn<Product>[] = [
  {
    name: 'name',
    label: 'Название',
    field: 'name',
    align: 'left',
    sortable: true
  },
  {
    name: 'price',
    label: 'Цена',
    field: 'price',
    align: 'right',
    sortable: true,
    format: (val: number) => `${val} ₸`
  },
  {
    name: 'discount_price',
    label: 'Цена со скидкой',
    field: 'discount_price',
    align: 'right',
    sortable: true,
    format: (val: number) => `${val} ₸`
  },
  {
    name: 'rating',
    label: 'Рейтинг',
    field: 'rating',
    align: 'center',
    sortable: true
  },
  {
    name: 'reviews_count',
    label: 'Отзывы',
    field: 'reviews_count',
    align: 'center',
    sortable: true
  }
]

const category = ref('')
const products = ref<Product[]>([])
const priceRange = ref({ min: 0, max: 100000 })
const minRating = ref(0)
const minReviews = ref(0)

const search = async  () => {
  const params = {
    query: category.value,
    price_min: priceRange.value.min,
    price_max: priceRange.value.max,
    rating_min: minRating.value,
    reviews_min: minReviews.value,
  }
  await api.get('api/core/products/parse/', {params})
    .then(
      response => {
        products.value = response.data
      }
    )
    .catch(
      error => {
        console.error(error)
        Notify.create({
          type: 'negative',
          message: 'Ошибка при загрузке данных. Пожалуйста, попробуйте позже.',
          position: 'center',
          timeout: 3000,
        })
      }
    )
}

const bucketLabels = ref<string[]>([])
const bucketCounts = ref<number[]>([])
const updatePriceHistogram = () => {
  const buckets = [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
  const counts = Array(buckets.length - 1).fill(0)

  products.value.forEach((p) => {
    const price = p.discount_price
    for (let i = 0; i < buckets.length - 1; i++) {
      const min = buckets[i]
      const max = buckets[i + 1]
      if (min !== undefined && max !== undefined && price >= min && price < max) {
        counts[i]++
        break
      }
    }
  })

  bucketLabels.value = buckets.slice(0, -1).map((min, i) => {
    const max = buckets[i + 1]
    return `${min}–${max}`
  })
  bucketCounts.value = counts
}

const discountRatingsLabels = ref<number[]>([])
const discountValues = ref<number[]>([])
const updateDiscountVsRating = () => {
  const ratingToDiscounts = new Map<number, number[]>()

  products.value.forEach((p) => {
    const rating = Math.round(p.rating * 10) / 10
    const discount = p.price - p.discount_price

    if (!ratingToDiscounts.has(rating)) {
      ratingToDiscounts.set(rating, [])
    }
    ratingToDiscounts.get(rating)?.push(discount)
  })

  const sortedRatings = Array.from(ratingToDiscounts.keys()).sort((a, b) => a - b)
  const averageDiscounts = sortedRatings.map((r) => {
    const discounts = ratingToDiscounts.get(r) ?? []
    const sum = discounts.reduce((acc, d) => acc + d, 0)
    return discounts.length ? Math.round(sum / discounts.length) : 0
  })

  discountRatingsLabels.value = sortedRatings
  discountValues.value = averageDiscounts
}

watch(products, updatePriceHistogram, { deep: true })
watch(products, updateDiscountVsRating, { deep: true })

export default {
  components: {
    BarChart,
    LineChart
  },
  setup() {
    return {
      search,
      products,
      category,
      columns,
      priceRange,
      minReviews,
      minRating,
      bucketCounts,
      bucketLabels,
      discountRatingsLabels,
      discountValues
    }
  }
}

</script>
