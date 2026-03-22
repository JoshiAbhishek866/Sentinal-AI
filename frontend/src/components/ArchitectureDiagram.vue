<template>
  <div class="architecture-3d-container">
    <div class="diagram-header">
      <div>
        <h3>{{ title }}</h3>
        <p class="subtitle">{{ subtitle }}</p>
      </div>
      <div class="diagram-controls">
        <button @click="resetCamera" class="control-btn" title="Reset View">
          🔄
        </button>
        <button
          @click="toggleAutoRotate"
          class="control-btn"
          title="Auto Rotate"
        >
          {{ autoRotate ? "⏸️" : "▶️" }}
        </button>
        <button @click="toggleWireframe" class="control-btn" title="Wireframe">
          🔲
        </button>
        <button
          @click="downloadScreenshot"
          class="control-btn"
          title="Screenshot"
        >
          📷
        </button>
        <button
          @click="toggleFullscreen"
          class="control-btn"
          title="Fullscreen"
        >
          ⛶
        </button>
      </div>
    </div>

    <div class="diagram-legend">
      <div class="legend-item">
        <div class="legend-color" style="background: #667eea"></div>
        <span>Web Services</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background: #10b981"></div>
        <span>Databases</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background: #f59e0b"></div>
        <span>APIs</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background: #ef4444"></div>
        <span>External</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background: #8b5cf6"></div>
        <span>Infrastructure</span>
      </div>
    </div>

    <div
      ref="canvasContainer"
      class="canvas-container"
      :class="{ fullscreen: isFullscreen }"
    ></div>

    <!-- Node Details Panel -->
    <div v-if="selectedNode" class="node-details-panel">
      <div class="panel-header">
        <h3>{{ selectedNode.name }}</h3>
        <button @click="selectedNode = null" class="close-btn">×</button>
      </div>
      <div class="panel-content">
        <div class="detail-row">
          <span class="label">Type:</span>
          <span class="value">{{ selectedNode.type }}</span>
        </div>
        <div v-if="selectedNode.technology" class="detail-row">
          <span class="label">Technology:</span>
          <span class="value">{{ selectedNode.technology }}</span>
        </div>
        <div v-if="selectedNode.version" class="detail-row">
          <span class="label">Version:</span>
          <span class="value">{{ selectedNode.version }}</span>
        </div>
        <div v-if="selectedNode.port" class="detail-row">
          <span class="label">Port:</span>
          <span class="value">{{ selectedNode.port }}</span>
        </div>
        <div
          v-if="selectedNode.vulnerabilities > 0"
          class="vulnerabilities-section"
        >
          <h4>Vulnerabilities ({{ selectedNode.vulnerabilities }})</h4>
          <div class="vulnerability-list">
            <div
              v-for="vuln in selectedNode.vulnerabilityDetails"
              :key="vuln.id"
              class="vulnerability-item"
            >
              <span :class="`severity-badge ${vuln.severity}`">{{
                vuln.severity
              }}</span>
              <span>{{ vuln.title }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading Indicator -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Initializing 3D Architecture...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { gsap } from "gsap";

const props = defineProps({
  title: {
    type: String,
    default: "3D Software Architecture Map",
  },
  subtitle: {
    type: String,
    default: "Interactive 3D visualization of infrastructure",
  },
  architectureData: {
    type: Object,
    default: () => ({
      nodes: [],
      connections: [],
    }),
  },
});

const emit = defineEmits(["node-selected", "download"]);

// Refs
const canvasContainer = ref(null);
const selectedNode = ref(null);
const isFullscreen = ref(false);
const loading = ref(true);
const autoRotate = ref(true);
const wireframeMode = ref(false);

// Three.js objects
let scene, camera, renderer, controls;
let nodeObjects = [];
let connectionLines = [];
let raycaster, mouse;
let animationFrameId;

// Colors
const colors = {
  "web-service": 0x667eea,
  database: 0x10b981,
  api: 0xf59e0b,
  external: 0xef4444,
  infrastructure: 0x8b5cf6,
};

// Sample data
const defaultNodes = [
  {
    id: "web1",
    name: "Web Server",
    type: "web-service",
    technology: "Nginx",
    version: "1.21.0",
    port: 80,
    position: { x: -4, y: 2, z: 0 },
    vulnerabilities: 2,
    vulnerabilityDetails: [
      { id: "vuln1", title: "Outdated Nginx version", severity: "medium" },
      { id: "vuln2", title: "Missing security headers", severity: "low" },
    ],
  },
  {
    id: "app1",
    name: "Application Server",
    type: "web-service",
    technology: "Node.js",
    version: "16.14.0",
    port: 3000,
    position: { x: 0, y: 2, z: 0 },
    vulnerabilities: 1,
    vulnerabilityDetails: [
      { id: "vuln3", title: "Prototype pollution", severity: "high" },
    ],
  },
  {
    id: "db1",
    name: "Database",
    type: "database",
    technology: "MongoDB",
    version: "5.0.6",
    port: 27017,
    position: { x: 4, y: 2, z: 0 },
    vulnerabilities: 0,
    vulnerabilityDetails: [],
  },
  {
    id: "api1",
    name: "REST API",
    type: "api",
    technology: "Express",
    version: "4.17.1",
    port: 8000,
    position: { x: -2, y: -1, z: 2 },
    vulnerabilities: 3,
    vulnerabilityDetails: [
      { id: "vuln4", title: "SQL Injection", severity: "critical" },
      { id: "vuln5", title: "Broken authentication", severity: "high" },
      { id: "vuln6", title: "CORS misconfiguration", severity: "medium" },
    ],
  },
  {
    id: "cache1",
    name: "Cache Server",
    type: "infrastructure",
    technology: "Redis",
    version: "6.2.0",
    port: 6379,
    position: { x: 2, y: -1, z: 2 },
    vulnerabilities: 0,
    vulnerabilityDetails: [],
  },
  {
    id: "ext1",
    name: "External API",
    type: "external",
    technology: "Third-party",
    position: { x: -4, y: -1, z: -2 },
    vulnerabilities: 0,
    vulnerabilityDetails: [],
  },
  {
    id: "cdn1",
    name: "CDN",
    type: "infrastructure",
    technology: "Cloudflare",
    position: { x: 0, y: -1, z: -2 },
    vulnerabilities: 0,
    vulnerabilityDetails: [],
  },
  {
    id: "storage1",
    name: "Object Storage",
    type: "infrastructure",
    technology: "AWS S3",
    position: { x: 4, y: -1, z: -2 },
    vulnerabilities: 1,
    vulnerabilityDetails: [
      { id: "vuln7", title: "Public bucket exposure", severity: "critical" },
    ],
  },
];

const defaultConnections = [
  { from: "web1", to: "app1", vulnerable: false },
  { from: "app1", to: "db1", vulnerable: false },
  { from: "app1", to: "api1", vulnerable: true },
  { from: "api1", to: "cache1", vulnerable: false },
  { from: "api1", to: "ext1", vulnerable: false },
  { from: "web1", to: "cdn1", vulnerable: false },
  { from: "app1", to: "storage1", vulnerable: true },
];

// Get nodes data
const getNodes = () => {
  return props.architectureData.nodes?.length > 0
    ? props.architectureData.nodes
    : defaultNodes;
};

const getConnections = () => {
  return props.architectureData.connections?.length > 0
    ? props.architectureData.connections
    : defaultConnections;
};

// Initialize Three.js scene
function initScene() {
  // Scene
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a0a);
  scene.fog = new THREE.Fog(0x0a0a0a, 10, 50);

  // Camera
  camera = new THREE.PerspectiveCamera(
    60,
    canvasContainer.value.clientWidth / canvasContainer.value.clientHeight,
    0.1,
    1000,
  );
  camera.position.set(8, 6, 8);
  camera.lookAt(0, 0, 0);

  // Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(
    canvasContainer.value.clientWidth,
    canvasContainer.value.clientHeight,
  );
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  canvasContainer.value.appendChild(renderer.domElement);

  // Controls
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.5;
  controls.minDistance = 5;
  controls.maxDistance = 30;

  // Raycaster for mouse interaction
  raycaster = new THREE.Raycaster();
  mouse = new THREE.Vector2();

  // Lights
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
  directionalLight.position.set(10, 10, 5);
  directionalLight.castShadow = true;
  directionalLight.shadow.camera.near = 0.1;
  directionalLight.shadow.camera.far = 50;
  scene.add(directionalLight);

  const pointLight1 = new THREE.PointLight(0x667eea, 1, 20);
  pointLight1.position.set(-5, 5, 5);
  scene.add(pointLight1);

  const pointLight2 = new THREE.PointLight(0x8b5cf6, 1, 20);
  pointLight2.position.set(5, 5, -5);
  scene.add(pointLight2);

  // Grid helper
  const gridHelper = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
  gridHelper.position.y = -3;
  scene.add(gridHelper);

  // Create nodes and connections
  createNodes();
  createConnections();

  // Event listeners
  window.addEventListener("resize", onWindowResize);
  renderer.domElement.addEventListener("click", onCanvasClick);
  renderer.domElement.addEventListener("mousemove", onCanvasMouseMove);

  loading.value = false;
}

