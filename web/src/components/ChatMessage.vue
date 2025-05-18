<template>
  <div class="flex items-start space-x-4" :class="{ 'flex-row-reverse space-x-reverse': isUser }">
    <!-- 头像 -->
    <div class="flex-shrink-0">
      <div class="w-8 h-8 rounded-full overflow-hidden" :class="{ 'bg-primary-500': !isUser, 'bg-gray-200': isUser }">
        <div class="w-full h-full flex items-center justify-center" :class="{ 'text-white': !isUser, 'text-gray-600': isUser }">
          <span class="text-sm font-medium">{{ isUser ? '我' : 'AI' }}</span>
        </div>
      </div>
    </div>

    <!-- 消息内容 -->
    <div class="flex-1">
      <div class="flex items-center space-x-2 mb-1">
        <span class="text-sm font-medium" :class="{ 'text-gray-900': !isUser, 'text-primary-600': isUser }">
          {{ isUser ? '我' : 'AI' }}
        </span>
        <span class="text-xs text-gray-500">
          {{ formatTime(timestamp) }}
        </span>
      </div>
      <div
        class="prose prose-sm max-w-none"
        :class="{
          'bg-white rounded-lg p-3 shadow-sm border border-gray-100': !isUser,
          'bg-primary-50 rounded-lg p-3': isUser
        }"
      >
        <div v-if="isThinking" class="flex items-center space-x-2 text-gray-500">
          <div class="animate-bounce">●</div>
          <div class="animate-bounce delay-100">●</div>
          <div class="animate-bounce delay-200">●</div>
        </div>
        <div v-else class="text-[15px] leading-6" v-html="renderedContent"></div>
      </div>

      <!-- 操作按钮 -->
      <div v-if="!isThinking" class="mt-1.5 flex items-center space-x-2" :class="{ 'justify-end': isUser }">
        <button
          @click="copyToClipboard"
          class="text-gray-500 hover:text-primary-500 transition-colors relative group"
          :class="{ 'text-primary-500': showCopySuccess }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
          </svg>
          <span class="absolute left-1/2 -translate-x-1/2 -top-8 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
            复制内容
          </span>
        </button>
        <template v-if="!isUser">
          <button
            @click="$emit('speak', content)"
            class="text-gray-500 hover:text-primary-500 transition-colors relative group"
            :class="{ 'text-primary-500': isSpeaking }"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M11 5L6 9H2v6h4l5 4V5z"/>
              <path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
              <path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>
            </svg>
            <span class="absolute left-1/2 -translate-x-1/2 -top-8 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
              {{ isSpeaking ? '停止播放' : '播放语音' }}
            </span>
          </button>
          <button
            @click="$emit('retry')"
            class="text-gray-500 hover:text-primary-500 transition-colors relative group"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
              <path d="M21 3v5h-5"/>
              <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
              <path d="M8 16H3v5"/>
            </svg>
            <span class="absolute left-1/2 -translate-x-1/2 -top-8 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
              重新生成
            </span>
          </button>
        </template>
      </div>
    </div>
  </div>

  <!-- 复制成功提示 -->
  <div v-if="showCopySuccess" 
       class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 
              bg-gray-800/90 text-white px-4 py-2 rounded-lg text-sm
              transition-opacity duration-300"
       :class="{ 'opacity-0': !showCopySuccess, 'opacity-100': showCopySuccess }">
    复制成功
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import { markedSmartypants } from 'marked-smartypants'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

// 配置 marked
marked.use(markedHighlight({
  langPrefix: 'hljs language-',
  highlight(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  }
}))

marked.use(markedSmartypants())

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  isUser: {
    type: Boolean,
    default: false
  },
  isThinking: {
    type: Boolean,
    default: false
  },
  isSpeaking: {
    type: Boolean,
    default: false
  },
  timestamp: {
    type: String,
    default: () => new Date().toISOString()
  }
})

const emit = defineEmits(['speak', 'retry'])
const showCopySuccess = ref(false)

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const renderedContent = computed(() => {
  if (props.isUser) return props.content.trim()
  return marked(props.content.trim(), {
    gfm: true,
    breaks: true,
    sanitize: false
  })
})

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(props.content)
    showCopySuccess.value = true
    setTimeout(() => {
      showCopySuccess.value = false
    }, 1500)
  } catch (err) {
    console.error('复制失败:', err)
  }
}
</script>

<style scoped>
.prose {
  @apply text-gray-800 leading-relaxed;
}

.prose p {
  @apply mb-4 last:mb-0;
}

.prose code {
  @apply px-1.5 py-0.5 bg-gray-100 rounded text-sm font-mono;
}

.prose pre {
  @apply p-4 bg-gray-100 rounded-lg overflow-x-auto;
}

.prose pre code {
  @apply bg-transparent p-0;
}

.prose :deep(h1) {
  @apply text-2xl font-bold mb-4;
}

.prose :deep(h2) {
  @apply text-xl font-bold mb-3;
}

.prose :deep(h3) {
  @apply text-lg font-bold mb-2;
}

.prose :deep(ul) {
  @apply list-disc list-inside mb-4;
}

.prose :deep(ol) {
  @apply list-decimal list-inside mb-4;
}

.prose :deep(li) {
  @apply mb-1;
}

.prose :deep(blockquote) {
  @apply border-l-4 border-gray-200 pl-4 italic my-4;
}

.prose :deep(a) {
  @apply text-primary-500 hover:underline;
}

.prose :deep(table) {
  @apply w-full border-collapse mb-4;
}

.prose :deep(th),
.prose :deep(td) {
  @apply border border-gray-200 p-2;
}

.prose :deep(th) {
  @apply bg-gray-50;
}

.delay-100 {
  animation-delay: 100ms;
}

.delay-200 {
  animation-delay: 200ms;
}
</style> 