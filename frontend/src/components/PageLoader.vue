<template>
  <Teleport to="body">
    <div class="preloader" ref="preloaderRef">
      <!-- Top half — slides upward -->
      <div class="preloader__panel preloader__panel--top" ref="topRef"></div>

      <!-- Bottom half — slides downward -->
      <div
        class="preloader__panel preloader__panel--bottom"
        ref="bottomRef"
      ></div>

      <!-- Counter displayed in the center seam -->
      <div class="preloader__counter" ref="counterRef">
        <span class="preloader__number" ref="numberRef">0</span>
        <span class="preloader__symbol">%</span>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { gsap } from "gsap";
import { pageLoaded } from "@/composables/usePageLoader";

const preloaderRef = ref(null);
const topRef = ref(null);
const bottomRef = ref(null);
const counterRef = ref(null);
const numberRef = ref(null);

onMounted(() => {
  const count = { value: 0 };

  const tl = gsap.timeline({ defaults: { ease: "power4.inOut" } });

  // 1 ─ Count 0 → 100 over 3.8 s
  tl.to(count, {
    value: 100,
    duration: 3.8,
    ease: "power2.inOut",
    onUpdate() {
      if (numberRef.value) {
        numberRef.value.textContent = Math.round(count.value);
      }
    },
  })

    // 2 ─ Fade counter out
    .to(
      counterRef.value,
      {
        opacity: 0,
        duration: 0.4,
        ease: "power1.out",
      },
      "-=0.15",
    )

    .to(
      topRef.value,
      {
        yPercent: -100,
        duration: 1.75,
      },
      "<",
    )
    .to(
      bottomRef.value,
      {
        yPercent: 100,
        duration: 1.75,
      },
      "<",
    )

    // 4 ─ Hide preloader container so it no longer blocks pointer events
    .set(preloaderRef.value, { display: "none" })

    // 5 ─ Signal the rest of the app
    .call(() => {
      pageLoaded.value = true;
    });
});
</script>

<style scoped>
.preloader {
  position: fixed;
  inset: 0;
  z-index: 9999;
  pointer-events: none;
}

/* Each panel is exactly half the viewport height */
.preloader__panel {
  position: absolute;
  left: 0;
  width: 100%;
  height: 50%;
  background: #0a0a0a;
}

.preloader__panel--top {
  top: 0;
}
.preloader__panel--bottom {
  bottom: 0;
}

/* Counter sits at the vertical seam between the two panels */
.preloader__counter {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: baseline;
  gap: 2px;
  color: #ffffff;
  font-family: var(--font-body, "Ubuntu", sans-serif);
  font-size: clamp(3rem, 8vw, 7rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1;
  will-change: opacity;
  /* Push counter above panels so it appears in the seam */
  z-index: 10000;
}

.preloader__symbol {
  font-size: 0.45em;
  opacity: 0.6;
  align-self: flex-start;
  margin-top: 0.2em;
}
</style>
