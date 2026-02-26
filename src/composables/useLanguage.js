import { ref, readonly } from 'vue'

const lang = ref(localStorage.getItem('ddart_lang') || 'en')

export function useLanguage() {
  function setLang(l) {
    lang.value = l
    localStorage.setItem('ddart_lang', l)
  }

  function t(en, gr) {
    return lang.value === 'gr' ? gr : en
  }

  return { lang: readonly(lang), setLang, t }
}