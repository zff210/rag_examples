<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-2xl mx-auto px-4">
      <!-- 标题和导航 -->
      <div class="mb-8 flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-900">文档管理</h1>
        <router-link to="/" class="btn btn-primary">返回首页</router-link>
      </div>
      <!-- 上传文档 -->
      <div class="bg-white shadow rounded-lg p-6 mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">上传文档</label>
        <input type="file" @change="handleFileUpload" accept=".pdf,.txt" class="input" />
      </div>
      <!-- 文档列表 -->
      <div class="bg-white shadow rounded-lg p-6">
        <h2 class="text-lg font-medium text-gray-900 mb-4">文档列表</h2>
        <ul v-if="documents.length" class="divide-y divide-gray-200">
          <li v-for="doc in documents" :key="doc.id" class="flex items-center justify-between py-2">
            <span>{{ doc.name }}</span>
            <button @click="deleteDocument(doc.id)" class="btn btn-secondary text-red-600">删除</button>
          </li>
        </ul>
        <div v-else class="text-gray-500">暂无文档</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchDocuments, uploadDocument, deleteDocument as deleteDocApi } from '@/api/documents'

const documents = ref([])

const getDocuments = async () => {
  try {
    documents.value = await fetchDocuments()
  } catch (error) {
    console.error('获取文档列表失败:', error)
    alert('获取文档列表失败！')
  }
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  try {
    await uploadDocument(file)
    alert('文件上传成功！')
    getDocuments()
  } catch (error) {
    console.error('文件上传失败:', error)
    alert('文件上传失败！')
  }
}

const deleteDocument = async (docId) => {
  if (!confirm('确定要删除该文档吗？')) return
  try {
    await deleteDocApi(docId)
    alert('文档删除成功！')
    getDocuments()
  } catch (error) {
    console.error('删除文档失败:', error)
    alert('删除文档失败！')
  }
}

onMounted(getDocuments)
</script> 