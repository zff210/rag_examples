<template>
  <div class="flex h-screen bg-gray-50">
    <!-- 侧边栏 -->
    <div class="flex-shrink-0 transition-all duration-300"
         :class="{ 'w-64': !isSidebarCollapsed, 'w-0': isSidebarCollapsed }">
      <div class="h-full w-64 bg-white border-r border-gray-200"
           :class="{ 'hidden': isSidebarCollapsed }">
        <Sidebar
          :sessions="sessions"
          :current-session-id="currentSessionId"
          :is-collapsed="isSidebarCollapsed"
          @toggle="isSidebarCollapsed = !isSidebarCollapsed"
          @new-chat="startNewChat"
          @select-session="loadSession"
          @export-session="exportSession"
          @delete-session="deleteSession"
          @update:auto-speech="autoSpeech = $event"
          @update:web-search="webSearch = $event"
          @update:agent-mode="agentMode = $event"
        />
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="flex-1 flex flex-col transition-all duration-300">
      <!-- 聊天消息区域 -->
      <div v-if="messages.length > 0" class="flex-1 overflow-y-auto" ref="chatContainer">
        <div class="w-full max-w-4xl mx-auto px-4 py-8">
          <div v-for="(message, index) in messages" :key="index" class="mb-8">
            <ChatMessage
              :content="message.content"
              :is-user="message.role === 'user'"
              :is-speaking="speakingIndex === index"
              :is-thinking="message.content === '正在思考...'"
              :timestamp="message.updated_at"
              @speak="toggleSpeech($event, index)"
              @retry="retryMessage(index)"
            />
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="flex-shrink-0 bg-white border-t border-gray-200">
        <div class="w-full max-w-4xl mx-auto px-4 py-4">
          <div v-if="messages.length === 0" class="text-center text-gray-500 mb-6">
            <h2 class="text-2xl font-semibold mb-3">欢迎使用</h2>
            <p class="text-gray-600">输入您的问题，或点击麦克风开始语音输入</p>
          </div>
          <div class="flex items-center space-x-3">
            <div class="flex-1 relative">
              <input
                v-model="userInput"
                @keyup.enter="sendMessage"
                type="text"
                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                placeholder="输入您的问题或点击麦克风..."
              />
              <button
                @click="toggleRecording"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-primary-500 transition-colors"
                :class="{ 'text-red-500': isRecording }"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/>
                  <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
                  <line x1="12" y1="19" x2="12" y2="22"/>
                </svg>
              </button>
            </div>
            <button
              @click="sendMessage"
              class="px-6 py-3 bg-primary-500 text-white rounded-xl hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all"
            >
              发送
            </button>
          </div>
          <div class="mt-3 flex items-center space-x-4 text-sm text-gray-500">
            <div class="flex items-center space-x-3">
              <span v-if="webSearch" class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-primary-500 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="11" cy="11" r="8"/>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                </svg>
                联网搜索已启用
              </span>
              <span v-if="agentMode" class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-primary-500 mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 2a5 5 0 0 1 5 5v2a5 5 0 0 1-10 0V7a5 5 0 0 1 5-5z"/>
                  <path d="M8 15v1a4 4 0 0 0 8 0v-1"/>
                </svg>
                Agent 已启用
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 展开按钮 -->
    <button
      v-if="isSidebarCollapsed"
      @click="isSidebarCollapsed = false"
      class="fixed left-0 top-4 w-8 h-8 bg-white rounded-r-lg shadow-md flex items-center justify-center text-gray-500 hover:text-gray-700 hover:bg-gray-50 transition-colors border border-l-0 border-gray-200 group"
      title="展开侧边栏"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 12h18M3 6h18M3 18h18"/>
      </svg>
      <span class="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-sm rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
        展开侧边栏
      </span>
    </button>

    <!-- Toast提示 -->
    <ToastManager ref="toastManager" />

    <!-- 确认对话框 -->
    <ConfirmDialog
      :show="showConfirmDialog"
      title="删除会话"
      message="确定要删除此会话吗？此操作不可恢复。"
      confirm-text="删除"
      @confirm="handleConfirmDelete"
      @cancel="showConfirmDialog = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, onUnmounted } from 'vue'
import { useSpeechRecognition, useSpeechSynthesis } from '@vueuse/core'
import Sidebar from '../components/Sidebar.vue'
import ChatMessage from '../components/ChatMessage.vue'
import ToastManager from '../components/ToastManager.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import {
  fetchChatHistory,
  fetchSession,
  deleteSession as deleteSessionApi,
  exportSession as exportSessionApi,
  createEventSource,
  handleStreamResponse
} from '@/api/chat'

