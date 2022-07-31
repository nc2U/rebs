<template>
  <CTableDataCell>
    <router-link to="" @click="callFormModal">
      {{ cutString(release.__str__, 25) }}
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
    <CButton type="button" color="danger" size="sm" @click="callFormModal">
      확인
    </CButton>
  </CTableDataCell>

  <FormModal size="lg" ref="releaseFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      계약 해지 수정 등록
    </template>
    <template v-slot:default>
      <ReleaseForm
        :release="release"
        :contractor="contractor"
        @on-submit="onSubmit"
        @close="$refs.releaseFormModal.visible = false"
      />
    </template>
  </FormModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import ReleaseForm from '@/views/contracts/Release/components/ReleaseForm.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'Release',
  components: { FormModal, ReleaseForm },
  props: { release: Object },
  computed: {
    ...mapState('contract', ['contractor']),
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
    callFormModal(this: any) {
      this.$emit('get-release', this.release.pk)
      this.$router.push({
        name: '계약해지 관리',
        query: { contractor: this.release.contractor },
      })
      this.$refs.releaseFormModal.callModal()
    },
    onSubmit(this: any, payload: any) {
      this.$emit('on-submit', payload)
      this.$refs.releaseFormModal.visible = false
    },
  },
})
</script>
