<script setup lang="ts">
import {defineProps, onMounted, onUnmounted, ref, watch} from 'vue'
import TrackedAppBackupsComponent from "@/components/TrackedAppBackupsComponent.vue";
import TrackedAppInfoComponent from "@/components/TrackedAppInfoComponent.vue";
import TrackedAppOptionsComponent from "@/components/TrackedAppOptionsComponent.vue";
import {useSSEStore} from "@/stores/ActiveSyncsStore";
import {useTrackedAppStore} from "@/stores/TrackedAppStore";

const props = defineProps<{ uuid: string }>();
const trackedAppStore = useTrackedAppStore();
const sse = useSSEStore();
const loading = ref(true)

onMounted(async () => {
  await trackedAppStore.fetchTrackedApp(props.uuid);
  loading.value = false;
  sse.startSync("/api/tracked-apps/syncs");
  sse.startTrackedApp(`/api/tracked-apps/next-cron/${props.uuid}`);
})

onUnmounted(() => {
  sse.stopAll();
  trackedAppStore.removeTrackedApp();
})
</script>

<template>
  <main>
    <header>
      <h1>Tracked Applications</h1>
      <div class="title">
        <p class="back" onclick="history.back()">Applications</p>
        <p>&lt;</p>
        <p>{{ trackedAppStore.trackedApp?.uuid }}</p>
      </div>
    </header>
    <div class="config-details-responsive">
      <TrackedAppInfoComponent v-if="trackedAppStore.trackedApp" :tracked-app="trackedAppStore.trackedApp" :sseMessage="sse.syncProgress" :sseTrackedApp="sse.nextRun"/>
      <TrackedAppOptionsComponent v-if="trackedAppStore.trackedApp" :tracked-app="trackedAppStore.trackedApp"/>
    </div>
    <TrackedAppBackupsComponent v-if="trackedAppStore.trackedApp" :trackedApp="trackedAppStore.trackedApp" :sseMessage="sse.syncProgress"/>
  </main>
</template>

<style scoped lang="scss">
h2 {
  padding: 0.4em 1em;
  margin: 0;
}

header {
  display: flex;
  flex-direction: column;
}

.title {
  display: flex;
  gap: 1em;
}

.title .back {
  cursor: pointer;
}

.config-details-responsive {
  display: grid;
  grid-template-columns: 7fr 3fr;
  gap: 2em;
}
</style>