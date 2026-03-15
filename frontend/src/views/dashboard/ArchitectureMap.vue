<template>
  <div class="architecture-map-page">
    <!-- Header -->
    <div class="page-header">
      <div>
        <h1>Architecture Maps</h1>
        <p class="subtitle">
          Visualize discovered infrastructure and software architecture
        </p>
      </div>
      <div class="header-actions">
        <button @click="refreshData" class="btn-secondary" :disabled="loading">
          <ArrowPathIcon class="icon-xs" :class="{ 'animate-spin': loading }" />
          Refresh
        </button>
        <button @click="showScanSelector = true" class="btn-primary">
          <MagnifyingGlassIcon class="icon-xs" />
          Select Scan
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && !selectedScan" class="loading-container">
      <div class="loading-spinner-large"></div>
      <p>Loading architecture data...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="!selectedScan" class="empty-state">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="empty-icon"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"
        />
      </svg>
      <h2>No Scan Selected</h2>
      <p>Select a scan to view the discovered architecture map</p>
      <button @click="showScanSelector = true" class="btn-primary">
        Select a Scan
      </button>
    </div>

    <!-- Main Content -->
    <div v-else class="architecture-content">
      <!-- Scan Info Card -->
      <div class="scan-info-card">
        <div class="scan-info-content">
          <div>
            <h3>{{ selectedScan.target }}</h3>
            <p class="scan-meta">
              Scanned on {{ formatDate(selectedScan.createdAt) }} •
              {{ selectedScan.agentsExecuted?.length || 0 }} agents •
              {{ totalComponents }} components discovered
            </p>
          </div>
          <div class="scan-stats">
            <div class="stat-item">
              <span class="stat-value">{{ totalComponents }}</span>
              <span class="stat-label">Components</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ totalConnections }}</span>
              <span class="stat-label">Connections</span>
            </div>
            <div class="stat-item">
              <span
                class="stat-value"
                :class="vulnerableComponents > 0 ? 'text-red' : 'text-green'"
              >
                {{ vulnerableComponents }}
              </span>
              <span class="stat-label">Vulnerable</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Architecture Diagram -->
      <ArchitectureDiagram
        :title="architectureTitle"
        :subtitle="architectureSubtitle"
        :architecture-data="architectureData"
        @node-selected="handleNodeSelected"
        @download="handleDownload"
      />

      <!-- Components List -->
      <div class="components-section">
        <h2>Discovered Components</h2>
        <div class="components-grid">
          <div
            v-for="component in componentsList"
            :key="component.id"
            class="component-card"
            :class="{ 'has-vulnerabilities': component.vulnerabilities > 0 }"
            @click="selectComponent(component)"
          >
            <div class="component-header">
              <div class="component-icon" :class="`icon-${component.type}`">
                <component
                  :is="getComponentIcon(component.type)"
                  class="icon-md"
                />
              </div>
              <div class="component-info">
                <h4>{{ component.name }}</h4>
                <p>{{ component.technology }} {{ component.version }}</p>
              </div>
              <div v-if="component.vulnerabilities > 0" class="vuln-badge">
                {{ component.vulnerabilities }}
              </div>
            </div>
            <div class="component-details">
              <div class="detail-item">
                <span class="label">Type:</span>
                <span class="value">{{ component.type }}</span>
              </div>
              <div v-if="component.port" class="detail-item">
                <span class="label">Port:</span>
                <span class="value">{{ component.port }}</span>
              </div>
              <div v-if="component.description" class="detail-item full-width">
                <span class="label">Description:</span>
                <span class="value">{{ component.description }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Network Connections -->
      <div class="connections-section">
        <h2>Network Connections</h2>
        <div class="connections-list">
          <div
            v-for="(connection, index) in connectionsList"
            :key="`conn-${index}`"
            class="connection-item"
            :class="{ vulnerable: connection.vulnerable }"
          >
            <div class="connection-flow">
              <div class="connection-node from">
                <component
                  :is="getComponentIcon(connection.fromType)"
                  class="icon-xs"
                />
                <span>{{ connection.fromName }}</span>
              </div>
              <div class="connection-arrow">
                <ArrowLongRightIcon class="icon-md" />
                <div class="connection-protocol">
                  {{ connection.protocol || "HTTP" }}
                  {{ connection.port ? `:${connection.port}` : "" }}
                </div>
              </div>
              <div class="connection-node to">
                <span>{{ connection.toName }}</span>
                <component
                  :is="getComponentIcon(connection.toType)"
                  class="icon-xs"
                />
              </div>
            </div>
            <div v-if="connection.vulnerable" class="connection-warning">
              <ExclamationTriangleIcon class="icon-xs" />
              <span>Vulnerable connection detected</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Scan Selector Modal -->
    <div
      v-if="showScanSelector"
      class="modal-overlay"
      @click="showScanSelector = false"
    >
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Select a Scan</h3>
          <button @click="showScanSelector = false" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="scans-list">
            <div
              v-for="scan in availableScans"
              :key="scan.executionId"
              class="scan-item"
              :class="{
                active: selectedScan?.executionId === scan.executionId,
              }"
              @click="selectScan(scan)"
            >
              <div class="scan-item-content">
                <h4>{{ scan.target }}</h4>
                <p class="scan-date">{{ formatDate(scan.createdAt) }}</p>
                <div class="scan-badges">
                  <span class="badge"
                    >{{ scan.agentsExecuted?.length || 0 }} agents</span
                  >
                  <span class="badge status" :class="scan.status">{{
                    scan.status
                  }}</span>
                </div>
              </div>
              <div class="scan-arrow">
                <ChevronRightIcon class="icon-sm" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Component Details Modal -->
    <div
      v-if="selectedComponent"
      class="modal-overlay"
      @click="selectedComponent = null"
    >
      <div class="modal-content large" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedComponent.name }}</h3>
          <button @click="selectedComponent = null" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <div class="component-full-details">
            <div class="details-grid">
              <div class="detail-row">
                <span class="label">Type:</span>
                <span class="value">{{ selectedComponent.type }}</span>
              </div>
              <div class="detail-row">
                <span class="label">Technology:</span>
                <span class="value">{{ selectedComponent.technology }}</span>
              </div>
              <div v-if="selectedComponent.version" class="detail-row">
                <span class="label">Version:</span>
                <span class="value">{{ selectedComponent.version }}</span>
              </div>
              <div v-if="selectedComponent.port" class="detail-row">
                <span class="label">Port:</span>
                <span class="value">{{ selectedComponent.port }}</span>
              </div>
            </div>

            <div
              v-if="selectedComponent.description"
              class="description-section"
            >
              <h4>Description</h4>
              <p>{{ selectedComponent.description }}</p>
            </div>

            <div
              v-if="selectedComponent.vulnerabilities > 0"
              class="vulnerabilities-section"
            >
              <h4>
                Vulnerabilities ({{
                  selectedComponent.vulnerabilityDetails?.length || 0
                }})
              </h4>
              <div class="vulnerability-list">
                <div
                  v-for="vuln in selectedComponent.vulnerabilityDetails"
                  :key="vuln.id"
                  class="vulnerability-item"
                >
                  <span :class="`severity-badge ${vuln.severity}`">{{
                    vuln.severity
                  }}</span>
                  <div class="vuln-info">
                    <p class="vuln-title">{{ vuln.title }}</p>
                    <p v-if="vuln.description" class="vuln-desc">
                      {{ vuln.description }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useSecurityStore } from "@/stores/security";
