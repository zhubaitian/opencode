# AGENTS.md - Trello Clone Project

This document provides guidelines for AI agents working on this Vue 3 + TypeScript Trello clone project.

## Project Overview

- **Framework**: Vue 3 with Composition API and `<script setup>` syntax
- **Language**: TypeScript
- **UI Library**: Vant (Mobile-first UI components)
- **State Management**: Pinia
- **Routing**: Vue Router
- **Drag & Drop**: vuedraggable + SortableJS
- **Styling**: Less CSS with scoped styles
- **Build Tool**: Vite

## Build & Development Commands

### Development
```bash
npm run dev          # Start development server
```

### Build & Production
```bash
npm run build        # Build for production
npm run preview      # Preview production build
```

### Code Quality
```bash
npm run lint         # Run ESLint with auto-fix
npm run type-check   # Run TypeScript type checking (no emit)
```

### Single File Operations
To run ESLint on a specific file:
```bash
npx eslint src/path/to/file.vue --fix
```

To check types for a specific file:
```bash
npx vue-tsc --noEmit src/path/to/file.vue
```

## Code Style Guidelines

### File Structure
- **Components**: `src/components/` - Reusable Vue components
- **Views**: `src/views/` - Page-level components
- **Stores**: `src/stores/` - Pinia stores
- **Types**: `src/types/` - TypeScript type definitions
- **Utils**: `src/utils/` - Utility functions
- **Styles**: `src/styles/` - Global styles and variables
- **Router**: `src/router/` - Vue Router configuration

### Vue Component Structure
Follow this order in `.vue` files:
1. `<template>` section
2. `<script setup lang="ts">` section
3. `<style scoped>` section

Example:
```vue
<template>
  <div class="component-name">
    <!-- Template content -->
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { SomeType } from '@/types'

// Props and emits first
interface Props {
  propName: string
}

interface Emits {
  (e: 'eventName', value: string): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Reactive state
const localState = ref('')

// Computed properties
const computedValue = computed(() => {
  return props.propName + localState.value
})

// Functions
function handleAction() {
  emit('eventName', 'value')
}
</script>

<style scoped>
.component-name {
  /* Scoped styles */
}
</style>
```

### TypeScript Guidelines

#### Imports Order
1. Vue and framework imports
2. Third-party library imports
3. Local utility/type imports
4. Component imports

Example:
```typescript
import { ref, computed } from 'vue'
import { useBoardStore } from '@/stores/board'
import type { Card, List } from '@/types'
import CardItem from '@/components/CardItem.vue'
```

#### Type Definitions
- Use TypeScript interfaces for object types
- Define props and emits interfaces within components
- Import types from `@/types` when available
- Use `type` keyword for type-only imports

#### Naming Conventions
- **Components**: PascalCase (e.g., `ListColumn.vue`)
- **Variables/Functions**: camelCase
- **Constants**: UPPER_SNAKE_CASE for true constants
- **Types/Interfaces**: PascalCase
- **Pinia Stores**: camelCase with `use` prefix (e.g., `useBoardStore`)
- **CSS Classes**: kebab-case

### Pinia Store Patterns
- Use `defineStore()` with Composition API syntax
- Define reactive state with `ref()`
- Use `computed()` for derived state
- Export store functions that modify state
- Include proper TypeScript types for all store members

Example store pattern:
```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { SomeType } from '@/types'

export const useStoreName = defineStore('storeName', () => {
  const state = ref<SomeType>(initialValue)
  
  const computedState = computed(() => {
    // Compute derived state
  })
  
  function actionName(param: string) {
    // Modify state
  }
  
  return { state, computedState, actionName }
})
```

### Error Handling
- Use `try/catch` for operations that can fail (localStorage, API calls)
- Log warnings with `console.warn()` for non-critical errors
- Use TypeScript's strict mode for compile-time error checking
- Validate user input before processing

### Styling Guidelines
- Use scoped styles (`<style scoped>`) for component-specific styles
- Use CSS custom properties (variables) from `src/styles/variables.less`
- Follow BEM-like naming for complex components
- Use Vant's design tokens and spacing when possible
- Mobile-first responsive design approach

### Component Communication
- Use props for parent-to-child data flow
- Use emits for child-to-parent communication
- Use Pinia stores for global/shared state
- Avoid prop drilling - use stores instead

### Drag & Drop Implementation
- Use `vuedraggable` component for drag functionality
- Implement proper event handling for drag end
- Update positions in both source and target lists
- Maintain consistent position indexing

### File Path Aliases
- Use `@/` alias for `src/` directory imports
- Example: `import CardItem from '@/components/CardItem.vue'`

## Testing Notes
- No test framework currently configured
- Manual testing via development server recommended
- Check console for errors during development
- Verify TypeScript compilation passes

## Git Guidelines
- Commit messages should be in English
- Use descriptive commit messages explaining "why" not just "what"
- Keep commits focused on single logical changes

## Common Patterns Observed

### Component Props & Emits
Define explicit interfaces for props and emits:
```typescript
interface Props {
  list: List
}

interface Emits {
  (e: 'addCard', listId: string, cardData: Omit<Card, 'id' | 'position'>): void
  (e: 'deleteCard', listId: string, cardId: string): void
}
```

### Reactive State Management
Use `ref()` for local component state:
```typescript
const showAddCard = ref(false)
const newCardTitle = ref('')
```

### Event Handlers
Use descriptive function names for event handlers:
```typescript
const handleCreateCard = () => {
  if (newCardTitle.value.trim()) {
    emit('addCard', props.list.id, {
      title: newCardTitle.value.trim()
    })
    newCardTitle.value = ''
    showAddCard.value = false
  }
}
```

### Watch Usage
Use `watch()` for reacting to prop changes:
```typescript
watch(() => props.list.cards, (newCards) => {
  localCards.value = [...newCards]
}, { deep: true })
```

## Project-Specific Notes
- This is a Trello-like kanban board application
- Data persistence via localStorage
- Mobile-optimized UI using Vant components
- Chinese language UI text observed in components
- No backend API - all data stored locally