<script lang="ts" setup>
import { ref } from 'vue'
import { useAccount } from '@/store/pinia/account'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { headerSecondary } from '@/utils/cssMixins'

const props = defineProps({
  company: {
    type: Object,
    default: null,
  },
})
const emit = defineEmits(['create-form', 'update-form'])

const alertModal = ref()

const account = useAccount()

const toEdit = () => {
  if (
    account.superAuth ||
    (account.staffAuth && account.staffAuth.company_settings === '2')
  )
    emit('update-form')
  else alertModal.value.callModal()
}
const toCreate = () => {
  if (account.superAuth) emit('create-form')
  else alertModal.value.callModal()
}
</script>

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
              <CTableHeaderCell scope="row" :color="headerSecondary">
                회사명
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.name }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" :color="headerSecondary">
                대표자명
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.ceo }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" :color="headerSecondary">
                사업자등록번호
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.tax_number }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" :color="headerSecondary">
                법인등록번호
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.org_number }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" :color="headerSecondary">
                업태
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.business_cond }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" :color="headerSecondary">
                종목
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.business_even }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" :color="headerSecondary">
                설립일자
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.es_date }}</span>
              </CTableDataCell>
            </CTableRow>
            <CTableRow>
              <CTableHeaderCell scope="row" :color="headerSecondary">
                개업일자
              </CTableHeaderCell>
              <CTableDataCell>
                <span v-if="company">{{ company.op_date }}</span>
              </CTableDataCell>
            </CTableRow>

            <CTableRow>
              <CTableHeaderCell scope="row" :color="headerSecondary">
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
          type="button"
          color="success"
          :disabled="!company"
          @click="toEdit"
        >
          <CIcon name="cil-check-circle" />
          수정하기
        </CButton>
      </CCol>
      <CCol xs="auto">
        <CButton type="button" color="primary" @click="toCreate">
          <CIcon name="cil-check-circle" />
          등록하기
        </CButton>
      </CCol>
    </CRow>
  </CCardFooter>

  <AlertModal ref="alertModal" />
</template>
