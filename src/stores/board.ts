import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import type { Board, List, Card } from '@/types'

const STORAGE_KEY = 'trello-clone-board'

// 默认看板数据
const defaultBoard: Board = {
  id: '1',
  title: '我的看板',
  lists: [
    {
      id: '1',
      title: '待办',
      cards: [
        {
          id: '1',
          title: '设计看板界面',
          description: '创建一个美观的看板界面',
          position: 0
        },
        {
          id: '2',
          title: '实现拖拽功能',
          description: '添加卡片拖拽功能',
          position: 1
        }
      ],
      position: 0
    },
    {
      id: '2',
      title: '进行中',
      cards: [
        {
          id: '3',
          title: '开发Vue组件',
          description: '使用Vue3和Vant开发组件',
          position: 0
        }
      ],
      position: 1
    },
    {
      id: '3',
      title: '已完成',
      cards: [
        {
          id: '4',
          title: '项目初始化',
          description: '完成项目基础设置',
          position: 0
        }
      ],
      position: 2
    }
  ]
}

// 从localStorage加载数据
const loadBoard = (): Board => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      return JSON.parse(stored)
    }
  } catch (error) {
    console.warn('Failed to load board from localStorage:', error)
  }
  return defaultBoard
}

export const useBoardStore = defineStore('board', () => {
  // 看板数据
  const board = ref<Board>(loadBoard())

  // 计算属性
  const lists = computed(() => board.value.lists.sort((a, b) => a.position - b.position))

  // 添加列表
  const addList = (title: string) => {
    const newList: List = {
      id: Date.now().toString(),
      title,
      cards: [],
      position: board.value.lists.length
    }
    board.value.lists.push(newList)
  }

  // 添加卡片
  const addCard = (listId: string, card: Omit<Card, 'id' | 'position'>) => {
    const list = board.value.lists.find(l => l.id === listId)
    if (list) {
      const newCard: Card = {
        ...card,
        id: Date.now().toString(),
        position: list.cards.length
      }
      list.cards.push(newCard)
    }
  }

  // 移动卡片
  const moveCard = (cardId: string, fromListId: string, toListId: string, newPosition: number) => {
    const fromList = board.value.lists.find(l => l.id === fromListId)
    const toList = board.value.lists.find(l => l.id === toListId)
    
    if (fromList && toList) {
      const cardIndex = fromList.cards.findIndex(c => c.id === cardId)
      if (cardIndex !== -1) {
        const [card] = fromList.cards.splice(cardIndex, 1)
        
        // 重新排序剩余卡片
        fromList.cards.forEach((c, index) => {
          c.position = index
        })
        
        // 插入到新位置
        toList.cards.splice(newPosition, 0, card)
        
        // 重新排序目标列表卡片
        toList.cards.forEach((c, index) => {
          c.position = index
        })
      }
    }
  }

  // 删除卡片
  const deleteCard = (listId: string, cardId: string) => {
    const list = board.value.lists.find(l => l.id === listId)
    if (list) {
      const cardIndex = list.cards.findIndex(c => c.id === cardId)
      if (cardIndex !== -1) {
        list.cards.splice(cardIndex, 1)
        // 重新排序
        list.cards.forEach((c, index) => {
          c.position = index
        })
      }
    }
  }

  // 更新卡片
  const updateCard = (listId: string, cardId: string, updates: Partial<Card>) => {
    const list = board.value.lists.find(l => l.id === listId)
    if (list) {
      const card = list.cards.find(c => c.id === cardId)
      if (card) {
        Object.assign(card, updates)
      }
    }
  }

  // 更新列表
  const updateList = (listId: string, updates: Partial<List>) => {
    const list = board.value.lists.find(l => l.id === listId)
    if (list) {
      Object.assign(list, updates)
    }
  }

  // 删除列表
  const deleteList = (listId: string) => {
    const index = board.value.lists.findIndex(l => l.id === listId)
    if (index !== -1) {
      board.value.lists.splice(index, 1)
      // 重新排序
      board.value.lists.forEach((list, index) => {
        list.position = index
      })
    }
  }

  // 移动列表
  const moveList = (fromIndex: number, toIndex: number) => {
    const [movedList] = board.value.lists.splice(fromIndex, 1)
    board.value.lists.splice(toIndex, 0, movedList)
    
    // 重新排序
    board.value.lists.forEach((list, index) => {
      list.position = index
    })
  }

  // 保存到localStorage
  const saveToStorage = () => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(board.value))
    } catch (error) {
      console.warn('Failed to save board to localStorage:', error)
    }
  }

  // 清除数据
  const clearBoard = () => {
    board.value = { ...defaultBoard }
    saveToStorage()
  }

  // 监听数据变化并自动保存
  watch(board, saveToStorage, { deep: true })

  return {
    board,
    lists,
    addList,
    addCard,
    moveCard,
    deleteCard,
    updateCard,
    updateList,
    deleteList,
    moveList,
    clearBoard,
    saveToStorage
  }
})