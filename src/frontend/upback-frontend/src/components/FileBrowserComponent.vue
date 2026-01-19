<script setup lang="ts">
import {defineProps, defineEmits, ref, watch, onMounted, computed} from 'vue'
import FileBrowserService from "@/services/FileBrowserService";
import {DirItem} from "@/interfaces/Files";

const props = defineProps({showBrowser: Boolean})
const emit = defineEmits(['update:showBrowser', 'selected']);

const entries = ref<DirItem[]>([]);
const dialogRef = ref<HTMLDialogElement | null>(null)
const searchQuery = ref('');
const currentPath = ref<string>("");
const filteredEntries = computed(() => {
  if (!searchQuery.value.trim()) return entries.value
  const q = searchQuery.value.toLowerCase()
  return entries.value.filter(e => e.name.toLowerCase().includes(q))
})

function closeModal() {
  emit('update:showBrowser', false)
  dialogRef.value?.close()
}

function selectDir(path: string) {
  emit('selected', path)
  closeModal()
}

async function fetchEntries(path: string) {
  try {
    searchQuery.value = "";

    const data: DirItem[] = await FileBrowserService.getDirectoryItems(path)

    const virtualDirs: DirItem[] = [
      {name: '.', path, isDir: true}
    ]

    if (path !== '/') {
      const parentPath = path.split('/').slice(0, -1).join('/') || '/'
      virtualDirs.push({name: '..', path: parentPath, isDir: true})
    }

    const allEntries = [...virtualDirs, ...data]

    allEntries.sort((a, b) => {
      if (a.isDir && !b.isDir) return -1
      if (!a.isDir && b.isDir) return 1
      return a.name.localeCompare(b.name)
    })

    entries.value = allEntries
  } catch (error) {
    console.error('Failed to fetch entries:', error)
  }
}

onMounted(async () => {
  const res = await FileBrowserService.getAppDirectory();
  if (res.ok) {
    currentPath.value = res.data;
    return
  }
})

watch(
    () => props.showBrowser,
    async (newVal) => {
      if (newVal) {
        dialogRef.value?.showModal()
        await fetchEntries(currentPath.value)
      } else {
        dialogRef.value?.close()
      }
    }
)
</script>

<template>
  <dialog id="folderDialog" ref="dialogRef">
    <div class="dialog-content">
      <input id="folder-search" type="text" placeholder="Search..." v-model="searchQuery">
      <div class="table-wrapper">
        <table>
          <tbody>
          <tr v-for="entry in filteredEntries" :key="entry.path" class="folder-row">
            <td class="td-name" @click="fetchEntries(entry.path)">{{ entry.name }}</td>
            <td class="td-select">
              <button v-if="entry.isDir" @click.stop="selectDir(entry.path)">
                Select
              </button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
      <button type="button" class="dialog-cancel" @click="closeModal">Close</button>
    </div>
  </dialog>
</template>

<style scoped lang="scss">
dialog {
  width: 50%;
  max-width: 50%;
  min-height: auto;
  max-height: 80vh;
  margin: auto;
  padding: 2em;
  border: none;
  border-radius: var(--normal-border);
  background-color: var(--bg-light);
}

.dialog-content {
  display: flex;
  flex-direction: column;
  gap: 1em;
  max-height: 100%;
}

dialog::backdrop {
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(4px);
}

.table-wrapper {
  overflow-y: scroll;
  max-height: 50vh;
  border-radius: var(--button-border);
  width: 100%;
  border: 1px solid var(--bg-dark);
  box-shadow: 0 0 1px var(--bg-dark),
  0 0 1px inset var(--bg-dark);
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
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

.td-name {
  width: 75%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}

.td-select {
  display: flex;
  justify-content: flex-end;
}

tr {
  background-color: var(--row-even);
}

tr:nth-child(even) {
  background-color: var(--row-odd);
}

.dialog-cancel {
  margin: 0 auto;
  display: flex;
  text-align: center;
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

button:hover {
  background-color: var(--primary-dark);
}
</style>