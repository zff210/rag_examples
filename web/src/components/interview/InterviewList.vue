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
              v-if="interview.status !== 1"
              @click="showGenerateDialog(interview.id)"
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
              v-if="interview.status >= 2"
              @click="handleViewQuestions(interview)"
              class="btn-action btn-view"
            >
              查看试题
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

    <!-- 生成试题配置弹窗 -->
    <div v-if="showDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full transform transition-all">
        <div class="p-6 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-semibold text-gray-900">生成试题配置</h3>
            <button @click="closeDialog" class="text-gray-400 hover:text-gray-500 focus:outline-none">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <div class="p-6 space-y-6">
          <!-- 试题数量 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">试题数量</label>
            <div class="relative rounded-md shadow-sm">
              <input
                type="number"
                v-model.number="generateConfig.questionCount"
                min="1"
                max="50"
                class="block w-full rounded-md border-gray-300 pl-4 pr-12 focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                placeholder="请输入试题数量"
              >
              <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                <span class="text-gray-500 sm:text-sm">题</span>
              </div>
            </div>
            <p class="mt-1 text-xs text-gray-500">建议生成 5-20 道题目</p>
          </div>

          <!-- 生成方式 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-3">生成方式</label>
            <div class="grid grid-cols-2 gap-4">
              <label class="relative flex cursor-pointer rounded-lg border border-gray-300 bg-white p-4 shadow-sm focus:outline-none"
                :class="{'border-primary-500 ring-2 ring-primary-500': !generateConfig.append}">
                <input
                  type="radio"
                  v-model="generateConfig.append"
                  :value="false"
                  class="sr-only"
                >
                <div class="flex flex-1">
                  <div class="flex flex-col">
                    <span class="block text-sm font-medium text-gray-900">重新生成</span>
                    <span class="mt-1 flex items-center text-xs text-gray-500">清空现有题目并重新生成</span>
                  </div>
                </div>
                <div class="pointer-events-none absolute -inset-px rounded-lg border-2" :class="{'border-primary-500': !generateConfig.append}"></div>
              </label>

              <label class="relative flex cursor-pointer rounded-lg border border-gray-300 bg-white p-4 shadow-sm focus:outline-none"
                :class="{'border-primary-500 ring-2 ring-primary-500': generateConfig.append}">
                <input
                  type="radio"
                  v-model="generateConfig.append"
                  :value="true"
                  class="sr-only"
                >
                <div class="flex flex-1">
                  <div class="flex flex-col">
                    <span class="block text-sm font-medium text-gray-900">追加生成</span>
                    <span class="mt-1 flex items-center text-xs text-gray-500">在现有题目基础上追加新题目</span>
                  </div>
                </div>
                <div class="pointer-events-none absolute -inset-px rounded-lg border-2" :class="{'border-primary-500': generateConfig.append}"></div>
              </label>
            </div>
          </div>

          <!-- 示例答案 -->
          <div class="relative flex items-start">
            <div class="flex h-6 items-center">
              <input
                type="checkbox"
                v-model="generateConfig.withExampleAnswer"
                class="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              >
            </div>
            <div class="ml-3">
              <label class="text-sm font-medium text-gray-900">生成示例答案</label>
              <p class="text-xs text-gray-500">为每道题目生成参考答案</p>
            </div>
          </div>
        </div>

        <div class="px-6 py-4 bg-gray-50 rounded-b-lg flex justify-end space-x-3">
          <button
            @click="closeDialog"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            取消
          </button>
          <button
            @click="handleGenerateQuestions"
            :disabled="isGenerating"
            class="px-4 py-2 text-sm font-medium text-white bg-primary-600 border border-transparent rounded-md shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isGenerating ? '生成中...' : '确认生成' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { formatTimestamp, interviewStatusMap, generateInterviewQuestions } from '@/api/interview'
import { ElMessage } from 'element-plus'

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

const emit = defineEmits(['edit', 'copy-link', 'download-report', 'delete', 'open-interview', 'view-questions', 'refresh'])

const showDialog = ref(false)
const currentInterviewId = ref(null)
const isGenerating = ref(false)
const generateConfig = ref({
  questionCount: 10,
  append: false,
  withExampleAnswer: false
})

const showGenerateDialog = (interviewId) => {
  currentInterviewId.value = interviewId
  generateConfig.value = {
    questionCount: 10,
    append: false,
    withExampleAnswer: false
  }
  showDialog.value = true
}

const closeDialog = () => {
  showDialog.value = false
  currentInterviewId.value = null
  isGenerating.value = false
}

const handleGenerateQuestions = async () => {
  if (isGenerating.value) return
  
  try {
    isGenerating.value = true
    await generateInterviewQuestions(
      currentInterviewId.value,
      generateConfig.value.questionCount,
      generateConfig.value.withExampleAnswer,
      generateConfig.value.append
    )
    ElMessage.success('试题正在生成中，请稍后查看')
    closeDialog()
    emit('refresh') // 触发列表刷新
  } catch (error) {
    console.error('生成试题失败:', error)
    ElMessage.error('生成试题失败，请重试')
  } finally {
    isGenerating.value = false
  }
}

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

const handleViewQuestions = (interview) => {
  window.open(`/interview/questions?token=${interview.token}`, '_blank')
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

.btn-view {
  @apply text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:ring-indigo-500;
}

.btn-secondary {
  @apply text-gray-700 bg-gray-100 hover:bg-gray-200 focus:ring-gray-500;
}
</style> 