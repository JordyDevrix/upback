<script setup lang="ts">

import TrackedAppsComponent from "@/components/TrackedAppsComponent.vue";
</script>

<template>
  <div class="background-layer"></div>
  <main>
    <header>
      <h1>Tracked Applications</h1>
      <div class="title">
        <p class="back">Applications</p>
      </div>
    </header>
    <TrackedAppsComponent/>
  </main>
</template>

<style scoped lang="scss">
header {
  display: flex;
  flex-direction: column;
}
</style>