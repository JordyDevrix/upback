// ✅ modern way without deprecation warnings
import { createI18n } from 'vue-i18n'
import en from '@/locales/en.json'
import nl from '@/locales/nl.json'
import fr from '@/locales/fr.json'

export const messages = { en, nl, fr }
export type Locale = keyof typeof messages

export const i18n = createI18n({
  locale: (localStorage.getItem('locale') || 'en') as Locale,
  fallbackLocale: 'en',
  messages,
})


export async function loadUserLocale() {
  try {
    const res = await fetch('/api/locale') // returns { "locale": "nl" }
    const data = await res.json()
    const locale = data.locale;

    // set i18n locale
    i18n.global.locale = locale
    localStorage.setItem('locale', locale) // optional persistence
  } catch (err) {
    console.error('Failed to fetch user locale', err)
    i18n.global.locale = 'en' // fallback
  }
}