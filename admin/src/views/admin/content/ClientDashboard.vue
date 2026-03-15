<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useAdminDataStore } from '@/stores/adminData'
import { useRoute } from 'vue-router'

const dataStore = useAdminDataStore()
const route = useRoute()
const isLoading = ref(true)
const activeSection = ref('overview')
const isSaving = ref(false)
const saveMessage = ref('')

const sections = [
  { key: 'overview', name: 'Overview Page', icon: 'cil-dashboard' },
  { key: 'attack-insights', name: 'Attack Insights', icon: 'cil-warning' },
  { key: 'defense-metrics', name: 'Defense Metrics', icon: 'cil-shield-alt' },
  { key: 'system-health', name: 'System Health', icon: 'cil-heart' },
  { key: 'activity-logs', name: 'Activity Logs', icon: 'cil-list' },
  { key: 'settings', name: 'Settings', icon: 'cil-settings' },
]

const content = computed(() => dataStore.content)

// Map section keys to content keys
const getSectionContentKey = (section) => {
  const keyMap = {
    'overview': 'clientDashboard_overview',
    'attack-insights': 'clientDashboard_attackInsights',
    'defense-metrics': 'clientDashboard_defenseMetrics',
    'system-health': 'clientDashboard_systemHealth',
    'activity-logs': 'clientDashboard_activityLogs',
    'settings': 'clientDashboard_settings'
  }
  return keyMap[section] || `clientDashboard_${section}`
}

const currentContent = computed(() => {
  const key = getSectionContentKey(activeSection.value)
  return content.value[key]?.content || {}
})


onMounted(async () => {
  await dataStore.fetchContent()
  
  // Check if there's a section query parameter
  if (route.query.section) {
    const sectionKey = route.query.section
    if (sections.find(s => s.key === sectionKey)) {
      activeSection.value = sectionKey
    }
  }
  
  isLoading.value = false
})

// Watch for query parameter changes
watch(() => route.query.section, (newSection) => {
  if (newSection && sections.find(s => s.key === newSection)) {
    activeSection.value = newSection
  }
})

async function saveContent() {
  isSaving.value = true
  saveMessage.value = ''
  const result = await dataStore.updateContent(`clientDashboard_${activeSection.value}`, currentContent.value)
  if (result.success) {
    saveMessage.value = 'Content saved successfully!'
    setTimeout(() => saveMessage.value = '', 3000)
  } else {
    saveMessage.value = `Error: ${result.error}`
  }
  isSaving.value = false
}

function initializeOverview() {
  if (!content.value.clientDashboard_overview) {
    content.value.clientDashboard_overview = { content: {} }
  }
  content.value.clientDashboard_overview.content = {
    pageTitle: 'Security Overview',
    pageDescription: 'Real-time security monitoring and threat analysis',
    stats: [
      { label: 'Total Events', icon: 'shield', value: 100 },
      { label: 'Events (24h)', icon: 'clock', value: 0, change: '-38.89%' },
      { label: 'Blocked Attacks', icon: 'warning', value: 0 },
      { label: 'System Uptime', icon: 'check', value: '99.87%' }
    ],
    charts: {
      threatActivity: {
        title: 'Threat Activity (Last 7 Days)',
        enabled: true
      },
      attackTypes: {
        title: 'Attack Types Distribution',
        enabled: true
      }
    }
  }
}
</script>

