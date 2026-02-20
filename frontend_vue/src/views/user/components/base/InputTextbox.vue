<script setup lang="ts">
  const model = defineModel<string>();
  defineOptions({
    inheritAttrs: false
  });
  defineProps<{
    label: string;
    type?: string;
  }>();
</script>

<template>
  <div class="mb-4">
    <label class="block text-slate-300 mb-2">{{ label }}</label>
    <input 
      v-model="model" 
      v-bind="$attrs"
      :type="type || 'text'" 
      maxlength="20"
      class="w-full p-2 rounded bg-slate-700 text-white border border-slate-600 focus:outline-none focus:ring-2 focus:ring-cyan-500"
    >
  </div>
</template>