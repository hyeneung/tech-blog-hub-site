import { Configuration } from '@/frontend-ts-axios-package'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api/v1'

export const apiConfig = new Configuration({
  basePath: API_BASE_URL,
})

export const getApiConfig = () => apiConfig