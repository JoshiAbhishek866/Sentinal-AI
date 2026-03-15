<template>
  <!-- This component doesn't render anything, just adds structured data -->
</template>

<script setup>
import { useHead } from "@unhead/vue";

const props = defineProps({
  type: {
    type: String,
    required: true,
  },
  data: {
    type: Object,
    required: true,
  },
});

const schema = {
  "@context": "https://schema.org",
  "@type": props.type,
  ...props.data,
};

useHead({
  script: [
    {
      type: "application/ld+json",
      children: JSON.stringify(schema),
    },
  ],
});
</script>
