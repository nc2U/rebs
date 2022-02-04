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
        Account - {{ userInfo.username }} 님
      </CDropdownHeader>
      <!--      <CDropdownItem>-->
      <!--        <CIcon icon="cil-bell" />-->
      <!--        Updates-->
      <!--        <CBadge color="info-gradient" class="ms-auto">{{ itemsCount }}</CBadge>-->
      <!--      </CDropdownItem>-->
      <!--      <CDropdownItem>-->
      <!--        <CIcon icon="cil-envelope-open" />-->
      <!--        Messages-->
      <!--        <CBadge color="success-gradient" class="ms-auto"-->
      <!--          >{{ itemsCount }}-->
      <!--        </CBadge>-->
      <!--      </CDropdownItem>-->
      <CDropdownItem>
        <CIcon icon="cil-task" />
        Tasks
        <CBadge color="danger-gradient" class="ms-auto">
          {{ itemsCount }}
        </CBadge>
      </CDropdownItem>
      <!--      <CDropdownItem>-->
      <!--        <CIcon icon="cil-comment-square" />-->
      <!--        Comments-->
      <!--        <CBadge color="warning-gradient" class="ms-auto"-->
      <!--          >{{ itemsCount }}-->
      <!--        </CBadge>-->
      <!--      </CDropdownItem>-->
      <CDropdownHeader component="h6" class="bg-light fw-semibold py-2">
        Settings
      </CDropdownHeader>
      <CDropdownItem>
        <CIcon icon="cil-user" />
        Profile
      </CDropdownItem>
      <!--      <CDropdownItem>-->
      <!--        <CIcon icon="cil-settings" />-->
      <!--        Settings-->
      <!--      </CDropdownItem>-->
      <!--      <CDropdownItem>-->
      <!--        <CIcon icon="cil-dollar" />-->
      <!--        Payments-->
      <!--        <CBadge color="secondary" class="ms-auto">{{ itemsCount }}</CBadge>-->
      <!--      </CDropdownItem>-->
      <!--      <CDropdownItem>-->
      <!--        <CIcon icon="cil-file" />-->
      <!--        Projects-->
      <!--        <CBadge color="primary-gradient" class="ms-auto">-->
      <!--          {{ itemsCount }}-->
      <!--        </CBadge>-->
      <!--      </CDropdownItem>-->
      <CDropdownDivider />
      <CDropdownItem @click="toLockScreen">
        <CIcon icon="cil-shield-alt" />
        Lock Account
      </CDropdownItem>
      <CDropdownItem @click="logOut" style="cursor: pointer">
        <CIcon icon="cil-lock-locked" />
        Logout
      </CDropdownItem>
    </CDropdownMenu>
  </CDropdown>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapActions } from 'vuex'
import avatar from '../../assets/images/avatars/6.jpg'

export default defineComponent({
  name: 'AppHeaderDropdownAccnt',
  setup() {
    return {
      avatar: '',
      itemsCount: 0,
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
