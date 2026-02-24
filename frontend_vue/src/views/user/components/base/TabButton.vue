<script setup lang="ts">
  const props = defineProps<{
    label: string;
    path: string;
    icon: string;
  }>();
</script>

<template>
  <router-link
    :key="props.label"
    :to="props.path"
    :title="props.label"
    class="flex items-center gap-2 px-4 py-2 rounded-t-lg transition-colors duration-200 border-x border-t border-slate-400 text-slate-400 hover:bg-slate-500"
    active-class="bg-cyan-400/40 text-white"
  >
    <i :class="props.icon"></i>
    <span class="hidden sm:inline whitespace-nowrap">{{ props.label }}</span>
  </router-link>
</template>