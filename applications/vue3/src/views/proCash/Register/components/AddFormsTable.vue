<template>
  <CTable hover responsive>
    <colgroup>
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
    </colgroup>
    <CTableHead color="dark">
      <CTableRow class="text-center">
        <CTableHeaderCell>구분</CTableHeaderCell>
        <CTableHeaderCell>계정[상위]</CTableHeaderCell>
        <CTableHeaderCell>계정[하위]</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
        <CTableHeaderCell>거래계좌</CTableHeaderCell>
        <CTableHeaderCell>입금액</CTableHeaderCell>
        <CTableHeaderCell>출금액</CTableHeaderCell>
        <CTableHeaderCell>증빙자료</CTableHeaderCell>
        <CTableHeaderCell>비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <AddForm v-for="i in forms" :key="i" />
    </CTableBody>
  </CTable>

  <CAlert color="secondary">
    <CRow>
      <CCol xs="6">
        <CIcon name="cilPlus" class="mr-2 text-dark" />
        <router-link to="#" @click="forms += 1">
          입출금 입력 폼 추가
        </router-link>
      </CCol>

      <CCol xs="6" class="text-right" v-show="minusShow">
        <CIcon name="cilMinus" class="mr-2 text-danger" />
        <router-link to="#" @click="forms -= 1">
          입출금 입력 폼 제거
        </router-link>
      </CCol>
    </CRow>
  </CAlert>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import AddForm from '@/views/proCash/Register/components/AddForm.vue'

export default defineComponent({
  name: 'AddFormsTable',
  components: { AddForm },
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      forms: 2,
    }
  },
  computed: {
    minusShow() {
      return this.forms > 1
    },
  },
  methods: {},
})
</script>
