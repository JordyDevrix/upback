<script setup lang="ts">
import HomeDetailsComponent from "@/components/HomeDetailsComponent.vue";
import {onMounted, ref} from "vue";
import UtilService from "@/services/UtilService";

const apiDetails = ref<any>(null);

onMounted(async () => {
  const res = await UtilService.getApiDetails();
  if (res.ok) {
    apiDetails.value = res.data;
  }
})
</script>

<template>
  <main>
    <header>
      <h1>Home</h1>
      <div class="title">
        <p>Welcome</p>
      </div>
    </header>
    <HomeDetailsComponent v-if="apiDetails" :apiDetails="apiDetails"/>
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