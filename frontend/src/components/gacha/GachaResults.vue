<script setup lang="ts">
    import { ref, onMounted } from 'vue';
    import ResultCard from './ResultCard.vue';

    defineProps<{ results: any[] }>();
    const emit = defineEmits(['close']);

    const resultCards = ref<InstanceType<typeof ResultCard>[]>([]);

    onMounted(() => {
        // Sort results so 3-stars are revealed first
        const sortedIndices = props.results
            .map((result, index) => ({ ...result, originalIndex: index }))
            .sort((a, b) => b.student_rarity - a.student_rarity)
            .map(result => result.originalIndex);

        // Reveal cards one by one based on the sorted order
        sortedIndices.forEach((cardIndex, revealIndex) => {
            const cardInstance = resultCards.value[cardIndex];
            if (cardInstance) {
                setTimeout(() => {cardInstance.reveal();}, revealIndex * 250); // Stagger the animation
            }
        });
    });
</script>

<template>
  <div class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="relative w-full max-w-7xl h-[90vh] bg-slate-800/80 border border-slate-600 p-6 rounded-lg">
      <div class="grid grid-cols-5 grid-rows-2 gap-4 h-full">
        <ResultCard
          v-for="(student, index) in results"
          :key="student.student_id + '-' + index"
          :student="student"
          ref="resultCards"
        />
      </div>
      <button @click="emit('close')" class="absolute top-2 right-2 text-slate-400 hover:text-white z-10 text-4xl leading-none">&times;</button>
    </div>
  </div>
</template>