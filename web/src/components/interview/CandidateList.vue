<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="table-th">ID</th>
          <th scope="col" class="table-th">姓名</th>
          <th scope="col" class="table-th">申请岗位</th>
          <th scope="col" class="table-th">联系邮箱</th>
          <th scope="col" class="table-th">操作</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="candidate in candidates" :key="candidate.id">
          <td class="table-td">{{ candidate.id }}</td>
          <td class="table-td">{{ candidate.name }}</td>
          <td class="table-td">{{ getPositionName(candidate.position_id) }}</td>
          <td class="table-td">{{ candidate.email }}</td>
          <td class="table-td space-x-2">
            <button
              @click="$emit('download-resume', candidate.id)"
              class="btn-action btn-download"
            >
              下载简历
            </button>
            <button
              @click="$emit('delete', candidate.id)"
              class="btn-action btn-delete"
            >
              删除
            </button>
          </td>
        </tr>
        <tr v-if="candidates.length === 0">
          <td colspan="5" class="table-td text-center text-gray-500">
            暂无数据
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  candidates: {
    type: Array,
    default: () => []
  },
  positions: {
    type: Array,
    default: () => []
  }
})

defineEmits(['download-resume', 'delete'])

const getPositionName = (positionIds) => {
  const positionNames = positionIds.map(id => {
    const numId = parseInt(id)
    const position = props.positions.find(p => p.id === numId)
    return position ? position.name : '未知'
  })
  return positionNames.join(', ')
}
</script>

<style scoped>
.table-th {
  @apply px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider;
}

.table-td {
  @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900;
}

.btn-action {
  @apply px-3 py-1 rounded text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2;
}

.btn-download {
  @apply text-green-700 bg-green-100 hover:bg-green-200 focus:ring-green-500;
}

.btn-delete {
  @apply text-red-700 bg-red-100 hover:bg-red-200 focus:ring-red-500;
}
</style> 