// 状态管理
const messages = ref([])
const userInput = ref('')
const sessions = ref([])
const currentSessionId = ref(null)
const isSidebarCollapsed = ref(false)
const autoSpeech = ref(false)
const webSearch = ref(false)
const agentMode = ref(false)
const chatContainer = ref(null)
const speakingIndex = ref(null)
const toastManager = ref(null)
const showConfirmDialog = ref(false)
const pendingDeleteSessionId = ref(null)

// 语音识别
const { isListening, start, stop, isRecording } = useSpeechRecognition({
  lang: 'zh-CN',
  continuous: true,
  interimResults: true
})

// 语音合成
const { isSupported } = useSpeechSynthesis()
const synth = window.speechSynthesis
let currentUtterance = null

// 监听语音识别结果
watch(isListening, (newVal) => {
  if (newVal) {
    // 开始录音
  } else {
    // 停止录音
  }
})

// 方法
const showToast = (message, type = 'success') => {
  toastManager.value?.addToast(message, type)
}

const toggleRecording = () => {
  if (isListening.value) {
    stop()
  } else {
    start()
  }
}

const toggleSpeech = async (text, index) => {
  
  if (!isSupported.value) {
    showToast('当前浏览器不支持语音合成功能', 'error')
    return
  }

  try {
    if (speakingIndex.value === index) {
      if (currentUtterance) {
        synth.cancel()
        currentUtterance = null
      }
      speakingIndex.value = null
    } else {
      // 停止当前正在播放的语音
      if (speakingIndex.value !== null) {
        console.log('停止之前的播放')
        synth.cancel()
        currentUtterance = null
      }
      
      // 开始播放新的语音
      currentUtterance = new SpeechSynthesisUtterance(text)
      currentUtterance.lang = 'zh-CN'
      currentUtterance.rate = 1.0
      currentUtterance.pitch = 1.0
      
      currentUtterance.onstart = () => {
      }
      
      currentUtterance.onend = () => {
        speakingIndex.value = null
        currentUtterance = null
      }
      
      currentUtterance.onerror = (error) => {
        console.error('语音播放错误:', error)
        showToast('语音播放失败', 'error')
        speakingIndex.value = null
        currentUtterance = null
      }

      synth.speak(currentUtterance)
      speakingIndex.value = index
    }
  } catch (error) {
    console.error('语音播放错误:', error)
    showToast('语音播放失败', 'error')
    speakingIndex.value = null
    currentUtterance = null
  }
}

const handleAutoSpeech = async (botMessage, botMessageIndex) => {
  console.log('尝试自动播放:', { botMessage, botMessageIndex, isSupported: isSupported.value })
  
  if (!isSupported.value) {
    console.warn('浏览器不支持语音合成，跳过自动播放')
    return
  }
  
  try {
    if (botMessage && botMessage.trim() && botMessage !== '正在思考...') {
      // 等待一小段时间确保内容完全加载
      await new Promise(resolve => setTimeout(resolve, 500))
      await toggleSpeech(botMessage, botMessageIndex)
    }
  } catch (error) {
    console.error('自动播放错误:', error)
    showToast('自动播放失败', 'error')
  }
}

const sendMessage = async () => {
  if (!userInput.value.trim()) return

  const userMessage = userInput.value
  userInput.value = ''
  
  // 添加用户消息
  messages.value.push({ 
    role: 'user', 
    content: userMessage,
    updated_at: new Date().toISOString()
  })
  
  // 添加机器人思考消息
  const botMessageIndex = messages.value.length
  messages.value.push({ 
    role: 'bot', 
    content: '正在思考...',
    updated_at: new Date().toISOString()
  })

  try {
    const stream = await createEventSource({
      query: userMessage,
      sessionId: currentSessionId.value,
      webSearch: webSearch.value,
      agentMode: agentMode.value
    })

    let botResponse = ''
    await handleStreamResponse(
      stream,
      (chunk) => {
        try {
          const data = JSON.parse(chunk)
          if (data.content) {
            // 累积响应内容
            botResponse += data.content
            // 更新机器人消息内容
            messages.value[botMessageIndex].content = botResponse
            if (data.session_id && !currentSessionId.value) {
              currentSessionId.value = data.session_id
            }
            nextTick(() => {
              chatContainer.value.scrollTop = chatContainer.value.scrollHeight
            })
          }
        } catch (e) {
          console.error('解析响应数据失败:', e)
          showToast('解析响应数据失败', 'error')
        }
      },
      (error) => {
        console.error('流处理错误:', error)
        messages.value[botMessageIndex].content = '服务器连接错误，请稍后再试'
        showToast('服务器连接错误，请稍后再试', 'error')
      },
      async () => {
        if (autoSpeech.value) {
          const botMessage = messages.value[botMessageIndex].content
          await handleAutoSpeech(botMessage, botMessageIndex)
        }
        await getChatHistory()
      }
    )
  } catch (error) {
    console.error('发送消息错误:', error)
    messages.value[botMessageIndex].content = `错误: ${error.message}`
    showToast(`发送消息失败: ${error.message}`, 'error')
  }
}

