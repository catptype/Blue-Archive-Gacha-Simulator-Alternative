<script setup lang="ts">
import { useToastStore } from '@/stores/toast';
import ToastNotification from './Notification.vue';

const toastStore = useToastStore();
</script>

<template>
  <!-- This container is fixed to the top-right of the viewport -->
  <div class="fixed top-24 right-4 z-[100] flex flex-col items-end gap-2">
    <!-- 
      <TransitionGroup> is a built-in Vue component that applies
      animations when items are added or removed from a list.
    -->
    <TransitionGroup name="toast-slide" tag="div">
      <ToastNotification
        v-for="toast in toastStore.toasts"
        :key="toast.id"
        :toast="toast"
        @close="toastStore.removeToast(toast.id)"
      />
    </TransitionGroup>
  </div>
</template>

<style scoped>
/* These classes control the enter/leave animation for the toasts */
.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.4s ease;
}
.toast-slide-enter-from,
.toast-slide-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
/* This handles the smooth re-positioning of other toasts when one is removed */
.toast-slide-move {
  transition: transform 0.3s ease;
}
</style>