import ArchitectureDiagram from "@/components/ArchitectureDiagram.vue";
import {
  ArrowPathIcon,
  MagnifyingGlassIcon,
  ServerIcon,
  CircleStackIcon,
  CloudIcon,
  CpuChipIcon,
  GlobeAltIcon,
  ChevronRightIcon,
  ArrowLongRightIcon,
  ExclamationTriangleIcon,
} from "@heroicons/vue/24/outline";

const securityStore = useSecurityStore();

// State
const loading = ref(false);
const selectedScan = ref(null);
const showScanSelector = ref(false);
const selectedComponent = ref(null);
const availableScans = ref([]);

// Mock data for demonstration
const mockArchitectureData = ref({
  nodes: [],
  connections: [],
});

// Computed
const architectureTitle = computed(() => {
  return selectedScan.value
    ? `Architecture Map: ${selectedScan.value.target}`
    : "Software Architecture Map";
});

const architectureSubtitle = computed(() => {
  return selectedScan.value
    ? `Discovered on ${formatDate(selectedScan.value.createdAt)}`
    : "Interactive visualization of discovered infrastructure";
});

const architectureData = computed(() => {
  return mockArchitectureData.value;
});

const componentsList = computed(() => {
  return architectureData.value.nodes || [];
});

const connectionsList = computed(() => {
  const connections = architectureData.value.connections || [];
  const nodeMap = {};

  componentsList.value.forEach((node) => {
    nodeMap[node.id] = node;
  });

  return connections.map((conn) => {
    const fromNode = nodeMap[conn.from];
    const toNode = nodeMap[conn.to];

    return {
      ...conn,
      fromName: fromNode?.name || conn.from,
      toName: toNode?.name || conn.to,
      fromType: fromNode?.type || "web-service",
      toType: toNode?.type || "web-service",
    };
  });
});

