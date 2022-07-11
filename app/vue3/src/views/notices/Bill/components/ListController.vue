<template>
  <CCallout color="primary" class="pb-0 mb-4">
    <CRow>
      <CCol lg="7">
        <CRow>
          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.limit">
              <option value="">표시 개수</option>
              <option value="5">5 개</option>
              <option value="10">10 개</option>
              <option value="15">15 개</option>
              <option value="20">20 개</option>
              <option value="25">25 개</option>
              <option value="30">30 개</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.group">
              <option value="">차수선택</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.type">
              <option value="">타입선택</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.dong">
              <option value="">동 선택</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="4" class="mb-3">
            <CFormSelect v-model="form.order">
              <option value="-created_at">등록일시 내림차순</option>
              <option value="created_at">등록일시 올림차순</option>
              <option value="-contractor__contract_date">
                계약일자 내림차순
              </option>
              <option value="contractor__contract_date">
                계약일자 올림차순
              </option>
              <option value="-serial_number">일련번호 내림차순</option>
              <option value="serial_number">일련번호 올림차순</option>
              <option value="-contractor__name">계약자명 내림차순</option>
              <option value="contractor__name">계약자명 올림차순</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="5">
        <CRow>
          <CCol md="6" class="pt-1 mb-3 text-primary light-yellow">
            <span>[계약금] - 4차계약금 </span>
          </CCol>
          <CCol md="6" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.q"
                placeholder="계약자, 일련번호, 비고"
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
        <strong>계약 건수 조회 결과 : {{ contractsCount }} 건</strong>
      </CCol>
      <CCol class="text-right mb-0" v-if="!formsCheck">
        <CButton color="info" @click="resetForm" size="sm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { maska } from 'maska'
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ListController',
  directives: { maska },
  data() {
    return {
      form: {
        limit: '',
        group: '',
        type: '',
        dong: '',
        order: '-created_at',
        q: '',
      },
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.limit === ''
      const b = this.form.group === ''
      const c = this.form.type === ''
      const d = this.form.dong === ''
      const e = this.form.order === '-created_at'
      const f = this.form.q === ''
      return a && b && c && d && e && f
    },
    ...mapState('contract', ['orderGroupList', 'contractsCount']),
    ...mapState('project', ['buildingList']),
    ...mapGetters('project', ['simpleTypes']),
  },
  methods: {
    listFiltering(this: any, page = 1) {
      this.$nextTick(() => {
        this.$emit('cont-filtering', {
          ...{ page },
          ...this.form,
        })
      })
    },
    resetForm() {
      this.form.limit = ''
      this.form.group = ''
      this.form.type = ''
      this.form.dong = ''
      this.form.order = '-created_at'
      this.form.q = ''
      this.listFiltering(1)
    },
  },
})
</script>

<style lang="scss" scoped>
.light-yellow {
  text-align: center;
  line-height: 30px;
  background: lightyellow !important;
}
</style>
