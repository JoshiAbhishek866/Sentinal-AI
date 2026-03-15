<template>
  <div>
    <CCard class="mb-4">
      <CCardHeader class="d-flex justify-content-between align-items-center">
        <strong>Pricing Page Editor</strong>
        <div class="d-flex gap-2">
          <!-- <CButton color="secondary" variant="outline" @click="loadContent" :disabled="loading">
            <CSpinner v-if="loading" size="sm" class="me-1" />Reload
          </CButton> -->
          <CButton color="primary" @click="saveContent" :disabled="saving">
            <CSpinner v-if="saving" size="sm" class="me-2" />{{
              saving ? 'Saving...' : 'Save Changes'
            }}
          </CButton>
        </div>
      </CCardHeader>

      <CCardBody>
        <CAlert
          v-if="message"
          :color="
            messageType === 'success' ? 'success' : messageType === 'error' ? 'danger' : 'info'
          "
          dismissible
          @close="message = ''"
        >
          {{ message }}
        </CAlert>

        <!-- Hero Section -->
        <CCard class="mb-4">
          <CCardHeader><strong>Hero Section</strong></CCardHeader>
          <CCardBody>
            <div class="mb-3">
              <CFormLabel>Title</CFormLabel>
              <CFormInput v-model="content.hero.title" placeholder="Simple, Transparent Pricing" />
            </div>
            <div class="mb-3">
              <CFormLabel>Subtitle</CFormLabel>
              <CFormTextarea
                v-model="content.hero.subtitle"
                rows="2"
                placeholder="Choose the perfect plan..."
              />
            </div>
            <div class="mb-3">
              <CFormLabel>Annual Savings Percentage (%)</CFormLabel>
              <CFormInput
                v-model.number="content.hero.savingsPercent"
                type="number"
                placeholder="20"
                style="max-width: 150px"
              />
            </div>
          </CCardBody>
        </CCard>

        <!-- Pricing Plans -->
        <CCard class="mb-4">
          <CCardHeader><strong>Pricing Plans</strong></CCardHeader>
          <CCardBody>
            <div
              v-for="(plan, index) in content.plans"
              :key="index"
              class="border rounded p-3 mb-4"
            >
              <div class="d-flex justify-content-between align-items-center mb-3">
                <strong>{{ plan.name || `Plan ${index + 1}` }}</strong>
                <CFormCheck
                  :id="`popular-${index}`"
                  v-model="plan.isPopular"
                  label="Mark as Popular"
                />
              </div>

              <CRow class="mb-2">
                <CCol :md="4">
                  <div class="mb-3">
                    <CFormLabel>Plan Name</CFormLabel>
                    <CFormInput v-model="plan.name" placeholder="Starter" />
                  </div>
                </CCol>
                <CCol :md="8">
                  <div class="mb-3">
                    <CFormLabel>Description</CFormLabel>
                    <CFormInput
                      v-model="plan.description"
                      placeholder="Perfect for small teams..."
                    />
                  </div>
                </CCol>
              </CRow>

              <CRow class="mb-2">
                <CCol :md="3">
                  <div class="mb-3">
                    <CFormLabel>Monthly Price ($)</CFormLabel>
                    <CFormInput v-model.number="plan.monthlyPrice" type="number" placeholder="49" />
                  </div>
                </CCol>
                <CCol :md="3">
                  <div class="mb-3">
                    <CFormLabel>Annual Price ($)</CFormLabel>
                    <CFormInput v-model.number="plan.annualPrice" type="number" placeholder="39" />
                  </div>
                </CCol>
                <CCol :md="3">
                  <div class="mb-3">
                    <CFormLabel>CTA Button Text</CFormLabel>
                    <CFormInput v-model="plan.ctaText" placeholder="Get Started" />
                  </div>
                </CCol>
                <CCol :md="3">
                  <div class="mb-3">
                    <CFormLabel>&nbsp;</CFormLabel>
                    <div>
                      <CFormCheck
                        :id="`custom-${index}`"
                        v-model="plan.isCustom"
                        label="Show 'Custom' instead of price"
                      />
                    </div>
                  </div>
                </CCol>
              </CRow>

              <!-- Features -->
              <div class="mb-2"><strong>Features</strong></div>
              <div
                v-for="(feature, fIndex) in plan.features"
                :key="fIndex"
                class="d-flex gap-2 mb-2"
              >
                <CFormInput v-model="plan.features[fIndex]" placeholder="Feature description" />
                <CButton
                  color="danger"
                  size="sm"
                  @click="removeFeature(index, fIndex)"
                  type="button"
                >
                  <CIcon icon="cil-trash" />
                </CButton>
              </div>
              <CButton
                color="success"
                variant="outline"
                size="sm"
                @click="addFeature(index)"
                type="button"
              >
                <CIcon icon="cil-plus" class="me-1" />Add Feature
              </CButton>
            </div>
          </CCardBody>
        </CCard>

        <!-- Comparison Table -->
        <CCard class="mb-4">
          <CCardHeader><strong>Comparison Table</strong></CCardHeader>
          <CCardBody>
            <div
              v-for="(row, index) in content.comparison"
              :key="index"
              class="border rounded p-3 mb-3"
            >
              <div class="d-flex justify-content-between align-items-center mb-2">
                <strong>Row {{ index + 1 }}</strong>
                <CButton color="danger" size="sm" @click="removeComparison(index)" type="button">
                  <CIcon icon="cil-trash" />
                </CButton>
              </div>
              <CRow>
                <CCol :md="3">
                  <div class="mb-2">
                    <CFormLabel class="small">Feature Name</CFormLabel>
                    <CFormInput v-model="row.feature" size="sm" placeholder="Scans per month" />
                  </div>
                </CCol>
                <CCol :md="3">
                  <div class="mb-2">
                    <CFormLabel class="small">Starter</CFormLabel>
                    <CFormInput v-model="row.starter" size="sm" placeholder="10" />
                  </div>
                </CCol>
                <CCol :md="3">
                  <div class="mb-2">
                    <CFormLabel class="small">Professional</CFormLabel>
                    <CFormInput v-model="row.professional" size="sm" placeholder="Unlimited" />
                  </div>
                </CCol>
                <CCol :md="3">
                  <div class="mb-2">
                    <CFormLabel class="small">Enterprise</CFormLabel>
                    <CFormInput v-model="row.enterprise" size="sm" placeholder="Unlimited" />
                  </div>
                </CCol>
              </CRow>
            </div>
            <CButton
              color="primary"
              variant="outline"
              size="sm"
              @click="addComparison"
              type="button"
            >
              <CIcon icon="cil-plus" class="me-1" />Add Comparison Row
            </CButton>
          </CCardBody>
        </CCard>

        <!-- FAQ Section -->
        <CCard class="mb-4">
          <CCardHeader><strong>FAQ Section</strong></CCardHeader>
          <CCardBody>
            <div v-for="(faq, index) in content.faq" :key="index" class="border rounded p-3 mb-3">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <strong>FAQ {{ index + 1 }}</strong>
                <CButton color="danger" size="sm" @click="removeFaq(index)" type="button">
                  <CIcon icon="cil-trash" />
                </CButton>
              </div>
              <div class="mb-2">
                <CFormLabel>Question</CFormLabel>
                <CFormInput v-model="faq.question" placeholder="Can I change plans later?" />
              </div>
              <div class="mb-2">
                <CFormLabel>Answer</CFormLabel>
                <CFormTextarea
                  v-model="faq.answer"
                  rows="3"
                  placeholder="Yes! You can upgrade..."
                />
              </div>
            </div>
            <CButton color="primary" variant="outline" size="sm" @click="addFaq" type="button">
              <CIcon icon="cil-plus" class="me-1" />Add FAQ
            </CButton>
          </CCardBody>
        </CCard>

        <!-- CTA Section -->
        <CCard class="mb-4">
          <CCardHeader><strong>CTA Section</strong></CCardHeader>
          <CCardBody>
            <div class="mb-3">
              <CFormLabel>Title</CFormLabel>
              <CFormInput
                v-model="content.cta.title"
                placeholder="Ready to secure your digital assets?"
              />
            </div>
            <div class="mb-3">
              <CFormLabel>Subtitle</CFormLabel>
              <CFormTextarea
                v-model="content.cta.subtitle"
                rows="2"
                placeholder="Start your 14-day free trial today..."
              />
            </div>
            <CRow>
              <CCol :md="6">
                <div class="mb-3">
                  <CFormLabel>Primary Button Text</CFormLabel>
                  <CFormInput v-model="content.cta.primaryButton" placeholder="Start Free Trial" />
                </div>
              </CCol>
              <CCol :md="6">
                <div class="mb-3">
                  <CFormLabel>Secondary Button Text</CFormLabel>
                  <CFormInput v-model="content.cta.secondaryButton" placeholder="Contact Sales" />
                </div>
              </CCol>
            </CRow>
          </CCardBody>
        </CCard>
      </CCardBody>
    </CCard>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

