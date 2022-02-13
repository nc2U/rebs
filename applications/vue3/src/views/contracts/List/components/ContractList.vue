<template>
  <CTable hover responsive>
    <colgroup>
      <col width="10%" />
      <col width="8%" />
      <col width="8%" />
      <col width="10%" />
      <col width="10%" />
      <col width="8%" />
      <col width="20%" />
      <col width="14%" />
      <col width="12%" />
    </colgroup>

    <CTableHead>
      <CTableRow color="dark">
        <CTableHeaderCell scope="col">일련번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">차수</CTableHeaderCell>
        <CTableHeaderCell scope="col">타입</CTableHeaderCell>
        <CTableHeaderCell scope="col">동호수</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약자</CTableHeaderCell>
        <CTableHeaderCell scope="col">인가 등록여부</CTableHeaderCell>
        <CTableHeaderCell scope="col">주소</CTableHeaderCell>
        <CTableHeaderCell scope="col">연락처</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약일자</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Contract
        v-for="contract in contractIndex"
        :contract="contract"
        :key="contract.pk"
      />
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Contract from '@/views/contracts/List/components/Contract.vue'
import { mapActions, mapGetters } from 'vuex'

export default defineComponent({
  name: 'ContractList',
  components: { Contract },
  created() {
    this.fetchContractList({ project: this.initProjId })
  },
  computed: {
    ...mapGetters('contract', ['contractIndex']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    onSelectAdd(this: any, target: any) {
      if (target !== '') this.fetchContractList(target)
      else this.$store.state.contract.contractList = []
    },
    ...mapActions('contract', ['fetchContractList']),
  },
})
</script>
