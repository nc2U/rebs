<template>
  <CAlert color="secondary">
    <CButton
      color="primary"
      :disabled="!contractors.length"
      @click="print_bill"
    >
      선택 건별 고지서 내려받기
    </CButton>
  </CAlert>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AlertModal from '@/components/Modals/AlertModal.vue'

export default defineComponent({
  name: 'DownloadButton',
  components: { AlertModal },
  props: {
    print_data: Object,
    contractors: Array,
  },
  methods: {
    print_bill(this: any) {
      if (!this.print_data.is_bill_issue) {
        this.$refs.alertModal.callModal(
          '',
          '고지서 관련 기본 설정 데이터를 입력하여 주십시요.',
        )
      } else {
        if (this.contractors?.length === 0) {
          this.$refs.alertModal.callModal(
            '',
            '다운로드(출력)할 계약 건을 선택하여 주십시요.',
          )
        } else {
          const project = this.print_data.project
          const pub_date = this.print_data.pub_date
          const seq = this.contractors.join('-')
          const url = 'rebs/pdf-bill/'
          location.href = `${url}?project=${project}&date=${pub_date}&seq=${seq}`
        }
      }
    },
  },
})
</script>
