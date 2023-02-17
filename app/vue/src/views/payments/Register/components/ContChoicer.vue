<script lang="ts" setup>
import { ref, reactive, computed, nextTick, onMounted } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { usePayment } from '@/store/pinia/payment'
import TableTitleRow from '@/components/TableTitleRow.vue'

const props = defineProps({
  project: { type: Object, default: null },
  contract: { type: Object, default: null },
})

const emit = defineEmits(['list-filtering', 'get-contract'])

const contractStore = useContract()
const contractIndex = computed(() => contractStore.contractIndex)

const paymentUrl = computed(() => {
  const url = '/rebs/pdf-payments/'
  const project = props.project ? props.project : ''
  const contract = props.contract ? props.contract.pk : ''
  return `${url}?project=${project}&contract=${contract}`
})

const form = reactive({ search: '' })
const msg = ref('')
const textClass = ref('')

const pageInit = () => {
  form.search = ''
  textClass.value = 'text-medium-emphasis'
  msg.value = '계약자 관련정보 또는 계약 일련변호를 입력하세요.'
  contractStore.contractList = []
}

const listFiltering = (page = 1) => {
  nextTick(() => {
    form.search = form.search.trim()
    if (form.search === '') pageInit()
    else emit('list-filtering', { ...{ page }, ...form })
  })
  if (contractIndex.value.length === 0) {
    msg.value = `해당 검색어로 등록된 데이터가 없습니다.`
    textClass.value = 'text-danger'
  }
}
const getContract = (cont: number) => {
  emit('get-contract', cont)
  pageInit()
}

const paymentStore = usePayment()
const removeContract = () => {
  contractStore.contract = null
  paymentStore.paymentList = []
  paymentStore.paymentsCount = 0
}

onMounted(() => pageInit())
</script>

<template>
  <CCallout color="warning" class="pb-0 mb-4">
    <CRow>
      <CCol>
        <CRow>
          <CCol md="4" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                placeholder="계약자, 비고, 계약 일련번호"
                aria-label="Search"
                aria-describedby="addon-wrapping"
                @keydown.enter="listFiltering(1)"
              />
              <CInputGroupText @click="listFiltering(1)">
                계약 건 찾기
              </CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
    <CRow>
      <CCol v-if="contractIndex.length !== 0" color="warning" class="p-2 pl-3">
        <CButton
          v-for="cont in contractIndex"
          :key="cont.pk"
          type="button"
          color="dark"
          variant="outline"
          size="sm"
          @click="getContract(cont.pk)"
        >
          {{ `${cont.contractor}(${cont.serial_number})` }}
        </CButton>
      </CCol>
      <CCol v-else class="mt-3 m-2" :class="textClass">
        {{ msg }}
      </CCol>
    </CRow>
  </CCallout>

  <CAlert v-if="contract" color="info">
    <CRow>
      <CCol xs="10">
        <strong v-if="contract">
          [일련번호 :
          <router-link
            v-c-tooltip="'계약 등록 관리'"
            :to="{ name: '계약 등록 관리', query: { contract: contract.pk } }"
          >
            {{ contract.serial_number }}
          </router-link>
          ] (타입 :
          {{ contract.unit_type.name }}
          {{
            contract.keyunit.houseunit
              ? contract.keyunit.houseunit.__str__
              : '--- 동호수 현재 미정 ---'
          }}
          |
          <router-link
            v-c-tooltip="'계약 등록 관리'"
            :to="{ name: '계약 등록 관리', query: { contract: contract.pk } }"
          >
            계약자 : {{ contract.contractor.name }})
          </router-link>
          (
          <a :href="paymentUrl"> 납부내역서 출력</a>
          )
        </strong>
      </CCol>
      <CCol v-if="contract" class="text-right">
        <router-link to="">
          <CIcon name="cilX" @click="removeContract" />
        </router-link>
      </CCol>
    </CRow>
  </CAlert>
  <TableTitleRow :disabled="!contract" pdf :url="paymentUrl" />
</template>
