<template>
  <div class="flex items-start space-x-4 py-4" :class="{ 'justify-end': isUser }">
    <div v-if="!isUser" class="flex-shrink-0">
      <div class="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center">
        <span class="text-white text-sm">AI</span>
      </div>
    </div>
    
    <div class="flex-1 max-w-3xl">
      <div class="rounded-lg px-4 py-3" :class="messageClasses">
        <div class="prose prose-sm max-w-none" v-html="renderedContent"></div>
      </div>
      <div v-if="!isUser" class="mt-2 flex items-center space-x-2">
        <button 
          @click="$emit('speak', content)"
          class="text-gray-500 hover:text-gray-700"
        >
          <span v-if="isSpeaking">停止</span>
          <span v-else>播放</span>
        </button>
      </div>
    </div>

    <div v-if="isUser" class="flex-shrink-0">
      <div class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
        <span class="text-gray-600 text-sm">我</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  isUser: {
    type: Boolean,
    default: false
  },
  isSpeaking: {
    type: Boolean,
    default: false
  }
})

defineEmits(['speak'])

const messageClasses = computed(() => ({
  'bg-white border border-gray-200': !props.isUser,
  'bg-primary-500 text-white': props.isUser
}))

const renderedContent = computed(() => {
  if (props.isUser) return props.content
  return marked(props.content, {
    highlight: (code, lang) => {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value
      }
      return hljs.highlightAuto(code).value
    }
  })
})
</script>

<style>
.prose pre {
  @apply bg-gray-800 text-gray-100 rounded-lg p-4 overflow-x-auto;
}

.prose code {
  @apply bg-gray-100 text-gray-800 px-1 py-0.5 rounded;
}

.prose pre code {
  @apply bg-transparent text-inherit p-0;
}
</style> 