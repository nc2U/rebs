<script lang="ts" setup>
import { ref, computed, watch } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { pageTitle, navMenu } from '@/views/_MyPage/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import PasswordCheck from '@/views/_MyPage/Secession/components/PasswordCheck.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const refConfirmModal = ref()
const removePass = ref('')

const accStore = useAccount()
const userInfo = computed(() => accStore.userInfo)
const passChecked = computed(() => accStore.passChecked)

const checkPassword = (payload: { email: string; password: string }) =>
  accStore.checkPassword(payload)

const removeConfirm = (password: string) => {
  removePass.value = password
  refConfirmModal.value.callModal('', '', '', 'danger')
}

const modalAction = () => {
  const email = userInfo.value?.email ?? ''
  checkPassword({ email, password: removePass.value })
  refConfirmModal.value.close()
}

watch(passChecked, nVal => {
  if (nVal) {
    alert('탈퇴 로직 진행!!')
    accStore.passChecked = false
  }
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <PasswordCheck :username="userInfo?.username" @remove-confirm="removeConfirm" />
  </ContentBody>

  <ConfirmModal ref="refConfirmModal">
    <template #header> 멤버 영구 탈퇴</template>
    <template #default>
      정말 멤버 탈퇴를 진행하시겠습니까?<br />
      탈퇴한 회원정보는 복구할 수 없으므로 신중히 선택하여 주십시요. <br />
      획인을 누르면 탈퇴가 진행됩니다.
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction"> 확인</CButton>
    </template>
  </ConfirmModal>
</template>
