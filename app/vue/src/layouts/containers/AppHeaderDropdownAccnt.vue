<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { useAccount } from '@/store/pinia/account'
import TodoModal from '@/components/Modals/TodoModal.vue'

const router = useRouter()
const store = useStore()
const account = useAccount()

const props = defineProps({ userInfo: { type: Object, required: true } })

const avatarSrc = computed(() => {
  return props.userInfo?.profile?.image ? props.userInfo?.profile?.image : ''
})
const avatarText = computed(() =>
  props.userInfo ? props.userInfo.username.substring(0, 1).toUpperCase() : 'A',
)

const itemsCount = computed(() => account.myTodos.length)
const headerClass = computed(() =>
  store.state.theme === 'dark' ? 'bg-secondary' : 'bg-light',
)

const logout = () => {
  account.logout()
  router.push({ name: 'Login' })
}
</script>

<template>
  <CDropdown>
    <CDropdownToggle class="py-0" color="link" :caret="false">
      <CAvatar
        color="secondary"
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
        Account -
        {{
          userInfo.profile && userInfo.profile.name
            ? userInfo.profile.name
            : userInfo.username
        }}
        님
      </CDropdownHeader>
      <CDropdownItem @click="$refs.todoModal.callModal()">
        <CIcon icon="cil-task" />
        할일목록
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
      <CDropdownItem @click="$router.push({ name: '프로필 관리' })">
        <CIcon icon="cil-user" />
        프로필
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
