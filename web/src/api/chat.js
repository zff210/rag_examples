import api from './index'

export const fetchChatHistory = async () => {
  const res = await api.get('/chat_session/sessions')
  return res.data
}

export const fetchSession = async (sessionId) => {
  const res = await api.get(`/chat_session/sessions/${sessionId}`)
  return res.data
}

export const deleteSession = async (sessionId) => {
  await api.delete(`/chat_session/sessions/${sessionId}`)
}

export const exportSession = (sessionId) => {
  const link = document.createElement('a')
  link.href = `/chat_session/export/${sessionId}`
  link.download = `session_${sessionId}.md`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

export const createEventSource = (params) => {
  // params: { query, sessionId, webSearch, agentMode }
  let apiUrl = `/stream?query=${encodeURIComponent(params.query)}`
  if (params.sessionId) apiUrl += `&session_id=${params.sessionId}`
  if (params.webSearch) apiUrl += '&web_search=true'
  if (params.agentMode) apiUrl += '&agent_mode=true'
  return new EventSource('/api' + apiUrl)
} 