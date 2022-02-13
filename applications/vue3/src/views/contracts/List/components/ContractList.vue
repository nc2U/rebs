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

  <span v-if="project">
    {{ project.name }}
  </span>

  <CSmartPagination
    :activePage="1"
    :limit="8"
    :pages="62"
    align="end"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Contract from '@/views/contracts/List/components/Contract.vue'
import { mapActions, mapGetters } from 'vuex'

export default defineComponent({
  name: 'ContractList',
  components: { Contract },
  props: ['project'],
  computed: {
    ...mapGetters('contract', ['contractIndex']),
  },
  methods: {
    pageSelect(page: number) {
      this.$emit('page-select', page)
    },
  },
})
</script>
