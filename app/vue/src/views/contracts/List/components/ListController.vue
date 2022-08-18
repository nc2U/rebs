<script lang="ts" setup>
import { ref, reactive, computed, watch, nextTick } from 'vue'
import { useStore } from 'vuex'
import { dateFormat } from '@/utils/baseMixins'
import DatePicker from '@/components/DatePicker/index.vue'
import { maska as vMaska } from 'maska'

const emit = defineEmits(['cont-filtering'])

const form = reactive({
  status: '2',
  order_group: '',
  unit_type: '',
  building: '',
  registed: '',
  ordering: '-created_at',
  search: '',
})
const from_date = ref('')
const to_date = ref('')

const formsCheck = computed(() => {
  const a = form.status === '2'
  const b = form.order_group === ''
  const c = form.unit_type === ''
  const d = form.building === ''
  const e = form.registed === ''
  const f = from_date.value === ''
  const g = to_date.value === ''
  const h = form.ordering === '-created_at'
  const i = form.search === ''
  const groupA = a && b && c && d && e
  const groupB = f && g && h && i
  return groupA && groupB
})

const store = useStore()

const orderGroupList = computed(() => store.state.contract.orderGroupList)
const contractsCount = computed(() => store.state.contract.contractsCount)
const buildingList = computed(() => store.state.project.buildingList)
const simpleTypes = computed(() => store.getters['project/simpleTypes'])

watch(from_date, () => listFiltering(1))
watch(to_date, () => listFiltering(1))

const listFiltering = (page = 1) => {
  nextTick(() => {
    const from = from_date.value ? dateFormat(from_date.value) : ''
    const to = to_date.value ? dateFormat(to_date.value) : ''
    emit('cont-filtering', {
      ...{ page, from_date: from, to_date: to },
      ...form,
    })
  })
}
defineExpose({ listFiltering })

const resetForm = () => {
  form.status = '2'
  form.order_group = ''
  form.unit_type = ''
  form.building = ''
  form.registed = ''
  from_date.value = ''
  to_date.value = ''
  form.ordering = '-created_at'
  form.search = ''
  listFiltering(1)
}
</script>

<template>
  <CCallout color="info" class="pb-0 mb-4">
    <CRow>
      <CCol lg="7">
        <CRow>
          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.status" @change="listFiltering(1)">
              <option value="2">계약 현황</option>
              <option value="1">청약 현황</option>
              <option value="3">해지 신청</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.order_group" @change="listFiltering(1)">
              <option value="">차수선택</option>
              <option
                v-for="order in orderGroupList"
                :key="order.pk"
                :value="order.pk"
              >
                {{ order.order_group_name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.unit_type" @change="listFiltering(1)">
              <option value="">타입선택</option>
              <option
                v-for="type in simpleTypes"
                :key="type.pk"
                :value="type.pk"
              >
                {{ type.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.building" @change="listFiltering(1)">
              <option value="">동 선택</option>
              <option
                v-for="bldg in buildingList"
                :key="bldg.pk"
                :value="bldg.pk"
              >
                {{ bldg.name }}동
              </option>
            </CFormSelect>
          </CCol>
          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.registed" @change="listFiltering(1)">
              <option value="">인가 구분</option>
              <option value="true">인가</option>
              <option value="false">미인가</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.ordering" @change="listFiltering(1)">
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

      <CCol lg="3">
        <CRow>
          <CCol md="6" class="mb-3">
            <DatePicker
              v-model="from_date"
              v-maska="'####-##-##'"
              placeholder="계약일 (From)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>

          <CCol md="6" class="mb-3">
            <DatePicker
              v-model="to_date"
              v-maska="'####-##-##'"
              placeholder="계약일 (To)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="2">
        <CRow>
          <CCol class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                placeholder="계약자, 전화번호, 일련번호, 비고"
                aria-label="Username"
                aria-describedby="addon-wrapping"
                @keydown.enter="listFiltering(1)"
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
        <CButton color="info" size="sm" @click="resetForm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>
