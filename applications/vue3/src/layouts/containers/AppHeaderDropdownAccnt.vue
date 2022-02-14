<template>
  <CDropdown variant="nav-item">
    <CDropdownToggle placement="bottom-end" class="py-0" :caret="false">
      <CAvatar
        color="info"
        text-color="white"
        size="md"
        :src="avatarSrc"
        status="success"
      >
        {{ avatarText }}
      </CAvatar>
    </CDropdownToggle>
    <CDropdownMenu class="pt-0">
      <CDropdownHeader component="h6" class="bg-light fw-semibold py-2">
        Account - {{ userInfo.profile.name || userInfo.username }} 님
      </CDropdownHeader>
      <CDropdownItem @click="$refs.todoModal.callModal()">
        <CIcon icon="cil-task" />
        할일목록
        <CBadge color="danger-gradient" class="ms-auto">
          {{ itemsCount }}
        </CBadge>
      </CDropdownItem>
      <CDropdownHeader component="h6" class="bg-light fw-semibold py-2">
        Settings
      </CDropdownHeader>
      <CDropdownItem>
        <CIcon icon="cil-user" />
        프로필
      </CDropdownItem>
      <CDropdownDivider />
      <CDropdownItem @click="logOut" style="cursor: pointer">
        <CIcon icon="cil-lock-locked" />
        Logout
      </CDropdownItem>
    </CDropdownMenu>
  </CDropdown>

  <TodoModal ref="todoModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import TodoModal from '@/components/Modals/TodoModal.vue'
import { mapActions } from 'vuex'
import avatar from '../../assets/images/avatars/6.jpg'

export default defineComponent({
  name: 'AppHeaderDropdownAccnt',
  components: { TodoModal },
  setup() {
    return {
      avatar: '',
    }
  },
  props: {
    userInfo: {
      type: Object,
      required: true,
    },
  },
  computed: {
    avatarSrc: () => (avatar ? avatar : ''),
    avatarText() {
      return this.userInfo
        ? this.userInfo.username.substring(0, 1).toUpperCase()
        : 'A'
    },
    itemsCount() {
      return (this as any).$store.getters['accounts/myTodos'].length
    },
  },
  methods: {
    toLockScreen() {
      this.$router.push({ name: 'LockScreen' })
    },
    logOut() {
      this.logout()
      this.$router.push({
        name: 'Login',
        query: { redirect: this.$route.path },
      })
    },
    ...mapActions('accounts', ['logout']),
  },
})
</script>
