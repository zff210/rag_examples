<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 标题和导航 -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <h1 class="text-3xl font-bold text-gray-900">MCP Servers 管理</h1>
          <router-link to="/" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-500 hover:bg-primary-600">
            返回对话页面
          </router-link>
        </div>
      </div>

      <!-- 服务器表单 -->
      <div class="bg-white shadow rounded-lg mb-8">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ editingServerId ? '编辑服务器' : '添加新服务器' }}
          </h3>
          <div class="space-y-4">
            <div>
              <label for="serverName" class="block text-sm font-medium text-gray-700">服务器名称</label>
              <input
                v-model="newServer.name"
                type="text"
                id="serverName"
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                placeholder="例如：Production MCP"
              />
            </div>
            <div>
              <label for="serverUrl" class="block text-sm font-medium text-gray-700">服务器 URL</label>
              <input
                v-model="newServer.url"
                type="text"
                id="serverUrl"
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                placeholder="例如：https://mcp.example.com/sse"
              />
            </div>
            <div>
              <label for="serverDescription" class="block text-sm font-medium text-gray-700">描述</label>
              <textarea
                v-model="newServer.description"
                id="serverDescription"
                rows="3"
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                placeholder="可选：服务器用途说明"
              ></textarea>
            </div>
            <div>
              <label for="serverAuthType" class="block text-sm font-medium text-gray-700">认证类型</label>
              <select
                v-model="newServer.auth_type"
                id="serverAuthType"
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              >
                <option value="none">无认证</option>
                <option value="api_key">API Key</option>
                <option value="bearer">Bearer Token</option>
              </select>
            </div>
            <div>
              <label for="serverAuthValue" class="block text-sm font-medium text-gray-700">认证值</label>
              <input
                v-model="newServer.auth_value"
                type="text"
                id="serverAuthValue"
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                placeholder="例如：API Key 或 Token"
              />
            </div>
            <div class="flex justify-end">
              <button
                @click="addServer"
                class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-500 hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                {{ editingServerId ? '更新服务器' : '添加服务器' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 服务器列表 -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">服务器列表</h3>
          <div class="space-y-4">
            <div v-for="server in mcpServers" :key="server.id" class="border border-gray-200 rounded-lg p-4">
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="text-lg font-medium text-gray-900">{{ server.name }}</h4>
                  <p class="text-sm text-gray-500">{{ server.url }}</p>
                  <p v-if="server.description" class="mt-1 text-sm text-gray-600">{{ server.description }}</p>
                </div>
                <div class="flex space-x-2">
                  <button
                    @click="refreshTools(server.id)"
                    class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-primary-700 bg-primary-100 hover:bg-primary-200"
                  >
                    刷新工具
                  </button>
                  <button
                    @click="editServer(server)"
                    class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-yellow-700 bg-yellow-100 hover:bg-yellow-200"
                  >
                    编辑
                  </button>
                  <button
                    @click="deleteServer(server.id)"
                    class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200"
                  >
                    删除
                  </button>
                </div>
              </div>
              <!-- 工具列表 -->
              <div v-if="serverTools[server.id]?.length" class="mt-4">
                <h5 class="text-sm font-medium text-gray-700 mb-2">工具列表：</h5>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div v-for="tool in serverTools[server.id]" :key="tool.id"
                       class="bg-gray-50 rounded-lg p-3">
                    <div class="text-sm font-medium text-gray-900">{{ tool.name }}</div>
                    <div class="text-xs text-gray-500">{{ tool.endpoint }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  fetchMcpServers as fetchServersApi,
  fetchServerTools as fetchToolsApi,
  addServer as addServerApi,
  updateServer as updateServerApi,
  deleteServer as deleteServerApi,
  refreshTools as refreshToolsApi
} from '@/api/mcp'

const mcpServers = ref([])
const serverTools = ref({})
const editingServerId = ref(null)
const newServer = ref({
  name: '',
  url: '',
  description: '',
  auth_type: 'none',
  auth_value: ''
})

const fetchServers = async () => {
  try {
    mcpServers.value = await fetchServersApi()
    for (const server of mcpServers.value) {
      await fetchTools(server.id)
    }
  } catch (error) {
    console.error('获取 MCP 服务器列表失败:', error)
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

const addServer = async () => {
  if (!newServer.value.name || !newServer.value.url) {
    alert('服务器名称和 URL 为必填项！')
    return
  }
  try {
    new URL(newServer.value.url)
  } catch (e) {
    alert('请输入有效的 URL！')
    return
  }
  try {
    if (editingServerId.value) {
      await updateServerApi(editingServerId.value, newServer.value)
      alert('服务器更新成功！')
    } else {
      await addServerApi(newServer.value)
      alert('服务器添加成功！')
    }
    newServer.value = {
      name: '',
      url: '',
      description: '',
      auth_type: 'none',
      auth_value: ''
    }
    editingServerId.value = null
    fetchServers()
  } catch (error) {
    console.error('操作服务器失败:', error)
    alert(`操作服务器失败：${error.response?.data?.detail || error.message}`)
  }
}

const editServer = (server) => {
  newServer.value = { ...server }
  editingServerId.value = server.id
}

const deleteServer = async (serverId) => {
  if (!confirm('确定要删除此 MCP 服务器吗？')) return
  try {
    await deleteServerApi(serverId)
    alert('服务器删除成功！')
    fetchServers()
  } catch (error) {
    console.error('删除服务器失败:', error)
    alert('删除服务器失败！')
  }
}

const refreshTools = async (serverId) => {
  try {
    await refreshToolsApi(serverId)
    alert('工具刷新成功！')
    await fetchTools(serverId)
  } catch (error) {
    console.error('刷新工具失败:', error)
    alert('刷新工具失败！')
  }
}

onMounted(() => {
  fetchServers()
})
</script> 