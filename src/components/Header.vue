<template>
  <div class="header">
    <van-nav-bar
      :title="boardStore.board.title"
      left-text="菜单"
      right-text="设置"
      :fixed="true"
      :placeholder="true"
    >
      <template #left>
        <van-icon name="apps-o" size="20" @click="showMenu = true" />
      </template>
      <template #right>
        <van-icon name="setting-o" size="20" @click="showSettings = true" />
      </template>
    </van-nav-bar>
    
    <!-- 左侧菜单 -->
    <van-action-sheet
      v-model:show="showMenu"
      :actions="menuActions"
      @select="handleMenuAction"
    />
    
    <!-- 右侧设置 -->
    <van-action-sheet
      v-model:show="showSettings"
      :actions="settingsActions"
      @select="handleSettingsAction"
    />
    
    <!-- 数据管理 -->
    <DataManager v-model:show="showDataManager" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useBoardStore } from '@/stores/board'
import DataManager from './DataManager.vue'
import { showDialog, showToast } from 'vant'

const boardStore = useBoardStore()

const showMenu = ref(false)
const showSettings = ref(false)
const showDataManager = ref(false)

const menuActions = [
  { name: '看板信息', icon: 'info-o' },
  { name: '统计', icon: 'chart-trending-o' },
  { name: '关于', icon: 'question-o' }
]

const settingsActions = [
  { name: '数据管理', icon: 'manager-o' },
  { name: '主题设置', icon: 'setting-o' },
  { name: '通知设置', icon: 'bell' }
]

const handleMenuAction = (action: any) => {
  switch (action.name) {
    case '看板信息':
      showBoardInfo()
      break
    case '统计':
      showStatistics()
      break
    case '关于':
      showAbout()
      break
  }
  showMenu.value = false
}

const handleSettingsAction = (action: any) => {
  switch (action.name) {
    case '数据管理':
      showDataManager.value = true
      break
    case '主题设置':
      showToast('主题设置功能开发中')
      break
    case '通知设置':
      showToast('通知设置功能开发中')
      break
  }
  showSettings.value = false
}

const showBoardInfo = () => {
  const totalCards = boardStore.lists.reduce((sum, list) => sum + list.cards.length, 0)
  const totalLists = boardStore.lists.length
  
  showDialog({
    title: '看板信息',
    message: `看板名称：${boardStore.board.title}\n列表数量：${totalLists}\n卡片总数：${totalCards}`,
    showCancelButton: false
  })
}

const showStatistics = () => {
  const stats = boardStore.lists.map(list => ({
    title: list.title,
    count: list.cards.length
  }))
  
  const message = stats.map(stat => `${stat.title}：${stat.count} 张卡片`).join('\n')
  
  showDialog({
    title: '统计信息',
    message,
    showCancelButton: false
  })
}

const showAbout = () => {
  showDialog({
    title: '关于',
    message: 'Trello Clone\n基于 Vue 3 + Vant 构建\n版本：1.0.0',
    showCancelButton: false
  })
}
</script>

<style scoped>
.header {
  background: var(--cute-gradient);
  border-radius: 0 0 20px 20px;
  box-shadow: var(--shadow-medium);
  position: relative;
  overflow: hidden;
}

.header::before {
  content: '🌸';
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  font-size: 20px;
  opacity: 0.6;
}

.header::after {
  content: '🌺';
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  font-size: 20px;
  opacity: 0.6;
}

:deep(.van-nav-bar) {
  background: transparent;
  border: none;
}

:deep(.van-nav-bar__title) {
  color: white;
  font-weight: 700;
  font-size: 18px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
  letter-spacing: 1px;
}

:deep(.van-nav-bar__text) {
  color: white;
  font-weight: 600;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}

:deep(.van-icon) {
  color: white;
  filter: drop-shadow(1px 1px 2px rgba(0,0,0,0.2));
  transition: transform 0.3s ease;
}

:deep(.van-icon:hover) {
  transform: scale(1.2) rotate(10deg);
}
</style>