<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
</script>
<template>
  <NavBar/>
  <router-view/>
</template>

<style lang="scss">
#app {
  font-family: "JetBrains Mono",serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
