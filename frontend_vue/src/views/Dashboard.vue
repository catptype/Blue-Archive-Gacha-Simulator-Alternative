<template>
  <div class="relative min-h-screen w-full bg-black antialiased text-white pt-20">
    <Background />

    <div class="w-full max-w-7xl mx-auto px-4 lg:px-6 py-8">
      <div class="relative w-full">
        <!-- Tab Buttons -->
        <div class="absolute -top-px left-6 z-20 flex gap-1">
          <router-link
            v-for="tab in tabs"
            :key="tab.name"
            :to="tab.path"
            class="dashboard-tab px-6 py-2 rounded-t-lg transition-colors duration-200 border-x border-t"
            active-class="bg-slate-800/80 border-slate-700 text-white font-semibold"
            inactive-class="bg-slate-900/50 border-transparent text-slate-400 hover:bg-slate-700/50"
          >
            {{ tab.name }}
          </router-link>
        </div>

        <!-- Dynamic Content Panel -->
        <div class="relative z-10 w-full h-[80vh] bg-slate-800/80 backdrop-blur-sm border border-slate-700 rounded-lg flex flex-col pt-12">
          <div id="dashboard-content" class="flex-grow overflow-y-auto p-6">
            <!-- 
              This is the magic part. Vue Router will render the active
              child component (SummaryTab, HistoryTab, etc.) here.
            -->
            <router-view v-slot="{ Component }">
              <Transition name="fade" mode="out-in">
                <Suspense>
                  <component :is="Component" />
                  <template #fallback>
                    <div class="w-full h-full flex items-center justify-center">
                      <svg class="animate-spin h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
                    </div>
                  </template>
                </Suspense>
              </Transition>
            </router-view>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Background from '../components/Background.vue';

// Define the tabs for easy rendering
const tabs = [
  { name: 'Summary', path: '/dashboard/summary' },
  { name: 'History', path: '/dashboard/history' },
  { name: 'Collection', path: '/dashboard/collection' },
  { name: 'Achievements', path: '/dashboard/achievements' },
];
</script>

<style scoped>
/* Scoped styles from your template */
#dashboard-content::-webkit-scrollbar { width: 8px; }
#dashboard-content::-webkit-scrollbar-track { background: transparent; }
#dashboard-content::-webkit-scrollbar-thumb {
  background-color: rgba(107, 114, 128, 0.4);
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: padding-box;
}
#dashboard-content::-webkit-scrollbar-thumb:hover { background-color: rgba(156, 163, 175, 0.6); }
#dashboard-content { scrollbar-width: thin; scrollbar-color: rgba(107, 114, 128, 0.4) transparent; }

/* Transition for the router-view content */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>