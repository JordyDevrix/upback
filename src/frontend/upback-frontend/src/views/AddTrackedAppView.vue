<script setup lang="ts">
import ConfigurationComponent from "@/components/ConfigurationComponent.vue";
</script>

<template>
  <main>
    <header>
      <h1>Add new tracked app</h1>
      <div class="title">
        <p>Add new tracked app</p>
      </div>
    </header>
    <ConfigurationComponent/>
  </main>
</template>

<style scoped lang="scss">
header {
  display: flex;
  flex-direction: column;
}

.title {
  display: flex;
  gap: 1em;
}
</style>