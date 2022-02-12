<template>
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
              <CTableDataCell>
                <span v-if="company">{{ company.name }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                대표자명
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.ceo }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                사업자등록번호
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.tax_number }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                법인등록번호
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.org_number }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                업태
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.business_cond }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                종목
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.business_even }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                설립일자
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.es_date }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                개업일자
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.op_date }}</span>
              </CTableDataCell>
            </CTableRow>

            <CTableRow>
              <CTableHeaderCell scope="row" color="dark">
                회사주소
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">
                  <span v-if="company.zipcode">({{ company.zipcode }})</span>
                  {{ company.address1 }} {{ company.address2 }}
                  {{ company.address3 }}
                </span>
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
        <CButton
          v-if="staffAuth && company"
          type="button"
          color="success"
          @click="toEdit"
        >
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
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'CompanyDetail',
  props: {
    company: {
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