const totalComponents = computed(() => componentsList.value.length);

const totalConnections = computed(() => connectionsList.value.length);

const vulnerableComponents = computed(() => {
  return componentsList.value.filter((c) => c.vulnerabilities > 0).length;
});

// Methods
function formatDate(dateString) {
  if (!dateString) return "N/A";
  const date = new Date(dateString);
  return date.toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function getComponentIcon(type) {
  const icons = {
    "web-service": ServerIcon,
    database: CircleStackIcon,
    api: CpuChipIcon,
    external: CloudIcon,
    infrastructure: GlobeAltIcon,
  };
  return icons[type] || ServerIcon;
}

async function refreshData() {
  if (!selectedScan.value) return;

  loading.value = true;
  try {
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // In real implementation, fetch from backend
    // const response = await fetch(`/api/architecture/${selectedScan.value.executionId}`);
    // const data = await response.json();
    // mockArchitectureData.value = data;
  } catch (error) {
    console.error("Failed to refresh architecture data:", error);
  } finally {
    loading.value = false;
  }
}

function selectScan(scan) {
  selectedScan.value = scan;
  showScanSelector.value = false;
  loadArchitectureData(scan.executionId);
}

async function loadArchitectureData(executionId) {
  loading.value = true;
  try {
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 800));

    // Mock architecture data (replace with actual API call)
    mockArchitectureData.value = {
      nodes: [
        {
          id: "web1",
          name: "Web Server",
          type: "web-service",
          technology: "Nginx",
          version: "1.21.0",
          port: 80,
          x: 100,
          y: 50,
          vulnerabilities: 2,
          description: "Main web server handling HTTP requests",
          vulnerabilityDetails: [
            {
              id: "vuln1",
              title: "Outdated Nginx version",
              severity: "medium",
              description: "Running an outdated version of Nginx",
            },
            {
              id: "vuln2",
              title: "Missing security headers",
              severity: "low",
              description: "CSP and HSTS headers not configured",
            },
          ],
        },
        {
          id: "app1",
          name: "Application Server",
          type: "web-service",
          technology: "Node.js",
          version: "16.14.0",
          port: 3000,
          x: 350,
          y: 50,
          vulnerabilities: 1,
          description: "Main application server",
          vulnerabilityDetails: [
            {
              id: "vuln3",
              title: "Prototype pollution",
              severity: "high",
              description: "Vulnerable to prototype pollution attacks",
            },
          ],
        },
        {
          id: "db1",
          name: "Database",
          type: "database",
          technology: "MongoDB",
          version: "5.0.6",
          port: 27017,
          x: 600,
          y: 50,
          vulnerabilities: 0,
          description: "Primary database for application data",
          vulnerabilityDetails: [],
        },
        {
          id: "api1",
          name: "REST API",
          type: "api",
          technology: "Express",
          version: "4.17.1",
          port: 8000,
          x: 225,
          y: 250,
          vulnerabilities: 3,
          description: "RESTful API endpoints",
          vulnerabilityDetails: [
            {
              id: "vuln4",
              title: "SQL Injection",
              severity: "critical",
              description: "Vulnerable to SQL injection attacks",
            },
            {
              id: "vuln5",
              title: "Broken authentication",
              severity: "high",
              description: "Weak authentication mechanism",
            },
            {
              id: "vuln6",
              title: "CORS misconfiguration",
              severity: "medium",
              description: "CORS headers improperly configured",
            },
          ],
        },
        {
          id: "cache1",
          name: "Cache Server",
          type: "infrastructure",
          technology: "Redis",
          version: "6.2.0",
          port: 6379,
          x: 475,
          y: 250,
          vulnerabilities: 0,
          description: "In-memory cache for performance",
          vulnerabilityDetails: [],
        },
        {
          id: "ext1",
          name: "External API",
          type: "external",
          technology: "Third-party",
          x: 100,
          y: 450,
          vulnerabilities: 0,
          description: "External third-party service",
          vulnerabilityDetails: [],
        },
        {
          id: "cdn1",
          name: "CDN",
          type: "infrastructure",
          technology: "Cloudflare",
          x: 350,
          y: 450,
          vulnerabilities: 0,
          description: "Content delivery network",
          vulnerabilityDetails: [],
        },
        {
          id: "storage1",
          name: "Object Storage",
          type: "infrastructure",
          technology: "AWS S3",
          x: 600,
          y: 450,
          vulnerabilities: 1,
          description: "Cloud storage for static assets",
          vulnerabilityDetails: [
            {
              id: "vuln7",
              title: "Public bucket exposure",
              severity: "critical",
              description: "S3 bucket is publicly accessible",
            },
          ],
        },
      ],
      connections: [
        {
          from: "web1",
          to: "app1",
          protocol: "HTTP",
          port: 3000,
          vulnerable: false,
        },
        {
          from: "app1",
          to: "db1",
          protocol: "MongoDB",
          port: 27017,
          vulnerable: false,
        },
        {
          from: "app1",
          to: "api1",
          protocol: "REST",
          port: 8000,
          vulnerable: true,
        },
        {
          from: "api1",
          to: "cache1",
          protocol: "Redis",
          port: 6379,
          vulnerable: false,
        },
        { from: "api1", to: "ext1", protocol: "HTTPS", vulnerable: false },
        { from: "web1", to: "cdn1", protocol: "HTTP", vulnerable: false },
        { from: "app1", to: "storage1", protocol: "S3", vulnerable: true },
      ],
    };
  } catch (error) {
    console.error("Failed to load architecture data:", error);
  } finally {
    loading.value = false;
  }
}