// Create 3D nodes
function createNodes() {
  const nodes = getNodes();

  nodes.forEach((nodeData) => {
    const group = new THREE.Group();
    group.userData = nodeData;

    // Main cube
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshStandardMaterial({
      color: colors[nodeData.type] || colors["web-service"],
      metalness: 0.5,
      roughness: 0.3,
      emissive: colors[nodeData.type] || colors["web-service"],
      emissiveIntensity: 0.2,
    });
    const cube = new THREE.Mesh(geometry, material);
    cube.castShadow = true;
    cube.receiveShadow = true;
    group.add(cube);

    // Wireframe overlay
    const wireframeGeometry = new THREE.EdgesGeometry(geometry);
    const wireframeMaterial = new THREE.LineBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.3,
    });
    const wireframe = new THREE.LineSegments(
      wireframeGeometry,
      wireframeMaterial,
    );
    group.add(wireframe);

    // Vulnerability indicator
    if (nodeData.vulnerabilities > 0) {
      const sphereGeometry = new THREE.SphereGeometry(0.15, 16, 16);
      const sphereMaterial = new THREE.MeshStandardMaterial({
        color: 0xef4444,
        emissive: 0xef4444,
        emissiveIntensity: 0.5,
      });
      const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
      sphere.position.set(0.6, 0.6, 0.6);
      group.add(sphere);

      // Pulsing animation
      gsap.to(sphere.scale, {
        x: 1.3,
        y: 1.3,
        z: 1.3,
        duration: 1,
        repeat: -1,
        yoyo: true,
        ease: "power1.inOut",
      });
    }

    // Position
    const pos = nodeData.position || { x: 0, y: 0, z: 0 };
    group.position.set(pos.x, pos.y, pos.z);

    // Entrance animation
    group.scale.set(0, 0, 0);
    gsap.to(group.scale, {
      x: 1,
      y: 1,
      z: 1,
      duration: 0.8,
      delay: Math.random() * 0.5,
      ease: "back.out(1.7)",
    });

    // Floating animation
    gsap.to(group.position, {
      y: pos.y + 0.2,
      duration: 2 + Math.random(),
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
    });

    // Rotation animation
    gsap.to(group.rotation, {
      y: Math.PI * 2,
      duration: 10 + Math.random() * 5,
      repeat: -1,
      ease: "none",
    });

    scene.add(group);
    nodeObjects.push(group);
  });
}

