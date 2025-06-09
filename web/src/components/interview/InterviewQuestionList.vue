<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-lg font-medium text-gray-900">面试题列表</h2>
      <div class="flex space-x-2">
        <button
          v-if="interview.status >= 2 && selectedQuestions.length > 0"
          @click="generateExampleAnswers"
          class="btn-action btn-generate"
          :disabled="isGenerating"
        >
          {{ isGenerating ? '生成中...' : '生成示例答案' }}
        </button>
      </div>
    </div>

    <div class="bg-white shadow rounded-lg overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="table-th w-12">
              <input
                type="checkbox"
                :checked="isAllSelected"
                @change="toggleSelectAll"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              >
            </th>
            <th scope="col" class="table-th">问题</th>
            <th scope="col" class="table-th">评分标准</th>
            <th scope="col" class="table-th">示例答案</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="question in questions" :key="question.id">
            <td class="table-td w-12">
              <input
                type="checkbox"
                :checked="selectedQuestions.includes(question.id)"
                @change="toggleQuestion(question.id)"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              >
            </td>
            <td class="table-td">
              <div class="text-gray-900">{{ question.question }}</div>
            </td>
            <td class="table-td">
              <div class="text-gray-700 whitespace-pre-line">{{ question.score_standard }}</div>
            </td>
            <td class="table-td">
              <div v-if="question.example_answer" class="text-gray-700 whitespace-pre-line">
                {{ question.example_answer }}
              </div>
              <div v-else class="text-gray-400 italic">
                暂无示例答案
              </div>
            </td>
          </tr>
          <tr v-if="questions.length === 0">
            <td colspan="4" class="table-td text-center text-gray-500">
              暂无面试题
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchInterviewQuestion, getExampleAnswer } from '@/api/interview'

const props = defineProps({
  interview: {
    type: Object,
    required: true
  }
})

const questions = ref([])
const isGenerating = ref(false)
const selectedQuestions = ref([])

const isAllSelected = computed(() => {
  return questions.value.length > 0 && selectedQuestions.value.length === questions.value.length
})

const toggleSelectAll = () => {
  if (isAllSelected.value) {
    selectedQuestions.value = []
  } else {
    selectedQuestions.value = questions.value.map(q => q.id)
  }
}

const toggleQuestion = (questionId) => {
  const index = selectedQuestions.value.indexOf(questionId)
  if (index === -1) {
    selectedQuestions.value.push(questionId)
  } else {
    selectedQuestions.value.splice(index, 1)
  }
}

const loadQuestions = async () => {
  try {
    const data = await fetchInterviewQuestion(props.interview.token)
    questions.value = data
  } catch (error) {
    console.error('获取面试题失败:', error)
  }
}

const generateExampleAnswer = async (questionId) => {
  try {
    const answer = await getExampleAnswer(props.interview.token, questionId)
    const question = questions.value.find(q => q.id === questionId)
    if (question) {
      question.example_answer = answer
    }
  } catch (error) {
    console.error('生成示例答案失败:', error)
  }
}

const generateExampleAnswers = async () => {
  if (selectedQuestions.value.length === 0) return
  
  isGenerating.value = true
  try {
    for (const questionId of selectedQuestions.value) {
      await generateExampleAnswer(questionId)
    }
  } catch (error) {
    console.error('生成示例答案失败:', error)
  } finally {
    isGenerating.value = false
    selectedQuestions.value = []
  }
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.table-th {
  @apply px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider;
}

.table-td {
  @apply px-6 py-4 whitespace-nowrap text-sm;
}

.btn-action {
  @apply px-3 py-1 rounded text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2;
}

.btn-generate {
  @apply text-purple-700 bg-purple-100 hover:bg-purple-200 focus:ring-purple-500;
}

.btn-action:disabled {
  @apply opacity-50 cursor-not-allowed;
}
</style> 