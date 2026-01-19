<template>
  <van-popup
    :show="show"
    @update:show="emit('update:show', $event)"
    position="bottom"
    :style="{ height: '80%' }"
    round
  >
    <div class="card-editor">
      <div class="editor-header">
        <van-nav-bar
          title="编辑卡片"
          left-text="取消"
          right-text="保存"
          @click-left="handleCancel"
          @click-right="handleSave"
        />
      </div>
      
      <div class="editor-content">
        <van-cell-group inset>
          <van-field
            v-model="localCard.title"
            label="标题"
            placeholder="输入卡片标题"
            required
          />
          
          <van-field
            v-model="localCard.description"
            type="textarea"
            label="描述"
            placeholder="输入卡片描述"
            :autosize="{ minHeight: 80, maxHeight: 150 }"
          />
        </van-cell-group>
        
        <!-- 标签管理 -->
        <van-cell-group inset title="标签">
          <div class="labels-section">
            <div class="existing-labels">
              <van-tag
                v-for="label in localCard.labels"
                :key="label.id"
                :color="label.color"
                closeable
                @close="removeLabel(label.id)"
                class="label-tag"
              >
                {{ label.name }}
              </van-tag>
            </div>
            
            <van-button
              type="default"
              size="small"
              icon="plus"
              @click="showLabelPicker = true"
            >
              添加标签
            </van-button>
          </div>
        </van-cell-group>
        
        <!-- 截止日期 -->
        <van-cell-group inset title="截止日期">
          <van-cell
            :title="localCard.dueDate ? formatDate(localCard.dueDate) : '设置截止日期'"
            :value="localCard.dueDate ? '' : '点击设置'"
            is-link
            @click="showDatePicker = true"
          >
            <template #right-icon v-if="localCard.dueDate">
              <van-icon name="clear" @click.stop="clearDueDate" />
            </template>
          </van-cell>
        </van-cell-group>
        
        <!-- 成员管理 -->
        <van-cell-group inset title="成员">
          <div class="members-section">
            <div class="existing-members">
              <van-avatar
                v-for="(member, index) in localCard.members"
                :key="index"
                :src="member"
                size="40"
                class="member-avatar"
                @click="removeMember(index)"
              />
            </div>
            
            <van-button
              type="default"
              size="small"
              icon="plus"
              @click="showMemberPicker = true"
            >
              添加成员
            </van-button>
          </div>
        </van-cell-group>
      </div>
    </div>
    
    <!-- 标签选择器 -->
    <van-action-sheet
      v-model:show="showLabelPicker"
      title="选择标签"
    >
      <div class="label-picker">
        <div class="preset-labels">
          <van-tag
            v-for="label in presetLabels"
            :key="label.id"
            :color="label.color"
            :class="{ 'selected': isLabelSelected(label.id) }"
            class="preset-label"
            @click="toggleLabel(label)"
          >
            {{ label.name }}
          </van-tag>
        </div>
      </div>
    </van-action-sheet>
    
    <!-- 日期选择器 -->
    <van-popup v-model:show="showDatePicker" position="bottom">
      <van-date-picker
        v-model="selectedDate"
        @confirm="handleDateConfirm"
        @cancel="showDatePicker = false"
      />
    </van-popup>
  </van-popup>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { Card, Label } from '@/types'

interface Props {
  show: boolean
  card: Card
}

interface Emits {
  (e: 'update:show', value: boolean): void
  (e: 'save', cardId: string, updates: Partial<Card>): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const localCard = ref<Card>({ ...props.card })
const showLabelPicker = ref(false)
const showDatePicker = ref(false)
const showMemberPicker = ref(false)
const selectedDate = ref(new Date())

// 预设标签
const presetLabels: Label[] = [
  { id: '1', name: '紧急', color: '#ee0a24' },
  { id: '2', name: '重要', color: '#ff976a' },
  { id: '3', name: '普通', color: '#07c160' },
  { id: '4', name: '低优先级', color: '#1989fa' },
  { id: '5', name: 'Bug', color: '#ff6034' },
  { id: '6', name: '功能', color: '#7232dd' }
]

// 监听卡片变化
watch(() => props.card, (newCard) => {
  localCard.value = { ...newCard }
}, { deep: true })

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const isLabelSelected = (labelId: string) => {
  return localCard.value.labels?.some(label => label.id === labelId)
}

const toggleLabel = (label: Label) => {
  if (!localCard.value.labels) {
    localCard.value.labels = []
  }
  
  const index = localCard.value.labels.findIndex(l => l.id === label.id)
  if (index > -1) {
    localCard.value.labels.splice(index, 1)
  } else {
    localCard.value.labels.push(label)
  }
}

const removeLabel = (labelId: string) => {
  if (localCard.value.labels) {
    const index = localCard.value.labels.findIndex(l => l.id === labelId)
    if (index > -1) {
      localCard.value.labels.splice(index, 1)
    }
  }
}

const handleDateConfirm = () => {
  localCard.value.dueDate = selectedDate.value.toISOString()
  showDatePicker.value = false
}

const clearDueDate = () => {
  localCard.value.dueDate = undefined
}

const removeMember = (index: number) => {
  if (localCard.value.members) {
    localCard.value.members.splice(index, 1)
  }
}

const handleCancel = () => {
  emit('update:show', false)
}

const handleSave = () => {
  emit('save', props.card.id, localCard.value)
  emit('update:show', false)
}
</script>

<style scoped>
.card-editor {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.editor-header {
  flex-shrink: 0;
}

.editor-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px 0;
}

.labels-section,
.members-section {
  padding: 16px;
}

.existing-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.label-tag {
  margin: 0;
}

.existing-members {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.member-avatar {
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s;
}

.member-avatar:hover {
  border-color: var(--primary-color);
}

.label-picker {
  padding: 20px;
}

.preset-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.preset-label {
  cursor: pointer;
  transition: transform 0.2s, opacity 0.2s;
}

.preset-label:hover {
  transform: scale(1.05);
}

.preset-label.selected {
  opacity: 0.7;
  transform: scale(0.95);
}
</style>