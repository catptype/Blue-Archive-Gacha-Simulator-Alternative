<script setup lang="ts">
import { computed } from 'vue';

// Define props inline using TypeScript literal types for the theme
const props = defineProps<{
  label: string;
  value?: string | number;
  theme?: 'default' | 'r3' | 'r2' | 'r1';
}>();

// Map themes to specific CSS classes
const themeClasses = {
  default: {
    card: 'bg-slate-700/50',
    label: 'text-slate-400'
  },
  r3: {
    card: 'bg-linear-to-br from-pink-400/50 via-purple-400/50 to-cyan-400/50',
    label: 'font-semibold text-pink-300'
  },
  r2: {
    card: 'bg-yellow-500/50',
    label: 'font-semibold text-yellow-300'
  },
  r1: {
    card: 'bg-blue-500/50',
    label: 'font-semibold text-blue-300'
  }
};

// Compute styles based on the theme prop (falling back to 'default')
const currentTheme = computed(() => themeClasses[props.theme || 'default']);
</script>

<template>
  <div :class="['p-4 rounded-lg flex flex-col justify-center', currentTheme.card]">
    <p :class="['text-sm mb-1', currentTheme.label]">{{ label }}</p>
    <div class="text-3xl font-bold flex items-center justify-center gap-2">
      <slot>
        {{ value }}
      </slot>
    </div>
  </div>
</template>