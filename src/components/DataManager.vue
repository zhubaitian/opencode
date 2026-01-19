<template>
  <van-action-sheet
    :show="show"
    @update:show="emit('update:show', $event)"
    title="数据管理"
  >
    <div class="data-manager">
      <van-cell-group>
        <van-cell
          title="导出数据"
          label="将看板数据导出为JSON文件"
          is-link
          @click="handleExport"
        />
        <van-cell
          title="导入数据"
          label="从JSON文件导入看板数据"
          is-link
          @click="handleImport"
        />
        <van-cell
          title="清除数据"
          label="删除所有看板数据"
          is-link
          @click="handleClear"
        />
      </van-cell-group>
      
      <!-- 隐藏的文件输入 -->
      <input
        ref="fileInput"
        type="file"
        accept=".json"
        style="display: none"
        @change="handleFileChange"
      />
    </div>
  </van-action-sheet>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useBoardStore } from '@/stores/board'
import { showToast } from 'vant'

interface Props {
  show: boolean
}

interface Emits {
  (e: 'update:show', value: boolean): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const boardStore = useBoardStore()
const fileInput = ref<HTMLInputElement>()

const handleExport = () => {
  try {
    const dataStr = JSON.stringify(boardStore.board, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    
    const link = document.createElement('a')
    link.href = url
    link.download = `trello-board-${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    
    showToast('导出成功')
  } catch (error) {
    showToast('导出失败')
    console.error('Export failed:', error)
  }
}

const handleImport = () => {
  fileInput.value?.click()
}

const handleFileChange = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const content = e.target?.result as string
      const data = JSON.parse(content)
      
      // 验证数据格式
      if (!data.id || !data.title || !Array.isArray(data.lists)) {
        throw new Error('Invalid data format')
      }
      
      // 导入数据
      boardStore.board = data
      boardStore.saveToStorage()
      
      showToast('导入成功')
      emit('update:show', false)
    } catch (error) {
      showToast('导入失败：文件格式不正确')
      console.error('Import failed:', error)
    }
  }
  
  reader.readAsText(file)
  
  // 清除文件输入
  if (event.target) {
    (event.target as HTMLInputElement).value = ''
  }
}

const handleClear = () => {
  if (confirm('确定要清除所有看板数据吗？此操作不可撤销。')) {
    boardStore.clearBoard()
    showToast('数据已清除')
    emit('update:show', false)
  }
}
</script>

<style scoped>
.data-manager {
  padding: 16px 0;
}
</style>