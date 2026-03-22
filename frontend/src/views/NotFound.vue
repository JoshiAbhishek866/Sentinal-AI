<template>
  <div class="not-found-page">
    <div class="container">
      <div class="not-found-content" data-testid="not-found-content">
        <div class="error-icon">
          <ShieldExclamationIcon class="icon-2xl nf-icon" />
        </div>

        <h1 class="error-title">404 - Page Not Found</h1>
        <p class="error-description">
          The page you're looking for seems to have been moved, deleted, or
          doesn't exist.
        </p>

        <div class="error-actions">
          <LuxuryButton @click="goHome" size="lg" data-testid="go-home-button">
            Return Home
          </LuxuryButton>
          <LuxuryButton
            @click="goBack"
            variant="outline"
            size="lg"
            data-testid="go-back-button"
          >
            Go Back
          </LuxuryButton>
        </div>

        <div class="helpful-links">
          <h3 class="links-title">You might be looking for:</h3>
          <div class="links-grid">
            <router-link
              v-for="link in helpfulLinks"
              :key="link.name"
              :to="link.path"
              class="helpful-link"
              :data-testid="`link-${link.name.toLowerCase().replace(/\s+/g, '-')}`"
            >
              <component :is="link.icon" class="icon-lg link-icon" />
              <span>{{ link.name }}</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import LuxuryButton from "@/components/LuxuryButton.vue";
import {
  ShieldExclamationIcon,
  HomeIcon,
  InformationCircleIcon,
  ChatBubbleLeftRightIcon,
  CalendarDaysIcon,
} from "@heroicons/vue/24/outline";

const router = useRouter();

const helpfulLinks = [
  { name: "Home", path: "/", icon: HomeIcon },
  { name: "About Us", path: "/about", icon: InformationCircleIcon },
  { name: "Blog", path: "/blog", icon: ChatBubbleLeftRightIcon },
  { name: "Book Demo", path: "/book-demo", icon: CalendarDaysIcon },
];

function goHome() {
  router.push("/");
}
function goBack() {
  router.go(-1);
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5rem 0;
  background: linear-gradient(
    135deg,
    rgba(139, 92, 246, 0.05),
    rgba(16, 185, 129, 0.05)
  );
}

.container {
  max-width: 56rem;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.not-found-content {
  text-align: center;
}

.error-icon {
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
}

.nf-icon {
  color: #8b5cf6;
}

.error-title {
  font-size: clamp(1.5rem, 4vw, 2.5rem);
  font-weight: 700;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #8b5cf6, #10b981);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.error-description {
  font-size: 1.125rem;
  color: #6b7280;
  margin-bottom: 3rem;
  max-width: 42rem;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.75;
}

.error-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 4rem;
  flex-wrap: wrap;
}

.helpful-links {
  margin-top: 4rem;
}

.links-title {
  font-size: clamp(0.75rem, 1.5vw, 1.1rem);
  font-weight: 700;
  margin-bottom: 2rem;
  color: #1a202c;
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.helpful-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem;
  border-radius: 0.75rem;
  text-decoration: none;
  transition:
    transform 0.3s,
    background 0.3s,
    color 0.3s,
    border-color 0.3s;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #6b7280;
}

.helpful-link:hover {
  transform: scale(1.05);
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
  border-color: rgba(139, 92, 246, 0.3);
}

.link-icon {
  color: currentColor;
}

@media (max-width: 640px) {
  .error-actions {
    flex-direction: column;
    gap: 0.75rem;
  }
  .links-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
}
</style>
