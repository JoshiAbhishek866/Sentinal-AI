<template>
  <div class="blog-page">
    <DynamicSEO page="blog" />
    <div class="container">
      <!-- Hero Section -->
      <section class="blog-hero" data-testid="blog-hero">
        <h1 class="heading-luxury">Security Insights & Updates</h1>
        <p class="hero-subtitle">
          Stay informed with the latest cybersecurity trends, threat analysis,
          and best practices from our security experts
        </p>
      </section>

      <!-- Blog Posts Grid -->
      <section class="blog-posts" data-testid="blog-posts">
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner-large"></div>
          <p>Loading articles...</p>
        </div>

        <div v-else class="posts-grid">
          <article
            v-for="post in posts"
            :key="post.id"
            class="post-card glass"
            @click="readPost(post)"
            :data-testid="`blog-post-${post.id}`"
          >
            <div class="post-image">
              <img :src="post.image" :alt="post.title" />
              <div class="post-overlay">
                <span class="read-time">{{ post.readTime }}</span>
              </div>
            </div>

            <div class="post-content">
              <div class="post-meta">
                <span class="post-author">{{ post.author }}</span>
                <span class="post-date">{{
                  formatDate(post.publishedDate)
                }}</span>
              </div>

              <h2 class="post-title">{{ post.title }}</h2>
              <p class="post-excerpt">{{ post.excerpt }}</p>

              <div class="post-tags">
                <span v-for="tag in post.tags" :key="tag" class="tag">
                  {{ tag }}
                </span>
              </div>
            </div>
          </article>
        </div>

        <!-- Load More Button -->
        <div v-if="hasMore && !loading" class="load-more-container">
          <LuxuryButton
            @click="loadMore"
            :loading="loadingMore"
            data-testid="load-more-button"
          >
            Load More Articles
          </LuxuryButton>
        </div>
      </section>

      <!-- Newsletter Signup -->
      <section
        class="newsletter-section glass"
        data-testid="newsletter-section"
      >
        <div class="newsletter-content">
          <h2 class="newsletter-title">Stay Updated</h2>
          <p class="newsletter-description">
            Get the latest security insights and threat updates delivered to
            your inbox
          </p>
          <form @submit.prevent="subscribeNewsletter" class="newsletter-form">
            <input
              v-model="email"
              type="email"
              placeholder="Enter your email address"
              required
              class="newsletter-input"
              data-testid="newsletter-email-input"
            />
            <LuxuryButton
              type="submit"
              :loading="subscribing"
              data-testid="newsletter-subscribe-button"
            >
              Subscribe
            </LuxuryButton>
          </form>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import LuxuryButton from "@/components/LuxuryButton.vue";
import DynamicSEO from "@/components/DynamicSEO.vue";

const router = useRouter();
const backendBaseUrl = (
  import.meta.env.VITE_BACKEND_URL || "http://localhost:8000"
).replace(/\/$/, "");
const API_BASE = `${backendBaseUrl}/api`;

const posts = ref([]);
const loading = ref(true);
const loadingMore = ref(false);
const hasMore = ref(true);
const email = ref("");
const subscribing = ref(false);
const currentOffset = ref(0);

async function fetchBlogPosts() {
  try {
    const response = await axios.get(
      `${API_BASE}/blog?limit=6&offset=${currentOffset.value}`,
    );

    if (currentOffset.value === 0) {
      posts.value = response.data.posts;
    } else {
      posts.value.push(...response.data.posts);
    }

    hasMore.value = response.data.hasMore;
    currentOffset.value += response.data.posts.length;
  } catch (error) {
    console.error("Failed to fetch blog posts:", error);
  }
}

async function loadMore() {
  loadingMore.value = true;
  await fetchBlogPosts();
  loadingMore.value = false;
}

function readPost(post) {
  // Navigate to blog post detail (you can implement this route)
  console.log("Reading post:", post.title);
}

async function subscribeNewsletter() {
  if (!email.value) return;

  subscribing.value = true;

  try {
    // Mock newsletter subscription
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Show success message (you can implement toast notifications)
    console.log("Newsletter subscription successful for:", email.value);
    email.value = "";
  } catch (error) {
    console.error("Newsletter subscription failed:", error);
  } finally {
    subscribing.value = false;
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

onMounted(async () => {
  await fetchBlogPosts();
  loading.value = false;
});
</script>

<style scoped>
.blog-page {
  @apply py-20;
  min-height: 100vh;
}

.container {
  @apply max-w-7xl mx-auto px-6 space-y-16;
}

/* Hero Section */
.blog-hero {
  @apply text-center py-16;
}

.hero-subtitle {
  @apply text-2xl text-gray-600 mt-6 max-w-3xl mx-auto leading-relaxed;
}

/* Loading */
.loading-container {
  @apply text-center py-20;
}

.loading-container p {
  @apply mt-4 text-gray-600;
}

/* Blog Posts */
.posts-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8;
  margin-top: 11rem !important;
}

.post-card {
  @apply rounded-xl overflow-hidden cursor-pointer transition-all duration-300 hover:scale-105;
}

.post-image {
  @apply relative aspect-video overflow-hidden;
}

.post-image img {
  @apply w-full h-full object-cover;
}

.post-overlay {
  @apply absolute top-4 right-4;
}

.read-time {
  @apply px-3 py-1 text-xs font-medium rounded-full bg-black bg-opacity-70 text-white;
}

.post-content {
  @apply p-6;
}

.post-meta {
  @apply flex items-center justify-between text-sm text-gray-500 mb-3;
}

.post-title {
  @apply text-xl font-bold mb-3 leading-tight;
  color: #1a202c;
}

.post-excerpt {
  @apply text-gray-600 mb-4 leading-relaxed;
}

.post-tags {
  @apply flex flex-wrap gap-2;
}

.tag {
  @apply px-3 py-1 text-xs font-medium rounded-full;
  background: linear-gradient(
    135deg,
    rgba(139, 92, 246, 0.2),
    rgba(16, 185, 129, 0.2)
  );
  color: #8b5cf6;
}

/* Load More */
.load-more-container {
  @apply text-center py-12;
}

/* Newsletter Section */
.newsletter-section {
  @apply p-12 text-center rounded-2xl;
}

.newsletter-title {
  @apply text-3xl font-bold mb-4;
  color: #1a202c;
}

.newsletter-description {
  @apply text-lg text-gray-600 mb-8 max-w-2xl mx-auto;
}

.newsletter-form {
  @apply flex flex-col sm:flex-row gap-4 max-w-md mx-auto;
}

.newsletter-input {
  @apply flex-1 px-4 py-3 rounded-lg transition-all duration-300;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
}

.newsletter-input:focus {
  @apply outline-none ring-2 ring-purple-500;
  background: rgba(255, 255, 255, 0.8);
  border-color: #8b5cf6;
}

.newsletter-input::placeholder {
  @apply text-gray-500;
}

/* Responsive Design */
@media (max-width: 768px) {
  .posts-grid {
    @apply grid-cols-1 gap-6;
  }

  .newsletter-form {
    @apply flex-col gap-3;
  }
}
</style>
