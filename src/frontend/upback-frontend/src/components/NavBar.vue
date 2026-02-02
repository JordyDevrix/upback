<script setup lang="ts">
import {useI18n} from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <nav>
    <router-link to="/">{{ t('navbar.home') }}</router-link>
    <router-link to="/tracked-apps">{{ t('navbar.trackedApps') }}</router-link>
    <router-link to="/add-tracked-app">{{ t('navbar.addNew') }}</router-link>
    <router-link to="/settings">{{ t('navbar.settings') }}</router-link>
    <a target="_blank" rel="noopener noreferrer" href="https://github.com/JordyDevrix/upback">GitHub</a>
  </nav>
  <div id="hr"></div>
</template>

<style scoped lang="scss">
nav {
  padding: 0;
  width: 80%;
  margin: 0 auto;
  background: var(--bg-dark);
}

nav a {
  display: inline-block;
  color: var(--text-light);
  text-decoration: none;
  margin: 0.75em 30px 0.75em 0;
  font-weight: bold;
}

nav a:hover {
  text-decoration: underline;
}

#hr {
  color: var(--bg-light);
  background-color: var(--bg-light);
  padding: 0;
  margin: 0;
  width: 100%;
  height: 1px;
  box-shadow: 0 0 1px var(--bg-light),
  0 0 1px inset var(--bg-light);
}
</style>