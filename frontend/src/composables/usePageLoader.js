import { ref } from "vue";

// Shared singleton state — true once the intro loader finishes
export const pageLoaded = ref(false);
