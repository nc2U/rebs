<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="8%" />
      <col width="10%" />
      <col width="10%" />
      <col width="8%" />
      <col width="10%" />
      <col width="10%" />
      <col width="12%" />
      <col width="20%" />
      <col width="12%" />
    </colgroup>

    <CTableHead>
      <CTableRow class="text-center">
        <CTableHeaderCell scope="col">
          <CFormCheck
            id="checkAll"
            v-model="allChecked"
            @change="checkedAll"
            label="전체"
          />
        </CTableHeaderCell>
        <CTableHeaderCell scope="col">일련번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">차수</CTableHeaderCell>
        <CTableHeaderCell scope="col">타입</CTableHeaderCell>
        <CTableHeaderCell scope="col">동호수</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약자</CTableHeaderCell>
        <CTableHeaderCell scope="col">납입금액합계</CTableHeaderCell>
        <CTableHeaderCell scope="col">최종납입회차</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약일자</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Contract
        v-for="contract in contractBill"
        :contract="contract"
        :key="contract.pk"
        @on-ctor-chk="onCtorChk"
        ref="contractor"
      />
    </CTableBody>
  </CTable>

  <CSmartPagination
    :activePage="1"
    :limit="8"
    :pages="contractPages(10)"
    class="mt-3"
    @on-ctor-pk="ctorChk"
    @active-page-change="pageSelect"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Contract from '@/views/notices/Bill/components/Contract.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ContractorList',
  components: { Contract },
  props: ['project'],
  data() {
    return {
      allChecked: false,
    }
  },
  computed: {
    ...mapGetters('contract', ['contractBill', 'contractPages']),
  },
  methods: {
    pageSelect(page: number) {
      this.$emit('page-select', page)
    },
    checkedAll(this: any) {
      // if (!this.allChecked) {
      //   this.contractors = this.contractBill.map((c: any) => c.ctor_pk)
      // } else {
      //   this.contractors = []
      // }
      // this.$nextTick(() => {
      //   this.$refs.contractor.toggleChk(this.allChecked)
      // })
    },

    onCtorChk(payload: { chk: boolean; pk: number }) {
      this.$emit('on-ctor-chk', payload)
    },
  },
})
</script>
