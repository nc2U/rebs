<template>
  <!--  <CCard>-->
  <CCardBody>
    <CRow>
      <CCol class="pt-2">
        <CTable hover responsive>
          <colgroup>
            <col width="25%" />
            <col width="75%" />
          </colgroup>
          <CTableHead>
            <CTableRow>
              <CTableHeaderCell scope="col"></CTableHeaderCell>
              <CTableHeaderCell scope="col"></CTableHeaderCell>
            </CTableRow>
          </CTableHead>
          <CTableBody>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                회사명
              </CTableHeaderCell>
              <CTableDataCell>{{ company.name }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                대표자명
              </CTableHeaderCell>
              <CTableDataCell>{{ company.ceo }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                사업자등록번호
              </CTableHeaderCell>
              <CTableDataCell>{{ company.tax_number }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                법인등록번호
              </CTableHeaderCell>
              <CTableDataCell>{{ company.org_number }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                업태
              </CTableHeaderCell>
              <CTableDataCell>{{ company.business_cond }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                종목
              </CTableHeaderCell>
              <CTableDataCell>{{ company.business_even }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                설립일자
              </CTableHeaderCell>
              <CTableDataCell>{{ company.es_date }}</CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                개업일자
              </CTableHeaderCell>
              <CTableDataCell>{{ company.op_date }}</CTableDataCell>
            </CTableRow>

            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                회사주소
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company.zipcode">({{ company.zipcode }})</span>
                {{ company.address1 }} {{ company.address2 }}
                {{ company.address3 }}
              </CTableDataCell>
            </CTableRow>
          </CTableBody>
        </CTable>
      </CCol>
    </CRow>
  </CCardBody>

  <CCardFooter>
    <CRow class="justify-content-between">
      <CCol xs="auto">
        <CButton v-if="staffAuth" type="button" color="success" @click="toEdit">
          <CIcon name="cil-check-circle" />
          수정하기
        </CButton>
      </CCol>
      <CCol xs="auto">
        <CButton
          v-if="superAuth"
          type="button"
          color="primary"
          @click="toCreate"
        >
          <CIcon name="cil-check-circle" />
          등록하기
        </CButton>
      </CCol>
    </CRow>
  </CCardFooter>
  <!--  </CCard>-->
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { CTableDataCell } from '@coreui/vue-pro/src/components/table'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'CompanyDetail',
  components: { CTableDataCell },
  props: {
    company: {
      type: Object,
      required: true,
    },
    userInfo: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    toEdit() {
      this.$emit('update-form')
    },
    toCreate() {
      this.$emit('create-form')
    },
  },
})
</script>

<style scoped></style>
