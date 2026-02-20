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
    class="dashboard-tab flex items-center gap-2 px-4 lg:px-6 py-2 rounded-t-lg transition-colors duration-200 border-x border-t"
    active-class="bg-slate-700/50 border-slate-700 text-white font-semibold"
    inactive-class="bg-slate-900/50 border-transparent text-slate-400 hover:bg-slate-700/50"
  >
    <i :class="props.icon"></i>
    <span class="hidden sm:inline whitespace-nowrap">{{ props.label }}</span>
  </router-link>
</template>