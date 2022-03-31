<template>
  <CTableDataCell>
    <router-link to="">
      {{ cutString(release.contractor.__str__, 25) }}
    </router-link>
  </CTableDataCell>
  <CTableDataCell>{{ getStatus(release.status) }}</CTableDataCell>
  <CTableDataCell class="text-right">
    {{ numFormat(release.refund_amount) }}
  </CTableDataCell>
  <CTableDataCell class="text-left">
    {{ release.refund_account_bank }}
  </CTableDataCell>
  <CTableDataCell class="text-left">
    {{ release.refund_account_number }}
  </CTableDataCell>
  <CTableDataCell>{{ release.refund_account_depositor }}</CTableDataCell>
  <CTableDataCell>{{ release.request_date }}</CTableDataCell>
  <CTableDataCell>{{ release.completion_date }}</CTableDataCell>
  <CTableDataCell>
    <CButton type="button" color="success" size="sm" @click="updateConfirm">
      확인
    </CButton>
  </CTableDataCell>

  <FormModal size="lg" ref="cancelFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      계약 해지 등록
    </template>
    <template v-slot:default>
      <ContCancelForm
        :release="release"
        @on-submit="onSubmit"
        @close="$refs.cancelFormModal.visible = false"
      />
    </template>
  </FormModal>

  <AlertModal ref="cancelAlertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import ContCancelForm from '@/views/contracts/Cancel/components/ContCancelForm.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'Canceled',
  components: { FormModal, ContCancelForm, AlertModal },
  props: { release: Object },
  computed: {
    pageManageAuth(this: any) {
      return (
        this.superAuth || (this.staffAuth && this.staffAuth.contract === '2')
      )
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    getStatus(num: string) {
      const status = [
        { code: '0', text: '신청 취소' },
        { code: '3', text: '신청 중' },
        { code: '4', text: '처리완료' },
        { code: '5', text: '자격상실(제명)' },
      ]
      return status.filter(s => s.code === num).map(s => s.text)[0]
    },
    updateConfirm(this: any) {
      if (this.pageManageAuth) this.$refs.cancelFormModal.callModal()
      else this.$refs.cancelAlertModal.callModal()
      this.$router.push({
        name: '계약해지 관리',
        query: { contractor: this.release.contractor.pk },
      })
    },
  },
})
</script>
