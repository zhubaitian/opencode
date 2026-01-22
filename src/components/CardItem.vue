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
  margin-bottom: 12px;
  cursor: grab;
  position: relative;
}

.card-item::before {
  content: '🌸';
  position: absolute;
  top: -8px;
  right: 8px;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.card-item:hover::before {
  opacity: 0.7;
}

.card-item:active {
  cursor: grabbing;
  transform: scale(1.02);
}

.card {
  background: var(--card-background);
  border-radius: 16px;
  box-shadow: var(--shadow-light);
  border: 2px solid var(--border-color);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--cute-gradient);
  opacity: 0.8;
}

.card:hover {
  box-shadow: var(--shadow-medium);
  transform: translateY(-2px);
  border-color: var(--primary-color);
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
  word-wrap: break-word;
  margin-bottom: 4px;
}

.card-title::before {
  content: '💕 ';
  font-size: 12px;
  opacity: 0.7;
}

.card-description {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 8px;
  line-height: 1.4;
  font-style: italic;
}

.card-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}

.card-label {
  font-size: 11px;
  padding: 4px 8px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  background: var(--pastel-pink);
  color: var(--text-primary);
  font-weight: 500;
}

.card-due-date {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  font-size: 13px;
  color: var(--text-secondary);
  background: var(--pastel-peach);
  padding: 4px 8px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.card-due-date::before {
  content: '⏰ ';
  font-size: 12px;
}

.due-date-text {
  font-size: 13px;
  font-weight: 500;
}

.card-members {
  display: flex;
  align-items: center;
  gap: -8px;
  margin-top: 10px;
}

.member-avatar {
  border: 3px solid var(--card-background);
  border-radius: 50%;
  box-shadow: var(--shadow-light);
}

.more-members {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--cute-gradient);
  color: white;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid var(--card-background);
  box-shadow: var(--shadow-light);
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}

.card-actions {
  display: flex;
  gap: 10px;
  opacity: 0;
  transition: all 0.3s ease;
  transform: translateY(5px);
}

.card:hover .card-actions {
  opacity: 1;
  transform: translateY(0);
}

:deep(.van-card__content) {
  padding: 8px 12px;
}

:deep(.van-card__footer) {
  padding: 0 12px 8px;
}
</style>