// Create connections between nodes
function createConnections() {
  const connections = getConnections();
  const nodes = getNodes();
  const nodeMap = {};

  nodes.forEach((node) => {
    nodeMap[node.id] = node;
  });

  connections.forEach((conn) => {
    const fromNode = nodeMap[conn.from];
    const toNode = nodeMap[conn.to];

    if (!fromNode || !toNode) return;

    const fromPos = fromNode.position || { x: 0, y: 0, z: 0 };
    const toPos = toNode.position || { x: 0, y: 0, z: 0 };

    // Create curved line
    const curve = new THREE.QuadraticBezierCurve3(
      new THREE.Vector3(fromPos.x, fromPos.y, fromPos.z),
      new THREE.Vector3(
        (fromPos.x + toPos.x) / 2,
        Math.max(fromPos.y, toPos.y) + 1,
        (fromPos.z + toPos.z) / 2,
      ),
      new THREE.Vector3(toPos.x, toPos.y, toPos.z),
    );

    const points = curve.getPoints(50);
    const geometry = new THREE.BufferGeometry().setFromPoints(points);

    const material = new THREE.LineBasicMaterial({
      color: conn.vulnerable ? 0xef4444 : 0x64748b,
      transparent: true,
      opacity: conn.vulnerable ? 0.8 : 0.4,
      linewidth: 2,
    });

    const line = new THREE.Line(geometry, material);
    scene.add(line);
    connectionLines.push(line);

    // Animated particles along connection
    if (conn.vulnerable) {
      createParticleFlow(curve, 0xef4444);
    } else {
      createParticleFlow(curve, 0x667eea);
    }
  });
}

