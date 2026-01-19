<script setup lang="ts">
import {TrackedApp} from "@/interfaces/TrackedApps";
import {computed, defineProps, onMounted, ref, watch} from "vue";
import cronstrue from 'cronstrue'

const humanCron = ref<string | null>(null);
const props = defineProps<{
  trackedApp: TrackedApp,
  sseMessage: Record<any, any>,
  sseTrackedApp: Record<any, any>
}>()

const isSyncing = computed(() => {
  const syncs = props.sseMessage?.current_app_syncs;
  if (!syncs) return false;

  return Object.values(syncs).some(
      (sync: any) => sync.app_id === props.trackedApp.uuid
  );
});

function copyToClipboard(text: string) {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).catch(console.error)
    console.log(`Copied: ${text}`);
  } else {
    console.log(`Fallback Copied: ${text}`)
    const el = document.createElement('textarea')
    el.value = text
    el.style.position = 'fixed'  // avoid scroll jump
    el.style.top = '0'
    el.style.left = '0'
    el.style.opacity = '0'
    document.body.appendChild(el)
    el.focus()
    el.select()
    try {
      document.execCommand('copy')
    } catch (err) {
      console.error('Fallback copy failed', err)
    }
    document.body.removeChild(el)
  }
}

function formatSecondsToHMS(seconds: number): string {
  const days = Math.floor(seconds / 86400);
  const hrs = Math.floor((seconds % 86400) / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  const pad = (n: number) => n.toString().padStart(2, "0");

  let result = `${pad(hrs)}:${pad(mins)}:${pad(secs)}`;
  if (days > 0) {
    result = `${days}d ${result}`;
  }
  return result;
}


onMounted(async () => {
  humanCron.value = cronstrue.toString(props.trackedApp.cron);
})
</script>

<template>
  <div class="table-responsive">
    <table>
      <thead>
      <tr>
        <th>File path</th>
        <td class="copy-cell">
          {{ props.trackedApp.filePath }}
          <button class="copy-btn" title="Copy" @click="copyToClipboard(props.trackedApp.filePath)">
            <img src="@/assets/icons/clipboard.svg" alt="Clipboard icon">
          </button>
        </td>
      </tr>
      <tr>
        <th>UUID</th>
        <td class="copy-cell">
          {{ props.trackedApp.uuid }}
          <button class="copy-btn" title="Copy" @click="copyToClipboard(props.trackedApp.uuid)">
            <img src="@/assets/icons/clipboard.svg" alt="Clipboard icon">
          </button>
        </td>
      </tr>
      <tr>
        <th>Auto sync enabled</th>
        <td>
          <span v-if="trackedApp.autoUpdate" id="sync-status-enabled">true</span>
          <span v-else id="sync-status-disabled">false</span>
        </td>

      </tr>
      <tr>
        <th>Cron</th>
        <td class="copy-cell">
          {{ props.trackedApp.cron }} <span class="human-cron">({{ humanCron }})</span>
          <button class="copy-btn" title="Copy" @click="copyToClipboard(props.trackedApp.cron)">
            <img src="@/assets/icons/clipboard.svg" alt="Clipboard icon">
          </button>
        </td>
      </tr>
      <tr>
        <th>Next run</th>
        <td>
          <span id="next-run">{{ formatSecondsToHMS(props.sseTrackedApp.seconds_remaining) }} </span>
          <img v-if="isSyncing" class="sync-icon spin-anim" src="@/assets/icons/sync.svg" alt="Sync icon">
        </td>
      </tr>
      </thead>
    </table>
  </div>
</template>

<style scoped lang="scss">
table {
  border-collapse: collapse;
  width: 100%;
}

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
  background: var(--row-even);
}

.copy-cell {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
}

.copy-btn {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  display: flex;
}

.copy-btn img {
  width: 16px;
  height: 16px;
}

.copy-btn:hover {
  filter: invert(55%) sepia(100%) saturate(500%) hue-rotate(190deg);
}

.human-cron {
  color: var(--text-muted);
  margin-left: 1rem;
}

.sync-icon {
  width: 16px;
  height: 16px;
  vertical-align: middle;
  text-align: center;
  margin-left: 0.5rem;
}

#sync-status-enabled {
  border-radius: var(--button-border);
  color: var(--success-text);
  background-color: var(--label-enabled);
  padding: 3px;
}

#sync-status-disabled {
  border-radius: var(--button-border);
  color: var(--danger-text);
  background-color: var(--label-disabled);
  padding: 3px;
}
</style>