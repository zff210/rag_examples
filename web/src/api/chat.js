import api from './index'

// 提取统一前缀/chat，将/chat_session替换为/chat
const chatPrefix = '/chat'
export const fetchChatHistory = async () => {
  const res = await api.get(`${chatPrefix}/sessions`)
  return res.data
}

export const fetchSession = async (sessionId) => {
  const res = await api.get(`${chatPrefix}/sessions/${sessionId}`)
  return res.data
}

export const deleteSession = async (sessionId) => {
  await api.delete(`${chatPrefix}/sessions/${sessionId}`)
}

export const exportSession = async (sessionId) => {
  const res = await api.get(`${chatPrefix}/export/${sessionId}`, {
    responseType: 'blob'
  })
  const url = window.URL.createObjectURL(new Blob([res.data]))
  const link = document.createElement('a')
  link.href = url
  link.download = `session_${sessionId}.md`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
}

export const createEventSource = (params) => {
  const requestBody = {
    query: params.query,
    session_id: params.sessionId,
    web_search: params.webSearch,
    agent_mode: params.agentMode
  }

  const apiUrl = '/api' + chatPrefix + '/stream'
  const response = fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody)
  }).then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    return response.body
  })
  
  return response
}

export const handleStreamResponse = async (stream, onData, onError, onComplete) => {
  try {
    const reader = stream.getReader()
    const decoder = new TextDecoder()
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) {
        onComplete?.()
        break
      }
      
      const chunk = decoder.decode(value)
      onData?.(chunk)
    }
  } catch (error) {
    onError?.(error)
  }
} 