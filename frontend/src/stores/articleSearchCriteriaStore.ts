import { defineStore } from 'pinia'

export const useArticleSearchCriteriaStore = defineStore('articleSearchCriteria', {
  state: () => ({
    hashtags: [] as string[],
    company: '',
    query: '',
    page: 0,
    size: 10,
  }),
  actions: {
    setHashtags(hashtags: string[]){
        this.hashtags = hashtags
        this.saveToLocalStorage()
    },
    setCompany(company: string){
        this.company = company
        this.saveToLocalStorage()
    },
    setQuery(query: string) {
        this.query = query
        this.saveToLocalStorage()
    },
    setPage(page: number){
        this.page = page
        this.saveToLocalStorage()
    },
    saveToLocalStorage(expiryMinutes = 30) {
      const now = new Date();
      const item = {
        value: {
          hashtags: this.hashtags,
          company: this.company,
          query: this.query,
          page: this.page,
          size: this.size,
        },
        expiry: now.getTime() + (expiryMinutes * 60 * 1000),
      };
      localStorage.setItem('articleSearchCriteria', JSON.stringify(item));
    },
    loadFromLocalStorage() {
      const savedCriteria = localStorage.getItem('articleSearchCriteria')
      if (savedCriteria) {
        const parsed = JSON.parse(savedCriteria);
        const now = new Date().getTime();
        
        if (parsed.expiry && parsed.expiry > now) {
          this.hashtags = parsed.value.hashtags;
          this.company = parsed.value.company;
          this.query = parsed.value.query;
          this.page = parsed.value.page;
          this.size = parsed.value.size;
        } else {
          this.resetCriteria();
          localStorage.removeItem('articleSearchCriteria');
        }
      } else{
        this.resetCriteria()
      }
    },
    resetCriteria() {
        this.hashtags = []
        this.company = ''
        this.query = ''
        this.page = 0
        this.size = 10
    },
  },
  getters: {
    currentCriteria(): object {
      return {
        hashtags: this.hashtags,
        company: this.company,
        query: this.query,
        page: this.page,
        size: this.size
      }
    }
  }
})