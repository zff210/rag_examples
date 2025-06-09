<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 标题和导航 -->
      <div class="mb-8 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-900">面试系统管理</h1>
        <div class="flex space-x-4">
          <router-link to="/" class="btn btn-secondary">返回首页</router-link>
        </div>
      </div>

      <!-- 导航选项卡 -->
      <div class="bg-white shadow rounded-lg mb-6">
        <nav class="flex space-x-4 p-4">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            class="px-4 py-2 rounded-md text-sm font-medium transition-colors"
            :class="[
              activeTab === tab.key
                ? 'bg-primary-100 text-primary-700'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
            ]"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>

      <!-- 主要内容区域 -->
      <div class="bg-white shadow rounded-lg p-6">
        <!-- 岗位管理 -->
        <div v-if="activeTab === 'positions'" class="space-y-6">
          <div class="flex justify-between items-center">
            <h2 class="text-lg font-medium text-gray-900">岗位管理</h2>
            <button
              @click="showPositionForm(null)"
              class="btn btn-primary"
            >
              添加岗位
            </button>
          </div>
          <PositionList
            :positions="positions"
            @edit="showPositionForm"
            @delete="handleDeletePosition"
          />
        </div>

        <!-- 候选人管理 -->
        <div v-if="activeTab === 'candidates'" class="space-y-6">
          <div class="flex justify-between items-center">
            <h2 class="text-lg font-medium text-gray-900">候选人管理</h2>
            <button
              @click="showCandidateForm()"
              class="btn btn-primary"
            >
              添加候选人
            </button>
          </div>
          <CandidateList
            :candidates="candidates"
            :positions="positions"
            @download-resume="handleDownloadResume"
            @delete="handleDeleteCandidate"
          />
        </div>

        <!-- 面试管理 -->
        <div v-if="activeTab === 'interviews'" class="space-y-6">
          <div class="flex justify-between items-center">
            <h2 class="text-lg font-medium text-gray-900">面试管理</h2>
            <button
              @click="showInterviewForm(null)"
              class="btn btn-primary"
            >
              添加面试
            </button>
          </div>
          <InterviewList
            :interviews="interviews"
            :candidates="candidates"
            :positions="positions"
            @edit="showInterviewForm"
            @copy-link="handleCopyInterviewLink"
            @download-report="handleDownloadReport"
            @delete="handleDeleteInterview"
            @generate-questions="handleGenerateQuestions"
            @open-interview="handleOpenInterview"
            @view-questions="handleViewQuestions"
          />
        </div>
      </div>
    </div>

    <!-- 岗位表单模态框 -->
    <div v-if="showPositionModal" class="modal-wrapper">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="text-lg font-medium text-gray-900">
            {{ editingPosition ? '编辑岗位' : '添加岗位' }}
          </h3>
          <button @click="showPositionModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <!-- 添加岗位表单 -->
          <div v-if="!editingPosition" class="space-y-4">
            <div>
              <label class="form-label">岗位信息</label>
              <textarea 
                v-model="positionForm.content" 
                class="form-input" 
                rows="8"
                placeholder="请输入岗位信息，包含岗位名称、岗位要求、岗位职责、招聘负责人等内容"
              ></textarea>
            </div>
          </div>
          <!-- 编辑岗位表单 -->
          <div v-else class="space-y-4">
            <div>
              <label class="form-label">岗位名称</label>
              <input 
                v-model="editPositionForm.name" 
                class="form-input" 
                placeholder="请输入岗位名称"
              />
            </div>
            <div>
              <label class="form-label">岗位要求</label>
              <textarea 
                v-model="editPositionForm.requirements" 
                class="form-input" 
                rows="4"
                placeholder="请输入岗位要求"
              ></textarea>
            </div>
            <div>
              <label class="form-label">岗位职责</label>
              <textarea 
                v-model="editPositionForm.responsibilities" 
                class="form-input" 
                rows="4"
                placeholder="请输入岗位职责"
              ></textarea>
            </div>
            <div>
              <label class="form-label">招聘负责人</label>
              <input 
                v-model="editPositionForm.recruiter" 
                class="form-input" 
                placeholder="请输入招聘负责人"
              />
            </div>
            <div>
              <label class="form-label">需求数量</label>
              <input 
                v-model="editPositionForm.quantity" 
                type="number"
                class="form-input" 
                placeholder="请输入需求数量"
              />
            </div>
            <div>
              <label class="form-label">职位链接</label>
              <input 
                v-model="editPositionForm.link" 
                class="form-input" 
                placeholder="请输入职位链接"
              />
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showPositionModal = false" class="btn btn-secondary">取消</button>
          <button @click="savePosition" class="btn btn-primary" :disabled="isSubmitting">
            {{ isSubmitting ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 候选人表单模态框 -->
    <div v-if="showCandidateModal" class="modal-wrapper">
      <div class="modal-content max-w-2xl">
        <div class="modal-header">
          <h3 class="text-lg font-medium text-gray-900">添加候选人</h3>
          <button @click="showCandidateModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="saveCandidate" class="space-y-6">
            <div class="grid grid-cols-2 gap-6">
              <div>
                <label class="form-label">姓名</label>
                <input 
                  v-model="candidateForm.name" 
                  type="text" 
                  class="form-input" 
                  placeholder="请输入候选人姓名"
                  required
                >
              </div>
              <div>
                <label class="form-label">联系邮箱</label>
                <input 
                  v-model="candidateForm.email" 
                  type="email" 
                  class="form-input" 
                  placeholder="请输入联系邮箱"
                  required
                >
              </div>
            </div>

            <div>
              <label class="form-label">申请岗位</label>
              <div class="relative">
                <div 
                  @click="showPositionDropdown = !showPositionDropdown"
                  class="form-input cursor-pointer flex items-center justify-between min-h-[42px]"
                >
                  <div class="flex flex-wrap gap-1">
                    <span v-if="candidateForm.position_ids.length === 0" class="text-gray-500">请选择岗位</span>
                    <span 
                      v-for="id in candidateForm.position_ids" 
                      :key="id"
                      class="bg-primary-100 text-primary-700 px-2 py-1 rounded-md text-sm flex items-center gap-1"
                    >
                      {{ positions.find(p => p.id === id)?.name }}
                      <button 
                        @click.stop="candidateForm.position_ids = candidateForm.position_ids.filter(p => p !== id)"
                        class="text-primary-500 hover:text-primary-700"
                      >
                        ×
                      </button>
                    </span>
                  </div>
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
                <div 
                  v-if="showPositionDropdown"
                  class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto"
                >
                  <div 
                    v-for="position in positions" 
                    :key="position.id"
                    @click="togglePosition(position.id)"
                    class="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center"
                    :class="{'bg-primary-50': candidateForm.position_ids.includes(position.id)}"
                  >
                    <input 
                      type="checkbox"
                      :checked="candidateForm.position_ids.includes(position.id)"
                      class="mr-2"
                      @click.stop
                    >
                    {{ position.name }}
                  </div>
                </div>
              </div>
            </div>

            <div>
              <label class="form-label">简历文件</label>
              <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                <div class="space-y-1 text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                  <div class="flex text-sm text-gray-600">
                    <label class="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500">
                      <span>上传文件</span>
                      <input 
                        type="file" 
                        @change="handleResumeUpload" 
                        accept=".pdf" 
                        class="sr-only"
                      >
                    </label>
                    <p class="pl-1">或拖拽文件到此处</p>
                  </div>
                  <p class="text-xs text-gray-500">仅支持 PDF 格式</p>
                </div>
              </div>
              <div v-if="candidateForm.resume_content" class="mt-2 text-sm text-gray-500">
                已选择文件: {{ candidateForm.resume_content.name }}
              </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button @click="showCandidateModal = false" class="btn btn-secondary">取消</button>
          <button 
            @click="saveCandidate" 
            class="btn btn-primary" 
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 面试表单模态框 -->
    <div v-if="showInterviewModal" class="modal-wrapper">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="text-lg font-medium text-gray-900">
            {{ editingInterview ? '编辑面试' : '添加面试' }}
          </h3>
          <button @click="showInterviewModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="space-y-6">
            <div>
              <label class="form-label">候选人</label>
              <select 
                v-model="interviewForm.candidate_id" 
                class="form-input" 
                required
                @change="handleCandidateChange"
              >
                <option value="">请选择候选人</option>
                <option 
                  v-for="candidate in candidates" 
                  :key="candidate.id" 
                  :value="candidate.id"
                >
                  {{ candidate.name }}
                </option>
              </select>
            </div>

            <div>
              <label class="form-label">面试岗位</label>
              <select 
                v-model="interviewForm.position_id" 
                class="form-input" 
                required
                :disabled="!interviewForm.candidate_id"
              >
                <option value="">请选择岗位</option>
                <option 
                  v-for="position in availablePositions" 
                  :key="position.id" 
                  :value="position.id"
                >
                  {{ position.name }}
                </option>
              </select>
            </div>

            <div>
              <label class="form-label">面试官</label>
              <input 
                v-model="interviewForm.interviewer" 
                type="text" 
                class="form-input" 
                placeholder="请输入面试官姓名"
                required
              >
            </div>

            <div>
              <label class="form-label">开始时间</label>
              <input 
                v-model="interviewForm.start_time" 
                type="datetime-local" 
                class="form-input" 
                required
              >
            </div>

            <div>
              <label class="form-label">状态</label>
              <select v-model="interviewForm.status" class="form-input">
                <option v-for="(text, value) in interviewStatusMap" :key="value" :value="Number(value)">
                  {{ text }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showInterviewModal = false" class="btn btn-secondary">取消</button>
          <button 
            @click="saveInterview" 
            class="btn btn-primary" 
            :disabled="isSubmitting || !interviewForm.candidate_id || !interviewForm.position_id"
          >
            {{ isSubmitting ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 生成面试题数量弹窗 -->
    <div v-if="showQuestionCountModal" class="modal-wrapper">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="text-lg font-medium text-gray-900">生成面试题</h3>
          <button @click="showQuestionCountModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="space-y-4">
            <div>
              <label class="form-label">试题数量</label>
              <input 
                v-model.number="questionCount" 
                type="number" 
                class="form-input" 
                min="1"
                max="50"
                placeholder="请输入要生成的试题数量"
              >
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showQuestionCountModal = false" class="btn btn-secondary">取消</button>
          <button 
            @click="confirmGenerateQuestions" 
            class="btn btn-primary" 
            :disabled="!questionCount || questionCount < 1 || questionCount > 50"
          >
            确认生成
          </button>
        </div>
      </div>
    </div>

    <!-- 面试题列表模态框 -->
    <div v-if="showQuestionModal" class="modal-wrapper">
      <div class="modal-content max-w-4xl">
        <div class="modal-header">
          <h3 class="text-lg font-medium text-gray-900">面试题列表</h3>
          <button @click="showQuestionModal = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <InterviewQuestionList
            v-if="selectedInterview"
            :interview="selectedInterview"
          />
        </div>
      </div>
    </div>

    <!-- Toast提示 -->
    <ToastManager ref="toastManager" />

    <!-- 确认对话框 -->
    <ConfirmDialog
      :show="showConfirmDialog"
      :title="confirmDialog.title"
      :message="confirmDialog.message"
      :confirm-text="confirmDialog.confirmText"
      @confirm="handleConfirmAction"
      @cancel="showConfirmDialog = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import ToastManager from '../components/ToastManager.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import PositionList from '../components/interview/PositionList.vue'
import CandidateList from '../components/interview/CandidateList.vue'
import InterviewList from '../components/interview/InterviewList.vue'
import InterviewQuestionList from '@/components/interview/InterviewQuestionList.vue'
import {
  fetchPositions,
  createPosition,
  updatePosition,
  deletePosition as deletePositionApi,
  fetchCandidates,
  createCandidate,
  deleteCandidate as deleteCandidateApi,
  downloadResume as downloadResumeApi,
  fetchInterviews,
  createInterview,
  updateInterview,
  deleteInterview as deleteInterviewApi,
  downloadReport as downloadReportApi,
  generateInterviewQuestions,
  positionStatusMap,
  interviewStatusMap
} from '@/api/interview'

// 状态管理
const activeTab = ref('positions')
const positions = ref([])
const candidates = ref([])
const interviews = ref([])
const showConfirmDialog = ref(false)
const toastManager = ref(null)
const isSubmitting = ref(false)

// 模态框状态
const showPositionModal = ref(false)
const showCandidateModal = ref(false)
const showInterviewModal = ref(false)

// 表单数据
const positionForm = ref({
  content: ''
})

const editPositionForm = ref({
  name: '',
  requirements: '',
  responsibilities: '',
  recruiter: '',
  quantity: '',
  link: ''
})

const candidateForm = ref({
  name: '',
  position_ids: [],
  email: '',
  resume_content: null
})

const interviewForm = ref({
  candidate_id: '',
  position_id: '',
  interviewer: '',
  start_time: new Date().toISOString().slice(0, 16),
  status: 0
})

// 编辑状态
const editingPosition = ref(null)
const editingInterview = ref(null)

// 确认对话框配置
const confirmDialog = ref({
  title: '',
  message: '',
  confirmText: '确认',
  action: null,
  data: null
})

// 导航选项卡配置
const tabs = [
  { key: 'positions', name: '岗位管理' },
  { key: 'candidates', name: '候选人管理' },
  { key: 'interviews', name: '面试管理' }
]

// 在 script setup 部分添加
const showPositionDropdown = ref(false)
const availablePositions = ref([])
const showQuestionCountModal = ref(false)
const questionCount = ref(10)
const currentInterviewId = ref(null)
const showQuestionModal = ref(false)
const selectedInterview = ref(null)

// 生命周期钩子
onMounted(() => {
  // 初始加载岗位数据
  fetchPositionsData()
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.relative')) {
      showPositionDropdown.value = false
    }
  })
})

// 监听 activeTab 变化
watch(activeTab, (newTab) => {
  switch (newTab) {
    case 'positions':
      if (positions.value.length === 0) {
        fetchPositionsData()
      }
      break
    case 'candidates':
      if (candidates.value.length === 0) {
        fetchCandidatesData()
      }
      break
    case 'interviews':
      if (interviews.value.length === 0) {
        fetchInterviewsData()
      }
      break
  }
})

// 数据获取方法
const fetchAllData = async () => {
  switch (activeTab.value) {
    case 'positions':
      await fetchPositionsData()
      break
    case 'candidates':
      await fetchCandidatesData()
      break
    case 'interviews':
      await fetchInterviewsData()
      break
  }
}

const fetchPositionsData = async () => {
  try {
    positions.value = await fetchPositions()
  } catch (error) {
    showToast('获取岗位列表失败', 'error')
  }
}

const fetchCandidatesData = async () => {
  try {
    candidates.value = await fetchCandidates()
  } catch (error) {
    showToast('获取候选人列表失败', 'error')
  }
}

const fetchInterviewsData = async () => {
  try {
    interviews.value = await fetchInterviews()
  } catch (error) {
    showToast('获取面试列表失败', 'error')
  }
}

// 工具方法
const showToast = (message, type = 'success') => {
  toastManager.value?.addToast(message, type)
}

const resetForm = (formName) => {
  switch (formName) {
    case 'position':
      positionForm.value = {
        content: ''
      }
      editPositionForm.value = {
        name: '',
        requirements: '',
        responsibilities: '',
        recruiter: '',
        quantity: '',
        link: ''
      }
      break
    case 'candidate':
      candidateForm.value = {
        name: '',
        position_ids: [],
        email: '',
        resume_content: null
      }
      break
    case 'interview':
      interviewForm.value = {
        candidate_id: '',
        position_id: '',
        interviewer: '',
        start_time: new Date().toISOString().slice(0, 16),
        status: 0
      }
      break
  }
}

// 岗位相关方法
const showPositionForm = (position) => {
  editingPosition.value = position
  if (position) {
    // 编辑时，设置编辑表单数据
    editPositionForm.value = {
      name: position.name,
      requirements: position.requirements,
      responsibilities: position.responsibilities,
      quantity: position.quantity,
      status: position.status,
      recruiter: position.recruiter,
      link: position.link
    }
  } else {
    resetForm('position')
  }
  showPositionModal.value = true
}

const savePosition = async () => {
  if (editingPosition.value) {
    if (!editPositionForm.value.name.trim()) {
      showToast('请输入岗位名称', 'error')
      return
    }
  } else {
    if (!positionForm.value.content.trim()) {
      showToast('请输入岗位信息', 'error')
      return
    }
  }

  isSubmitting.value = true
  try {
    if (editingPosition.value) {
      const position = {
        id: editingPosition.value.id,
        ...editPositionForm.value
      }
      await updatePosition(editingPosition.value.id, position)
      showToast('岗位更新成功')
    } else {
      await createPosition(positionForm.value)
      showToast('岗位创建成功')
    }
    showPositionModal.value = false
    fetchPositionsData()
  } catch (error) {
    showToast(error.message || '操作失败', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const handleDeletePosition = (positionId) => {
  confirmDialog.value = {
    title: '删除岗位',
    message: '确定要删除此岗位吗？此操作不可恢复。',
    confirmText: '删除',
    action: 'deletePosition',
    data: positionId
  }
  showConfirmDialog.value = true
}

// 候选人相关方法
const showCandidateForm = () => {
  resetForm('candidate')
  showCandidateModal.value = true
}

const handleResumeUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    candidateForm.value.resume_content = file
  } else {
    showToast('请选择文件', 'error')
    event.target.value = ''
  }
}

const saveCandidate = async () => {
  if (!candidateForm.value.resume_content) {
    showToast('请上传简历', 'error')
    return
  }

  if (candidateForm.value.position_ids.length === 0) {
    showToast('请至少选择一个岗位', 'error')
    return
  }

  isSubmitting.value = true
  try {
    const formData = new FormData()
    formData.append('name', candidateForm.value.name)
    formData.append('email', candidateForm.value.email)
    
    // 确保每个 position_id 都是字符串
    candidateForm.value.position_ids.forEach(id => {
      formData.append('position_id', String(id))
    })
    
    formData.append('resume_content', candidateForm.value.resume_content)

    await createCandidate(formData)
    showToast('候选人创建成功')
    showCandidateModal.value = false
    fetchCandidatesData()
  } catch (error) {
    console.error('保存候选人失败:', error)
    showToast(error.message || '操作失败', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const handleDeleteCandidate = (candidateId) => {
  confirmDialog.value = {
    title: '删除候选人',
    message: '确定要删除此候选人吗？此操作不可恢复。',
    confirmText: '删除',
    action: 'deleteCandidate',
    data: candidateId
  }
  showConfirmDialog.value = true
}

const handleDownloadResume = async (candidateId) => {
  try {
    const blob = await downloadResumeApi(candidateId)
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `resume_${candidateId}.pdf`
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    showToast('下载简历失败', 'error')
  }
}

// 面试相关方法
const showInterviewForm = async (interview) => {
  // 确保有候选人数据
  if (candidates.value.length === 0) {
    try {
      await fetchCandidatesData()
    } catch (error) {
      showToast('获取候选人列表失败', 'error')
      return
    }
  }

  editingInterview.value = interview
  if (interview) {
    const startTime = new Date(interview.start_time * 1000)
      .toISOString()
      .slice(0, 16)
    interviewForm.value = { 
      ...interview, 
      start_time: startTime,
      position_id: interview.position_id || ''
    }
    // 如果是编辑状态，需要设置可选的岗位
    handleCandidateChange()
  } else {
    resetForm('interview')
    availablePositions.value = []
  }
  showInterviewModal.value = true
}

const saveInterview = async () => {
  isSubmitting.value = true
  try {
    const formData = { 
      ...interviewForm.value,
      position_id: parseInt(interviewForm.value.position_id),
      start_time: Math.floor(new Date(interviewForm.value.start_time).getTime() / 1000)
    }

    if (editingInterview.value) {
      await updateInterview(editingInterview.value.id, formData)
      showToast('面试更新成功')
    } else {
      await createInterview(formData)
      showToast('面试创建成功')
    }
    showInterviewModal.value = false
    fetchInterviewsData()
  } catch (error) {
    showToast(error.message || '操作失败', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const handleDeleteInterview = (interviewId) => {
  confirmDialog.value = {
    title: '删除面试',
    message: '确定要删除此面试吗？此操作不可恢复。',
    confirmText: '删除',
    action: 'deleteInterview',
    data: interviewId
  }
  showConfirmDialog.value = true
}

const handleCopyInterviewLink = (token) => {
  const link = `${window.location.origin}/interview/take?token=${token}`
  navigator.clipboard.writeText(link)
  showToast('面试链接已复制到剪贴板')
}

const handleDownloadReport = async (interviewId) => {
  try {
    const blob = await downloadReportApi(interviewId)
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `interview_report_${interviewId}.pdf`
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    showToast('下载面试报告失败', 'error')
  }
}

// 确认对话框动作处理
const handleConfirmAction = async () => {
  const { action, data } = confirmDialog.value
  try {
    switch (action) {
      case 'deletePosition':
        await deletePositionApi(data)
        await fetchPositionsData()
        showToast('岗位已删除')
        break
      case 'deleteCandidate':
        await deleteCandidateApi(data)
        await fetchCandidatesData()
        showToast('候选人已删除')
        break
      case 'deleteInterview':
        await deleteInterviewApi(data)
        await fetchInterviewsData()
        showToast('面试已删除')
        break
    }
  } catch (error) {
    showToast('操作失败', 'error')
  }
  showConfirmDialog.value = false
}

const togglePosition = (positionId) => {
  const index = candidateForm.value.position_ids.indexOf(positionId)
  if (index === -1) {
    candidateForm.value.position_ids.push(positionId)
  } else {
    candidateForm.value.position_ids.splice(index, 1)
  }
}

const handleCandidateChange = () => {
  if (interviewForm.value.candidate_id) {
    const candidate = candidates.value.find(c => c.id === interviewForm.value.candidate_id)
    if (candidate) {
      // 获取候选人关联的岗位列表，将position_id转换为整数
      availablePositions.value = positions.value.filter(p => 
        candidate.position_id.map(id => parseInt(id)).includes(p.id)
      )
    }
  } else {
    availablePositions.value = []
  }
  // 重置岗位选择
  interviewForm.value.position_id = ''
}

const handleGenerateQuestions = (interviewId) => {
  currentInterviewId.value = interviewId
  questionCount.value = 10
  showQuestionCountModal.value = true
}

const confirmGenerateQuestions = async () => {
  try {
    await generateInterviewQuestions(currentInterviewId.value, questionCount.value)
    showToast('面试题生成成功')
    showQuestionCountModal.value = false
    fetchInterviewsData()
  } catch (error) {
    showToast(error.message || '生成面试题失败', 'error')
  }
}

const handleOpenInterview = (token) => {
  const url = `${window.location.origin}/interview/take?token=${token}`
  window.open(url, '_blank')
}

const handleViewQuestions = (interview) => {
  selectedInterview.value = interview
  showQuestionModal.value = true
}
</script>

<style scoped>
.btn {
  @apply px-4 py-2 rounded-md text-sm font-medium transition-colors;
}

.btn-primary {
  @apply bg-primary-600 text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500;
}

.btn-secondary {
  @apply bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500;
}

.modal-wrapper {
  @apply fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50;
}

.modal-content {
  @apply bg-white rounded-lg w-full max-w-md;
}

.modal-header {
  @apply flex justify-between items-center p-4 border-b border-gray-200;
}

.modal-body {
  @apply p-4;
}

.modal-footer {
  @apply flex justify-end space-x-3 p-4 border-t border-gray-200;
}

.modal-close {
  @apply text-gray-400 hover:text-gray-500 text-2xl font-light focus:outline-none;
}

.form-label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}

.form-input {
  @apply block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm;
}
</style> 