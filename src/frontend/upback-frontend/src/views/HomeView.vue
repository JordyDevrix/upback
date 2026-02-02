<script setup lang="ts">
import HomeDetailsComponent from "@/components/HomeDetailsComponent.vue";
import {onMounted, ref} from "vue";
import UtilService from "@/services/UtilService";
import {useI18n} from 'vue-i18n'

const {t} = useI18n()
const apiDetails = ref<any>(null);

onMounted(async () => {
  const res = await UtilService.getApiDetails();
  if (res.ok) {
    apiDetails.value = res.data;
  }
})
</script>

<template>
  <div class="background-layer"></div>
  <main>
    <header>
      <h1>{{t('home.home')}}</h1>
      <div class="title">
        <p>{{t('home.welcome')}}</p>
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