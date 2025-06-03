<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="table-th">ID</th>
          <th scope="col" class="table-th">候选人</th>
          <th scope="col" class="table-th">面试官</th>
          <th scope="col" class="table-th">开始时间</th>
          <th scope="col" class="table-th">状态</th>
          <th scope="col" class="table-th">操作</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="interview in interviews" :key="interview.id">
          <td class="table-td">{{ interview.id }}</td>
          <td class="table-td">{{ getCandidateName(interview.candidate_id) }}</td>
          <td class="table-td">{{ interview.interviewer }}</td>
          <td class="table-td">{{ formatTimestamp(interview.start_time) }}</td>
          <td class="table-td">
            <span class="status-badge" :class="getStatusClass(interview.status)">
              {{ interviewStatusMap[interview.status] }}
            </span>
          </td>
          <td class="table-td space-x-2">
            <button
              @click="$emit('edit', interview)"
              class="btn-action btn-edit"
            >
              编辑
            </button>
            <button
              v-if="interview.status === 0"
              @click="$emit('generate-questions', interview.id)"
              class="btn-action btn-generate"
            >
              生成试题
            </button>
            <button
              v-if="interview.status >= 2"
              @click="$emit('copy-link', interview.token)"
              class="btn-action btn-copy"
            >
              复制链接
            </button>
            <button
              v-if="interview.status >= 2"
              @click="$emit('open-interview', interview.token)"
              class="btn-action btn-open"
            >
              打开面试页面
            </button>
            <button
              v-if="interview.status >= 5"
              @click="$emit('download-report', interview.id)"
              class="btn-action btn-download"
            >
              下载报告
            </button>
            <button
              @click="$emit('delete', interview.id)"
              class="btn-action btn-delete"
            >
              删除
            </button>
          </td>
        </tr>
        <tr v-if="interviews.length === 0">
          <td colspan="6" class="table-td text-center text-gray-500">
            暂无数据
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { formatTimestamp, interviewStatusMap } from '@/api/interview'

const props = defineProps({
  interviews: {
    type: Array,
    default: () => []
  },
  candidates: {
    type: Array,
    default: () => []
  }
})

defineEmits(['edit', 'copy-link', 'download-report', 'delete', 'generate-questions', 'open-interview'])

const getCandidateName = (candidateId) => {
  const candidate = props.candidates.find(c => c.id === parseInt(candidateId))
  return candidate ? candidate.name : '未知'
}

const getStatusClass = (status) => {
  const classes = {
    0: 'bg-gray-100 text-gray-800', // 未开始
    1: 'bg-yellow-100 text-yellow-800', // 试题准备中
    2: 'bg-blue-100 text-blue-800', // 试题已备好
    3: 'bg-green-100 text-green-800', // 面试进行中
    4: 'bg-purple-100 text-purple-800', // 面试完毕
    5: 'bg-red-100 text-red-800' // 报告已生成
  }
  return classes[status] || classes[0]
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

.btn-edit {
  @apply text-blue-700 bg-blue-100 hover:bg-blue-200 focus:ring-blue-500;
}

.btn-copy {
  @apply text-yellow-700 bg-yellow-100 hover:bg-yellow-200 focus:ring-yellow-500;
}

.btn-download {
  @apply text-green-700 bg-green-100 hover:bg-green-200 focus:ring-green-500;
}

.btn-delete {
  @apply text-red-700 bg-red-100 hover:bg-red-200 focus:ring-red-500;
}

.btn-generate {
  @apply text-purple-700 bg-purple-100 hover:bg-purple-200 focus:ring-purple-500;
}

.btn-open {
  @apply text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:ring-indigo-500;
}
</style> 