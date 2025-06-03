<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 标题和导航 -->
      <div class="mb-8 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-900">MCP Servers 管理</h1>
        <div class="flex space-x-4">
          <button 
            @click="showAddModal = true" 
            class="btn btn-primary"
          >
            添加服务器
          </button>
          <router-link to="/" class="btn btn-secondary">返回首页</router-link>
        </div>
      </div>

      <!-- 服务器列表 -->
      <div class="bg-white shadow rounded-lg p-6">
        <table v-if="mcpServers.length" class="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">服务器名称</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">URL</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">认证类型</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="server in mcpServers" :key="server.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ server.name }}</div>
                <div v-if="server.description" class="text-sm text-gray-500">{{ server.description }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ server.url }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ getAuthTypeLabel(server.auth_type) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                <button 
                  @click="handleViewTools(server.id)" 
                  class="text-blue-600 hover:text-blue-900"
                >
                  查看工具
                </button>
                <button 
                  @click="handleRefreshTools(server.id)" 
                  class="text-primary-600 hover:text-primary-900"
                  :disabled="server.isRefreshing"
                >
                  {{ server.isRefreshing ? '刷新中...' : '刷新工具' }}
                </button>
                <button 
                  @click="handleEditClick(server)" 
                  class="text-yellow-600 hover:text-yellow-900"
                >
                  编辑
                </button>
                <button 
                  @click="handleDeleteClick(server.id)" 
                  class="text-red-600 hover:text-red-900"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="text-gray-500 text-center py-4">暂无服务器</div>
      </div>
    </div>

    <!-- 添加/编辑服务器弹窗 -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            {{ editingServerId ? '编辑服务器' : '添加新服务器' }}
          </h3>
          <button @click="closeAddModal" class="text-gray-400 hover:text-gray-500">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">服务器名称</label>
            <input
              v-model="newServer.name"
              type="text"
              class="input"
              placeholder="例如：Production MCP"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">服务器 URL</label>
            <input
              v-model="newServer.url"
              type="text"
              class="input"
              placeholder="例如：https://mcp.example.com/sse"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">描述</label>
            <textarea
              v-model="newServer.description"
              rows="3"
              class="input"
              placeholder="可选：服务器用途说明"
            ></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">认证类型</label>
            <select
              v-model="newServer.auth_type"
              class="input"
            >
              <option value="none">无认证</option>
              <option value="api_key">API Key</option>
              <option value="bearer">Bearer Token</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">认证值</label>
            <input
              v-model="newServer.auth_value"
              type="text"
              class="input"
              placeholder="例如：API Key 或 Token"
            />
          </div>
          <div class="flex justify-end space-x-3">
            <button @click="closeAddModal" class="btn btn-secondary">取消</button>
            <button 
              @click="handleAddServer" 
              class="btn btn-primary"
              :disabled="!isValidServer || isSubmitting"
            >
              {{ isSubmitting ? '提交中...' : (editingServerId ? '更新' : '添加') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 工具列表弹窗 -->
    <div v-if="showToolsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-full max-w-4xl">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900">
            工具列表
          </h3>
          <button @click="closeToolsModal" class="text-gray-400 hover:text-gray-500">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">工具名称</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">描述</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">版本</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="tool in currentTools" :key="tool.name">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ tool.name }}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{{ tool.description }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ tool.version }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <span :class="tool.status === 'active' ? 'text-green-600' : 'text-red-600'">
                    {{ tool.status === 'active' ? '可用' : '不可用' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
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
import { ref, computed, onMounted } from 'vue'
import {
  fetchMcpServers as fetchServersApi,
  fetchServerTools as fetchToolsApi,
  addServer as addServerApi,
  updateServer as updateServerApi,
  deleteServer as deleteServerApi,
  refreshTools as refreshToolsApi
} from '@/api/mcp'
import ToastManager from '@/components/ToastManager.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

const mcpServers = ref([])
const serverTools = ref({})
const showAddModal = ref(false)
const editingServerId = ref(null)
const isSubmitting = ref(false)
const toastManager = ref(null)

// 确认对话框状态
const showConfirmDialog = ref(false)
const confirmDialogTitle = ref('')
const confirmDialogMessage = ref('')
const confirmDialogConfirmText = ref('')
const pendingAction = ref(null)
const pendingServerId = ref(null)

const newServer = ref({
  name: '',
  url: '',
  description: '',
  auth_type: 'none',
  auth_value: ''
})

const isValidServer = computed(() => {
  return newServer.value.name && newServer.value.url
})

const showToast = (message, type = 'success') => {
  toastManager.value?.addToast(message, type)
}

const showConfirm = (title, message, confirmText, action, serverId = null) => {
  confirmDialogTitle.value = title
  confirmDialogMessage.value = message
  confirmDialogConfirmText.value = confirmText
  pendingAction.value = action
  pendingServerId.value = serverId
  showConfirmDialog.value = true
}

const handleConfirmAction = async () => {
  showConfirmDialog.value = false
  if (pendingAction.value === 'delete') {
    await deleteServer(pendingServerId.value)
  }
  pendingAction.value = null
  pendingServerId.value = null
}

const getAuthTypeLabel = (type) => {
  const labels = {
    none: '无认证',
    api_key: 'API Key',
    bearer: 'Bearer Token'
  }
  return labels[type] || type
}

const fetchServers = async () => {
  try {
    mcpServers.value = await fetchServersApi()
    for (const server of mcpServers.value) {
      await fetchTools(server.id)
    }
  } catch (error) {
    console.error('获取 MCP 服务器列表失败:', error)
    showToast('获取服务器列表失败', 'error')
  }
}

const fetchTools = async (serverId) => {
  try {
    serverTools.value[serverId] = await fetchToolsApi(serverId)
  } catch (error) {
    console.error(`获取服务器 ${serverId} 的工具列表失败:`, error)
    serverTools.value[serverId] = []
  }
}

const closeAddModal = () => {
  showAddModal.value = false
  editingServerId.value = null
  newServer.value = {
    name: '',
    url: '',
    description: '',
    auth_type: 'none',
    auth_value: ''
  }
}

const handleAddServer = async () => {
  if (!isValidServer.value) {
    showToast('服务器名称和 URL 为必填项', 'error')
    return
  }

  try {
    new URL(newServer.value.url)
  } catch (e) {
    showToast('请输入有效的 URL', 'error')
    return
  }

  isSubmitting.value = true
  try {
    if (editingServerId.value) {
      await updateServerApi(editingServerId.value, newServer.value)
      showToast('服务器更新成功')
    } else {
      await addServerApi(newServer.value)
      showToast('服务器添加成功')
    }
    closeAddModal()
    fetchServers()
  } catch (error) {
    console.error('操作服务器失败:', error)
    showToast(`操作服务器失败：${error.response?.data?.detail || error.message}`, 'error')
  } finally {
    isSubmitting.value = false
  }
}

const handleEditClick = (server) => {
  newServer.value = { ...server }
  editingServerId.value = server.id
  showAddModal.value = true
}

const handleDeleteClick = (serverId) => {
  showConfirm(
    '删除服务器',
    '确定要删除此 MCP 服务器吗？此操作不可恢复。',
    '删除',
    'delete',
    serverId
  )
}

const deleteServer = async (serverId) => {
  try {
    await deleteServerApi(serverId)
    showToast('服务器删除成功')
    fetchServers()
  } catch (error) {
    console.error('删除服务器失败:', error)
    showToast('删除服务器失败', 'error')
  }
}

const handleRefreshTools = async (serverId) => {
  const server = mcpServers.value.find(s => s.id === serverId)
  if (!server) return

  server.isRefreshing = true
  try {
    await refreshToolsApi(serverId)
    showToast('工具刷新成功')
    await fetchTools(serverId)
  } catch (error) {
    console.error('刷新工具失败:', error)
    showToast('刷新工具失败', 'error')
  } finally {
    server.isRefreshing = false
  }
}

const showToolsModal = ref(false)
const currentTools = ref([])

const handleViewTools = (serverId) => {
  currentTools.value = serverTools.value[serverId] || []
  showToolsModal.value = true
}

const closeToolsModal = () => {
  showToolsModal.value = false
  currentTools.value = []
}

onMounted(() => {
  fetchServers()
})
</script>

<style scoped>
.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors;
}

.btn-primary {
  @apply bg-primary-500 text-white hover:bg-primary-600 disabled:bg-primary-300;
}

.btn-secondary {
  @apply bg-gray-100 text-gray-700 hover:bg-gray-200;
}

.input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500;
}
</style> 