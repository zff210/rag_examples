<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 py-12">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- 错误提示 -->
      <div v-if="error" class="mb-8 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg shadow-sm">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-red-700">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- 状态提示 -->
      <div v-if="!error && interviewStatus === 0" class="bg-white rounded-2xl shadow-xl p-8 mb-8">
        <div class="text-center">
          <div class="mb-6">
            <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h2 class="text-3xl font-bold text-gray-900 mb-4">面试尚未开始</h2>
          <p class="text-lg text-gray-600 mb-6">您的面试尚未开始，请在约定时间再次访问此页面。</p>
          <div class="bg-gray-50 rounded-xl p-6 space-y-4">
            <p class="flex items-center text-gray-700">
              <svg class="h-5 w-5 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <strong class="mr-2">面试时间:</strong> {{ interviewInfo.time }}
            </p>
            <p class="flex items-center text-gray-700">
              <svg class="h-5 w-5 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              <strong class="mr-2">面试岗位:</strong> {{ interviewInfo.position }}
            </p>
            <p class="flex items-center text-gray-700">
              <svg class="h-5 w-5 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              <strong class="mr-2">候选人:</strong> {{ interviewInfo.candidate }}
            </p>
          </div>
        </div>
      </div>

      <!-- 初始提示框 -->
      <div v-if="!error && !isInterviewStarted && (interviewStatus === 1 || interviewStatus === 2)" 
           class="bg-white rounded-2xl shadow-xl p-8 mb-8">
        <div class="text-center">
          <div class="mb-6">
            <svg class="mx-auto h-16 w-16 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h2 class="text-3xl font-bold text-gray-900 mb-4">欢迎参加面试</h2>
          <div class="bg-gray-50 rounded-xl p-6 space-y-4 mb-8">
            <p class="flex items-center text-gray-700">
              <svg class="h-5 w-5 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <strong class="mr-2">面试时间:</strong> {{ interviewInfo.time }}
            </p>
            <p class="flex items-center text-gray-700">
              <svg class="h-5 w-5 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              <strong class="mr-2">面试岗位:</strong> {{ interviewInfo.position }}
            </p>
            <p class="flex items-center text-gray-700">
              <svg class="h-5 w-5 text-blue-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              <strong class="mr-2">候选人:</strong> {{ interviewInfo.candidate }}
            </p>
          </div>
          <button @click="startInterview" 
                  class="inline-flex items-center px-8 py-4 border border-transparent text-xl font-medium rounded-xl text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200">
            <svg class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            开始面试
          </button>
        </div>
      </div>

      <!-- 面试已完成提示 -->
      <div v-if="!error && (interviewStatus >= 3)" class="bg-white rounded-2xl shadow-xl p-8 mb-8">
        <div class="text-center">
          <div class="mb-6">
            <svg class="mx-auto h-16 w-16 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="text-3xl font-bold text-gray-900 mb-4">面试已完成</h3>
          <p class="text-lg text-gray-600 mb-4">您的面试已完成，感谢您的参与。</p>
          <p class="text-lg text-gray-600">我们将尽快对您的面试进行评估，并通过邮件通知您结果。</p>
        </div>
      </div>

      <!-- 面试界面 -->
      <div v-if="isInterviewStarted && !isFinished" class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-6">
          <div class="flex justify-between items-center mb-4">
            <span class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-white text-blue-600">
              问题 {{ currentQuestionIndex + 1 }}/{{ totalQuestions }}
            </span>
            <div class="flex items-center space-x-2">
              <span class="text-white">朗读问题</span>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="voiceReadingEnabled" @change="toggleVoiceReading" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          </div>
          
          <!-- 进度条 -->
          <div class="w-full bg-gray-200 rounded-full h-2.5">
            <div class="bg-white h-2.5 rounded-full transition-all duration-300"
                 :style="{ width: progressPercentage + '%' }">
            </div>
          </div>
          
          <div v-if="isRecording" class="mt-4 flex justify-end items-center">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800 animate-pulse">
              <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
              </svg>
              录音中
            </span>
            <span class="ml-3 text-white font-medium">{{ formatTime(recordingTime) }}</span>
          </div>
        </div>
        
        <div class="p-8">
          <div class="mb-8">
            <h3 class="text-2xl font-bold text-gray-900 mb-4">{{ currentQuestion?.question }}</h3>
            <div class="bg-blue-50 rounded-xl p-6 border border-blue-100">
              <h4 class="text-lg font-semibold text-blue-800 mb-2">评分标准：</h4>
              <p class="text-blue-700 whitespace-pre-line">{{ currentQuestion?.score_standard }}</p>
            </div>
          </div>
          
          <div class="flex justify-center mt-8 space-x-4">
            <button v-if="!isRecording && !isTextInput" 
                    @click="startRecording" 
                    :disabled="loading"
                    class="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-xl text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
              <svg class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
              </svg>
              <span v-if="!loading">语音作答</span>
              <span v-else>准备中...</span>
            </button>
            <button v-if="!isRecording && !isTextInput"
                    @click="startTextInput"
                    :disabled="loading"
                    class="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-xl text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
              <svg class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
              文本作答
            </button>
            <button v-if="!isRecording && !isTextInput"
                    @click="getExampleAnswer"
                    :disabled="loading || !currentQuestion"
                    class="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-xl text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
              <svg class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              获取示例答案
            </button>
            <button v-if="isRecording" 
                    @click="stopRecording"
                    class="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-xl text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200">
              <svg class="h-6 w-6 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z"/>
              </svg>
              作答完毕
            </button>
          </div>

          <!-- 文本输入区域 -->
          <div v-if="isTextInput" class="mt-8">
            <div class="bg-white rounded-xl border border-gray-200 p-4">
              <textarea
                v-model="textAnswer"
                rows="6"
                class="w-full px-4 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-blue-500"
                placeholder="请输入您的答案..."
              ></textarea>
              <div class="mt-4 flex justify-end space-x-4">
                <button
                  @click="cancelTextInput"
                  class="px-6 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-400"
                >
                  取消
                </button>
                <button
                  @click="submitTextAnswer"
                  :disabled="!textAnswer.trim() || loading"
                  class="px-6 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  提交答案
                </button>
              </div>
            </div>
          </div>

          <div v-if="exampleAnswer" class="mt-8 bg-gray-50 rounded-xl p-6 border border-gray-200">
            <h4 class="text-lg font-semibold text-gray-800 mb-2">示例答案：</h4>
            <div class="prose prose-blue max-w-none" v-html="formattedAnswer"></div>
          </div>

          <div v-if="loading" class="mt-8 text-center">
            <div class="inline-flex items-center px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loadingMessage }}
            </div>
          </div>
        </div>
        
        <div class="bg-gray-50 px-8 py-4 text-center">
          <p class="text-sm text-gray-600">请清晰地回答问题，回答完成后点击"作答完毕"</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import {
  fetchInterviewInfo,
  fetchInterviewQuestion,
  submitInterviewAnswer,
  toggleVoiceReading as toggleVoiceReadingApi,
  getExampleAnswer as getExampleAnswerApi,
  interviewStatusMap
} from '@/api/interview'

