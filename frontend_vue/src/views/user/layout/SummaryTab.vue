<script setup lang="ts">
    import { defineAsyncComponent } from 'vue';
    import LoadSpinner from '@/components/base/LoadSpinner.vue';
    const Kpi = defineAsyncComponent(() => import('../components/summary/Kpi.vue'));
    const TopStudents = defineAsyncComponent(() => import('../components/summary/TopStudents.vue'));
    const FirstR3 = defineAsyncComponent(() => import('../components/summary/FirstR3.vue'));
    const CollectionChart = defineAsyncComponent(() => import('../components/summary/CollectionChart.vue'));
    const DistributionChart = defineAsyncComponent(() => import('../components/summary/DistributionChart.vue'));
    const Milestone = defineAsyncComponent(() => import('../components/summary/Milestone.vue'));
    const PerformanceTable = defineAsyncComponent(() => import('../components/summary/PerformanceTable.vue'));
</script>

<template>
  <div class="flex flex-col gap-6">
    <!-- KPI -->
    <Suspense>
      <Kpi />
      <template #fallback>
        <div class="w-full h-24 flex items-center justify-center bg-slate-700/50 rounded-lg">
          <LoadSpinner />
        </div>
      </template>
    </Suspense>

    <!-- Top-3 and First -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <div class="lg:col-span-3">
        <Suspense>
          <TopStudents />
          <template #fallback>
            <div class="w-full h-48 flex items-center justify-center bg-slate-700/50 rounded-lg">
              <LoadSpinner />
            </div>
          </template>
        </Suspense>
      </div>
      <div class="lg:col-span-1">
        <Suspense>
          <FirstR3 />
          <template #fallback>
            <div class="w-full h-48 flex items-center justify-center bg-slate-700/50 rounded-lg">
              <LoadSpinner />
            </div>
          </template>
        </Suspense>
      </div>
    </div>

    <!--  -->
    <Suspense>
      <CollectionChart />
      <template #fallback>
        <div class="w-full h-48 flex items-center justify-center bg-slate-700/50 rounded-lg">
          <LoadSpinner />
        </div>
      </template>
    </Suspense>
    
    <!-- Charts & Analysis Grid -->
    <div class="grid grid-cols-1 gap-6">

      <!-- Barchart breakdown -->
      <Suspense>
        <DistributionChart />
        <template #fallback>
          <div class="w-full h-72 flex items-center justify-center bg-slate-700/50 rounded-lg">
            <LoadSpinner />
          </div>
        </template>
      </Suspense>
      
      <!-- Milestone -->
      <Suspense>
        <Milestone />
        <template #fallback>
          <div class="w-full h-48 flex items-center justify-center bg-slate-700/50 rounded-lg">
            <LoadSpinner />
          </div>
        </template>
      </Suspense>

      <!-- Table -->
      <Suspense>
        <PerformanceTable />
        <template #fallback>
          <div class="w-full h-72 flex items-center justify-center bg-slate-700/50 rounded-lg">
            <LoadSpinner />
          </div>
        </template>
      </Suspense>
      
    </div>

  </div>
</template>

