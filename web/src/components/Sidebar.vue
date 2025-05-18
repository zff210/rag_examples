<template>
  <div class="fixed inset-y-0 left-0 w-64 bg-gray-900 text-white transition-transform duration-300"
       :class="{ '-translate-x-full': isCollapsed }">
    <div class="h-full flex flex-col">
      <!-- 顶部控制栏 -->
      <div class="p-4 border-b border-gray-800">
        <div class="flex items-center justify-between">
          <button @click="$emit('toggle')" class="text-gray-400 hover:text-white group relative">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12h18M3 6h18M3 18h18"/>
            </svg>
            <span class="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-sm rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
              {{ isCollapsed ? '展开侧边栏' : '收起侧边栏' }}
            </span>
          </button>
          <h2 class="text-lg font-semibold">历史对话</h2>
          <button @click="$emit('new-chat')" class="text-gray-400 hover:text-white">
            <span class="text-xl">+</span>
          </button>
        </div>
      </div>

      <!-- 历史记录列表 -->
      <div class="flex-1 overflow-y-auto">
        <div v-for="session in sessions" :key="session.id"
             class="p-3 hover:bg-gray-800 cursor-pointer"
             :class="{ 'bg-gray-800': session.id === currentSessionId }"
             @click="$emit('select-session', session.id)">
          <div class="flex justify-between items-center">
            <div class="truncate">{{ session.summary }}</div>
            <div class="flex space-x-2">
              <button @click.stop="$emit('export-session', session.id)"
                      class="text-gray-400 hover:text-white">
                <span>↑</span>
              </button>
              <button @click.stop="$emit('delete-session', session.id)"
                      class="text-gray-400 hover:text-white">
                <span>×</span>
              </button>
            </div>
          </div>
          <div class="text-xs text-gray-500 mt-1">
            {{ formatTime(session.updated_at) }}
          </div>
        </div>
      </div>

      <!-- 底部设置 -->
      <div class="p-4 border-t border-gray-800">
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span>自动语音播放</span>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="autoSpeech" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer 
                          peer-checked:after:translate-x-full peer-checked:after:border-white 
                          after:content-[''] after:absolute after:top-[2px] after:left-[2px] 
                          after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all 
                          peer-checked:bg-primary-500"></div>
            </label>
          </div>
          <div class="flex items-center justify-between">
            <span>联网搜索</span>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="webSearch" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer 
                          peer-checked:after:translate-x-full peer-checked:after:border-white 
                          after:content-[''] after:absolute after:top-[2px] after:left-[2px] 
                          after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all 
                          peer-checked:bg-primary-500"></div>
            </label>
          </div>
          <div class="flex items-center justify-between">
            <span>启用 Agent</span>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="agentMode" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer 
                          peer-checked:after:translate-x-full peer-checked:after:border-white 
                          after:content-[''] after:absolute after:top-[2px] after:left-[2px] 
                          after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all 
                          peer-checked:bg-primary-500"></div>
            </label>
          </div>
        </div>
        <router-link to="/mcp" class="mt-4 block w-full text-center py-2 bg-gray-800 rounded-lg hover:bg-gray-700">
          MCP Servers
        </router-link>
        <router-link to="/documents" class="mt-2 block w-full text-center py-2 bg-gray-800 rounded-lg hover:bg-gray-700">
          文档管理
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  sessions: {
    type: Array,
    default: () => []
  },
  currentSessionId: {
    type: String,
    default: null
  },
  isCollapsed: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'toggle',
  'new-chat',
  'select-session',
  'export-session',
  'delete-session',
  'update:autoSpeech',
  'update:webSearch',
  'update:agentMode'
])

const autoSpeech = ref(false)
const webSearch = ref(false)
const agentMode = ref(false)

watch(autoSpeech, (val) => emit('update:autoSpeech', val))
watch(webSearch, (val) => emit('update:webSearch', val))
watch(agentMode, (val) => emit('update:agentMode', val))

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const now = new Date()
  const diffDays = Math.floor((now - date) / (24 * 60 * 60 * 1000))
  
  if (diffDays === 0) {
    return '今天 ' + date.toLocaleTimeString('zh-CN', {hour: '2-digit', minute:'2-digit'})
  } else if (diffDays === 1) {
    return '昨天 ' + date.toLocaleTimeString('zh-CN', {hour: '2-digit', minute:'2-digit'})
  } else if (diffDays < 7) {
    const weekdays = ['日', '一', '二', '三', '四', '五', '六']
    return '星期' + weekdays[date.getDay()]
  } else {
    return date.toLocaleDateString('zh-CN')
  }
}
</script> 