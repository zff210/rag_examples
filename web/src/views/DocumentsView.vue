<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-2xl mx-auto px-4">
      <!-- 标题和导航 -->
      <div class="mb-8 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-900">文档管理</h1>
        <div class="flex space-x-4">
          <button 
            @click="showUploadModal = true" 
            class="btn btn-primary"
          >
            添加文档
          </button>
          <button 
            @click="handleResetIndexClick" 
            class="btn btn-warning"
            :disabled="isResetting"
          >
            {{ isResetting ? '重置中...' : '重置索引' }}
          </button>
          <router-link to="/" class="btn btn-secondary">返回首页</router-link>
        </div>
      </div>

      <!-- 文档列表 -->
      <div class="bg-white shadow rounded-lg p-6">
        <table v-if="documents.length" class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">文件名</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="doc in documents" :key="doc.id">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ doc.file_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <button 
                  @click="handleResetDocIndexClick(doc.id)" 
                  class="text-yellow-600 hover:text-yellow-900"
                  :disabled="doc.isResetting"
                >
                  {{ doc.isResetting ? '重置中...' : '重置索引' }}
                </button>
                <button 
                  @click="handleDeleteClick(doc.id)" 
                  class="text-red-600 hover:text-red-900"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="text-gray-500 text-center py-4">暂无文档</div>
      </div>
    </div>

    <!-- 上传文档弹窗 -->
    <div v-if="showUploadModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">上传文档</h3>
          <button @click="showUploadModal = false" class="text-gray-400 hover:text-gray-500">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">选择文件</label>
          <input type="file" @change="handleFileUpload" accept=".pdf,.txt" class="input" />
        </div>
        <div class="flex justify-end space-x-3">
          <button @click="showUploadModal = false" class="btn btn-secondary">取消</button>
          <button 
            @click="handleUpload" 
            class="btn btn-primary"
            :disabled="!selectedFile || isUploading"
          >
            {{ isUploading ? '上传中...' : '上传' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast提示 -->
    <ToastManager ref="toastManager" />

    <!-- 确认对话框 -->
    <ConfirmDialog
      :show="showConfirmDialog"
      :title="confirmDialogTitle"
      :message="confirmDialogMessage"
      :confirm-text="confirmDialogConfirmText"
      @confirm="handleConfirmAction"
      @cancel="showConfirmDialog = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchDocuments, uploadDocument, deleteDocument as deleteDocApi, resetIndex, resetDocumentIndex as resetDocIndexApi } from '@/api/documents'
import ToastManager from '@/components/ToastManager.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

const documents = ref([])
const isResetting = ref(false)
const showUploadModal = ref(false)
const selectedFile = ref(null)
const isUploading = ref(false)
const toastManager = ref(null)

// 确认对话框状态
const showConfirmDialog = ref(false)
const confirmDialogTitle = ref('')
const confirmDialogMessage = ref('')
const confirmDialogConfirmText = ref('')
const pendingAction = ref(null)
const pendingDocId = ref(null)

const showToast = (message, type = 'success') => {
  toastManager.value?.addToast(message, type)
}

const showConfirm = (title, message, confirmText, action, docId = null) => {
  confirmDialogTitle.value = title
  confirmDialogMessage.value = message
  confirmDialogConfirmText.value = confirmText
  pendingAction.value = action
  pendingDocId.value = docId
  showConfirmDialog.value = true
}

const handleConfirmAction = async () => {
  showConfirmDialog.value = false
  if (pendingAction.value === 'delete') {
    await deleteDocument(pendingDocId.value)
  } else if (pendingAction.value === 'resetIndex') {
    await resetDocumentIndex(pendingDocId.value)
  } else if (pendingAction.value === 'resetAll') {
    await handleResetIndex()
  }
  pendingAction.value = null
  pendingDocId.value = null
}

const getDocuments = async () => {
  try {
    documents.value = await fetchDocuments()
  } catch (error) {
    console.error('获取文档列表失败:', error)
    showToast('获取文档列表失败', 'error')
  }
}

const handleFileUpload = (event) => {
  selectedFile.value = event.target.files[0]
}

const handleUpload = async () => {
  if (!selectedFile.value) return
  
  isUploading.value = true
  try {
    await uploadDocument(selectedFile.value)
    showToast('文件上传成功')
    showUploadModal.value = false
    selectedFile.value = null
    getDocuments()
  } catch (error) {
    console.error('文件上传失败:', error)
    showToast('文件上传失败', 'error')
  } finally {
    isUploading.value = false
  }
}

const deleteDocument = async (docId) => {
  try {
    await deleteDocApi(docId)
    showToast('文档删除成功')
    getDocuments()
  } catch (error) {
    console.error('删除文档失败:', error)
    showToast('删除文档失败', 'error')
  }
}

const handleResetIndex = async () => {
  isResetting.value = true
  try {
    await resetIndex()
    showToast('索引重置成功')
    getDocuments()
  } catch (error) {
    console.error('重置索引失败:', error)
    showToast('重置索引失败', 'error')
  } finally {
    isResetting.value = false
  }
}

const resetDocumentIndex = async (docId) => {
  const doc = documents.value.find(d => d.id === docId)
  if (!doc) return
  
  doc.isResetting = true
  try {
    await resetDocIndexApi(docId)
    showToast('文档索引重置成功')
    getDocuments()
  } catch (error) {
    console.error('重置文档索引失败:', error)
    showToast('重置文档索引失败', 'error')
  } finally {
    doc.isResetting = false
  }
}

// 修改按钮点击事件处理
const handleDeleteClick = (docId) => {
  showConfirm(
    '删除文档',
    '确定要删除该文档吗？此操作不可恢复。',
    '删除',
    'delete',
    docId
  )
}

const handleResetIndexClick = () => {
  showConfirm(
    '重置索引',
    '确定要重置索引吗？这将删除所有已建立的向量索引，但不会删除文档文件。',
    '重置',
    'resetAll'
  )
}

const handleResetDocIndexClick = (docId) => {
  showConfirm(
    '重置文档索引',
    '确定要重置该文档的索引吗？',
    '重置',
    'resetIndex',
    docId
  )
}

onMounted(getDocuments)
</script>

<style scoped>
.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors;
}

.btn-primary {
  @apply bg-primary-500 text-white hover:bg-primary-600 disabled:bg-primary-300;
}

.btn-warning {
  @apply bg-yellow-500 text-white hover:bg-yellow-600 disabled:bg-yellow-300;
}

.btn-secondary {
  @apply bg-gray-100 text-gray-700 hover:bg-gray-200;
}

.input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500;
}
</style> 