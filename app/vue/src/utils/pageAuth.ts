import { useAccount } from '@/store/pinia/account'
import { computed } from 'vue'

const account = useAccount()

export const isSuperUser = computed(() => account.superAuth)

export const read_contract = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.contract === '1'),
)

export const write_contract = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.contract === '2'),
)

export const read_payment = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.payment === '1'),
)

export const write_payment = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.payment === '2'),
)

export const read_notice = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.notice === '1'),
)

export const write_notice = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.notice === '2'),
)

export const read_project_cash = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.project_cash === '1'),
)

export const write_project_cash = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.project_cash === '2'),
)

export const read_project_docs = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.project_docs === '1'),
)

export const write_project_docs = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.project_docs === '2'),
)

export const read_project = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.project === '1'),
)
export const write_project = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.project === '2'),
)

export const read_company_cash = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.company_cash === '1'),
)
export const write_company_cash = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.company_cash === '2'),
)

export const read_company_docs = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.company_docs === '1'),
)
export const write_company_docs = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.company_docs === '2'),
)

export const read_human_resource = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.human_resource === '1'),
)
export const write_human_resource = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.human_resource === '2'),
)

export const read_company_settings = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.company_settings === '1'),
)
export const write_company_settings = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.company_settings === '2'),
)

export const read_auth_manage = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.auth_manage === '1'),
)
export const write_auth_manage = computed(
  () =>
    isSuperUser.value ||
    (account.staffAuth && account.staffAuth.auth_manage === '2'),
)
