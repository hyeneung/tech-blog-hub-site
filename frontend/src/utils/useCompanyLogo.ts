import { ref, Ref } from 'vue'
import { companies } from '@/data/companies'

interface LogoCache {
  [key: string]: Ref<string | null>
}

const logoCache: LogoCache = {}

export function useCompanyLogo(companyName: string) {
  if (!logoCache[companyName]) {
    logoCache[companyName] = ref<string | null>(null)
    loadLogo(companyName)
  }
  return logoCache[companyName]
}

async function loadLogo(companyName: string) {
  const company = companies.find(c => c.name === companyName)
  if (company && company.logo) {
    try {
      const module = await company.logo()
      logoCache[companyName].value = module.default
    } catch (error) {
      console.error(`Error loading logo for ${companyName}:`, error)
      logoCache[companyName].value = null
    }
  } else {
    logoCache[companyName].value = null
  }
}