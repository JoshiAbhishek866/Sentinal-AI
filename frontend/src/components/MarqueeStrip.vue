<template>
  <section class="marquee-section">
    <div
      class="marquee-wrapper"
      @mouseenter="paused = true"
      @mouseleave="paused = false"
    >
      <!-- Track A + its clone for seamless loop -->
      <div class="marquee-track" :class="{ 'is-paused': paused }">
        <div class="marquee-inner" v-for="n in 2" :key="n">
          <div class="marquee-item" v-for="item in items" :key="item.label + n">
            <component
              :is="item.icon"
              class="marquee-icon"
              aria-hidden="true"
            />
            <span class="marquee-label">{{ item.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import {
  ShieldCheckIcon,
  LockClosedIcon,
  EyeIcon,
  BoltIcon,
  ServerStackIcon,
  FingerPrintIcon,
  BugAntIcon,
  CloudIcon,
  CpuChipIcon,
  KeyIcon,
} from "@heroicons/vue/24/solid";

const paused = ref(false);

const items = [
  { label: "Zero-Trust Security", icon: ShieldCheckIcon },
  { label: "End-to-End Encryption", icon: LockClosedIcon },
  { label: "Threat Intelligence", icon: EyeIcon },
  { label: "Real-Time Detection", icon: BoltIcon },
  { label: "SOC Automation", icon: ServerStackIcon },
  { label: "Identity & Access", icon: FingerPrintIcon },
  { label: "Malware Analysis", icon: BugAntIcon },
  { label: "Cloud Security", icon: CloudIcon },
  { label: "AI-Powered Defense", icon: CpuChipIcon },
  { label: "Key Management", icon: KeyIcon },
];
</script>

<style scoped>
/* ─── Section wrapper ──────────────────────────────────────────────────────── */
.marquee-section {
  width: 100%;
  background: #0a0a0a;
  border-top: 1px solid rgba(139, 92, 246, 0.2);
  border-bottom: 1px solid rgba(139, 92, 246, 0.2);
  overflow: hidden;
  padding: 0;
  position: relative;
  isolation: isolate; /* own stacking context */
  contain: layout style; /* confine repaints to this element */
}

/* Fade edges out */
.marquee-section::before,
.marquee-section::after {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  width: 12rem;
  z-index: 2;
  pointer-events: none;
}
.marquee-section::before {
  left: 0;
  background: linear-gradient(to right, #0d0d0d 0%, transparent 100%);
}
.marquee-section::after {
  right: 0;
  background: linear-gradient(to left, #0d0d0d 0%, transparent 100%);
}

/* ─── Scrolling wrapper ────────────────────────────────────────────────────── */
.marquee-wrapper {
  display: flex;
  width: 100%;
  cursor: default;
  padding: 1.5rem 0;
}

/* ─── Track = one complete set of items, duplicated via v-for ─────────────── */
.marquee-track {
  display: flex;
  flex-shrink: 0;
  animation: marquee-scroll 32s linear infinite;
  will-change: transform;
}

.marquee-track.is-paused {
  animation-play-state: paused;
}

/* Inner row: one copy of all items */
.marquee-inner {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

/* ─── Individual item ──────────────────────────────────────────────────────── */
.marquee-item {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  padding: 0 2.5rem;
  white-space: nowrap;
  position: relative;
  transition: opacity 0.25s ease;
}

/* Dot separator */
.marquee-item::after {
  content: "✦";
  position: absolute;
  right: 0;
  transform: translateX(50%);
  font-size: 0.5rem;
  color: rgba(139, 92, 246, 0.55);
}

.marquee-item:hover .marquee-label {
  color: #a78bfa;
}
.marquee-item:hover .marquee-icon {
  color: #a78bfa;
}

.marquee-icon {
  width: 1.1rem;
  height: 1.1rem;
  color: #00b090;
  flex-shrink: 0;
  transition: color 0.25s ease;
}

.marquee-label {
  font-family: var(--font-body);
  font-size: 0.85rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  color: #d1d5db;
  text-transform: uppercase;
  transition: color 0.25s ease;
}

/* ─── Keyframes ────────────────────────────────────────────────────────────── */
@keyframes marquee-scroll {
  0% {
    transform: translate3d(0, 0, 0);
  }
  100% {
    transform: translate3d(-50%, 0, 0);
  }
  /* -50%: track has 2 identical copies, so -50% = one full set */
}
</style>
