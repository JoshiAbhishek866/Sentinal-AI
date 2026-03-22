import { ref } from "vue";
import axios from "axios";

export function useAI() {
  const loading = ref(false);
  const error = ref(null);

  const MCP_URL = "http://localhost:8001";
  const OLLAMA_URL = "http://localhost:11434";

  // Search similar CVEs using RAG
  const searchSimilarCVEs = async (query, nResults = 5) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.post(`${MCP_URL}/rag/search/cves`, {
        query,
        n_results: nResults,
      });
      return response.data.results || [];
    } catch (err) {
      error.value = err.message;
      console.error("Error searching CVEs:", err);
      return [];
    } finally {
      loading.value = false;
    }
  };

  // Search similar incidents
  const searchSimilarIncidents = async (query, nResults = 3) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.post(`${MCP_URL}/rag/search/incidents`, {
        query,
        n_results: nResults,
      });
      return response.data.results || [];
    } catch (err) {
      error.value = err.message;
      console.error("Error searching incidents:", err);
      return [];
    } finally {
      loading.value = false;
    }
  };

  // Get AI analysis of vulnerability
  const analyzeVulnerability = async (cveId, description) => {
    loading.value = true;
    error.value = null;
    try {
      const prompt = `Analyze this vulnerability:
CVE ID: ${cveId}
Description: ${description}

Provide:
1. Severity assessment
2. Potential impact
3. Recommended mitigation steps
4. Priority level

Keep the response concise and actionable.`;

      const response = await axios.post(
        `${OLLAMA_URL}/api/generate`,
        {
          model: "deepseek-r1:8b",
          prompt,
          stream: false,
        },
        {
          timeout: 60000, // 60 second timeout for AI generation
        },
      );

      return response.data.response;
    } catch (err) {
      error.value = err.message;
      console.error("Error analyzing vulnerability:", err);
      return null;
    } finally {
      loading.value = false;
    }
  };

  // Execute security scan via MCP
  const runSecurityScan = async (target, scanType = "quick") => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.post(`${MCP_URL}/tools/call`, {
        tool_name: "run_security_scan",
        parameters: { target, scan_type: scanType },
      });
      return response.data;
    } catch (err) {
      error.value = err.message;
      console.error("Error running security scan:", err);
      return null;
    } finally {
      loading.value = false;
    }
  };

  // Create incident via MCP
  const createIncident = async (title, severity, description) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.post(`${MCP_URL}/tools/call`, {
        tool_name: "create_incident",
        parameters: { title, severity, description },
      });
      return response.data;
    } catch (err) {
      error.value = err.message;
      console.error("Error creating incident:", err);
      return null;
    } finally {
      loading.value = false;
    }
  };

  // Apply patch via MCP
  const applyPatch = async (vulnerabilityId, patchId) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.post(`${MCP_URL}/tools/call`, {
        tool_name: "apply_patch",
        parameters: { vulnerability_id: vulnerabilityId, patch_id: patchId },
      });
      return response.data;
    } catch (err) {
      error.value = err.message;
      console.error("Error applying patch:", err);
      return null;
    } finally {
      loading.value = false;
    }
  };

  // Chat with AI
  const chatWithAI = async (message, conversationHistory = []) => {
    loading.value = true;
    error.value = null;
    try {
      // Build context from conversation history
      let prompt = message;
      if (conversationHistory.length > 0) {
        const context = conversationHistory
          .map(
            (msg) =>
              `${msg.role === "user" ? "User" : "Assistant"}: ${msg.content}`,
          )
          .join("\n");
        prompt = `${context}\nUser: ${message}\nAssistant:`;
      }

      const response = await axios.post(
        `${OLLAMA_URL}/api/generate`,
        {
          model: "deepseek-r1:8b",
          prompt,
          stream: false,
          options: {
            temperature: 0.7,
            num_predict: 500, // Limit response length for faster generation
          },
        },
        {
          timeout: 120000, // Increased to 120 seconds for local LLM
        },
      );

      return response.data.response;
    } catch (err) {
      error.value = err.message;
      console.error("Error chatting with AI:", err);
      console.error("Full error:", err.response?.data || err);
      return null;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    searchSimilarCVEs,
    searchSimilarIncidents,
    analyzeVulnerability,
    runSecurityScan,
    createIncident,
    applyPatch,
    chatWithAI,
  };
}
