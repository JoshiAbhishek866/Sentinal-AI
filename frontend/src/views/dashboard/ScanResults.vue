<template>
  <div class="scan-results-page">
    <!-- Header -->
    <div class="results-header">
      <div>
        <h1>Security Scan Results</h1>
        <p class="subtitle">{{ scanInfo.target || "No active scan" }}</p>
      </div>
      <button @click="$router.push('/dashboard/overview')" class="btn-back">
        ← Back to Dashboard
      </button>
    </div>

    <!-- No Scan State -->
    <div v-if="!hasScanData" class="empty-state">
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
          d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
        />
      </svg>
      <h2>No Scan Results</h2>
      <p>Run a security scan to see detailed results here</p>
      <button @click="$router.push('/dashboard/overview')" class="btn-primary">
        Go to Dashboard
      </button>
    </div>

    <!-- Scan Results -->
    <div v-else class="results-content">
      <!-- Progress Section -->
      <div class="progress-section">
        <div class="progress-card">
          <div class="progress-header">
            <h3>Scan Progress</h3>
            <span class="status-badge" :class="scanStatus">{{
              scanStatus
            }}</span>
          </div>

          <div class="progress-bar-container">
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: progressPercentage + '%' }"
              ></div>
            </div>
            <span class="progress-text"
              >{{ progressPercentage }}% Complete</span
            >
          </div>

          <div class="progress-details">
            <div class="detail-item">
              <span class="label">Started:</span>
              <span class="value">{{ formatTime(scanInfo.startTime) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Estimated Time:</span>
              <span class="value">{{
                scanInfo.estimatedTime || "15-20 min"
              }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Time Elapsed:</span>
              <span class="value">{{ timeElapsed }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Agents Running:</span>
              <span class="value">{{ activeAgents }}/{{ totalAgents }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Summary Cards -->
      <div class="summary-grid">
        <div class="summary-card critical">
          <div class="card-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
              />
            </svg>
          </div>
          <div class="card-content">
            <h4>Critical</h4>
            <p class="card-value">{{ vulnerabilities.critical }}</p>
            <span class="card-label">CVSS 9.0-10.0</span>
          </div>
        </div>

        <div class="summary-card high">
          <div class="card-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"
              />
            </svg>
          </div>
          <div class="card-content">
            <h4>High</h4>
            <p class="card-value">{{ vulnerabilities.high }}</p>
            <span class="card-label">CVSS 7.0-8.9</span>
          </div>
        </div>

        <div class="summary-card medium">
          <div class="card-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
              />
            </svg>
          </div>
          <div class="card-content">
            <h4>Medium</h4>
            <p class="card-value">{{ vulnerabilities.medium }}</p>
            <span class="card-label">CVSS 4.0-6.9</span>
          </div>
        </div>

        <div class="summary-card low">
          <div class="card-icon">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <div class="card-content">
            <h4>Low</h4>
            <p class="card-value">{{ vulnerabilities.low }}</p>
            <span class="card-label">CVSS 0.1-3.9</span>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tabs-container">
        <div class="tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="['tab', { active: activeTab === tab.id }]"
          >
            {{ tab.label }}
            <span v-if="tab.count" class="tab-badge">{{ tab.count }}</span>
          </button>
        </div>

        <!-- Tab Content -->
        <div class="tab-content">
          <!-- Vulnerabilities Tab -->
          <div
            v-if="activeTab === 'vulnerabilities'"
            class="vulnerabilities-list"
          >
            <div
              v-for="vuln in sortedVulnerabilities"
              :key="vuln.id"
              class="vuln-card"
            >
              <div class="vuln-header">
                <div class="vuln-title-section">
                  <h4>{{ vuln.title }}</h4>
                  <span class="vuln-id">{{ vuln.cve || vuln.id }}</span>
                </div>
                <div class="vuln-badges">
                  <span class="severity-badge" :class="vuln.severity">
                    {{ vuln.severity }}
                  </span>
                  <span class="cvss-badge"> CVSS {{ vuln.cvss }} </span>
                  <span class="priority-badge" :class="vuln.priority">
                    {{ vuln.priority }} Priority
                  </span>
                </div>
              </div>

              <p class="vuln-description">{{ vuln.description }}</p>

              <div class="vuln-details">
                <div class="detail-row">
                  <span class="detail-label">Affected Component:</span>
                  <span class="detail-value">{{ vuln.component }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Attack Vector:</span>
                  <span class="detail-value">{{ vuln.attackVector }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">Exploit Available:</span>
                  <span
                    class="detail-value"
                    :class="vuln.exploitAvailable ? 'text-red' : 'text-green'"
                  >
                    {{ vuln.exploitAvailable ? "Yes" : "No" }}
                  </span>
                </div>
              </div>

              <div class="vuln-actions">
                <button class="btn-secondary">View Details</button>
                <button class="btn-primary">Apply Patch</button>
              </div>
            </div>

            <div
              v-if="sortedVulnerabilities.length === 0"
              class="empty-message"
            >
              <p>No vulnerabilities found</p>
            </div>
          </div>

          <!-- Patches Tab -->
          <div v-if="activeTab === 'patches'" class="patches-list">
            <div v-for="patch in patches" :key="patch.id" class="patch-card">
              <div class="patch-header">
                <div>
                  <h4>{{ patch.title }}</h4>
                  <p class="patch-description">{{ patch.description }}</p>
                </div>
                <span class="status-badge" :class="patch.status">
                  {{ patch.status }}
                </span>
              </div>

              <div class="patch-details">
                <div class="detail-item">
                  <span class="label">Vulnerabilities Fixed:</span>
                  <span class="value">{{ patch.vulnerabilitiesFixed }}</span>
                </div>
                <div class="detail-item">
                  <span class="label">Applied:</span>
                  <span class="value">{{ formatTime(patch.appliedAt) }}</span>
                </div>
                <div class="detail-item">
                  <span class="label">Success Rate:</span>
                  <span class="value">{{ patch.successRate }}%</span>
                </div>
              </div>

              <div class="patch-actions">
                <button class="btn-secondary">View Changelog</button>
                <button v-if="patch.status === 'pending'" class="btn-primary">
                  Apply Now
                </button>
                <button v-if="patch.status === 'applied'" class="btn-secondary">
                  Rollback
                </button>
              </div>
            </div>
          </div>

          <!-- Analysis Tab -->
          <div v-if="activeTab === 'analysis'" class="analysis-section">
            <div class="analysis-card">
              <h3>AI-Powered Risk Analysis</h3>
              <p class="analysis-summary">{{ aiAnalysis.summary }}</p>

              <div class="analysis-metrics">
                <div class="metric">
                  <span class="metric-label">Overall Risk Score</span>
                  <div
                    class="risk-score"
                    :class="getRiskClass(aiAnalysis.riskScore)"
                  >
                    {{ aiAnalysis.riskScore }}/100
                  </div>
                </div>
                <div class="metric">
                  <span class="metric-label">Attack Surface</span>
                  <span class="metric-value">{{
                    aiAnalysis.attackSurface
                  }}</span>
                </div>
                <div class="metric">
                  <span class="metric-label">Remediation Priority</span>
                  <span class="metric-value">{{
                    aiAnalysis.remediationPriority
                  }}</span>
                </div>
              </div>

              <div class="recommendations">
                <h4>Top Recommendations</h4>
                <ul>
                  <li
                    v-for="(rec, index) in aiAnalysis.recommendations"
                    :key="index"
                  >
                    {{ rec }}
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Report Tab -->
          <div v-if="activeTab === 'report'" class="report-section">
            <div class="report-actions">
              <button class="btn-primary">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="icon"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3"
                  />
                </svg>
                Download PDF Report
              </button>
              <button class="btn-secondary">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="icon"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3"
                  />
                </svg>
                Export as JSON
              </button>
              <button class="btn-secondary">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                  stroke="currentColor"
                  class="icon"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M7.217 10.907a2.25 2.25 0 100 2.186m0-2.186c.18.324.283.696.283 1.093s-.103.77-.283 1.093m0-2.186l9.566-5.314m-9.566 7.5l9.566 5.314m0 0a2.25 2.25 0 103.935 2.186 2.25 2.25 0 00-3.935-2.186zm0-12.814a2.25 2.25 0 103.933-2.185 2.25 2.25 0 00-3.933 2.185z"
                  />
                </svg>
                Share Report
              </button>
            </div>

            <div class="report-preview">
              <h3>Executive Summary</h3>
              <p>{{ reportSummary }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useSecurityStore } from "@/stores/security";

const securityStore = useSecurityStore();

// Active tab
const activeTab = ref("vulnerabilities");

// Tabs configuration
const tabs = computed(() => [
  {
    id: "vulnerabilities",
    label: "Vulnerabilities",
    count: totalVulnerabilities.value,
  },
  { id: "patches", label: "Patches & Fixes", count: patches.value.length },
  { id: "analysis", label: "AI Analysis", count: null },
  { id: "report", label: "Report", count: null },
]);

// Scan info
const scanInfo = computed(() => securityStore.currentScan || {});
const hasScanData = computed(() => !!securityStore.currentScan);

// Scan status
const scanStatus = computed(() => scanInfo.value.status || "pending");

// Progress
const progressPercentage = ref(0);
const activeAgents = ref(0);
const totalAgents = ref(7);

// Time tracking
const timeElapsed = ref("0m 0s");
let startTime = null;
let intervalId = null;

// Mock vulnerabilities data (replace with actual data from store)
const vulnerabilitiesData = ref([
  {
    id: "CVE-2024-0001",
    cve: "CVE-2024-0001",
    title: "SQL Injection in Login Form",
    description:
      "Improper input validation allows SQL injection attacks through the login form",
    severity: "critical",
    cvss: 9.8,
    priority: "immediate",
    component: "Authentication Module",
    attackVector: "Network",
    exploitAvailable: true,
  },
  {
    id: "CVE-2024-0002",
    cve: "CVE-2024-0002",
    title: "Cross-Site Scripting (XSS) Vulnerability",
    description: "Reflected XSS vulnerability in search functionality",
    severity: "high",
    cvss: 7.5,
    priority: "high",
    component: "Search Module",
    attackVector: "Network",
    exploitAvailable: false,
  },
  {
    id: "CVE-2024-0003",
    cve: "CVE-2024-0003",
    title: "Insecure Direct Object Reference",
    description:
      "Users can access other users' data by manipulating object IDs",
    severity: "high",
    cvss: 8.1,
    priority: "high",
    component: "API Endpoints",
    attackVector: "Network",
    exploitAvailable: true,
  },
  {
    id: "CVE-2024-0004",
    cve: "CVE-2024-0004",
    title: "Weak Password Policy",
    description: "Password policy allows weak passwords",
    severity: "medium",
    cvss: 5.3,
    priority: "medium",
    component: "User Management",
    attackVector: "Local",
    exploitAvailable: false,
  },
  {
    id: "CVE-2024-0005",
    cve: "CVE-2024-0005",
    title: "Missing Security Headers",
    description: "Application missing critical security headers",
    severity: "low",
    cvss: 3.7,
    priority: "low",
    component: "Web Server",
    attackVector: "Network",
    exploitAvailable: false,
  },
]);

// Vulnerabilities summary
const vulnerabilities = computed(() => {
  const summary = { critical: 0, high: 0, medium: 0, low: 0 };
  vulnerabilitiesData.value.forEach((v) => {
    if (v.cvss >= 9.0) summary.critical++;
    else if (v.cvss >= 7.0) summary.high++;
    else if (v.cvss >= 4.0) summary.medium++;
    else summary.low++;
  });
  return summary;
});

const totalVulnerabilities = computed(
  () =>
    vulnerabilities.value.critical +
    vulnerabilities.value.high +
    vulnerabilities.value.medium +
    vulnerabilities.value.low,
);

const sortedVulnerabilities = computed(() => {
  return [...vulnerabilitiesData.value].sort((a, b) => b.cvss - a.cvss);
});

// Patches data
const patches = ref([
  {
    id: "PATCH-001",
    title: "Security Update 2024-01",
    description:
      "Critical security patches for authentication and SQL injection vulnerabilities",
    status: "applied",
    vulnerabilitiesFixed: 2,
    appliedAt: new Date(Date.now() - 3600000),
    successRate: 100,
  },
  {
    id: "PATCH-002",
    title: "XSS Protection Update",
    description: "Implements input sanitization and output encoding",
    status: "pending",
    vulnerabilitiesFixed: 1,
    appliedAt: null,
    successRate: 0,
  },
]);

// AI Analysis
const aiAnalysis = ref({
  summary:
    "Your system has 5 vulnerabilities with 1 critical issue requiring immediate attention. The overall security posture is moderate with several high-priority items that should be addressed within 48 hours.",
  riskScore: 72,
  attackSurface: "Medium",
  remediationPriority: "High",
  recommendations: [
    "Immediately patch SQL injection vulnerability (CVE-2024-0001)",
    "Implement Web Application Firewall (WAF) to protect against common attacks",
    "Enable multi-factor authentication for all user accounts",
    "Review and strengthen password policies",
    "Add security headers (CSP, HSTS, X-Frame-Options)",
  ],
});

// Report summary
const reportSummary = ref(
  "This comprehensive security assessment identified 5 vulnerabilities across your infrastructure. " +
    "Critical findings include SQL injection and IDOR vulnerabilities that require immediate remediation. " +
    "The scan covered authentication, API security, and web application components. " +
    "Detailed remediation steps and patches are available for all identified issues.",
);

// Methods
const formatTime = (date) => {
  if (!date) return "N/A";
  const d = new Date(date);
  return d.toLocaleString();
};

const getRiskClass = (score) => {
  if (score >= 80) return "risk-critical";
  if (score >= 60) return "risk-high";
  if (score >= 40) return "risk-medium";
  return "risk-low";
};

const updateProgress = () => {
  // Simulate progress (replace with actual progress from backend)
  if (progressPercentage.value < 100 && scanStatus.value === "running") {
    progressPercentage.value = Math.min(
      100,
      progressPercentage.value + Math.random() * 5,
    );
    activeAgents.value = Math.min(
      totalAgents.value,
      Math.floor((progressPercentage.value / 100) * totalAgents.value),
    );
  }
};

const updateTimeElapsed = () => {
  if (!startTime) startTime = Date.now();
  const elapsed = Date.now() - startTime;
  const minutes = Math.floor(elapsed / 60000);
  const seconds = Math.floor((elapsed % 60000) / 1000);
  timeElapsed.value = `${minutes}m ${seconds}s`;
};

// Lifecycle
onMounted(() => {
  // Simulate scan progress
  intervalId = setInterval(() => {
    updateProgress();
    updateTimeElapsed();
  }, 1000);
});

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId);
});
</script>

<style scoped>
.scan-results-page {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* Header */
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.results-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.subtitle {
  color: #6b7280;
  font-size: 16px;
  margin: 0;
}

.btn-back {
  background: white;
  border: 2px solid #e5e7eb;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-back:hover {
  border-color: #667eea;
  color: #667eea;
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

.empty-state p {
  color: #6b7280;
  margin-bottom: 24px;
}

/* Progress Section */
.progress-section {
  margin-bottom: 32px;
}

.progress-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.progress-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.status-badge {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.running {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.completed {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.applied {
  background: #d1fae5;
  color: #065f46;
}

.progress-bar-container {
  margin-bottom: 20px;
}

.progress-bar {
  height: 12px;
  background: #f3f4f6;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
  border-radius: 6px;
}

.progress-text {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.progress-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e5e7eb;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item .label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.detail-item .value {
  font-size: 15px;
  color: #1a1a1a;
  font-weight: 600;
}

/* Summary Grid */
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.summary-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 16px;
  border-left: 4px solid;
}

.summary-card.critical {
  border-left-color: #dc2626;
}

.summary-card.high {
  border-left-color: #f59e0b;
}

.summary-card.medium {
  border-left-color: #fbbf24;
}

.summary-card.low {
  border-left-color: #10b981;
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.critical .card-icon {
  background: #fee2e2;
  color: #dc2626;
}

.high .card-icon {
  background: #fed7aa;
  color: #f59e0b;
}

.medium .card-icon {
  background: #fef3c7;
  color: #fbbf24;
}

.low .card-icon {
  background: #d1fae5;
  color: #10b981;
}

.card-icon svg {
  width: 24px;
  height: 24px;
}

.card-content h4 {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  margin: 0 0 8px 0;
}

.card-value {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 4px 0;
}

.card-label {
  font-size: 12px;
  color: #9ca3af;
}

/* Tabs */
.tabs-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 24px;
  gap: 8px;
}

.tab {
  padding: 16px 20px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  font-weight: 600;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab:hover {
  color: #667eea;
}

.tab.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab-badge {
  background: #f3f4f6;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.tab.active .tab-badge {
  background: #ede9fe;
  color: #667eea;
}

.tab-content {
  padding: 24px;
}

/* Vulnerabilities List */
.vulnerabilities-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.vuln-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
  border-left: 4px solid;
}

.vuln-card:has(.severity-badge.critical) {
  border-left-color: #dc2626;
}

.vuln-card:has(.severity-badge.high) {
  border-left-color: #f59e0b;
}

.vuln-card:has(.severity-badge.medium) {
  border-left-color: #fbbf24;
}

.vuln-card:has(.severity-badge.low) {
  border-left-color: #10b981;
}

.vuln-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 16px;
}

.vuln-title-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 4px 0;
}

.vuln-id {
  font-size: 13px;
  color: #6b7280;
  font-family: monospace;
}

.vuln-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.severity-badge,
.cvss-badge,
.priority-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
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
  background: #d1fae5;
  color: #065f46;
}

.cvss-badge {
  background: #e0e7ff;
  color: #3730a3;
}

.priority-badge.immediate {
  background: #fee2e2;
  color: #991b1b;
}

.priority-badge.high {
  background: #fed7aa;
  color: #9a3412;
}

.priority-badge.medium {
  background: #fef3c7;
  color: #92400e;
}

.priority-badge.low {
  background: #d1fae5;
  color: #065f46;
}

.vuln-description {
  color: #374151;
  margin-bottom: 16px;
  line-height: 1.6;
}

.vuln-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
  padding: 16px;
  background: white;
  border-radius: 8px;
}

.detail-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
}

.detail-value {
  font-size: 14px;
  color: #1a1a1a;
  font-weight: 600;
}

.text-red {
  color: #dc2626;
}

.text-green {
  color: #10b981;
}

.vuln-actions {
  display: flex;
  gap: 12px;
}

/* Patches List */
.patches-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.patch-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
}

.patch-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.patch-header h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.patch-description {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

.patch-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
  padding: 16px;
  background: white;
  border-radius: 8px;
}

.patch-actions {
  display: flex;
  gap: 12px;
}

/* Analysis Section */
.analysis-section {
  max-width: 900px;
}

.analysis-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 24px;
}

.analysis-card h3 {
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 16px 0;
}

.analysis-summary {
  color: #374151;
  line-height: 1.6;
  margin-bottom: 24px;
}

.analysis-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.metric {
  background: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}

.metric-label {
  display: block;
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
  margin-bottom: 12px;
}

.risk-score {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 8px;
}

.risk-critical {
  color: #dc2626;
}

.risk-high {
  color: #f59e0b;
}

.risk-medium {
  color: #fbbf24;
}

.risk-low {
  color: #10b981;
}

.metric-value {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
}

.recommendations {
  background: white;
  padding: 20px;
  border-radius: 12px;
}

.recommendations h4 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
}

.recommendations ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recommendations li {
  padding: 12px 0;
  border-bottom: 1px solid #e5e7eb;
  color: #374151;
  line-height: 1.6;
}

.recommendations li:last-child {
  border-bottom: none;
}

.recommendations li::before {
  content: "→";
  color: #667eea;
  font-weight: 700;
  margin-right: 12px;
}

/* Report Section */
.report-section {
  max-width: 900px;
}

.report-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.report-preview {
  background: #f9fafb;
  border-radius: 12px;
  padding: 24px;
}

.report-preview h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px 0;
}

.report-preview p {
  color: #374151;
  line-height: 1.6;
}

/* Buttons */
.btn-primary,
.btn-secondary {
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
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

.icon {
  width: 18px;
  height: 18px;
}

.empty-message {
  text-align: center;
  padding: 40px;
  color: #6b7280;
}

/* Responsive */
@media (max-width: 768px) {
  .results-header {
    flex-direction: column;
    gap: 16px;
  }

  .tabs {
    overflow-x: auto;
    padding: 0 16px;
  }

  .vuln-header,
  .patch-header {
    flex-direction: column;
  }

  .report-actions {
    flex-direction: column;
  }

  .report-actions button {
    width: 100%;
    justify-content: center;
  }
}
</style>
