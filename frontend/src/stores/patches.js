import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePatchStore = defineStore('patches', () => {
  // Store for patched vulnerabilities
  const patchedVulnerabilities = ref([])

  // Add a patched vulnerability
  const addPatchedVulnerability = (vulnerability) => {
    const patchedVuln = {
      ...vulnerability,
      patchedAt: new Date().toISOString(),
      patchStatus: 'applied',
      patchVersion: vulnerability.patch.version,
      patchDescription: vulnerability.patch.description
    }
    
    patchedVulnerabilities.value.unshift(patchedVuln)
    
    // Keep only last 50 patches
    if (patchedVulnerabilities.value.length > 50) {
      patchedVulnerabilities.value = patchedVulnerabilities.value.slice(0, 50)
    }
  }

  // Get all patched vulnerabilities
  const getPatchedVulnerabilities = () => {
    return patchedVulnerabilities.value
  }

  // Get patch count
  const getPatchCount = () => {
    return patchedVulnerabilities.value.length
  }

  return {
    patchedVulnerabilities,
    addPatchedVulnerability,
    getPatchedVulnerabilities,
    getPatchCount
  }
})
