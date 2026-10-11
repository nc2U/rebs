import { computed } from 'vue'
import { useStore } from '@/store'

const isDark = computed(() => useStore().isDark)

// -----------------------------------------------------------------------
export const TableSecondary = computed(() => (isDark.value ? 'dark' : 'secondary'))
export const TablePrimary = computed(() => (isDark.value ? 'dark' : 'primary'))
export const TableSuccess = computed(() => (isDark.value ? 'dark' : 'success'))
export const TableInfo = computed(() => (isDark.value ? 'dark' : 'info'))

// -----------------------------------------------------------------------

export const AlertSecondary = computed(() => (isDark.value ? '' : 'secondary'))
export const AlertLight = computed(() => (isDark.value ? '' : 'light'))

export const bgLight = computed(() => (isDark.value ? '' : 'bg-light'))
export const colorLight = computed(() => (isDark.value ? '' : 'light'))
