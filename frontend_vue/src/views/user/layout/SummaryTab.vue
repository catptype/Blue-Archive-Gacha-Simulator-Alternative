<script setup lang="ts">
    import { defineAsyncComponent } from 'vue';
    import LoadSpinner from '@/components/base/LoadSpinner.vue';
    const WidgetKpi = defineAsyncComponent(() => import('../components/widget/Kpi.vue'));
    const TopStudentsWidget = defineAsyncComponent(() => import('../components/widget/TopStudents.vue'));
    const FirstR3 = defineAsyncComponent(() => import('../components/widget/FirstR3.vue'));
    // const RarityOriginChart = defineAsyncComponent(() => import('./widgets/RarityOriginChart.vue'));
    // const MilestoneTimelineWidget = defineAsyncComponent(() => import('./widgets/MilestoneTimelineWidget.vue'));
    // const PerformanceTableWidget = defineAsyncComponent(() => import('./widgets/PerformanceTableWidget.vue'));
    // const CollectionProgressionWidget = defineAsyncComponent(() => import('./widgets/CollectionProgressionWidget.vue'));
</script>

<template>
  <div class="flex flex-col gap-6">
    <!-- KPI Widgets -->
    <Suspense>
      <WidgetKpi />
      <template #fallback>
        <div class="w-full h-24 flex items-center justify-center bg-slate-700/50 rounded-lg text-slate-400">
          <LoadSpinner />
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
              <LoadSpinner />
            </div>
          </template>
        </Suspense>
      </div>
      <div class="lg:col-span-1">
        <Suspense>
          <FirstR3 />
          <template #fallback>
            <div class="w-full h-48 flex items-center justify-center bg-slate-700/50 rounded-lg text-slate-400">
              <LoadSpinner />
            </div>
          </template>
        </Suspense>
      </div>
    </div>

    <Suspense>
      <CollectionProgressionWidget />
      <template #fallback>
        <div class="w-full h-48 flex items-center justify-center bg-slate-700/50 rounded-lg text-slate-400">
          Loading Collection Data...
        </div>
      </template>
    </Suspense>
    
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

      <Suspense>
        <PerformanceTableWidget />
        <template #fallback>
          <div class="w-full h-72 flex items-center justify-center bg-slate-700/50 rounded-lg text-slate-400">
            Loading Performance Data...
          </div>
        </template>
      </Suspense>
      
    </div>
    <!-- ... other widgets ... -->
  </div>
</template>

