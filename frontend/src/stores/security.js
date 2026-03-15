import { defineStore } from 'pinia'

export const useSecurityStore = defineStore('security', {
  state: () => ({
    // Scan state
    currentScan: null,
    scanHistory: [],
    isScanning: false,
    
    // Available workflows
    workflows: [],
    
    // Agent status
    agentStatus: null,
    
    // Statistics
    statistics: null,
    
    // Errors
    error: null
  }),
  
  actions: {
    /**
     * Fetch available scan workflows
     */
    async fetchWorkflows() {
      try {
        const response = await fetch('http://localhost:8000/api/security/workflows')
        if (!response.ok) throw new Error('Failed to fetch workflows')
        
        const data = await response.json()
        this.workflows = data.workflows
      } catch (error) {
        console.error('Error fetching workflows:', error)
        this.error = error.message
      }
    },
    
    /**
     * Start a security scan
     * @param {string} workflow - Workflow ID (e.g., 'full_scan', 'quick_scan')
     * @param {string} target - Target domain/IP
     * @param {object} options - Additional scan options
     */
    async startScan(workflow, target, options = null) {
      this.isScanning = true
      this.error = null
      
      try {
        const response = await fetch('http://localhost:8000/api/security/scan', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            workflow,
            target,
            options
          })
        })
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Scan failed to start')
        }
        
        const result = await response.json()
        
        this.currentScan = {
          scan_id: result.scan_id,
          workflow,
          target,
          status: result.status,
          started_at: new Date().toISOString()
        }
        
        // Add to history
        this.scanHistory.unshift(this.currentScan)
        
        return result
      } catch (error) {
        console.error('Error starting scan:', error)
        this.error = error.message
        throw error
      } finally {
        this.isScanning = false
      }
    },
    
    /**
     * Get agent status
     */
    async fetchAgentStatus() {
      try {
        const response = await fetch('http://localhost:8000/api/security/agents/status')
        if (!response.ok) {
          console.warn('Agent status endpoint not available')
          // Set default empty status instead of throwing error
          this.agentStatus = {
            offensive_agents: {},
            defensive_agents: {},
            core_agents: {},
            summary: {
              total_agents: 0,
              offensive: 0,
              defensive: 0,
              core: 0
            }
          }
          return
        }
        
        this.agentStatus = await response.json()
      } catch (error) {
        console.warn('Could not fetch agent status:', error.message)
        // Set default empty status on error
        this.agentStatus = {
          offensive_agents: {},
          defensive_agents: {},
          core_agents: {},
          summary: {
            total_agents: 0,
            offensive: 0,
            defensive: 0,
            core: 0
          }
        }
        // Don't set this.error to avoid showing error to user
      }
    },
    
    /**
     * Get statistics
     */
    async fetchStatistics() {
      try {
        const response = await fetch('http://localhost:8000/api/security/statistics')
        if (!response.ok) throw new Error('Failed to fetch statistics')
        
        this.statistics = await response.json()
      } catch (error) {
        console.error('Error fetching statistics:', error)
        this.error = error.message
      }
    },
    
    /**
     * Get execution history
     */
    async fetchHistory(agentType = null, limit = 50) {
      try {
        const params = new URLSearchParams()
        if (agentType) params.append('agent_type', agentType)
        params.append('limit', limit)
        
        const response = await fetch(`http://localhost:8000/api/security/history?${params}`)
        if (!response.ok) throw new Error('Failed to fetch history')
        
        this.scanHistory = await response.json()
      } catch (error) {
        console.error('Error fetching history:', error)
        this.error = error.message
      }
    }
  },
  
  getters: {
    /**
     * Get workflow by ID
     */
    getWorkflowById: (state) => (id) => {
      return state.workflows.find(w => w.id === id)
    },
    
    /**
     * Check if any scan is running
     */
    hasActiveScan: (state) => {
      return state.isScanning || (state.currentScan && state.currentScan.status === 'started')
    }
  }
})
