<template>
  <div class="board-view">
    <div class="board-container">
      <div class="lists-container">
        <ListColumn
          v-for="list in boardStore.lists"
          :key="list.id"
          :list="list"
          @add-card="handleAddCard"
          @delete-card="handleDeleteCard"
          @move-card="handleMoveCard"
          @update-list="handleUpdateList"
          @delete-list="handleDeleteList"
        />
        
        <div class="add-list-container">
          <van-button
            v-if="!showAddList"
            type="default"
            size="large"
            block
            icon="plus"
            @click="showAddList = true"
          >
            添加列表
          </van-button>
          
          <van-card
            v-else
            class="add-list-card"
          >
            <van-field
              v-model="newListTitle"
              placeholder="输入列表标题..."
              @blur="handleCreateList"
              @keyup.enter="handleCreateList"
            />
            <div class="add-list-actions">
              <van-button
                type="primary"
                size="small"
                @click="handleCreateList"
              >
                添加列表
              </van-button>
              <van-button
                type="default"
                size="small"
                icon="cross"
                @click="cancelAddList"
              />
            </div>
          </van-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useBoardStore } from '@/stores/board'
import ListColumn from '@/components/ListColumn.vue'
import type { Card, List } from '@/types'

const boardStore = useBoardStore()

const showAddList = ref(false)
const newListTitle = ref('')

const handleAddCard = (listId: string, cardData: Omit<Card, 'id' | 'position'>) => {
  boardStore.addCard(listId, cardData)
}

const handleDeleteCard = (listId: string, cardId: string) => {
  boardStore.deleteCard(listId, cardId)
}

const handleMoveCard = (cardId: string, fromListId: string, toListId: string, newPosition: number) => {
  boardStore.moveCard(cardId, fromListId, toListId, newPosition)
}

const handleUpdateList = (listId: string, updates: Partial<List>) => {
  boardStore.updateList(listId, updates)
}

const handleDeleteList = (listId: string) => {
  boardStore.deleteList(listId)
}

const handleCreateList = () => {
  if (newListTitle.value.trim()) {
    boardStore.addList(newListTitle.value.trim())
    newListTitle.value = ''
    showAddList.value = false
  }
}

const cancelAddList = () => {
  newListTitle.value = ''
  showAddList.value = false
}
</script>

<style scoped>
.board-view {
  height: 100vh;
  background: var(--background-color);
  padding-top: 46px;
  position: relative;
}

.board-view::before {
  content: '🌈';
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 30px;
  opacity: 0.3;
  animation: float 3s ease-in-out infinite;
}

.board-view::after {
  content: '⭐';
  position: absolute;
  top: 60px;
  right: 40px;
  font-size: 20px;
  opacity: 0.3;
  animation: float 3s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.board-container {
  height: 100%;
  overflow-x: auto;
  overflow-y: hidden;
}

.lists-container {
  display: flex;
  height: 100%;
  padding: 20px;
  gap: 20px;
  min-width: min-content;
}

.add-list-container {
  min-width: 272px;
  height: fit-content;
}

.add-list-card {
  background: var(--card-background);
  border-radius: 20px;
  box-shadow: var(--shadow-medium);
  border: 3px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

.add-list-card::before {
  content: '✨';
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 16px;
  opacity: 0.6;
}

.add-list-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}
</style>