<template>
  <div>
    <CCard class="mb-4">
      <CCardHeader class="d-flex justify-content-between align-items-center">
        <strong>Client Dashboard Management</strong>
        <CButton color="primary" @click="saveContent" :disabled="isSaving">
          <CSpinner v-if="isSaving" size="sm" class="me-2" />{{ isSaving ? 'Saving...' : 'Save Changes' }}
        </CButton>
      </CCardHeader>
      <CCardBody>
        <CAlert v-if="saveMessage" :color="saveMessage.includes('Error') ? 'danger' : 'success'">{{ saveMessage }}</CAlert>
        <div v-if="isLoading" class="text-center py-5"><CSpinner color="primary" /></div>
        <div v-else>
          <CCard>
            <CCardHeader><strong>{{ sections.find(s => s.key === activeSection)?.name }}</strong></CCardHeader>
            <CCardBody>
              <!-- Overview Section -->
              <template v-if="activeSection === 'overview'">
                <div v-if="!currentContent.pageTitle">
                  <CButton color="primary" @click="initializeOverview">Initialize Overview Content</CButton>
                </div>
                <div v-else>
                  <div class="mb-3">
                    <CFormLabel>Page Title</CFormLabel>
                    <CFormInput v-model="currentContent.pageTitle" placeholder="Security Overview" />
                  </div>
                  <div class="mb-3">
                    <CFormLabel>Page Description</CFormLabel>
                    <CFormTextarea v-model="currentContent.pageDescription" rows="2" placeholder="Real-time security monitoring..." />
                  </div>
                  
                  <hr class="my-4" />
                  
                  <h5 class="mb-3">Statistics Cards</h5>
                  <div v-for="(stat, index) in currentContent.stats" :key="index" class="border rounded p-3 mb-3">
                    <CRow>
                      <CCol :md="4">
                        <CFormLabel>Label</CFormLabel>
                        <CFormInput v-model="stat.label" placeholder="Total Events" />
                      </CCol>
                      <CCol :md="4">
                        <CFormLabel>Icon</CFormLabel>
                        <CFormInput v-model="stat.icon" placeholder="shield" />
                      </CCol>
                      <CCol :md="4">
                        <CFormLabel>Default Value</CFormLabel>
                        <CFormInput v-model="stat.value" placeholder="100" />
                      </CCol>
                    </CRow>
                  </div>
                  
                  <hr class="my-4" />
                  
                  <h5 class="mb-3">Charts Configuration</h5>
                  <div class="mb-3">
                    <CFormCheck 
                      v-model="currentContent.charts.threatActivity.enabled" 
                      label="Enable Threat Activity Chart"
                    />
                    <CFormInput 
                      v-model="currentContent.charts.threatActivity.title" 
                      placeholder="Threat Activity (Last 7 Days)" 
                      class="mt-2"
                    />
                  </div>
                  <div class="mb-3">
                    <CFormCheck 
                      v-model="currentContent.charts.attackTypes.enabled" 
                      label="Enable Attack Types Chart"
                    />
                    <CFormInput 
                      v-model="currentContent.charts.attackTypes.title" 
                      placeholder="Attack Types Distribution" 
                      class="mt-2"
                    />
                  </div>
                </div>
              </template>

              <!-- Attack Insights Section -->
              <template v-else-if="activeSection === 'attack-insights'">
                <div class="mb-3">
                  <CFormLabel>Page Title</CFormLabel>
                  <CFormInput v-model="currentContent.title" placeholder="Attack Insights" />
                </div>
                <div class="mb-3">
                  <CFormLabel>Description</CFormLabel>
                  <CFormTextarea v-model="currentContent.description" rows="3" placeholder="Detailed analysis of attack patterns..." />
                </div>
                <div class="mb-3">
                  <CFormCheck 
                    v-model="currentContent.showRealTimeAlerts" 
                    label="Show Real-time Alerts"
                  />
                </div>
              </template>

              <!-- Defense Metrics Section -->
              <template v-else-if="activeSection === 'defense-metrics'">
                <div class="mb-3">
                  <CFormLabel>Page Title</CFormLabel>
                  <CFormInput v-model="currentContent.title" placeholder="Defense Metrics" />
                </div>
                <div class="mb-3">
                  <CFormLabel>Description</CFormLabel>
                  <CFormTextarea v-model="currentContent.description" rows="3" placeholder="Monitor your defense effectiveness..." />
                </div>
              </template>

              <!-- System Health Section -->
              <template v-else-if="activeSection === 'system-health'">
                <div class="mb-3">
                  <CFormLabel>Page Title</CFormLabel>
                  <CFormInput v-model="currentContent.title" placeholder="System Health" />
                </div>
                <div class="mb-3">
                  <CFormLabel>Description</CFormLabel>
                  <CFormTextarea v-model="currentContent.description" rows="3" placeholder="Monitor system performance and health..." />
                </div>
              </template>

              <!-- Activity Logs Section -->
              <template v-else-if="activeSection === 'activity-logs'">
                <div class="mb-3">
                  <CFormLabel>Page Title</CFormLabel>
                  <CFormInput v-model="currentContent.title" placeholder="Activity Logs" />
                </div>
                <div class="mb-3">
                  <CFormLabel>Log Retention (days)</CFormLabel>
                  <CFormInput v-model.number="currentContent.retentionDays" type="number" placeholder="30" />
                </div>
              </template>

              <!-- Settings Section -->
              <template v-else-if="activeSection === 'settings'">
                <div class="mb-3">
                  <CFormLabel>Page Title</CFormLabel>
                  <CFormInput v-model="currentContent.title" placeholder="Dashboard Settings" />
                </div>
                <div class="mb-3">
                  <CFormCheck 
                    v-model="currentContent.allowCustomization" 
                    label="Allow User Customization"
                  />
                </div>
                <div class="mb-3">
                  <CFormCheck 
                    v-model="currentContent.enableNotifications" 
                    label="Enable Notifications"
                  />
                </div>
              </template>

              <template v-else>
                <CAlert color="info">Select a section from the sidebar dropdown to edit.</CAlert>
              </template>
            </CCardBody>
          </CCard>
        </div>
      </CCardBody>
    </CCard>
  </div>
</template>
