<template>
  <div
    class="fixed inset-0 flex items-end px-4 py-6 pointer-events-none sm:p-6 sm:items-start z-50"
  >
    <div class="w-full flex flex-col items-center space-y-4 sm:items-end">
      <TransitionGroup
        enter-active-class="transform ease-out duration-300 transition"
        enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
        enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
        leave-active-class="transition ease-in duration-100"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <Toast
          v-for="toast in toasts"
          :key="toast.id"
          :message="toast.message"
          :type="toast.type"
          :duration="toast.duration"
          @close="removeToast(toast.id)"
        />
      </TransitionGroup>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Toast from './Toast.vue'

const toasts = ref([])
let nextId = 1

const addToast = (message, type = 'success', duration = 3000) => {
  const id = nextId++
  toasts.value.push({ id, message, type, duration })
}

const removeToast = (id) => {
  const index = toasts.value.findIndex((t) => t.id === id)
  if (index !== -1) {
    toasts.value.splice(index, 1)
  }
}

// 暴露方法给父组件
defineExpose({
  addToast
})
</script> 