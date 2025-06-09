import api from './index'

const prefix = '/interview'

// 岗位相关接口
export const fetchPositions = async () => {
  const response = await api.get(`${prefix}/positions`)
  return response.data
}

export const createPosition = async (data) => {
  const response = await api.post(`${prefix}/positions`, data)
  return response.data
}

export const updatePosition = async (id, data) => {
  const response = await api.put(`${prefix}/positions/${id}`, data)
  return response.data
}

export const deletePosition = async (id) => {
  await api.delete(`${prefix}/positions/${id}`)
}

// 候选人相关接口
export const fetchCandidates = async () => {
  const response = await api.get(`${prefix}/candidates`)
  return response.data
}

export const createCandidate = async (formData) => {
  const response = await api.post(`${prefix}/candidates`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return response.data
}

export const deleteCandidate = async (id) => {
  await api.delete(`${prefix}/candidates/${id}`)
}

export const downloadResume = async (id) => {
  const response = await api.get(`${prefix}/candidates/${id}/resume`, {
    responseType: 'blob'
  })
  return response.data
}

// 面试相关接口
export const fetchInterviews = async () => {
  const response = await api.get(`${prefix}/interviews`)
  return response.data
}

export const createInterview = async (interview) => {
  const response = await api.post(`${prefix}/interviews`, interview)
  return response.data
}

export const updateInterview = async (id, interview) => {
  const response = await api.put(`${prefix}/interviews/${id}`, interview)
  return response.data
}

export const deleteInterview = async (id) => {
  await api.delete(`${prefix}/interviews/${id}`)
}

export const generateInterviewQuestions = async (interviewId, questionCount, withExampleAnswer = false, append = false) => {
  const response = await api.post(`${prefix}/candidates/${interviewId}/generate_interview_questions`, {
    question_count: questionCount,
    with_example_answer: withExampleAnswer,
    append: append
  })
  return response.data
}

export const downloadReport = async (id) => {
  const response = await api.get(`${prefix}/interviews/${id}/report`, {
    responseType: 'blob'
  })
  return response.data
}

// 面试页面相关接口
export const fetchInterviewInfo = async (token) => {
  const response = await api.get(`${prefix}/interviews/${token}/info`)
  return response.data
}

export const fetchInterviewQuestion = async (token, params = {}) => {
  const response = await api.get(`${prefix}/interviews/${token}/get_question`, {
    params: {
      page: params.page || 1,
      page_size: params.page_size || 10
    }
  })
  return response.data
}

export const getExampleAnswer = async (token, questionId) => {
  const response = await api.get(`${prefix}/interviews/${token}/get_example_answer`, {
    params: {
      question_id: questionId
    }
  })
  return response.data
}

export const submitInterviewAnswer = async (token, data) => {
  const response = await api.post(`${prefix}/interviews/${token}/submit_answer`, data)
  return response.data
}

export const toggleVoiceReading = async (token, data) => {
  const response = await api.post(`${prefix}/interviews/${token}/toggle_voice_reading`, data)
  return response.data
}

// 工具方法
export const formatTimestamp = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp * 1000).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 状态映射
export const positionStatusMap = {
  0: '未启动',
  1: '进行中',
  2: '已完成'
}

export const interviewStatusMap = {
  0: '未开始',
  1: '试题准备中',
  2: '试题已备好',
  3: '面试进行中',
  4: '面试完毕',
  5: '报告已生成'
} 