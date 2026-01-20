<script setup lang="ts">
import {defineProps} from 'vue';

const props = defineProps<{
  apiDetails: any
}>()

</script>

<template>
  <div class="table-responsive">
    <table>
      <thead>
      <tr>
        <th>Tracked apps</th>
        <td>
          {{ apiDetails.tracked_apps_amount }}
        </td>
      </tr>
      <tr>
        <th>Enabled tracked apps</th>
        <td>
          {{ apiDetails.tracked_apps_amount }}
        </td>
      </tr>
      <tr>
        <th>Backups made</th>
        <td>
          {{ apiDetails.backups_amount }}
        </td>
      </tr>
      <tr>
        <th>Tracked backups files found</th>
        <td>
          {{ apiDetails.backup_files_found_amount }}
        </td>
      </tr>
      <tr>
        <th>Total tracked backups file size</th>
        <td>
          {{ apiDetails.backup_files_size }}
        </td>
      </tr>
      <tr>
        <th>Next run</th>
        <td>
          {{ apiDetails.tracked_apps[0].uuid }}
        </td>
      </tr>
      </thead>
    </table>
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