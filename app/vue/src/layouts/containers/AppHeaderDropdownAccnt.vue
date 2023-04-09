<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { useAccount } from '@/store/pinia/account'
import TodoModal from '@/components/Modals/TodoModal.vue'

const props = defineProps({
  userInfo: { type: Object, required: true },
  profile: { type: Object, default: null },
})

const router = useRouter()

const avatarSrc = computed(() => {
  return props.profile?.image ? props.profile?.image : ''
})

const avatarText = computed(() =>
  props.userInfo ? props.userInfo.username.substring(0, 1).toUpperCase() : 'A',
)

const store = useStore()
const headerClass = computed(() =>
  store.state.theme === 'dark' ? 'bg-secondary' : 'bg-light',
)

const locationBlank = (url: string) => window.open(url, '_blank')

const account = useAccount()
const itemsCount = computed(() => account.myTodos.length)

const logout = () => {
  account.logout()
  router.push({ name: 'Login' })
}
</script>

<template>
  <CDropdown>
    <CDropdownToggle class="py-0" color="link" :caret="false">
      <CAvatar
        color="blue-grey-lighten-3"
        text-color="white"
        size="md"
        :src="avatarSrc"
        status="success"
      >
        {{ avatarText }}
      </CAvatar>
    </CDropdownToggle>
    <CDropdownMenu>
      <CDropdownHeader
        component="h6"
        class="fw-semibold py-2"
        :class="headerClass"
      >
        {{ profile && profile.name ? profile.name : userInfo.username }}님
      </CDropdownHeader>
      <CDropdownItem @click="$refs.todoModal.callModal()">
        <CIcon icon="cil-task" />
        할일 관리
        <CBadge color="danger" size="sm" class="ms-auto">
          {{ itemsCount }}
        </CBadge>
      </CDropdownItem>
      <CDropdownHeader
        component="h6"
        class="fw-semibold py-2"
        :class="headerClass"
      >
        Settings
      </CDropdownHeader>
      <CDropdownItem @click="router.push({ name: '프로필 관리' })">
        <CIcon icon="cil-user" />
        프로필
      </CDropdownItem>
      <CDropdownItem
        v-if="userInfo.is_superuser"
        @click="locationBlank('/admin/')"
      >
        <CIcon icon="cil-settings" />
        관리자 페이지
      </CDropdownItem>
      <CDropdownItem
        v-if="userInfo.pk === 1"
        @click="locationBlank('https://nc2u.github.io/rebs/')"
      >
        <CIcon icon="cil-description" />
        사용자 매뉴얼
      </CDropdownItem>
      <CDropdownDivider />
      <CDropdownItem style="cursor: pointer" @click="logout">
        <CIcon icon="cil-lock-locked" />
        로그아웃
      </CDropdownItem>
    </CDropdownMenu>
  </CDropdown>

  <TodoModal ref="todoModal" />
</template>
