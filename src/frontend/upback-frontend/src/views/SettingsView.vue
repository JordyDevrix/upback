<script setup lang="ts">
import {ref} from 'vue'
import {useI18n} from 'vue-i18n'

const {t, locale} = useI18n()
const dropdownOpen = ref(false)

const languages = [
  {code: 'en', label: 'English'},
  {code: 'fr', label: 'Français'},
  {code: 'nl', label: 'Nederlands'}
]

async function selectLanguage(langCode: string) {
  try {
    const res = await fetch('/api/locale', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({locale: langCode})
    })

    if (!res.ok) throw new Error('Failed to set locale')

    // Update vue-i18n locale
    locale.value = langCode
    dropdownOpen.value = false
  } catch (err) {
    console.error(err)
  }
}
</script>

<template>
  <main>
    <header>
      <h1>{{ t('settings.settings') }}</h1>
      <div class="title">
        <p>{{ t('settings.changeApplicationSettings') }}</p>
      </div>

      <!-- Language dropdown -->
      <div class="language-dropdown">
        <button @click="dropdownOpen = !dropdownOpen">
          {{ t('settings.selectLanguage') }}
        </button>

        <ul v-if="dropdownOpen" class="dropdown-menu">
          <li v-for="lang in languages" :key="lang.code" @click.stop="selectLanguage(lang.code)">
            {{ lang.label }}
          </li>
        </ul>
      </div>
    </header>
  </main>
</template>

<style scoped lang="scss">
.language-dropdown {
  position: relative;
  display: inline-block;
  margin-top: 1rem;

  button {
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-weight: bold;
    color: var(--text-light);
    background: var(--bg-dark);
  }

  .dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    background: white;
    border: 1px solid #ccc;
    list-style: none;
    padding: 0;
    margin: 0;
    width: 150px;
    z-index: 10;

    li {
      padding: 0.5rem 1rem;
      cursor: pointer;

      &:hover {
        background: #eee;
      }
    }
  }
}
</style>
