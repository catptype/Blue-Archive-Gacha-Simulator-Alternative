<script setup lang="ts">
    import { defineAsyncComponent } from 'vue';

    // Use defineAsyncComponent for better code splitting.
    // Vue will only download the code for a widget when it's needed.
    const KpiWidget = defineAsyncComponent(() => import('./widgets/Kpi.vue'));
    const TopStudentsWidget = defineAsyncComponent(() => import('./widgets/TopStudents.vue'));
    const FirstPullWidget = defineAsyncComponent(() => import('./widgets/FirstPullWidget.vue'));
    // const OverallRarityChart = defineAsyncComponent(() => import('./widgets/OverallRarityChart.vue'));
    // const BannerBreakdownChart = defineAsyncComponent(() => import('./widgets/BannerBreakdownChart.vue'));
    const RarityOriginChart = defineAsyncComponent(() => import('./widgets/RarityOriginChart.vue'));
    const MilestoneTimelineWidget = defineAsyncComponent(() => import('./widgets/MilestoneTimelineWidget.vue'));
</script>

<template>
  <div class="flex flex-col gap-6">
    <!-- KPI Widgets -->
    <Suspense>
      <KpiWidget />
      <template #fallback>
        <div class="w-full h-24 flex items-center justify-center bg-slate-700/50 rounded-lg text-slate-400">
          Loading KPIs...
        </div>
      </template>
    </Suspense>

    <!-- "Hall of Fame" Row -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <div class="lg:col-span-3">
        <Suspense>
          <TopStudentsWidget />
          <template #fallback>
            <div class="w-full h-48 flex items-center justify-center bg-slate-700/50 rounded-lg text-slate-400">
              Loading Top Students...
            </div>
          </template>
        </Suspense>
      </div>
      <div class="lg:col-span-1">
        <Suspense>
          <FirstPullWidget />
          <template #fallback>
            <div class="w-full h-48 flex items-center justify-center bg-slate-700/50 rounded-lg text-slate-400">
              Loading First Pull...
            </div>
          </template>
        </Suspense>
      </div>
    </div>
    
    <!-- Charts & Analysis Grid -->
    <div class="grid grid-cols-1 gap-6">

      <!-- Barchart breakdown -->
      <Suspense>
        <RarityOriginChart />
        <template #fallback>
          <div class="w-full h-72 flex items-center justify-center bg-slate-700/50 rounded-lg text-slate-400">
            Loading Chart...
          </div>
        </template>
      </Suspense>
      
      <Suspense>
        <MilestoneTimelineWidget />
        <template #fallback>
          <div class="w-full h-48 flex items-center justify-center bg-slate-700/50 rounded-lg text-slate-400">
            Loading Timeline...
          </div>
        </template>
      </Suspense>
      
    </div>
    <!-- ... other widgets ... -->
  </div>
</template>

