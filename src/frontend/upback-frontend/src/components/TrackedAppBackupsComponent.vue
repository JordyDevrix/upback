<script setup lang="ts">
import {computed, defineProps, onMounted, onUnmounted, ref} from "vue";
import {TrackedApp} from "@/interfaces/TrackedApps";
import {useBackupStore} from "@/stores/BackupStore";

const props = defineProps<{
  trackedApp: TrackedApp,
  sseMessage: Record<any, any>
}>()
const backupStore = useBackupStore();

function timeAgo(timestamp: string) {
  const now: Date = new Date();
  const time: Date = new Date(Number(timestamp) * 1000);
  const diff: number = Math.floor((now.getTime() - time.getTime()) / 1000);

  if (diff < 60) {
    return "Now";
  } else if (diff < 120) {
    return "A minute ago";
  } else if (diff < 3600) { // less than 1 hour
    const minutes = Math.floor(diff / 60);
    return `${minutes} minutes ago`;
  } else if (diff < 7200) { // less than 2 hours
    return "An hour ago";
  } else if (diff < 86400) { // less than 1 day
    const hours = Math.floor(diff / 3600);
    return `${hours} hours ago`;
  } else if (diff < 172800) { // less than 2 days
    return "Yesterday";
  } else {
    const year = time.getFullYear();
    const month = String(time.getMonth() + 1).padStart(2, "0");
    const day = String(time.getDate()).padStart(2, "0");
    const hours = String(time.getHours()).padStart(2, "0");
    const minutes = String(time.getMinutes()).padStart(2, "0");
    return `${year}-${month}-${day} ${hours}:${minutes}`;
  }
}

const isSyncing = (syncId: string) => {
  const syncs = props.sseMessage?.current_app_syncs;
  if (!syncs) return false;
  return syncId in syncs;
};

onMounted(async () => {
  backupStore.fetchbackups(props.trackedApp.uuid)
})

onUnmounted(async () => {
  backupStore.removeBackups()
})
</script>

<template>
  <div class="table-responsive">
    <table>
      <colgroup>
        <col class="col-file">
        <col class="col-timestamp">
        <col class="col-backup-id">
        <col class="col-status">
      </colgroup>
      <thead>
      <tr>
        <th>File</th>
        <th>Timestamp</th>
        <th>Backup ID</th>
        <th class="sync-status">Status</th>
      </tr>
      </thead>
      <tbody id="backups-body">
      <tr v-for="backup in backupStore.backups"
          :key="backup.uuid"
      >
        <td>{{ backup.filePath }}</td>
        <td>{{ timeAgo(backup.timestamp) }}</td>
        <td>{{ backup.uuid }}</td>
        <td class="td-sync">
          <img v-if="isSyncing(backup.uuid)" class="sync-icon spin-anim"
               src="@/assets/icons/sync.svg"
               alt="Sync icon"
          >
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped lang="scss">
table {
  border-collapse: collapse;
  table-layout: fixed;
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
}

.col-file {
  width: 45%;
}

.col-timestamp {
  width: 25%;
}

.col-backup-id {
  width: 30%;
}

.col-status {
  width: 8em;
}

.sync-icon {
  width: 16px;
  height: 16px;
  vertical-align: middle;
}

.td-sync {
  text-align: center;
}
</style>