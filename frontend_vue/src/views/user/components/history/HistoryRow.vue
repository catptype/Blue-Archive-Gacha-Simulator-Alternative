<script setup lang="ts">
  import { computed } from 'vue';
  import { type Transaction } from '@/types/web';
  import yellowStarImage from '@/assets/student_card/star_yellow.png'

  // 1. Assign props to a constant
  const props = defineProps<{ tx: Transaction }>();

  // 2. Logic is now easier to handle in script
  const formattedDate = computed(() => {
    return new Date(props.tx.create_on).toLocaleString();
  });

  const isR3 = computed(() => props.tx.student.rarity === 3);
</script>

<template>
  <tr
    class="border-b border-slate-700 transition-colors hover:bg-slate-800/50"
    :class="{ 'font-semibold bg-linear-to-r from-pink-500/20 via-purple-500/20 to-cyan-500/20': isR3 }"
  >
    <!-- Date -->
    <td class="p-2 text-center text-slate-300">{{ formattedDate }}</td>
    
    <!-- Banner image -->
    <td class="p-2">
      <div class="flex justify-center">
        <img 
          v-if="props.tx.banner.image_url" 
          :src="props.tx.banner.image_url" 
          :alt="props.tx.banner.name" 
          class="w-48 h-auto rounded-md object-cover border border-slate-700/50"
        >
        <span v-else class="text-slate-500">{{ props.tx.banner.name }}</span>
      </div>
    </td>
    
    <!-- Rarity -->
    <td class="p-2">
      <!-- <span v-for="i in props.tx.student.rarity" :key="i">★</span> -->
      <div class="flex justify-center gap-1">
        <img v-for="i in props.tx.student.rarity" 
          :key="i" :src="yellowStarImage" 
          alt="star" 
          class="w-6 h-6">
      </div>
      
    </td>
    
    <!-- Result -->
    <td class="p-2">
      <div class="flex justify-center">
        <!-- Container for the Character Portrait -->
        <div class="relative w-70 h-24 overflow-hidden">
          
          <!-- Student Portrait Image -->
          <img 
            v-if="props.tx.student.portrait_url"
            :src="props.tx.student.portrait_url" 
            :alt="props.tx.student.name"
            class="w-full h-full object-cover"
          />
          
          <!-- Fallback if no image exists -->
          <div v-else class="w-full h-full bg-slate-800 flex items-center justify-center text-xs text-slate-500">
            No Portrait
          </div>

          <!-- Absolute Overlay-->
          <div class="absolute inset-0 bg-linear-to-t from-black/80 via-black/5 to-transparent flex flex-row items-end justify-end p-1.5 text-sm text-right gap-1">
            
            <!-- Student Name -->
            <span class="leading-none text-white drop-shadow-md">
              {{ props.tx.student.name }}
            </span>

            <!-- Version -->
            <span 
              v-if="props.tx.student.version.name !== 'Original'" 
              class=" text-slate-300 leading-none"
            >
              ({{ props.tx.student.version.name }})
            </span>
          </div>

        </div>
      </div>
      
    </td>

  </tr>
</template>