// Create particle flow animation
function createParticleFlow(curve, color) {
  const particleGeometry = new THREE.SphereGeometry(0.05, 8, 8);
  const particleMaterial = new THREE.MeshBasicMaterial({
    color: color,
    transparent: true,
    opacity: 0.8,
  });
  const particle = new THREE.Mesh(particleGeometry, particleMaterial);

  scene.add(particle);

  // Animate particle along curve
  const animate = () => {
    let progress = 0;
    const duration = 3;

    const update = () => {
      progress += 0.01;
      if (progress > 1) progress = 0;

      const point = curve.getPoint(progress);
      particle.position.copy(point);

      setTimeout(update, (duration * 1000) / 100);
    };

    update();
  };

  animate();
}

// Animation loop
function animate() {
  animationFrameId = requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

// Window resize handler
function onWindowResize() {
  if (!canvasContainer.value) return;

  camera.aspect =
    canvasContainer.value.clientWidth / canvasContainer.value.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(
    canvasContainer.value.clientWidth,
    canvasContainer.value.clientHeight,
  );
}

// Mouse click handler
function onCanvasClick(event) {
  const rect = renderer.domElement.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(nodeObjects, true);

  if (intersects.length > 0) {
    const clickedObject = intersects[0].object.parent;
    if (clickedObject.userData) {
      selectedNode.value = clickedObject.userData;
      emit("node-selected", clickedObject.userData);

      // Highlight animation
      gsap.to(clickedObject.scale, {
        x: 1.2,
        y: 1.2,
        z: 1.2,
        duration: 0.3,
        yoyo: true,
        repeat: 1,
      });
    }
  }
}

// Mouse move handler for hover effects
function onCanvasMouseMove(event) {
  const rect = renderer.domElement.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(nodeObjects, true);

  // Reset all nodes
  nodeObjects.forEach((obj) => {
    if (obj.children[0].material) {
      obj.children[0].material.emissiveIntensity = 0.2;
    }
  });

  // Highlight hovered node
  if (intersects.length > 0) {
    const hoveredObject = intersects[0].object.parent;
    if (hoveredObject.children[0].material) {
      hoveredObject.children[0].material.emissiveIntensity = 0.5;
    }
    renderer.domElement.style.cursor = "pointer";
  } else {
    renderer.domElement.style.cursor = "default";
  }
}

// Control functions
function resetCamera() {
  gsap.to(camera.position, {
    x: 8,
    y: 6,
    z: 8,
    duration: 1,
    ease: "power2.inOut",
    onUpdate: () => {
      camera.lookAt(0, 0, 0);
    },
  });
}

function toggleAutoRotate() {
  autoRotate.value = !autoRotate.value;
  controls.autoRotate = autoRotate.value;
}

function toggleWireframe() {
  wireframeMode.value = !wireframeMode.value;
  nodeObjects.forEach((obj) => {
    if (obj.children[0].material) {
      obj.children[0].material.wireframe = wireframeMode.value;
    }
  });
}

function downloadScreenshot() {
  renderer.render(scene, camera);
  const dataURL = renderer.domElement.toDataURL("image/png");
  const link = document.createElement("a");
  link.href = dataURL;
  link.download = "3d-architecture-diagram.png";
  link.click();
  emit("download");
}

function toggleFullscreen() {
  isFullscreen.value = !isFullscreen.value;
  if (isFullscreen.value) {
    canvasContainer.value?.requestFullscreen?.();
  } else {
    document.exitFullscreen?.();
  }
}

// Lifecycle
onMounted(() => {
  setTimeout(() => {
    initScene();
    animate();
  }, 100);
});

onUnmounted(() => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }

  window.removeEventListener("resize", onWindowResize);

  if (renderer) {
    renderer.domElement.removeEventListener("click", onCanvasClick);
    renderer.domElement.removeEventListener("mousemove", onCanvasMouseMove);
    renderer.dispose();
  }

  if (scene) {
    scene.traverse((object) => {
      if (object.geometry) object.geometry.dispose();
      if (object.material) {
        if (Array.isArray(object.material)) {
          object.material.forEach((material) => material.dispose());
        } else {
          object.material.dispose();
        }
      }
    });
  }
});
</script>

