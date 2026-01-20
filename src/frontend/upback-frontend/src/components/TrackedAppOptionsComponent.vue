<script setup lang="ts">
import {defineProps, onMounted, ref} from "vue";
import {TrackedApp} from "@/interfaces/TrackedApps";
import TrackedAppsService from "@/services/TrackedAppsService";
import {useBackupStore} from "@/stores/BackupStore";
import {useTrackedAppStore} from "@/stores/TrackedAppStore";

const props = defineProps<{ trackedApp: TrackedApp }>()
const backupStore = useBackupStore();
const trackedAppStore = useTrackedAppStore();
const autoUpdate = ref<boolean | null>(null);

async function startSync() {
  await TrackedAppsService.createBackup(props.trackedApp.uuid);
  backupStore.fetchbackups(props.trackedApp.uuid);
}

async function deleteApp() {
  if (!confirm("Are you sure you want to delete this app?\nbackups files will not be deleted but will not be visible in the app anymore")) return;
  const res = await TrackedAppsService.deleteTrackedApp(props.trackedApp.uuid);
  if (res !== 200) {
    alert("couldn't delete app")
  }
}

async function toggleCronState() {
  const params = {
    auto_update: !props.trackedApp.autoUpdate,
    cron: props.trackedApp.cron,
    filePath: props.trackedApp.filePath,
    uuid: props.trackedApp.uuid
  }

  await TrackedAppsService.updateTrackedApp(props.trackedApp.uuid, params);
  trackedAppStore.fetchTrackedApp(props.trackedApp.uuid);
}

onMounted(() => {
  autoUpdate.value = !props.trackedApp.autoUpdate;
});
</script>

<template>
  <div class="table-responsive">
    <h2>Options</h2>
    <hr>
    <div class="table-options">
      <div class="table-options-row">
        <div class="toggle-sync">
          <div class="toggle-text">
            <span>Active status</span>
            <small>Disable/enable</small>
          </div>
          <div class="toggle-switch">
            <input class="toggle-input" id="toggle" type="checkbox" v-model="autoUpdate"
                   @click="toggleCronState">
            <label class="toggle-label" for="toggle"></label>
          </div>
        </div>
      </div>
      <div class="table-options-row">
        <div class="table-options-row-responsive">
          <button id="sync-now" title="Sync now" @click="startSync">
            <img style="width: 20%" src="@/assets/icons/sync.svg"
                 alt="Sync icon">
            Sync now
          </button>
          <button id="delete" title="Remove" @click="deleteApp">
            <img style="width: 20%" src="@/assets/icons/trashcan.svg"
                 alt="Trashcan icon">
            Remove
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import "@/assets/styles/toggle.css";

h2 {
  padding: 0.4em 1em;
  margin: 0;
}

.table-responsive {
  width: 100%;
  border: 1px solid var(--text-light);
  border-radius: var(--normal-border);
  overflow: hidden;
}

.table-options {
  display: flex;
  flex-direction: column;
  gap: 0.75em;
  padding: 1em;
  margin: 0;
}

.table-options-row-responsive {
  gap: 0.75em;
  display: grid;
  width: 100%;
  grid-template-columns: 1fr 1fr;
}

.table-options-row-responsive button {
  font-family: 'JetBrainsMono', monospace;
  background-color: inherit;
  border: 1px solid var(--bg-light);
  border-radius: var(--button-border);
  box-shadow: 0 0 1px var(--bg-light),
  0 0 1px inset var(--bg-light);
  padding: 1em;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.table-options-row-responsive button:hover {
  transition-duration: 0.1s;
  background-color: var(--bg-light);
}

button:hover img {
  filter: invert(50%) sepia(100%) saturate(500%) hue-rotate(200deg);
}

.toggle-sync {
  border: 1px solid var(--bg-light);
  border-radius: var(--button-border);
  box-shadow: 0 0 1px var(--bg-light),
  0 0 1px inset var(--bg-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: row;
  padding: 1em;
}

.toggle-text {
  display: flex;
  flex-direction: column;
}

small {
  color: var(--text-muted);
}

hr {
  margin: 0;
}
</style>