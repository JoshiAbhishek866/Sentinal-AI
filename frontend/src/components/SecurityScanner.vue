<template>
  <div class="security-scanner-modal">
    <!-- Trigger Button -->
    <button @click="openModal" class="scan-trigger-btn">
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
          d="M9.75 3.104v5.714a2.25 2.25 0 01-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 014.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0112 15a9.065 9.065 0 00-6.23-.693L5 14.5m14.8.8l1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0112 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5"
        />
      </svg>
      Run Security Scan
    </button>

    <!-- Modal Overlay -->
    <Transition name="modal">
      <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
        <div class="modal-container" @click.stop>
          <!-- Modal Header -->
          <div class="modal-header">
            <h2>Security Scanner</h2>
            <button @click="closeModal" class="close-btn">
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
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <p class="modal-description">
              Run comprehensive security assessments on your infrastructure
            </p>

            <!-- Scan Form -->
            <div class="scan-form">
              <div class="form-group">
                <label for="workflow">Scan Type</label>
                <select
                  id="workflow"
                  v-model="selectedWorkflow"
                  :disabled="isScanning"
                  class="form-control"
                >
                  <option value="">Select a scan type...</option>
                  <option
                    v-for="workflow in workflows"
                    :key="workflow.id"
                    :value="workflow.id"
                  >
                    {{ workflow.name }}
                    <!-- - {{ workflow.duration }} -->
                  </option>
                </select>
                <small v-if="selectedWorkflowDetails" class="form-text">
                  {{ selectedWorkflowDetails.description }}
                </small>
              </div>

              <div class="form-group">
                <label for="target">Target (Domain or IP)</label>
                <input
                  id="target"
                  v-model="target"
                  type="text"
                  placeholder="example.com or 192.168.1.1"
                  :disabled="isScanning"
                  class="form-control"
                />
              </div>

              <button
                @click="startScan"
                :disabled="!canStartScan"
                class="btn-primary"
              >
                <span v-if="!isScanning">🚀 Start Scan</span>
                <span v-else>⏳ Scanning...</span>
              </button>
            </div>

            <!-- Current Scan Status -->
            <div v-if="currentScan" class="scan-status">
              <h3>Current Scan</h3>
              <div class="status-card">
                <div class="status-item">
                  <span class="label">Workflow:</span>
                  <span class="value">{{ currentScan.workflow }}</span>
                </div>
                <div class="status-item">
                  <span class="label">Target:</span>
                  <span class="value">{{ currentScan.target }}</span>
                </div>
                <div class="status-item">
                  <span class="label">Status:</span>
                  <span class="value status-badge" :class="currentScan.status">
                    {{ currentScan.status }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Error Display -->
            <div v-if="error" class="error-message">⚠️ {{ error }}</div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useSecurityStore } from "@/stores/security";

const securityStore = useSecurityStore();

// Modal state
const isModalOpen = ref(false);

// Local state
const selectedWorkflow = ref("");
const target = ref("");

// Computed
const workflows = computed(() => securityStore.workflows);
const isScanning = computed(() => securityStore.isScanning);
const currentScan = computed(() => securityStore.currentScan);
const error = computed(() => securityStore.error);

const selectedWorkflowDetails = computed(() => {
  if (!selectedWorkflow.value) return null;
  return workflows.value.find((w) => w.id === selectedWorkflow.value);
});

const canStartScan = computed(() => {
  return selectedWorkflow.value && target.value && !isScanning.value;
});

// Methods
const openModal = async () => {
  isModalOpen.value = true;
  // Load workflows when modal opens
  if (workflows.value.length === 0) {
    await securityStore.fetchWorkflows();
  }
};

const closeModal = () => {
  isModalOpen.value = false;
};

const startScan = async () => {
  if (!canStartScan.value) return;

  try {
    await securityStore.startScan(selectedWorkflow.value, target.value);
    // Close modal
    closeModal();
    // Navigate to attack insights page to see results
    window.location.href = "/dashboard/attack-insights";
  } catch (error) {
    console.error("Scan failed:", error);
  }
};

// Close modal on Escape key
watch(isModalOpen, (newValue) => {
  if (newValue) {
    const handleEscape = (e) => {
      if (e.key === "Escape") closeModal();
    };
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }
});
</script>

<style scoped>
/* Trigger Button */
.scan-trigger-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #667eea;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.scan-trigger-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.scan-trigger-btn .icon {
  width: 20px;
  height: 20px;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9);
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

/* Modal Container */
.modal-container {
  background: white;
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* Modal Header */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 30px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.2s;
  color: #6b7280;
}

.close-btn:hover {
  background: #f3f4f6;
  color: #1a1a1a;
}

.close-btn svg {
  width: 20px;
  height: 20px;
}

/* Modal Body */
.modal-body {
  padding: 30px;
}

.modal-description {
  color: #6b7280;
  font-size: 15px;
  margin-bottom: 24px;
}

/* Scan Form */
.scan-form {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #374151;
  font-size: 14px;
}

.form-control {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 15px;
  transition: border-color 0.3s;
  font-family: inherit;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
}

.form-control:disabled {
  background: #f9fafb;
  cursor: not-allowed;
  color: #9ca3af;
}

.form-text {
  display: block;
  margin-top: 6px;
  color: #6b7280;
  font-size: 13px;
}

.btn-primary {
  width: 100%;
  background: #667eea;
  color: white;
  border: none;
  padding: 14px 32px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Scan Status */
.scan-status {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
}

.scan-status h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #374151;
}

.status-card {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.status-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.status-item .label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-item .value {
  font-size: 15px;
  color: #1a1a1a;
  font-weight: 600;
}

.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.started {
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

.status-badge.failed {
  background: #fee2e2;
  color: #991b1b;
}

/* Error Message */
.error-message {
  background: #fee2e2;
  color: #991b1b;
  padding: 12px 16px;
  border-radius: 8px;
  margin-top: 16px;
  border-left: 4px solid #dc2626;
  font-size: 14px;
}

/* Scrollbar Styling */
.modal-container::-webkit-scrollbar {
  width: 8px;
}

.modal-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.modal-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.modal-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
