<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="table-th">ID</th>
          <th scope="col" class="table-th">名称</th>
          <th scope="col" class="table-th">状态</th>
          <th scope="col" class="table-th">需求数量</th>
          <th scope="col" class="table-th">招聘负责人</th>
          <th scope="col" class="table-th">创建时间</th>
          <th scope="col" class="table-th">操作</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="position in positions" :key="position.id">
          <td class="table-td">{{ position.id }}</td>
          <td class="table-td">{{ position.name }}</td>
          <td class="table-td">
            <span class="status-badge" :class="getStatusClass(position.status)">
              {{ positionStatusMap[position.status] }}
            </span>
          </td>
          <td class="table-td">{{ position.quantity }}</td>
          <td class="table-td">{{ position.recruiter }}</td>
          <td class="table-td">{{ formatTimestamp(position.created_at) }}</td>
          <td class="table-td space-x-2">
            <button
              @click="showPositionDetail(position)"
              class="btn-action btn-view"
            >
              查看详情
            </button>
            <button
              @click="$emit('edit', position)"
              class="btn-action btn-edit"
            >
              编辑
            </button>
            <button
              @click="$emit('delete', position.id)"
              class="btn-action btn-delete"
            >
              删除
            </button>
          </td>
        </tr>
        <tr v-if="positions.length === 0">
          <td colspan="7" class="table-td text-center text-gray-500">
            暂无数据
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 岗位详情弹窗 -->
    <div v-if="showDetail" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full flex flex-col max-h-[90vh]">
        <div class="px-6 py-4 border-b border-gray-200 flex-shrink-0">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-medium text-gray-900">岗位详情</h3>
            <button
              @click="showDetail = false"
              class="text-gray-400 hover:text-gray-500 focus:outline-none"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <div class="px-6 py-4 overflow-y-auto flex-grow">
          <div class="space-y-4">
            <div>
              <h4 class="text-sm font-medium text-gray-500">岗位名称</h4>
              <p class="mt-1 text-sm text-gray-900">{{ selectedPosition?.name }}</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500">岗位要求</h4>
              <div class="mt-1 text-sm text-gray-900 whitespace-pre-line bg-gray-50 p-3 rounded-lg max-h-40 overflow-y-auto">
                {{ selectedPosition?.requirements }}
              </div>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500">岗位职责</h4>
              <div class="mt-1 text-sm text-gray-900 whitespace-pre-line bg-gray-50 p-3 rounded-lg max-h-40 overflow-y-auto">
                {{ selectedPosition?.responsibilities }}
              </div>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500">招聘负责人</h4>
              <p class="mt-1 text-sm text-gray-900">{{ selectedPosition?.recruiter }}</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500">需求数量</h4>
              <p class="mt-1 text-sm text-gray-900">{{ selectedPosition?.quantity }} 人</p>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500">职位状态</h4>
              <span class="mt-1 inline-flex px-2 py-1 text-xs font-medium rounded-full" :class="getStatusClass(selectedPosition?.status)">
                {{ positionStatusMap[selectedPosition?.status] }}
              </span>
            </div>
            <div>
              <h4 class="text-sm font-medium text-gray-500">职位链接</h4>
              <a
                v-if="selectedPosition?.link"
                :href="selectedPosition.link"
                target="_blank"
                class="mt-1 text-sm text-blue-600 hover:text-blue-800 break-all"
              >
                {{ selectedPosition.link }}
              </a>
              <p v-else class="mt-1 text-sm text-gray-500">暂无链接</p>
            </div>
          </div>
        </div>
        <div class="px-6 py-4 bg-gray-50 rounded-b-lg flex-shrink-0">
          <button
            @click="showDetail = false"
            class="w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            关闭
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { formatTimestamp, positionStatusMap } from '@/api/interview'
import { ref } from 'vue'

defineProps({
  positions: {
    type: Array,
    default: () => []
  }
})

defineEmits(['edit', 'delete'])

const showDetail = ref(false)
const selectedPosition = ref(null)

const getStatusClass = (status) => {
  const classes = {
    0: 'bg-gray-100 text-gray-800', // 未启动
    1: 'bg-blue-100 text-blue-800', // 进行中
    2: 'bg-green-100 text-green-800' // 已完成
  }
  return classes[status] || classes[0]
}

const showPositionDetail = (position) => {
  selectedPosition.value = position
  showDetail.value = true
}
</script>

<style scoped>
.table-th {
  @apply px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider;
}

.table-td {
  @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900;
}

.status-badge {
  @apply px-2 py-1 text-xs font-medium rounded-full;
}

.btn-action {
  @apply px-3 py-1 rounded text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2;
}

.btn-view {
  @apply text-purple-700 bg-purple-100 hover:bg-purple-200 focus:ring-purple-500;
}

.btn-edit {
  @apply text-blue-700 bg-blue-100 hover:bg-blue-200 focus:ring-blue-500;
}

.btn-delete {
  @apply text-red-700 bg-red-100 hover:bg-red-200 focus:ring-red-500;
}
</style> 