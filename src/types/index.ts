export interface Card {
  id: string
  title: string
  description?: string
  labels?: Label[]
  dueDate?: string
  members?: string[]
  position: number
}

export interface Label {
  id: string
  name: string
  color: string
}

export interface List {
  id: string
  title: string
  cards: Card[]
  position: number
}

export interface Board {
  id: string
  title: string
  lists: List[]
}