const saving = ref(false)
const loading = ref(false)
const message = ref('')
const messageType = ref('success')

const content = ref({
  hero: {
    title: 'Simple, Transparent Pricing',
    subtitle: "Choose the perfect plan for your organization's security needs",
    savingsPercent: 20,
  },
  plans: [
    {
      name: 'Starter',
      description: 'Perfect for small teams getting started',
      monthlyPrice: 49,
      annualPrice: 39,
      features: [
        'Up to 10 scans per month',
        'Basic vulnerability detection',
        'Email support',
        '1 user account',
        '30-day scan history',
        'PDF reports',
      ],
      ctaText: 'Get Started',
      isPopular: false,
      isCustom: false,
    },
    {
      name: 'Professional',
      description: 'For growing teams with advanced needs',
      monthlyPrice: 99,
      annualPrice: 79,
      features: [
        'Unlimited scans',
        'Advanced threat detection',
        'Priority support (24/7)',
        'Up to 5 user accounts',
        '1-year scan history',
        'Custom reports & exports',
        'API access',
        'Compliance templates',
      ],
      ctaText: 'Get Started',
      isPopular: true,
      isCustom: false,
    },
    {
      name: 'Enterprise',
      description: 'For large organizations with custom requirements',
      monthlyPrice: 0,
      annualPrice: 0,
      features: [
        'Everything in Professional',
        'Unlimited scans & users',
        'Dedicated account manager',
        'Custom integrations',
        'On-premise deployment',
        'Advanced analytics',
        'SLA guarantees',
        'Custom training',
        'White-label options',
      ],
      ctaText: 'Contact Sales',
      isPopular: false,
      isCustom: true,
    },
  ],
  comparison: [
    {
      feature: 'Scans per month',
      starter: '10',
      professional: 'Unlimited',
      enterprise: 'Unlimited',
    },
    { feature: 'User accounts', starter: '1', professional: '5', enterprise: 'Unlimited' },
    {
      feature: 'Scan history',
      starter: '30 days',
      professional: '1 year',
      enterprise: 'Unlimited',
    },
    {
      feature: 'Support',
      starter: 'Email',
      professional: '24/7 Priority',
      enterprise: 'Dedicated Manager',
    },
    { feature: 'API Access', starter: 'false', professional: 'true', enterprise: 'true' },
  ],
  faq: [
    {
      question: 'Can I change plans later?',
      answer:
        'Yes! You can upgrade or downgrade your plan at any time. Changes will be reflected in your next billing cycle.',
    },
    {
      question: 'What payment methods do you accept?',
      answer:
        'We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and wire transfers for Enterprise plans.',
    },
    {
      question: 'Is there a free trial?',
      answer: 'Yes! All plans come with a 14-day free trial. No credit card required to start.',
    },
    {
      question: 'What happens after my trial ends?',
      answer:
        "You'll be automatically enrolled in your selected plan. You can cancel anytime before the trial ends with no charges.",
    },
    {
      question: 'Do you offer refunds?',
      answer:
        "Yes, we offer a 30-day money-back guarantee. If you're not satisfied, contact us for a full refund.",
    },
    {
      question: 'Can I get a custom plan?',
      answer:
        'Absolutely! Contact our sales team to discuss custom requirements and pricing for your organization.',
    },
  ],
  cta: {
    title: 'Ready to secure your digital assets?',
    subtitle: 'Start your 14-day free trial today. No credit card required.',
    primaryButton: 'Start Free Trial',
    secondaryButton: 'Contact Sales',
  },
})

