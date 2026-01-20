<script setup lang="ts">
import {ref, onMounted} from "vue";
import trackedAppsService from "@/services/TrackedAppsService";
import type {TrackedApp} from "@/interfaces/TrackedApps";
import router from "@/router";

const trackedApps = ref<TrackedApp[]>([]);

function goToTrackedApp(uuid: string) {
  router.push(`/tracked-apps/${uuid}`);
}

onMounted(async () => {
  trackedApps.value = await trackedAppsService.getTrackedApps();
  console.log(trackedApps.value);
});
</script>

<template>
  <div class="table-responsive">
    <table>
      <thead>
      <tr>
        <th>UUID</th>
        <th>File Path</th>
        <th>Auto Update</th>
        <th>Cron</th>
      </tr>
      </thead>
      <tbody>
      <tr
          v-for="app in trackedApps"
          :key="app.uuid"
          @click="goToTrackedApp(app.uuid)"
      >
        <td>{{ app.uuid }}</td>
        <td>{{ app.filePath }}</td>
        <td>{{ app.autoUpdate }}</td>
        <td>{{ app.cron }}</td>
      </tr>
      </tbody>
    </table>
    <a class="add-tracked-app" href="/add-tracked-app">Add new tracked app</a>
  </div>
</template>

<style scoped lang="scss">
th {
  font-family: JetBrainsMono;
  font-weight: bold;
  text-align: left;
  padding: 1em;
  color: var(--text-light);
}

td {
  font-family: JetBrainsMono;
  font-weight: lighter;
  padding: 1em;
  color: var(--text-light);
}

tr:hover td {
  color: var(--text-muted);
  cursor: pointer;
}

.add-tracked-app {
  font-family: JetBrainsMono;
  font-weight: lighter;
  padding: 1em;
  text-align: center;
  display: block;
  background-color: var(--primary);
  color: var(--text-light);
  text-decoration: none;
}

.add-tracked-app:hover {
  background-color: var(--primary-dark);
  cursor: pointer;
}

tr {
  background-color: var(--row-even);
}

tr:nth-child(even) {
  background-color: var(--row-odd);
}

.table-responsive {
  width: 100%;
  border: 1px solid var(--text-light);
  border-radius: var(--normal-border);
  overflow: hidden;
}

table {
  border-collapse: collapse;
  width: 100%;
}
</style>