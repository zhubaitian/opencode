<template>
  <div class="list-column">
    <div class="list-header">
      <h3 class="list-title">{{ list.title }}</h3>
      <van-button
        type="default"
        size="mini"
        icon="ellipsis"
        @click="showListMenu = true"
      />
    </div>
    
    <div class="cards-container">
      <draggable
        v-model="localCards"
        :group="{ name: 'cards' }"
        :id="`list-${list.id}`"
        item-key="id"
        @end="handleDragEnd"
      >
        <template #item="{ element: card }">
          <CardItem
            :card="card"
            :list-id="list.id"
            @delete="$emit('deleteCard', list.id, card.id)"
            @edit="handleEditCard"
          />
        </template>
      </draggable>
    </div>
    
    <div class="add-card-container">
      <van-button
        v-if="!showAddCard"
        type="default"
        size="large"
        block
        icon="plus"
        @click="showAddCard = true"
      >
        添加卡片
      </van-button>
      
      <van-card
        v-else
        class="add-card-card"
      >
        <van-field
          v-model="newCardTitle"
          type="textarea"
          :autosize="{ minHeight: 60, maxHeight: 120 }"
          placeholder="输入卡片标题..."
          @blur="handleCreateCard"
        />
        <div class="add-card-actions">
          <van-button
            type="primary"
            size="small"
            @click="handleCreateCard"
          >
            添加卡片
          </van-button>
          <van-button
            type="default"
            size="small"
            icon="cross"
            @click="cancelAddCard"
          />
        </div>
      </van-card>
    </div>
    
    <!-- 列表菜单 -->
    <van-action-sheet
      v-model:show="showListMenu"
      :actions="listMenuActions"
      @select="handleListMenuAction"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import draggable from 'vuedraggable'
import CardItem from './CardItem.vue'
import type { List, Card } from '@/types'

interface Props {
  list: List
}

interface Emits {
  (e: 'addCard', listId: string, cardData: Omit<Card, 'id' | 'position'>): void
  (e: 'deleteCard', listId: string, cardId: string): void
  (e: 'moveCard', cardId: string, fromListId: string, toListId: string, newPosition: number): void
  (e: 'updateList', listId: string, updates: Partial<List>): void
  (e: 'deleteList', listId: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const showAddCard = ref(false)
const newCardTitle = ref('')
const showListMenu = ref(false)

const localCards = ref([...props.list.cards])

const listMenuActions = [
  { name: '添加卡片', icon: 'plus' },
  { name: '重命名列表', icon: 'edit' },
  { name: '删除列表', icon: 'delete', color: '#ee0a24' }
]

const handleCreateCard = () => {
  if (newCardTitle.value.trim()) {
    emit('addCard', props.list.id, {
      title: newCardTitle.value.trim()
    })
    newCardTitle.value = ''
    showAddCard.value = false
  }
}

const cancelAddCard = () => {
  newCardTitle.value = ''
  showAddCard.value = false
}

const handleEditCard = (cardId: string, updates: Partial<Card>) => {
  // 这里可以实现卡片编辑功能
  console.log('Edit card:', cardId, updates)
}

// 监听list.cards变化，同步到localCards
watch(() => props.list.cards, (newCards) => {
  localCards.value = [...newCards]
}, { deep: true })

const handleDragEnd = (event: any) => {
  const { oldIndex, newIndex, from, to } = event
  
  if (from.id !== to.id) {
    // 跨列表移动
    const fromListId = from.id.replace('list-', '')
    const toListId = to.id.replace('list-', '')
    const card = localCards.value[oldIndex]
    
    emit('moveCard', card.id, fromListId, toListId, newIndex)
  } else if (oldIndex !== newIndex) {
    // 同列表内重新排序
    const [movedCard] = localCards.value.splice(oldIndex, 1)
    localCards.value.splice(newIndex, 0, movedCard)
    
    // 更新位置
    localCards.value.forEach((card, index) => {
      card.position = index
    })
  }
}

const handleListMenuAction = (action: any) => {
  switch (action.name) {
    case '添加卡片':
      showAddCard.value = true
      break
    case '重命名列表':
      handleRenameList()
      break
    case '删除列表':
      handleDeleteList()
      break
  }
  showListMenu.value = false
}

const handleRenameList = () => {
  const newName = prompt('请输入新的列表名称:', props.list.title)
  if (newName && newName.trim()) {
    emit('updateList', props.list.id, { title: newName.trim() })
  }
}

const handleDeleteList = () => {
  if (confirm(`确定要删除列表"${props.list.title}"吗？此操作不可撤销。`)) {
    emit('deleteList', props.list.id)
  }
}
</script>

<style scoped>
.list-column {
  min-width: 272px;
  max-width: 272px;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
}

.list-column::before {
  content: '🎀';
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 20px;
  opacity: 0.7;
  z-index: 10;
}

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: var(--cute-gradient);
  border-radius: 20px 20px 0 0;
  box-shadow: var(--shadow-medium);
  border: 3px solid var(--border-color);
  border-bottom: none;
  position: relative;
}

.list-header::before {
  content: '💕';
  position: absolute;
  top: 50%;
  left: 8px;
  transform: translateY(-50%);
  font-size: 14px;
  opacity: 0.8;
}

.list-title {
  font-size: 16px;
  font-weight: 700;
  color: white;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
  letter-spacing: 1px;
}

.cards-container {
  flex: 1;
  padding: 12px;
  background: var(--card-background);
  overflow-y: auto;
  min-height: 100px;
  border: 3px solid var(--border-color);
  border-top: none;
  border-bottom: none;
}

.add-card-container {
  margin-top: 12px;
}

.add-card-card {
  background: var(--card-background);
  border-radius: 20px;
  box-shadow: var(--shadow-medium);
  border: 3px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

.add-card-card::before {
  content: '🌟';
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 16px;
  opacity: 0.6;
}

.add-card-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

/* 可爱拖拽样式 */
.sortable-ghost {
  opacity: 0.3;
  background: var(--pastel-pink);
  border: 2px dashed var(--primary-color);
  border-radius: 15px;
}

.sortable-chosen {
  transform: rotate(8deg) scale(1.05);
  box-shadow: var(--shadow-heavy);
  border-radius: 20px;
  background: var(--pastel-peach);
}

.sortable-drag {
  transform: rotate(8deg) scale(1.05);
  box-shadow: var(--shadow-heavy);
  border-radius: 20px;
  background: var(--pastel-peach);
  transition: all 0.3s ease;
}
</style>