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
    },
    setCompany(company: string){
        this.company = company
    },
    setQuery(query: string) {
        this.query = query
    },
    setPage(page: number){
        this.page = page
    },
    // Move to post page
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
    // Come back from post page(to maintain search criteria)
    loadFromLocalStorage() {
      const savedCriteria = localStorage.getItem('articleSearchCriteria')
      if (savedCriteria) {
        const { value, expiry } = JSON.parse(savedCriteria);
        if (expiry && expiry > Date.now()) {
          // If the saved search criteria is valid, update the state.
          // This will trigger the watch function in PostList to load the data.
          this.$patch(value);
          return;
        }
      }
      // If there are no saved criteria or they have expired, reset to default values.
      // This change will trigger the watch function in PostList to load new data.
      this.resetCriteriaAndLoad();
    },
    // Click home button
    resetCriteriaAndLoad() {
      this.$patch({
        hashtags: [],
        company: '',
        query: '',
        page: 0,
        size: 10
      });
      this.saveToLocalStorage();
    },
    // Click search button
    resetCriteriaExceptQuery(query : string){
      // Reset all criteria except for the query parameter.
      this.$patch({
        hashtags: [],
        company: '',
        query: query,
        page: 0,
        size: 10
      });
    }
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