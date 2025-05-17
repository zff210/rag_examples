<template>
  <div class="flex h-screen bg-gray-50">
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

    <div class="flex-1 flex flex-col ml-64 transition-all duration-300"
         :class="{ 'ml-16': isSidebarCollapsed }">
      <!-- 聊天消息区域 -->
      <div class="flex-1 overflow-y-auto p-4" ref="chatContainer">
        <div v-for="(message, index) in messages" :key="index">
          <ChatMessage
            :content="message.content"
            :is-user="message.role === 'user'"
            :is-speaking="speakingIndex === index"
            @speak="toggleSpeech($event, index)"
          />
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="border-t border-gray-200 bg-white p-4">
        <div class="max-w-4xl mx-auto">
          <div class="flex items-center space-x-2">
            <div class="flex-1 relative">
              <input
                v-model="userInput"
                @keyup.enter="sendMessage"
                type="text"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="输入您的问题或点击麦克风..."
              />
              <button
                @click="toggleRecording"
                class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                :class="{ 'text-red-500': isRecording }"
              >
                <span class="text-xl">🎤</span>
              </button>
            </div>
            <button
              @click="sendMessage"
              class="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              发送
            </button>
          </div>
          <div class="mt-2 flex items-center space-x-4 text-sm text-gray-500">
            <div class="flex items-center space-x-2">
              <span v-if="webSearch" class="flex items-center">
                <span class="text-primary-500 mr-1">🌐</span> 联网搜索已启用
              </span>
              <span v-if="agentMode" class="flex items-center">
                <span class="text-primary-500 mr-1">🤖</span> Agent 已启用
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useSpeechRecognition, useSpeechSynthesis } from '@vueuse/core'
import Sidebar from '../components/Sidebar.vue'
import ChatMessage from '../components/ChatMessage.vue'
import {
  fetchChatHistory,
  fetchSession,
  deleteSession as deleteSessionApi,
  exportSession as exportSessionApi,
  createEventSource
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

// 语音识别
const { isListening, start, stop } = useSpeechRecognition({
  lang: 'zh-CN',
  continuous: true,
  interimResults: true
})

// 语音合成
const { speak, stop: stopSpeaking } = useSpeechSynthesis()

// 监听语音识别结果
watch(isListening, (newVal) => {
  if (newVal) {
    // 开始录音
  } else {
    // 停止录音
  }
})

// 方法
const toggleRecording = () => {
  if (isListening.value) {
    stop()
  } else {
    start()
  }
}

const toggleSpeech = (text, index) => {
  if (speakingIndex.value === index) {
    stopSpeaking()
    speakingIndex.value = null
  } else {
    stopSpeaking()
    speak(text)
    speakingIndex.value = index
  }
}

const sendMessage = async () => {
  if (!userInput.value.trim()) return

  const userMessage = userInput.value
  messages.value.push({ role: 'user', content: userMessage })
  userInput.value = ''
  messages.value.push({ role: 'bot', content: '正在思考...' })

  try {
    const botMessageIndex = messages.value.length - 1
    messages.value[botMessageIndex].content = ''

    const eventSource = createEventSource({
      query: userMessage,
      sessionId: currentSessionId.value,
      webSearch: webSearch.value,
      agentMode: agentMode.value
    })

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.done) {
          eventSource.close()
          if (data.session_id) {
            currentSessionId.value = data.session_id
          }
          if (autoSpeech.value) {
            const botMessage = messages.value[botMessageIndex].content
            if (botMessage && botMessage.trim()) {
              toggleSpeech(botMessage, botMessageIndex)
            }
          }
          getChatHistory()
          return
        }
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
      }
    }
    eventSource.onerror = (error) => {
      console.error('SSE错误:', error)
      eventSource.close()
      if (!messages.value[botMessageIndex].content) {
        messages.value[botMessageIndex].content = '服务器连接错误，请稍后再试'
      }
    }
  } catch (error) {
    console.error('发送消息错误:', error)
    messages.value[messages.value.length - 1].content = `错误: ${error.message}`
  }
}

const getChatHistory = async () => {
  try {
    sessions.value = await fetchChatHistory()
  } catch (error) {
    console.error('获取历史对话失败:', error)
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
  }
}

const startNewChat = () => {
  messages.value = []
  currentSessionId.value = null
  stopSpeaking()
  speakingIndex.value = null
}

const exportSession = (sessionId) => {
  try {
    exportSessionApi(sessionId)
  } catch (error) {
    console.error('导出会话失败:', error)
  }
}

const deleteSession = async (sessionId) => {
  if (!confirm('确定要删除此会话吗？')) return
  try {
    await deleteSessionApi(sessionId)
    sessions.value = sessions.value.filter(session => session.id !== sessionId)
    if (currentSessionId.value === sessionId) {
      startNewChat()
    }
  } catch (error) {
    console.error('删除会话失败:', error)
  }
}

// 生命周期钩子
onMounted(() => {
  getChatHistory()
})
</script> 