import api from './index'

export const fetchDocuments = async () => {
  const response = await api.get('/documents')
  return response.data
}

export const uploadDocument = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const deleteDocument = async (docId) => {
  await api.delete(`/documents/${docId}`)
} 