function handleNodeSelected(node) {
  console.log("Node selected:", node);
}

function handleDownload() {
  console.log("Download requested");
}

function selectComponent(component) {
  selectedComponent.value = component;
}

async function loadAvailableScans() {
  loading.value = true;
  try {
    // In real implementation, fetch from backend
    // const response = await fetch('/api/executions');
    // availableScans.value = await response.json();

    // Mock data
    availableScans.value = [
      {
        executionId: "exec_001",
        target: "example.com",
        status: "completed",
        createdAt: new Date(Date.now() - 86400000), // 1 day ago
        agentsExecuted: ["recon", "scanner", "analyzer"],
      },
      {
        executionId: "exec_002",
        target: "api.example.com",
        status: "completed",
        createdAt: new Date(Date.now() - 172800000), // 2 days ago
        agentsExecuted: ["recon", "scanner"],
      },
      {
        executionId: "exec_003",
        target: "app.example.com",
        status: "completed",
        createdAt: new Date(Date.now() - 259200000), // 3 days ago
        agentsExecuted: ["recon", "scanner", "analyzer", "validator"],
      },
    ];
  } catch (error) {
    console.error("Failed to load scans:", error);
  } finally {
    loading.value = false;
  }
}

// Lifecycle
onMounted(() => {
  loadAvailableScans();
});
</script>

