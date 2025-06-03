import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'chat',
      component: () => import('../views/ChatView.vue')
    },
    {
      path: '/mcp',
      name: 'mcp',
      component: () => import('../views/McpView.vue')
    },
    {
      path: '/documents',
      name: 'documents',
      component: () => import('../views/DocumentsView.vue')
    },
    {
      path: '/interview',
      name: 'interview',
      component: () => import('../views/InterviewSystemView.vue')
    },
    {
      path: '/interview/take',
      name: 'interview-take',
      component: () => import('../views/InterviewView.vue')
    }
  ]
})

export default router 