const getChatHistory = async () => {
  try {
    const history = await fetchChatHistory()
    sessions.value = history.filter(session => session.id !== null)
  } catch (error) {
    console.error('获取历史对话失败:', error)
    showToast('获取历史对话失败', 'error')
  }
}

const loadSession = async (sessionId) => {
  try {
    const data = await fetchSession(sessionId)
    messages.value = data.messages
    currentSessionId.value = sessionId
    nextTick(() => {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    })
  } catch (error) {
    console.error('加载对话失败:', error)
    showToast('加载对话失败', 'error')
  }
}

const startNewChat = () => {
  messages.value = []
  currentSessionId.value = null
  if (currentUtterance) {
    synth.cancel()
    currentUtterance = null
  }
  speakingIndex.value = null
}

const exportSession = async (sessionId) => {
  try {
    await exportSessionApi(sessionId)
    showToast('会话导出成功')
  } catch (error) {
    console.error('导出会话失败:', error)
    showToast('导出会话失败', 'error')
  }
}

const deleteSession = async (sessionId) => {
  pendingDeleteSessionId.value = sessionId
  showConfirmDialog.value = true
}

const handleConfirmDelete = async () => {
  const sessionId = pendingDeleteSessionId.value
  showConfirmDialog.value = false
  pendingDeleteSessionId.value = null

  try {
    await deleteSessionApi(sessionId)
    sessions.value = sessions.value.filter(session => session.id !== sessionId)
    if (currentSessionId.value === sessionId) {
      startNewChat()
    }
    showToast('会话删除成功')
  } catch (error) {
    console.error('删除会话失败:', error)
    showToast('删除会话失败', 'error')
  }
}

const retryMessage = async (index) => {
  // 找到最后一条用户消息
  const lastUserMessageIndex = messages.value
    .slice(0, index)
    .map((msg, i) => ({ msg, i }))
    .reverse()
    .find(({ msg }) => msg.role === 'user')?.i

  if (lastUserMessageIndex === undefined) return

  // 删除从用户消息之后到当前消息的所有消息
  messages.value = messages.value.slice(0, lastUserMessageIndex + 1)
  
  // 重新发送用户消息
  const userMessage = messages.value[lastUserMessageIndex].content
  messages.value.push({ role: 'bot', content: '正在思考...' })

  try {
    const botMessageIndex = messages.value.length - 1
    messages.value[botMessageIndex].content = ''

    const stream = await createEventSource({
      query: userMessage,
      sessionId: currentSessionId.value,
      webSearch: webSearch.value,
      agentMode: agentMode.value
    })

    await handleStreamResponse(
      stream,
      (chunk) => {
        try {
          const data = JSON.parse(chunk)
          if (data.content) {
            messages.value[botMessageIndex].content += data.content
            if (data.session_id && !currentSessionId.value) {
              currentSessionId.value = data.session_id
            }
            nextTick(() => {
              chatContainer.value.scrollTop = chatContainer.value.scrollHeight
            })
          }
        } catch (e) {
          console.error('解析响应数据失败:', e)
          showToast('解析响应数据失败', 'error')
        }
      },
      (error) => {
        console.error('流处理错误:', error)
        if (!messages.value[botMessageIndex].content) {
          messages.value[botMessageIndex].content = '服务器连接错误，请稍后再试'
          showToast('服务器连接错误，请稍后再试', 'error')
        }
      },
      async () => {
        if (autoSpeech.value) {
          const botMessage = messages.value[botMessageIndex].content
          await handleAutoSpeech(botMessage, botMessageIndex)
        }
        await getChatHistory()
      }
    )
  } catch (error) {
    console.error('重试消息错误:', error)
    messages.value[messages.value.length - 1].content = `错误: ${error.message}`
    showToast(`重试消息失败: ${error.message}`, 'error')
  }
}

// 生命周期钩子
onMounted(() => {
  if (!isSupported.value) {
    console.warn('当前浏览器不支持语音合成功能')
    showToast('当前浏览器不支持语音合成功能', 'error')
  } else {
    console.log('语音合成功能已支持')
  }
  getChatHistory()
})

// 组件卸载时停止所有语音
onUnmounted(() => {
  console.log('组件卸载，停止所有语音')
  if (currentUtterance) {
    synth.cancel()
    currentUtterance = null
  }
  speakingIndex.value = null
})
</script> 