export default {
  name: 'InterviewView',
  setup() {
    const route = useRoute()
    const token = ref(route.query.token)

    const isInterviewStarted = ref(false)
    const isFinished = ref(false)
    const currentQuestion = ref(null)
    const currentQuestionIndex = ref(0)
    const totalQuestions = ref(10)
    const questions = ref([])
    const isRecording = ref(false)
    const mediaRecorder = ref(null)
    const loading = ref(false)
    const loadingMessage = ref('')
    const error = ref('')
    const recordingTime = ref(0)
    const timerInterval = ref(null)
    const interviewStatus = ref(0)
    const voiceReadingEnabled = ref(true)
    const exampleAnswer = ref('')
    const isTextInput = ref(false)
    const textAnswer = ref('')
    const currentPage = ref(1)
    const pageSize = ref(5)
    const hasMoreQuestions = ref(true)

    const interviewInfo = ref({
      time: '',
      position: '',
      candidate: '',
      voice_reading: true,
      question_count: 10
    })

    const progressPercentage = computed(() => {
      return Math.round(((currentQuestionIndex.value + 1) / totalQuestions.value) * 100)
    })

    const formattedAnswer = computed(() => {
      if (!exampleAnswer.value) return ''
      return marked(exampleAnswer.value)
    })

    onMounted(async () => {
      await loadInterviewInfo()
    })

    const loadInterviewInfo = async () => {
      loading.value = true
      loadingMessage.value = '获取面试信息...'
      try {
        const data = await fetchInterviewInfo(token.value)
        interviewInfo.value = data
        if (data.status !== undefined) {
          interviewStatus.value = data.status
        }
        if (data.voice_reading !== undefined) {
          voiceReadingEnabled.value = Boolean(data.voice_reading)
        }
        if (interviewStatus.value >= 4) { // 面试完毕或报告已生成
          isFinished.value = true
        }
        if (data.question_count !== undefined) {
          totalQuestions.value = data.question_count
        }
      } catch (err) {
        console.error('获取面试信息失败:', err)
        error.value = err.response?.data?.error || '获取面试信息失败，请检查链接是否正确'
      } finally {
        loading.value = false
      }
    }

    const toggleVoiceReading = async () => {
      try {
        await toggleVoiceReadingApi(token.value, {
          enabled: voiceReadingEnabled.value ? 1 : 0
        })
        if (voiceReadingEnabled.value) {
          readQuestionAloud(currentQuestion.value.question)
        } else {
          window.speechSynthesis.cancel()
        }
      } catch (err) {
        console.error('更新语音朗读设置失败:', err)
        voiceReadingEnabled.value = !voiceReadingEnabled.value
      }
    }

    const startInterview = () => {
      if (interviewStatus.value === 1 || interviewStatus.value === 2) {
        isInterviewStarted.value = true
        fetchQuestion()
      } else {
        error.value = '当前状态无法开始面试'
      }
    }

    const fetchQuestion = async () => {
      loading.value = true
      loadingMessage.value = '获取问题中...'
      try {
        const data = await fetchInterviewQuestion(token.value, {
          page: currentPage.value,
          page_size: pageSize.value
        })
        if (data.length === 0) {
          isFinished.value = true
          interviewStatus.value = 3
        } else {
          if (currentPage.value === 1) {
            questions.value = data
          } else {
            questions.value = [...questions.value, ...data]
          }
          currentQuestion.value = data[0]
          hasMoreQuestions.value = data.length === pageSize.value
          if (voiceReadingEnabled.value) {
            readQuestionAloud(currentQuestion.value.question)
          }
        }
      } catch (err) {
        console.error('获取问题失败:', err)
        error.value = err.response?.data?.error || '获取问题失败，请刷新页面重试'
      } finally {
        loading.value = false
      }
    }

    const readQuestionAloud = (text) => {
      if (!voiceReadingEnabled.value || !text) return
      window.speechSynthesis.cancel() // 取消之前的朗读
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'zh-CN'
      window.speechSynthesis.speak(utterance)
    }

    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }

    const startTimer = () => {
      recordingTime.value = 0
      timerInterval.value = setInterval(() => {
        recordingTime.value++
      }, 1000)
    }

    const stopTimer = () => {
      if (timerInterval.value) {
        clearInterval(timerInterval.value)
        timerInterval.value = null
      }
    }

    const startRecording = async () => {
      loading.value = true
      loadingMessage.value = '准备录音...'
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        mediaRecorder.value = new MediaRecorder(stream)
        const chunks = []
        
        mediaRecorder.value.ondataavailable = (e) => chunks.push(e.data)
        mediaRecorder.value.onstop = async () => {
          const audioBlob = new Blob(chunks, { type: 'audio/wav' })
          const questionId = currentQuestion.value.id
          
          const formData = new FormData()
          formData.append('question_id', questionId)
          formData.append('audio_answer', audioBlob, 'answer.wav')
          
          loading.value = true
          loadingMessage.value = '提交答案中...'
          try {
            await submitInterviewAnswer(token.value, formData)
            
            currentQuestionIndex.value++
            if (currentQuestionIndex.value >= questions.value.length) {
              if (hasMoreQuestions.value) {
                currentPage.value++
                await fetchQuestion()
                currentQuestionIndex.value = 0
              } else {
                isFinished.value = true
                interviewStatus.value = 3
              }
            } else {
              currentQuestion.value = questions.value[currentQuestionIndex.value]
              if (voiceReadingEnabled.value) {
                readQuestionAloud(currentQuestion.value.question)
              }
            }
          } catch (err) {
            console.error('提交答案失败:', err)
            error.value = err.response?.data?.error || '提交答案失败，请重试'
          } finally {
            loading.value = false
          }

          stream.getTracks().forEach(track => track.stop())
        }
        
        mediaRecorder.value.start()
        isRecording.value = true
        startTimer()
        loading.value = false
      } catch (err) {
        console.error('录音失败:', err)
        error.value = '无法访问麦克风，请确保您已授予麦克风权限'
        loading.value = false
      }
    }

    const stopRecording = () => {
      if (mediaRecorder.value && mediaRecorder.value.state === 'recording') {
        mediaRecorder.value.stop()
        stopTimer()
        isRecording.value = false
        exampleAnswer.value = ''
      }
    }

    const getExampleAnswer = async () => {
      if (!currentQuestion.value) return
      
      if (currentQuestion.value.example_answer) {
        exampleAnswer.value = currentQuestion.value.example_answer
        return
      }
      
      loading.value = true
      loadingMessage.value = '获取示例答案中...'
      try {
        const data = await getExampleAnswerApi(token.value, currentQuestion.value.id)
        exampleAnswer.value = data
        currentQuestion.value.example_answer = data
      } catch (err) {
        console.error('获取示例答案失败:', err)
        error.value = err.response?.data?.error || '获取示例答案失败'
      } finally {
        loading.value = false
      }
    }

    const startTextInput = () => {
      isTextInput.value = true
      textAnswer.value = ''
    }

    const cancelTextInput = () => {
      isTextInput.value = false
      textAnswer.value = ''
    }

    const submitTextAnswer = async () => {
      if (!textAnswer.value.trim()) return
      
      loading.value = true
      loadingMessage.value = '提交答案中...'
      try {
        const formData = new FormData()
        formData.append('question_id', currentQuestion.value.id)
        formData.append('text_answer', textAnswer.value.trim())
        
        await submitInterviewAnswer(token.value, formData)
        
        currentQuestionIndex.value++
        if (currentQuestionIndex.value >= questions.value.length) {
          if (hasMoreQuestions.value) {
            currentPage.value++
            await fetchQuestion()
            currentQuestionIndex.value = 0
          } else {
            isFinished.value = true
            interviewStatus.value = 3
          }
        } else {
          currentQuestion.value = questions.value[currentQuestionIndex.value]
          if (voiceReadingEnabled.value) {
            readQuestionAloud(currentQuestion.value.question)
          }
        }
        isTextInput.value = false
        textAnswer.value = ''
        exampleAnswer.value = ''
      } catch (err) {
        console.error('提交答案失败:', err)
        error.value = err.response?.data?.error || '提交答案失败，请重试'
      } finally {
        loading.value = false
      }
    }

    return {
      isInterviewStarted,
      isFinished,
      currentQuestion,
      currentQuestionIndex,
      totalQuestions,
      progressPercentage,
      isRecording,
      loading,
      loadingMessage,
      interviewInfo,
      error,
      recordingTime,
      interviewStatus,
      voiceReadingEnabled,
      formatTime,
      startInterview,
      startRecording,
      stopRecording,
      toggleVoiceReading,
      exampleAnswer,
      formattedAnswer,
      getExampleAnswer,
      isTextInput,
      textAnswer,
      startTextInput,
      cancelTextInput,
      submitTextAnswer
    }
  }
}
</script>

