<script lang="ts" setup>
import { computed, reactive, nextTick } from 'vue'
import { useContract } from '@/store/pinia/contract'
import { useProjectData } from '@/store/pinia/project_data'
import { bgLight } from '@/utils/cssMixins'

defineProps({ nowOrderName: { type: String, default: '' } })
const emit = defineEmits(['list-filtering'])

const contractStore = useContract()
const orderGroupList = computed(() => contractStore.orderGroupList)
const contractsCount = computed(() => contractStore.contractsCount)

const projectDataStore = useProjectData()
const buildingList = computed(() => projectDataStore.buildingList)
const simpleTypes = computed(() => projectDataStore.simpleTypes)

const form = reactive({
  order_group: '',
  unit_type: '',
  building: '',
  ordering: 'contractor__name',
  search: '',
  // limit: '',
})

const formsCheck = computed(() => {
  const a = form.order_group === ''
  const b = form.unit_type === ''
  const c = form.building === ''
  const d = form.ordering === 'contractor__name'
  const e = form.search.trim() === ''
  // const a = form.limit === ''
  return a && b && c && d && e
})

const listFiltering = (page = 1) => {
  nextTick(() => {
    form.search = form.search.trim()
    emit('list-filtering', {
      ...{ page },
      ...form,
    })
  })
}

const resetForm = () => {
  form.order_group = ''
  form.unit_type = ''
  form.building = ''
  form.ordering = 'contractor__name'
  form.search = ''
  // form.limit = ''
  listFiltering(1)
}

defineExpose({ listFiltering })
</script>

<template>
  <CCallout color="primary" class="pb-0 mb-4" :class="bgLight">
    <CRow>
      <CCol lg="7">
        <CRow>
          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect disabled @change="listFiltering(1)">
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
            <CFormSelect v-model="form.order_group" @change="listFiltering(1)">
              <option value="">차수선택</option>
              <option v-for="order in orderGroupList" :key="order.pk" :value="order.pk">
                {{ order.order_group_name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.unit_type" @change="listFiltering(1)">
              <option value="">타입선택</option>
              <option v-for="type in simpleTypes" :key="type.pk" :value="type.pk">
                {{ type.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.building" @change="listFiltering(1)">
              <option value="">동 선택</option>
              <option v-for="dong in buildingList" :key="dong.pk" :value="dong.pk">
                {{ dong.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="4" class="mb-3">
            <CFormSelect v-model="form.ordering" @change="listFiltering(1)">
              <option value="contractor__name">계약자명 올림차순</option>
              <option value="-contractor__name">계약자명 내림차순</option>
              <option value="contractor__contract_date">계약일자 올림차순</option>
              <option value="-contractor__contract_date">계약일자 내림차순</option>
              <option value="created_at">등록일시 올림차순</option>
              <option value="-created_at">등록일시 내림차순</option>
              <option value="serial_number">일련번호 올림차순</option>
              <option value="-serial_number">일련번호 내림차순</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="5">
        <CRow>
          <CCol md="6" class="mb-3 text-primary light-yellow">
            <strong>{{ nowOrderName }}</strong>
          </CCol>
          <CCol md="6" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                placeholder="계약자, 전화번호, 일련번호, 비고"
                aria-label="Username"
                aria-describedby="addon-wrapping"
                @change="listFiltering(1)"
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
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm"> 검색조건 초기화 </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>

<style lang="scss" scoped>
.light-yellow {
  text-align: center;
  line-height: 30px;
  background: lightyellow !important;
}
</style>
