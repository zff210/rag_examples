import api from './index'

const documentsPrefix = '/documents'

export const fetchDocuments = async () => {
  const response = await api.get(documentsPrefix + '/list_all')
  return response.data
}

export const uploadDocument = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  await api.post(documentsPrefix + '/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const deleteDocument = async (docId) => {
  await api.delete(documentsPrefix + '/' + docId)
}

export const resetIndex = async () => {
  await api.post(documentsPrefix + '/reload_index')
} 

export const getDocumentIndexStatus = async () => {
  const response = await api.get(documentsPrefix + '/get_index_status')
  return response.data
}

export const resetDocumentIndex = async (docId) => {
  await api.post(documentsPrefix + '/reset_index/' + docId)
}