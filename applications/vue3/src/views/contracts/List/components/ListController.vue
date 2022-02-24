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
                :value="order.pk"
                :key="order.pk"
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
                :value="type.pk"
                :key="type.pk"
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
                :value="bldg.pk"
                :key="bldg.pk"
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
      <CCol lg="5">
        <CRow>
          <CCol md="6" lg="3" class="mb-3">
            <CFormInput
              v-model="form.from_date"
              @keydown.enter="listFiltering(1)"
              v-maska="'####-##-##'"
              placeholder="계약일자(From)"
            />
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormInput
              v-model="form.to_date"
              @keydown.enter="listFiltering(1)"
              v-maska="'####-##-##'"
              placeholder="계약일자(To)"
            />
          </CCol>

          <CCol lg="6" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                @keydown.enter="listFiltering(1)"
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
import { mapGetters, mapState } from 'vuex'
import { maska } from 'maska'

export default defineComponent({
  name: 'ListController',
  components: {},

  directives: { maska },
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      form: {
        status: '2',
        order_group: '',
        unit_type: '',
        building: '',
        registed: '',
        from_date: '',
        to_date: '',
        ordering: '-created_at',
        search: '',
      },
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.status === '2'
      const b = this.form.order_group === ''
      const c = this.form.unit_type === ''
      const d = this.form.building === ''
      const e = this.form.registed === ''
      const f = this.form.from_date === ''
      const g = this.form.to_date === ''
      const h = this.form.ordering === '-created_at'
      const i = this.form.search === ''
      const groupA = a && b && c && d && e
      const groupB = f && g && h && i
      return groupA && groupB
    },
    ...mapState('contract', ['orderGroupList', 'contractsCount']),
    ...mapState('project', ['buildingList']),
    ...mapGetters('project', ['simpleTypes']),
  },
  methods: {
    listFiltering(page = 1) {
      this.$nextTick(() =>
        this.$emit('cont-filtering', { ...{ page }, ...this.form }),
      )
    },
    resetForm() {
      this.form.status = '2'
      this.form.order_group = ''
      this.form.unit_type = ''
      this.form.building = ''
      this.form.registed = ''
      this.form.from_date = ''
      this.form.to_date = ''
      this.form.ordering = '-created_at'
      this.form.search = ''
      this.listFiltering(1)
    },
  },
})
</script>
