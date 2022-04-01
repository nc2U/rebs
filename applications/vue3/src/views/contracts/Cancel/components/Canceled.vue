<template>
  <CTableDataCell>
    <router-link to="" @click="updateConfirm">
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
    <CButton type="button" color="danger" size="sm" @click="updateConfirm">
      확인
    </CButton>
  </CTableDataCell>

  <FormModal size="lg" ref="cancelFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      계약 해지 수정 등록
    </template>
    <template v-slot:default>
      <ContCancelForm
        :release="release"
        @on-submit="onSubmit"
        @close="$refs.cancelFormModal.visible = false"
      />
    </template>
  </FormModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import ContCancelForm from '@/views/contracts/Cancel/components/ContCancelForm.vue'

export default defineComponent({
  name: 'Canceled',
  components: { FormModal, ContCancelForm },
  props: { release: Object },
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
      this.$router.push({
        name: '계약해지 관리',
        query: { contractor: this.release.contractor.pk },
      })
      this.$emit('update-confirm', this.release.pk)
      this.$refs.cancelFormModal.callModal()
    },
    onSubmit(this: any, payload: any) {
      this.$emit('on-submit', payload)
      this.$refs.cancelFormModal.visible = false
    },
  },
})
</script>
