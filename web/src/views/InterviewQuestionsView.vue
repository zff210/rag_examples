<template>
  <div class="min-h-screen bg-gray-50 py-4 sm:py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 标题和导航 -->
      <div class="mb-4 sm:mb-8 flex flex-col sm:flex-row sm:items-center justify-between space-y-4 sm:space-y-0">
        <h1 class="text-xl sm:text-2xl font-bold text-gray-900">面试题列表</h1>
        <div class="flex space-x-4">
          <router-link to="/interview" class="btn btn-secondary">返回面试管理</router-link>
        </div>
      </div>

      <!-- 面试信息 -->
      <div v-if="interviewInfo" class="bg-white shadow rounded-lg p-4 sm:p-6 mb-4 sm:mb-6">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6">
          <div>
            <h3 class="text-sm font-medium text-gray-500">候选人</h3>
            <p class="mt-1 text-base sm:text-lg text-gray-900">{{ interviewInfo.candidate }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-500">面试岗位</h3>
            <p class="mt-1 text-base sm:text-lg text-gray-900">{{ interviewInfo.position }}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-500">面试时间</h3>
            <p class="mt-1 text-base sm:text-lg text-gray-900">{{ interviewInfo.time }}</p>
          </div>
        </div>
      </div>

      <!-- 面试题列表 -->
      <div class="bg-white shadow rounded-lg overflow-hidden">
        <div class="p-4 border-b border-gray-200 flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
          <h2 class="text-lg font-medium text-gray-900">面试题列表</h2>
          <div class="flex space-x-2">
            <button
              v-if="selectedQuestions.length > 0"
              @click="generateExampleAnswers"
              class="btn-action btn-generate"
              :disabled="isGenerating"
            >
              {{ isGenerating ? '生成中...' : '生成示例答案' }}
            </button>
          </div>
        </div>

        <!-- 移动端视图 -->
        <div class="sm:hidden">
          <div v-for="question in questions" :key="question.id" class="p-4 border-b border-gray-200">
            <div class="flex items-start space-x-3">
              <input
                type="checkbox"
                :checked="selectedQuestions.includes(question.id)"
                @change="toggleQuestion(question.id)"
                :disabled="question.example_answer"
                class="mt-1 h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed"
              >
              <div class="flex-1 space-y-3">
                <div>
                  <h3 class="text-sm font-medium text-gray-900">问题</h3>
                  <div class="mt-1 text-sm text-gray-900 break-words">{{ question.question }}</div>
                </div>
                <div>
                  <h3 class="text-sm font-medium text-gray-900">评分标准</h3>
                  <div class="mt-1 text-sm text-gray-700 break-words whitespace-pre-line">{{ question.score_standard }}</div>
                </div>
                <div>
                  <h3 class="text-sm font-medium text-gray-900">示例答案</h3>
                  <div class="mt-1">
                    <button
                      v-if="question.example_answer"
                      @click="showAnswerModal(question)"
                      class="text-sm text-purple-600 hover:text-purple-700 font-medium"
                    >
                      查看示例答案
                    </button>
                    <div v-else class="text-sm text-gray-400 italic">
                      暂无示例答案
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="questions.length === 0" class="p-4 text-center text-gray-500">
            暂无面试题
          </div>
        </div>

        <!-- 桌面端视图 -->
        <div class="hidden sm:block">
          <table class="min-w-full divide-y divide-gray-200 table-fixed">
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
                <th scope="col" class="table-th w-2/5">问题</th>
                <th scope="col" class="table-th w-2/5">评分标准</th>
                <th scope="col" class="table-th w-1/5">示例答案</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="question in questions" :key="question.id">
                <td class="table-td w-12">
                  <input
                    type="checkbox"
                    :checked="selectedQuestions.includes(question.id)"
                    @change="toggleQuestion(question.id)"
                    :disabled="question.example_answer"
                    class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                </td>
                <td class="table-td w-2/5">
                  <div class="text-gray-900 break-words">{{ question.question }}</div>
                </td>
                <td class="table-td w-2/5">
                  <div class="text-gray-700 break-words whitespace-pre-line">{{ question.score_standard }}</div>
                </td>
                <td class="table-td w-1/5">
                  <button
                    v-if="question.example_answer"
                    @click="showAnswerModal(question)"
                    class="text-sm text-purple-600 hover:text-purple-700 font-medium"
                  >
                    查看示例答案
                  </button>
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

        <!-- 加载更多按钮 -->
        <div v-if="hasMore" class="p-4 border-t border-gray-200 text-center">
          <button
            @click="loadMoreQuestions"
            class="btn-action btn-secondary"
            :disabled="isLoading"
          >
            {{ isLoading ? '加载中...' : '加载更多' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 示例答案弹窗 -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
        <div class="p-4 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-lg font-medium text-gray-900">示例答案</h3>
          <button @click="closeAnswerModal" class="text-gray-400 hover:text-gray-500">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-6 overflow-y-auto flex-1">
          <div class="markdown-content" v-html="renderMarkdown(selectedAnswer)"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchInterviewInfo, fetchInterviewQuestion, getExampleAnswer } from '@/api/interview'
import { marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js'

// 配置 marked
marked.use(markedHighlight({
  langPrefix: 'hljs language-',
  highlight(code, lang) {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext'
    return hljs.highlight(code, { language }).value
  }
}))

// 启用 GFM
marked.setOptions({
  gfm: true,
  breaks: true
})

const route = useRoute()
const token = computed(() => route.query.token)

const interviewInfo = ref(null)
const questions = ref([])
const isGenerating = ref(false)
const selectedQuestions = ref([])
const showModal = ref(false)
const selectedAnswer = ref('')

// 分页相关
const page = ref(1)
const pageSize = ref(20)
const hasMore = ref(true)
const isLoading = ref(false)

const isAllSelected = computed(() => {
  const selectableQuestions = questions.value.filter(q => !q.example_answer)
  return selectableQuestions.length > 0 && 
         selectedQuestions.value.length === selectableQuestions.length
})

const toggleSelectAll = () => {
  if (isAllSelected.value) {
    selectedQuestions.value = []
  } else {
    // 只选择没有示例答案的题目
    selectedQuestions.value = questions.value
      .filter(q => !q.example_answer)
      .map(q => q.id)
  }
}

const toggleQuestion = (questionId) => {
  const question = questions.value.find(q => q.id === questionId)
  if (question?.example_answer) return // 如果已有示例答案，不允许切换选中状态
  
  const index = selectedQuestions.value.indexOf(questionId)
  if (index === -1) {
    selectedQuestions.value.push(questionId)
  } else {
    selectedQuestions.value.splice(index, 1)
  }
}

const loadInterviewInfo = async () => {
  try {
    interviewInfo.value = await fetchInterviewInfo(token.value)
  } catch (error) {
    console.error('获取面试信息失败:', error)
  }
}

const loadQuestions = async (isLoadMore = false) => {
  if (isLoading.value) return
  
  try {
    isLoading.value = true
    const data = await fetchInterviewQuestion(token.value, {
      page: page.value,
      page_size: pageSize.value
    })
    
    // 确保 data 是数组
    const items = Array.isArray(data) ? data : []
    
    if (isLoadMore) {
      questions.value = [...questions.value, ...items]
    } else {
      questions.value = items
    }
    
    // 检查是否还有更多数据
    hasMore.value = items.length === pageSize.value
    if (hasMore.value) {
      page.value++
    }
  } catch (error) {
    console.error('获取面试题失败:', error)
    // 发生错误时清空数据
    if (!isLoadMore) {
      questions.value = []
    }
    hasMore.value = false
  } finally {
    isLoading.value = false
  }
}

const loadMoreQuestions = () => {
  loadQuestions(true)
}

const generateExampleAnswer = async (questionId) => {
  try {
    const answer = await getExampleAnswer(token.value, questionId)
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

const renderMarkdown = (text) => {
  if (!text) return ''
  return marked(text)
}

const showAnswerModal = (question) => {
  selectedAnswer.value = question.example_answer
  showModal.value = true
}

const closeAnswerModal = () => {
  showModal.value = false
  selectedAnswer.value = ''
}

onMounted(async () => {
  await loadInterviewInfo()
  await loadQuestions()
})
</script>

<style scoped>
.btn {
  @apply px-4 py-2 rounded-md text-sm font-medium transition-colors;
}

.btn-secondary {
  @apply text-gray-700 bg-gray-100 hover:bg-gray-200 focus:ring-gray-500;
}

.table-th {
  @apply px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider;
}

.table-td {
  @apply px-6 py-4 text-sm;
}

.table-td > div {
  @apply max-h-40 overflow-y-auto;
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

.markdown-content {
  @apply max-w-none text-gray-700;
}

.markdown-content :deep(h1) {
  @apply text-xl font-bold mb-4;
}

.markdown-content :deep(h2) {
  @apply text-lg font-bold mb-3;
}

.markdown-content :deep(h3) {
  @apply text-base font-bold mb-2;
}

.markdown-content :deep(p) {
  @apply mb-2;
}

.markdown-content :deep(ul), .markdown-content :deep(ol) {
  @apply ml-4 mb-2;
}

.markdown-content :deep(li) {
  @apply mb-1;
}

.markdown-content :deep(code) {
  @apply bg-gray-100 px-1 py-0.5 rounded text-sm font-mono;
}

.markdown-content :deep(pre) {
  @apply bg-gray-100 p-2 rounded mb-2 overflow-x-auto;
}

.markdown-content :deep(pre code) {
  @apply bg-transparent p-0;
}

.markdown-content :deep(blockquote) {
  @apply border-l-4 border-gray-300 pl-4 italic my-2;
}

.markdown-content :deep(table) {
  @apply border-collapse w-full mb-2;
}

.markdown-content :deep(th), .markdown-content :deep(td) {
  @apply border border-gray-300 px-2 py-1;
}

.markdown-content :deep(th) {
  @apply bg-gray-100;
}

.markdown-content :deep(a) {
  @apply text-blue-600 hover:text-blue-800 underline;
}

.markdown-content :deep(img) {
  @apply max-w-full h-auto my-2;
}

/* 代码高亮样式 */
.markdown-content :deep(.hljs) {
  @apply bg-gray-100;
}

.markdown-content :deep(.hljs-keyword) {
  @apply text-purple-600;
}

.markdown-content :deep(.hljs-string) {
  @apply text-green-600;
}

.markdown-content :deep(.hljs-comment) {
  @apply text-gray-500 italic;
}

.markdown-content :deep(.hljs-function) {
  @apply text-blue-600;
}

.markdown-content :deep(.hljs-number) {
  @apply text-orange-600;
}
</style> 