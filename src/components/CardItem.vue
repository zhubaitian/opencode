<template>
  <div class="card-item" @click="handleCardClick">
    <van-card class="card">
      <template #title>
        <div class="card-title">{{ card.title }}</div>
      </template>
      
      <template #desc>
        <div class="card-description" v-if="card.description">
          {{ card.description }}
        </div>
        
        <!-- 标签 -->
        <div class="card-labels" v-if="card.labels && card.labels.length > 0">
          <van-tag
            v-for="label in card.labels"
            :key="label.id"
            :color="label.color"
            size="small"
            class="card-label"
          >
            {{ label.name }}
          </van-tag>
        </div>
        
        <!-- 截止日期 -->
        <div class="card-due-date" v-if="card.dueDate">
          <van-icon name="clock-o" size="14" />
          <span class="due-date-text">{{ formatDate(card.dueDate) }}</span>
        </div>
        
        <!-- 成员 -->
        <div class="card-members" v-if="card.members && card.members.length > 0">
          <van-avatar
            v-for="(member, index) in card.members.slice(0, 3)"
            :key="index"
            :src="member"
            size="small"
            class="member-avatar"
          />
          <div
            v-if="card.members.length > 3"
            class="more-members"
          >
            +{{ card.members.length - 3 }}
          </div>
        </div>
      </template>
      
      <template #footer>
        <div class="card-actions" @click.stop>
          <van-button
            type="default"
            size="mini"
            icon="edit"
            @click="handleEdit"
          />
          <van-button
            type="default"
            size="mini"
            icon="cross"
            @click="handleDelete"
          />
        </div>
      </template>
    </van-card>
    
    <!-- 卡片编辑器 -->
    <CardEditor
      v-model:show="showEditor"
      :card="card"
      @save="handleSave"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CardEditor from './CardEditor.vue'
import type { Card } from '@/types'

interface Props {
  card: Card
  listId: string
}

interface Emits {
  (e: 'edit', cardId: string, updates: Partial<Card>): void
  (e: 'delete', listId: string, cardId: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const showEditor = ref(false)

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric'
  })
}

const handleCardClick = () => {
  showEditor.value = true
}

const handleEdit = () => {
  showEditor.value = true
}

const handleSave = (cardId: string, updates: Partial<Card>) => {
  emit('edit', cardId, updates)
}

const handleDelete = () => {
  emit('delete', props.listId, props.card.id)
}
</script>

<style scoped>
.card-item {
  margin-bottom: 8px;
  cursor: grab;
}

.card-item:active {
  cursor: grabbing;
}

.card {
  background: var(--card-background);
  border-radius: 8px;
  box-shadow: var(--shadow-light);
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: var(--shadow-medium);
}

.card-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1.4;
  word-wrap: break-word;
}

.card-description {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 8px;
  line-height: 1.4;
}

.card-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 8px;
}

.card-label {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 3px;
}

.card-due-date {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}

.due-date-text {
  font-size: 12px;
}

.card-members {
  display: flex;
  align-items: center;
  gap: -8px;
  margin-top: 8px;
}

.member-avatar {
  border: 2px solid var(--card-background);
}

.more-members {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--border-color);
  color: var(--text-secondary);
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--card-background);
}

.card-actions {
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.card:hover .card-actions {
  opacity: 1;
}

:deep(.van-card__content) {
  padding: 8px 12px;
}

:deep(.van-card__footer) {
  padding: 0 12px 8px;
}
</style>