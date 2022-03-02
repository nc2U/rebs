<template>
  <CCallout color="warning" class="pb-0 mb-4">
    <CRow>
      <CCol>
        <CRow>
          <CFormLabel class="col-sm-1 col-form-label">타입</CFormLabel>
          <CCol md="6" lg="3" class="mb-3">
            <CMultiSelect
              v-model="unitType"
              @change="listFiltering(1)"
              :options="unitTypes"
            />
          </CCol>

          <CFormLabel class="col-sm-1 col-form-label">계약자</CFormLabel>
          <CCol md="6" lg="3" class="mb-3">
            <CMultiSelect
              v-model="contract"
              @change="listFiltering(1)"
              :multiple="false"
              placeholder="계약자 선택"
            />
          </CCol>

          <CFormLabel class="col-sm-1 col-form-label">검색</CFormLabel>
          <CCol md="3" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="search"
                @keydown.enter="listFiltering(1)"
                placeholder="계약자, 입금자, 적요, 비고"
                aria-label="Username"
                aria-describedby="addon-wrapping"
              />
              <CInputGroupText @click="listFiltering(1)">검색</CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
    <CRow>
      <CCol color="warning" class="p-2 pl-3">
        <strong>납부 건수 조회 결과 : 0건</strong>
      </CCol>
      <!--      <CCol class="text-right mb-0" v-if="!formsCheck">-->
      <!--        <CButton color="info" @click="resetForm" size="sm">-->
      <!--          검색조건 초기화-->
      <!--        </CButton>-->
      <!--      </CCol>-->
    </CRow>
  </CCallout>

  <CAlert color="info"></CAlert>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { maska } from 'maska'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'ListController',
  directives: { maska },
  data() {
    return {
      unitType: '',
      contract: '',
      search: '',
    }
  },
  computed: {
    unitTypes(this: any) {
      return this.unitTypeList.map((t: any) => ({
        value: t.pk,
        label: t.name,
        text: t.name,
      }))
    },
    contracts(this: any) {
      return []
    },
    formsCheck(this: any) {
      const a = this.unitType === ''
      const b = this.contract === ''
      const c = this.search === ''
      return a && b && c
    },
    ...mapState('project', ['unitTypeList']),
  },
  methods: {
    listFiltering(page = 1) {
      this.$nextTick(() =>
        this.$emit('payment-filtering', { ...{ page }, ...this }),
      )
    },
    resetForm() {
      this.unitType = ''
      this.contract = ''
      this.search = ''
      this.listFiltering(1)
    },
  },
})
</script>