<style scoped>
.architecture-3d-container {
  background: linear-gradient(
    135deg,
    rgba(10, 10, 10, 0.95) 0%,
    rgba(20, 20, 30, 0.95) 100%
  );
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  position: relative;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.diagram-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.diagram-header h3 {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  margin: 4px 0 0 0;
}

.diagram-controls {
  display: flex;
  gap: 8px;
}

.control-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: 1px solid rgba(139, 92, 246, 0.3);
  background: rgba(30, 30, 40, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 18px;
}

.control-btn:hover {
  background: rgba(139, 92, 246, 0.3);
  border-color: rgba(139, 92, 246, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
}

.diagram-legend {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  box-shadow: 0 0 10px currentColor;
}

.canvas-container {
  width: 100%;
  height: 600px;
  border-radius: 12px;
  overflow: hidden;
  background: radial-gradient(
    circle at center,
    rgba(102, 126, 234, 0.1) 0%,
    transparent 70%
  );
  position: relative;
}

.canvas-container.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;
  border-radius: 0;
}

.node-details-panel {
  position: absolute;
  top: 100px;
  right: 24px;
  width: 320px;
  background: linear-gradient(
    135deg,
    rgba(30, 30, 40, 0.98) 0%,
    rgba(20, 20, 30, 0.98) 100%
  );
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  z-index: 10;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.panel-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: white;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.close-btn:hover {
  background: rgba(239, 68, 68, 0.3);
}

.panel-content {
  padding: 16px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 14px;
}

.detail-row .label {
  color: rgba(255, 255, 255, 0.6);
  font-weight: 500;
}

.detail-row .value {
  color: white;
  font-weight: 400;
}

.vulnerabilities-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.vulnerabilities-section h4 {
  font-size: 14px;
  font-weight: 600;
  color: #ef4444;
  margin: 0 0 12px 0;
}

.vulnerability-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.vulnerability-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
}

.severity-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.severity-badge.critical {
  background: #ef4444;
  color: white;
}

.severity-badge.high {
  background: #f59e0b;
  color: white;
}

.severity-badge.medium {
  background: #eab308;
  color: white;
}

.severity-badge.low {
  background: #10b981;
  color: white;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(10, 10, 10, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  z-index: 100;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(139, 92, 246, 0.2);
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-overlay p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 16px;
  font-weight: 500;
}

@media (max-width: 768px) {
  .node-details-panel {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    top: auto;
    width: 100%;
    border-radius: 16px 16px 0 0;
  }

  .canvas-container {
    height: 400px;
  }
}
</style>
