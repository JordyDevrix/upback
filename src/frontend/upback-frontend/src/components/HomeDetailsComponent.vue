<script setup lang="ts">
import {defineProps} from 'vue';
import {useI18n} from 'vue-i18n'

const {t} = useI18n()
defineProps<{
  apiDetails: any
}>()

</script>

<template>
  <div class="table-responsive">
    <table>
      <thead>
      <tr>
        <th>{{t('home.trackedApps')}}</th>
        <td>
          {{ apiDetails.tracked_apps_amount }}
        </td>
      </tr>
      <tr>
        <th>{{t('home.enabledTrackedApps')}}</th>
        <td>
          {{ apiDetails.tracked_apps_amount }}
        </td>
      </tr>
      <tr>
        <th>{{t('home.backupsMade')}}</th>
        <td>
          {{ apiDetails.backups_amount }}
        </td>
      </tr>
      <tr>
        <th>{{t('home.trackedBackupFilesFound')}}</th>
        <td>
          {{ apiDetails.backup_files_found_amount }}
        </td>
      </tr>
      <tr>
        <th>{{t('home.totalTrackedBackupsFileSize')}}</th>
        <td>
          {{ apiDetails.backup_files_size }}
        </td>
      </tr>
      <tr>
        <th>{{t('home.nextRun')}}</th>
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