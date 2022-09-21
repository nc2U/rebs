import store from '@/store'
import { computed } from 'vue'

export const headerSecondary = computed(() =>
  store.state.theme === 'dark' ? 'dark' : 'secondary',
)

export const headerPrimary = computed(() =>
  store.state.theme === 'dark' ? 'dark' : 'primary',
)

export const headerSuccess = computed(() =>
  store.state.theme === 'dark' ? 'dark' : 'success',
)

export const headerInfo = computed(() =>
  store.state.theme === 'dark' ? 'dark' : 'info',
)

export const headerWarning = computed(() =>
  store.state.theme === 'dark' ? 'dark' : 'warning',
)

export const headerDanger = computed(() =>
  store.state.theme === 'dark' ? 'dark' : 'danger',
)

export const headerLight = computed(() =>
  store.state.theme === 'dark' ? '' : 'light',
)

export const AlertSecondary = computed(() =>
  store.state.theme === 'dark' ? '' : 'secondary',
)
