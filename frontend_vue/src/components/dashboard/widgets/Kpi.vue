<script setup lang="ts">
    import apiClient from '../../../services/client';
    import pyroxeneImage from '../../../assets/pyroxene.png';
    const { data } = await apiClient.get('/dashboard/summary/kpis');
</script>

<template>

<div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
    <div class="p-4 bg-slate-700/50 rounded-lg">
        <p class="text-sm text-slate-400">Total Pulls</p>
        <p class="text-3xl font-bold">{{ data.total_pulls }}</p>
    </div>

    <div class="sm:col-span-2 p-4 bg-slate-700/50 rounded-lg flex flex-col justify-center">
        <p class="text-sm text-slate-400">Pyroxene Spent</p>
        <div class="flex items-center justify-center gap-2 text-3xl font-bold">
            <img :src=pyroxeneImage class="h-8 w-8">
            <span>{{ data.total_pyroxene_spent }}</span>
        </div>
    </div>

    <div class="p-4 bg-gradient-to-br from-pink-400/50 via-purple-400/50 to-cyan-400/50 rounded-lg">
        <p class="text-sm font-semibold text-pink-300">★★★ Students</p>
        <p class="text-3xl font-bold text-white">{{ data.r3_count }}</p>
    </div>
    <div class="p-4 bg-yellow-500/50 rounded-lg">
        <p class="text-sm font-semibold text-yellow-300">★★ Students</p>
        <p class="text-3xl font-bold text-white">{{ data.r2_count }}</p>
    </div>
    <div class="p-4 bg-blue-500/50 rounded-lg">
        <p class="text-sm font-semibold text-blue-300">★ Students</p>
        <p class="text-3xl font-bold text-white">{{ data.r1_count }}</p>
    </div>

  </div>
</template>
