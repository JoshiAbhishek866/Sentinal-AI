<template>
  <div class="pricing-page">
    <DynamicSEO page="pricing" />
    <!-- Hero Section -->
    <section class="pricing-hero">
      <div class="hero-content">
        <h1 class="hero-title">{{ hero.title }}</h1>
        <p class="hero-subtitle">{{ hero.subtitle }}</p>

        <!-- Billing Toggle -->
        <div class="billing-toggle">
          <span :class="{ active: !isAnnual }">Monthly</span>
          <button @click="isAnnual = !isAnnual" class="toggle-switch">
            <span class="toggle-slider" :class="{ annual: isAnnual }"></span>
          </button>
          <span :class="{ active: isAnnual }">
            Annual
            <span class="save-badge">Save {{ hero.savingsPercent }}%</span>
          </span>
        </div>
      </div>
    </section>

    <!-- Pricing Cards -->
    <section class="pricing-cards">
      <div class="container">
        <div class="cards-grid">
          <!-- Dynamic Pricing Cards -->
          <div
            v-for="(plan, index) in plans"
            :key="index"
            class="pricing-card"
            :class="{ popular: plan.isPopular }"
          >
            <div v-if="plan.isPopular" class="popular-badge">Most Popular</div>
            <div class="card-header">
              <h3 class="plan-name">{{ plan.name }}</h3>
              <p class="plan-description">{{ plan.description }}</p>
            </div>

            <div class="card-price">
              <template v-if="!plan.isCustom">
                <span class="currency">$</span>
                <span class="amount">{{
                  isAnnual ? plan.annualPrice : plan.monthlyPrice
                }}</span>
                <span class="period">/month</span>
              </template>
              <template v-else>
                <span class="amount custom">Custom</span>
              </template>
            </div>

            <ul class="features-list">
              <li v-for="(feature, fIndex) in plan.features" :key="fIndex">
                <CheckIcon class="check-icon" /> {{ feature }}
              </li>
            </ul>

            <button
              class="cta-button"
              :class="plan.isPopular ? 'primary' : 'secondary'"
            >
              {{ plan.ctaText }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Comparison -->
    <section class="features-comparison">
      <div class="container">
        <h2 class="section-title">Compare Plans</h2>

        <div class="comparison-table">
          <table>
            <thead>
              <tr>
                <th class="feature-column">Features</th>
                <th>Starter</th>
                <th class="popular-column">Professional</th>
                <th>Enterprise</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in comparison" :key="index">
                <td class="feature-name">{{ row.feature }}</td>
                <td>
                  <template v-if="row.starter === 'true'">
                    <CheckIcon class="check-icon" />
                  </template>
                  <template v-else-if="row.starter === 'false'">
                    <XMarkIcon class="x-icon" />
                  </template>
                  <template v-else>
                    {{ row.starter }}
                  </template>
                </td>
                <td>
                  <template v-if="row.professional === 'true'">
                    <CheckIcon class="check-icon" />
                  </template>
                  <template v-else-if="row.professional === 'false'">
                    <XMarkIcon class="x-icon" />
                  </template>
                  <template v-else>
                    {{ row.professional }}
                  </template>
                </td>
                <td>
                  <template v-if="row.enterprise === 'true'">
                    <CheckIcon class="check-icon" />
                  </template>
                  <template v-else-if="row.enterprise === 'false'">
                    <XMarkIcon class="x-icon" />
                  </template>
                  <template v-else>
                    {{ row.enterprise }}
                  </template>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section">
      <div class="container">
        <h2 class="section-title">Frequently Asked Questions</h2>

        <div class="faq-grid">
          <div v-for="(item, index) in faq" :key="index" class="faq-item">
            <h3 class="faq-question">{{ item.question }}</h3>
            <p class="faq-answer">{{ item.answer }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-content">
        <h2 class="cta-title">{{ cta.title }}</h2>
        <p class="cta-subtitle">{{ cta.subtitle }}</p>
        <div class="cta-buttons">
          <button class="cta-button primary large">
            {{ cta.primaryButton }}
          </button>
          <button class="cta-button secondary large">
            {{ cta.secondaryButton }}
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { CheckIcon, XMarkIcon } from "@heroicons/vue/24/solid";
import { useContentStore } from "@/stores/content";
import DynamicSEO from "@/components/DynamicSEO.vue";

const contentStore = useContentStore();
const isAnnual = ref(false);

// Fetch pricing content on mount
onMounted(() => {
  contentStore.fetchPricing();
});

// Default fallback data
const defaultHero = {
  title: "Simple, Transparent Pricing",
  subtitle: "Choose the perfect plan for your organization's security needs",
  savingsPercent: 20,
};

const defaultPlans = [
  {
    name: "Starter",
    description: "Perfect for small teams getting started",
    monthlyPrice: 49,
    annualPrice: 39,
    features: [
      "Up to 10 scans per month",
      "Basic vulnerability detection",
      "Email support",
      "1 user account",
      "30-day scan history",
      "PDF reports",
    ],
    ctaText: "Get Started",
    isPopular: false,
    isCustom: false,
  },
  {
    name: "Professional",
    description: "For growing teams with advanced needs",
    monthlyPrice: 99,
    annualPrice: 79,
    features: [
      "Unlimited scans",
      "Advanced threat detection",
      "Priority support (24/7)",
      "Up to 5 user accounts",
      "1-year scan history",
      "Custom reports & exports",
      "API access",
      "Compliance templates",
    ],
    ctaText: "Get Started",
    isPopular: true,
    isCustom: false,
  },
  {
    name: "Enterprise",
    description: "For large organizations with custom requirements",
    monthlyPrice: 0,
    annualPrice: 0,
    features: [
      "Everything in Professional",
      "Unlimited scans & users",
      "Dedicated account manager",
      "Custom integrations",
      "On-premise deployment",
      "Advanced analytics",
      "SLA guarantees",
      "Custom training",
      "White-label options",
    ],
    ctaText: "Contact Sales",
    isPopular: false,
    isCustom: true,
  },
];

const defaultComparison = [
  {
    feature: "Scans per month",
    starter: "10",
    professional: "Unlimited",
    enterprise: "Unlimited",
  },
  {
    feature: "User accounts",
    starter: "1",
    professional: "5",
    enterprise: "Unlimited",
  },
  {
    feature: "Scan history",
    starter: "30 days",
    professional: "1 year",
    enterprise: "Unlimited",
  },
  {
    feature: "Support",
    starter: "Email",
    professional: "24/7 Priority",
    enterprise: "Dedicated Manager",
  },
  {
    feature: "API Access",
    starter: "false",
    professional: "true",
    enterprise: "true",
  },
];

const defaultFaq = [
  {
    question: "Can I change plans later?",
    answer:
      "Yes! You can upgrade or downgrade your plan at any time. Changes will be reflected in your next billing cycle.",
  },
  {
    question: "What payment methods do you accept?",
    answer:
      "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and wire transfers for Enterprise plans.",
  },
  {
    question: "Is there a free trial?",
    answer:
      "Yes! All plans come with a 14-day free trial. No credit card required to start.",
  },
  {
    question: "What happens after my trial ends?",
    answer:
      "You'll be automatically enrolled in your selected plan. You can cancel anytime before the trial ends with no charges.",
  },
  {
    question: "Do you offer refunds?",
    answer:
      "Yes, we offer a 30-day money-back guarantee. If you're not satisfied, contact us for a full refund.",
  },
  {
    question: "Can I get a custom plan?",
    answer:
      "Absolutely! Contact our sales team to discuss custom requirements and pricing for your organization.",
  },
];

const defaultCta = {
  title: "Ready to secure your digital assets?",
  subtitle: "Start your 14-day free trial today. No credit card required.",
  primaryButton: "Start Free Trial",
  secondaryButton: "Contact Sales",
};

// Computed properties with fallbacks
const hero = computed(() => contentStore.pricing?.hero || defaultHero);
const plans = computed(() => contentStore.pricing?.plans || defaultPlans);
const comparison = computed(
  () => contentStore.pricing?.comparison || defaultComparison,
);
const faq = computed(() => contentStore.pricing?.faq || defaultFaq);
const cta = computed(() => contentStore.pricing?.cta || defaultCta);
</script>

<style scoped>
.pricing-page {
  min-height: 100vh;
  background: #ffffff;
}

/* Hero Section */
.pricing-hero {
  padding: 120px 20px 80px;
  text-align: center;
  /* background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%); */
  position: relative;
  overflow: hidden;
}

/* */

.pricing-hero::before {
  content: "";
  position: absolute;
  top: -50%;
  right: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(
    circle,
    rgba(139, 92, 246, 0.1) 0%,
    transparent 70%
  );
  border-radius: 50%;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 20px;
  line-height: 1.2;
}

.gradient-text {
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #666;
  margin-bottom: 40px;
}

/* Billing Toggle */
.billing-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  font-size: 1rem;
  font-weight: 600;
  color: #666;
}

.billing-toggle span {
  transition: all 0.3s ease;
}

.billing-toggle span.active {
  color: #8b5cf6;
}

.toggle-switch {
  position: relative;
  width: 60px;
  height: 30px;
  background: #e0e0e0;
  border-radius: 30px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-slider {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 24px;
  height: 24px;
  background: #ffffff;
  border-radius: 50%;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-slider.annual {
  transform: translateX(30px);
  background: #8b5cf6;
}

.save-badge {
  display: inline-block;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  margin-left: 8px;
  font-weight: 700;
}

/* Pricing Cards */
.pricing-cards {
  padding: 80px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.pricing-card {
  background: #ffffff;
  border: 2px solid #e5e7eb;
  border-radius: 20px;
  padding: 40px 30px;
  position: relative;
  transition: all 0.3s ease;
}

.pricing-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 60px rgba(139, 92, 246, 0.2);
  border-color: #8b5cf6;
}

.pricing-card.popular {
  border-color: #8b5cf6;
  border-width: 3px;
  transform: scale(1.05);
}

.popular-badge {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  color: white;
  padding: 8px 24px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
}

.card-header {
  margin-bottom: 30px;
}

.plan-name {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 10px;
}

.plan-description {
  color: #666;
  font-size: 0.95rem;
}

.card-price {
  margin-bottom: 30px;
  display: flex;
  align-items: baseline;
  gap: 5px;
}

.currency {
  font-size: 1.5rem;
  color: #8b5cf6;
  font-weight: 600;
}

.amount {
  font-size: 3.5rem;
  font-weight: 800;
  color: #1a1a1a;
}

.amount.custom {
  font-size: 2.5rem;
}

.period {
  font-size: 1rem;
  color: #666;
}

.features-list {
  list-style: none;
  padding: 0;
  margin: 0 0 30px 0;
}

.features-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  color: #333;
  font-size: 0.95rem;
  border-bottom: 1px solid #f0f0f0;
}

.check-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
  flex-shrink: 0;
}

.x-icon {
  width: 20px;
  height: 20px;
  color: #ef4444;
  flex-shrink: 0;
}

/* CTA Buttons */
.cta-button {
  width: 100%;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.cta-button.primary {
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
}

.cta-button.secondary {
  background: transparent;
  color: #8b5cf6;
  border: 2px solid #8b5cf6;
}

.cta-button.secondary:hover {
  background: #8b5cf6;
  color: white;
}

.cta-button.large {
  padding: 18px 40px;
  font-size: 1.1rem;
  width: auto;
}

/* Features Comparison */
.features-comparison {
  padding: 80px 20px;
  background: #f9fafb;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  text-align: center;
  color: #1a1a1a;
  margin-bottom: 50px;
}

.comparison-table {
  overflow-x: auto;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

table {
  width: 100%;
  background: white;
  border-collapse: collapse;
}

thead {
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  color: white;
}

th {
  padding: 20px;
  text-align: left;
  font-weight: 700;
  font-size: 1.1rem;
}

.popular-column {
  background: rgba(255, 255, 255, 0.2);
}

td {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  color: #333;
}

.feature-name {
  font-weight: 600;
  color: #1a1a1a;
}

/* FAQ Section */
.faq-section {
  padding: 80px 20px;
}

.faq-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

.faq-item {
  background: white;
  padding: 30px;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.faq-item:hover {
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.15);
  border-color: #8b5cf6;
}

.faq-question {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 15px;
}

.faq-answer {
  color: #666;
  line-height: 1.6;
}

/* CTA Section */
.cta-section {
  padding: 100px 20px;
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  text-align: center;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
  margin-bottom: 20px;
}

.cta-subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 40px;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-section .cta-button.primary {
  background: white;
  color: #8b5cf6;
}

.cta-section .cta-button.secondary {
  background: transparent;
  color: white;
  border-color: white;
}

.cta-section .cta-button.secondary:hover {
  background: white;
  color: #8b5cf6;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .pricing-card.popular {
    transform: scale(1);
  }

  .faq-grid {
    grid-template-columns: 1fr;
  }

  .cta-title {
    font-size: 2rem;
  }

  .comparison-table {
    font-size: 0.875rem;
  }

  th,
  td {
    padding: 12px;
  }
}
</style>
