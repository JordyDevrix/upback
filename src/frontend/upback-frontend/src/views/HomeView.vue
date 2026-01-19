<template>
  <main>
    <header>
      <h1>Home</h1>
      <div class="title">
        <p>Welcome</p>
      </div>
    </header>
  </main>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomeView',
});
</script>

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