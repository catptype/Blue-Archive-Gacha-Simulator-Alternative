<script setup lang="ts">
  const link = "font-medium text-cyan-400 hover:text-cyan-300 hover:underline";
</script>

<template>
  <div class="p-4 text-center text-sm text-slate-400 bg-black/50 backdrop-blur-lg border border-slate-800 rounded-lg">
    <p>
      Developed by <a href="https://github.com/catptype/" :class="link"  target="_blank">Catptype</a>. This website is not affiliated with Nexon, Nexon Games, or Yostar.
    </p>
    <p>
      Source code: <a href="https://github.com/catptype/Blue-Archive-Gacha-Simulator-V2" :class="link" target="_blank">GitHub</a>
    </p>
  </div>
</template>