async function loadContent() {
  loading.value = true
  try {
    const response = await axios.get(`${API_BASE}/content/pricing`)
    if (response.data && response.data.content) {
      content.value = response.data.content
      showMessage('Content loaded successfully', 'success')
    }
  } catch (error) {
    if (error.response?.status === 404) {
      showMessage('Using default content (not yet saved)', 'info')
    } else {
      showMessage('Error loading content', 'error')
    }
  } finally {
    loading.value = false
  }
}

async function saveContent() {
  saving.value = true
  try {
    await axios.put(`${API_BASE}/content/pricing`, { content: content.value })
    showMessage('Pricing content saved successfully!', 'success')
  } catch (error) {
    showMessage('Error saving content', 'error')
  } finally {
    saving.value = false
  }
}

function addFeature(planIndex) {
  content.value.plans[planIndex].features.push('')
}
function removeFeature(planIndex, featureIndex) {
  content.value.plans[planIndex].features.splice(featureIndex, 1)
}
function addComparison() {
  content.value.comparison.push({ feature: '', starter: '', professional: '', enterprise: '' })
}
function removeComparison(index) {
  content.value.comparison.splice(index, 1)
}
function addFaq() {
  content.value.faq.push({ question: '', answer: '' })
}
function removeFaq(index) {
  content.value.faq.splice(index, 1)
}
function showMessage(text, type = 'success') {
  message.value = text
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

onMounted(() => {
  loadContent()
})
</script>
