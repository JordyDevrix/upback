<script setup lang="ts">
import {ref} from "vue";
import {useRouter} from 'vue-router';
import {TrackedAppRequest} from "@/interfaces/TrackedApps";
import TrackedAppsService from "@/services/TrackedAppsService";
import FileBrowserComponent from "@/components/FileBrowserComponent.vue";

const showBrowser = ref<boolean>(false)
const router = useRouter();
const form = ref({
  filePath: "",
  autoUpdate: true, // boolean directly
  cron: ""
});

function handleSelected(path: string) {
  form.value.filePath = path;
}

async function onClickSave() {
  const body: TrackedAppRequest = {
    auto_update: form.value.autoUpdate,
    file_path: form.value.filePath,
    cron: form.value.cron
  }

  const res = await TrackedAppsService.saveNewTrackedApp(body);

  if (!res.ok) {
    alert("Failed to save app");
    return;
  }

  await router.push('/tracked-apps');
}
</script>

<template>
  <section>
    <div class="form-header">
      <h2>Configuration</h2>
      <h3 id="h3">Configure settings for the new application</h3>
    </div>
    <hr>
    <form @submit.prevent="onClickSave">
      <!-- File path with browse -->
      <div class="form-group">
        <label for="file_path">File path</label>
        <div class="form-group-inline">
          <input id="file_path" type="text" placeholder="C:/path/to/folder" required v-model="form.filePath">
          <button type="button" @click="showBrowser = true">
            <img class="folder-icon" src="@/assets/icons/folder.svg"
                 alt="Folder icon">
            Browse
          </button>
        </div>
      </div>

      <!-- Enabled/Disabled -->
      <div class="form-group">
        <label for="enabled">Auto sync enabled/disabled</label>
        <select id="enabled" v-model="form.autoUpdate">
          <option :value="true">Enabled</option>
          <option :value="false">Disabled</option>
        </select>
      </div>

      <!-- Cron schedule -->
      <div class="form-group">
        <label for="cron">Cron schedule</label>
        <input id="cron" type="text" placeholder="0 */6 * * *" required v-model="form.cron">
        <small id="cron-human" class="cron-human">Enter a cron expression</small>
        <small>
          [<a target="_blank" rel="noopener noreferrer" href="https://cronitor.io/guides/cron-jobs">info</a>]
        </small>
      </div>

      <!-- Save button -->
      <div class="form-group">
        <div class="form-group-inline-submit">
          <button id="b-cancel" type="button" onclick="history.back()">Cancel</button>
          <button id="b-reset" type="reset">Reset</button>
          <button id="b-submit" type="submit">
            <img class="plus-icon" src="@/assets/icons/plus.svg" alt="Plus icon">
            Save app
          </button>
        </div>
      </div>
    </form>
  </section>
  <FileBrowserComponent v-model:showBrowser="showBrowser" @selected="handleSelected"/>
</template>

<style scoped lang="scss">
section {
  background-color: var(--bg-light);
  border-radius: var(--normal-border);
  border: 1px solid var(--text-light);
}

.form-header {
  margin: 2em;
  display: flex;
  flex-direction: column;
  gap: 1em;
}

h2, h3 {
  margin: 0;
}

#h3 {
  color: var(--text-muted);
  font-weight: lighter;
}

form {
  margin: 2em;
  display: flex;
  flex-direction: column;
  gap: 2em;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5em;
}

button,
input,
option,
select {
  font-family: JetBrainsMono;
  border-radius: var(--button-border);
  border: none;
  padding: 0.75em;
  box-sizing: border-box;
  background-color: var(--bg-dark);
  color: var(--text-light);
}

.form-group-inline {
  display: flex;
  flex-direction: row;
  gap: 0.5em;
}

.form-group-inline-submit {
  display: flex;
  flex-direction: row;
  gap: 0.5em;
  justify-content: center;
}

input {
  width: 100%;
}

input:focus,
select:focus {
  border: none;
  outline: 1px solid var(--primary-dark);
}

button {
  display: flex;
  flex-direction: row;
  gap: 0.5em;
  align-content: center;
  align-items: center;
  background-color: var(--primary);
}

#b-cancel, #b-reset {
  background-color: var(--text-light);
  color: var(--bg-dark);

}

#b-cancel:hover, #b-reset:hover {
  background-color: var(--danger);
}

img {
  height: 16px;
}

small, a {
  color: var(--text-muted);
}
</style>