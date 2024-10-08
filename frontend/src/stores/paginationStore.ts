import { defineStore } from 'pinia'
import type { PageInfo } from '@/frontend-ts-axios-package/model'

export const usePaginationStore = defineStore('pagination', {
  state: () => ({
    pageInfo: null as PageInfo | null,
  }),
  actions: {
    setPageInfo(pageInfo: PageInfo) {
      this.pageInfo = pageInfo
    },
  },
})