<style scoped>
.architecture-map-page {
  padding: 24px;
  max-width: 1600px;
  margin: 0 auto;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.dark .page-header h1 {
  color: #f7fafc;
}

.subtitle {
  color: #6b7280;
  font-size: 16px;
  margin: 0;
}

.dark .subtitle {
  color: #94a3b8;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-primary,
.btn-secondary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: white;
  border: 2px solid #e5e7eb;
  color: #374151;
}

.btn-secondary:hover {
  border-color: #667eea;
  color: #667eea;
}

.dark .btn-secondary {
  background: rgba(30, 30, 30, 0.8);
  border-color: rgba(139, 92, 246, 0.3);
  color: #f7fafc;
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Loading */
.loading-container {
  text-align: center;
  padding: 80px 20px;
}

.loading-container p {
  margin-top: 20px;
  color: #6b7280;
}

.dark .loading-container p {
  color: #94a3b8;
}

.loading-spinner-large {
  width: 60px;
  height: 60px;
  border: 4px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  color: #9ca3af;
  margin: 0 auto 24px;
}

.empty-state h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 12px;
}

.dark .empty-state h2 {
  color: #f7fafc;
}

.empty-state p {
  color: #6b7280;
  margin-bottom: 24px;
}

.dark .empty-state p {
  color: #94a3b8;
}

/* Scan Info Card */
.scan-info-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.dark .scan-info-card {
  background: rgba(15, 15, 15, 0.9);
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.scan-info-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.scan-info-card h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.dark .scan-info-card h3 {
  color: #f7fafc;
}

.scan-meta {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

.dark .scan-meta {
  color: #94a3b8;
}

.scan-stats {
  display: flex;
  gap: 32px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
}

.dark .stat-value {
  color: #f7fafc;
}

.stat-value.text-red {
  color: #ef4444;
}

.stat-value.text-green {
  color: #10b981;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.dark .stat-label {
  color: #94a3b8;
}

/* Components Section */
.components-section,
.connections-section {
  margin-top: 32px;
}

.components-section h2,
.connections-section h2 {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 20px;
}

.dark .components-section h2,
.dark .connections-section h2 {
  color: #f7fafc;
}

.components-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.component-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.component-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
}

.dark .component-card {
  background: rgba(20, 20, 20, 0.8);
  border-color: rgba(139, 92, 246, 0.2);
}

.dark .component-card:hover {
  border-color: rgba(139, 92, 246, 0.5);
  box-shadow: 0 8px 16px rgba(139, 92, 246, 0.2);
}

.component-card.has-vulnerabilities {
  border-color: rgba(239, 68, 68, 0.3);
}

.component-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.component-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.component-icon.icon-web-service {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.component-icon.icon-database {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.component-icon.icon-api {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.component-icon.icon-external {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.component-icon.icon-infrastructure {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.component-info {
  flex: 1;
}

.component-info h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 4px 0;
}

.dark .component-info h4 {
  color: #f7fafc;
}

.component-info p {
  font-size: 13px;
  color: #6b7280;
  margin: 0;
}

.dark .component-info p {
  color: #94a3b8;
}

.vuln-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #ef4444;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.component-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.dark .component-details {
  border-top-color: rgba(139, 92, 246, 0.2);
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-item .label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.dark .detail-item .label {
  color: #94a3b8;
}

.detail-item .value {
  font-size: 14px;
  color: #1a1a1a;
  font-weight: 500;
}

.dark .detail-item .value {
  color: #f7fafc;
}

/* Connections */
.connections-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.connection-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
}

.dark .connection-item {
  background: rgba(20, 20, 20, 0.8);
  border-color: rgba(139, 92, 246, 0.2);
}

.connection-item.vulnerable {
  border-color: rgba(239, 68, 68, 0.4);
  background: rgba(239, 68, 68, 0.05);
}

.connection-flow {
  display: flex;
  align-items: center;
  gap: 16px;
}

.connection-node {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #f3f4f6;
  border-radius: 8px;
  font-weight: 500;
  color: #374151;
}

.dark .connection-node {
  background: rgba(30, 30, 30, 0.8);
  color: #f7fafc;
}

.connection-arrow {
  position: relative;
  color: #6b7280;
}

.connection-protocol {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 11px;
  font-weight: 600;
  color: #8b5cf6;
  white-space: nowrap;
}

.connection-warning {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  padding: 8px 12px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 6px;
  color: #dc2626;
  font-size: 13px;
  font-weight: 500;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
}

.dark .modal-content {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.modal-content.large {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.dark .modal-header {
  border-bottom-color: rgba(139, 92, 246, 0.2);
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
}

.dark .modal-header h3 {
  color: #f7fafc;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  color: #6b7280;
  cursor: pointer;
  padding: 0;
  width: 28px;
  height: 28px;
  line-height: 1;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #1a1a1a;
}

.dark .close-btn:hover {
  color: #f7fafc;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

/* Scans List in Modal */
.scans-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.scan-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.scan-item:hover {
  background: #f3f4f6;
  border-color: #667eea;
}

.dark .scan-item {
  background: rgba(30, 30, 30, 0.8);
}

.dark .scan-item:hover {
  background: rgba(139, 92, 246, 0.1);
  border-color: rgba(139, 92, 246, 0.4);
}

.scan-item.active {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
}

.scan-item-content h4 {
  margin: 0 0 6px 0;
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
}

.dark .scan-item-content h4 {
  color: #f7fafc;
}

.scan-date {
  font-size: 13px;
  color: #6b7280;
  margin: 0 0 8px 0;
}

.dark .scan-date {
  color: #94a3b8;
}

.scan-badges {
  display: flex;
  gap: 8px;
}

.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  background: #e5e7eb;
  color: #374151;
}

.dark .badge {
  background: rgba(100, 100, 100, 0.3);
  color: #f7fafc;
}

.badge.status {
  text-transform: capitalize;
}

.badge.status.completed {
  background: #d1fae5;
  color: #065f46;
}

.dark .badge.status.completed {
  background: rgba(16, 185, 129, 0.2);
  color: #6ee7b7;
}

.scan-arrow {
  color: #9ca3af;
}

/* Component Details */
.component-full-details {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.description-section,
.vulnerabilities-section {
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.dark .description-section,
.dark .vulnerabilities-section {
  border-top-color: rgba(139, 92, 246, 0.2);
}

.description-section h4,
.vulnerabilities-section h4 {
  margin: 0 0 12px 0;
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
}

.dark .description-section h4,
.dark .vulnerabilities-section h4 {
  color: #f7fafc;
}

.description-section p {
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}

.dark .description-section p {
  color: #94a3b8;
}

.vulnerability-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.vulnerability-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
}

.dark .vulnerability-item {
  background: rgba(30, 30, 30, 0.6);
}

.severity-badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  height: fit-content;
}

.severity-badge.critical {
  background: #fee2e2;
  color: #991b1b;
}

.severity-badge.high {
  background: #fed7aa;
  color: #9a3412;
}

.severity-badge.medium {
  background: #fef3c7;
  color: #92400e;
}

.severity-badge.low {
  background: #dbeafe;
  color: #1e40af;
}

.dark .severity-badge.critical {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
}

.dark .severity-badge.high {
  background: rgba(251, 146, 60, 0.2);
  color: #fdba74;
}

.dark .severity-badge.medium {
  background: rgba(245, 158, 11, 0.2);
  color: #fcd34d;
}

.dark .severity-badge.low {
  background: rgba(59, 130, 246, 0.2);
  color: #93c5fd;
}

.vuln-info {
  flex: 1;
}

.vuln-title {
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 4px 0;
  font-size: 14px;
}

.dark .vuln-title {
  color: #f7fafc;
}

.vuln-desc {
  color: #6b7280;
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
}

.dark .vuln-desc {
  color: #94a3b8;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }

  .components-grid {
    grid-template-columns: 1fr;
  }

  .scan-info-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .details-grid {
    grid-template-columns: 1fr;
  }
}
</style>
