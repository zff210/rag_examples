import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 300000, // 5分钟
})

export default api 