<style>
.prose {
  color: #374151;
}

.prose h1,
.prose h2,
.prose h3,
.prose h4 {
  color: #1f2937;
  font-weight: 600;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

.prose p {
  margin-top: 1.25em;
  margin-bottom: 1.25em;
}

.prose ul,
.prose ol {
  margin-top: 1.25em;
  margin-bottom: 1.25em;
  padding-left: 1.625em;
}

.prose li {
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}

.prose code {
  color: #1f2937;
  background-color: #f3f4f6;
  padding: 0.2em 0.4em;
  border-radius: 0.25em;
  font-size: 0.875em;
}

.prose pre {
  background-color: #1f2937;
  color: #f3f4f6;
  padding: 1em;
  border-radius: 0.5em;
  overflow-x: auto;
  margin: 1.5em 0;
}

.prose pre code {
  color: inherit;
  background-color: transparent;
  padding: 0;
  font-size: 0.875em;
}

.prose blockquote {
  border-left: 4px solid #e5e7eb;
  padding-left: 1em;
  font-style: italic;
  color: #4b5563;
  margin: 1.5em 0;
}

.prose a {
  color: #2563eb;
  text-decoration: underline;
}

.prose strong {
  font-weight: 600;
  color: #1f2937;
}

.prose em {
  font-style: italic;
  color: #4b5563;
}
</style> 