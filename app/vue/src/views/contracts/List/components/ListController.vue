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

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
import { mapGetters, mapState } from 'vuex'
import { maska } from 'maska'

export default defineComponent({
  name: 'ListController',
  components: { DatePicker },
  directives: { maska },
  data() {
    return {
      form: {
        status: '2',
        order_group: '',
        unit_type: '',
        building: '',
        registed: '',
        ordering: '-created_at',
        search: '',
      },
      from_date: '',
      to_date: '',
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.status === '2'
      const b = this.form.order_group === ''
      const c = this.form.unit_type === ''
      const d = this.form.building === ''
      const e = this.form.registed === ''
      const f = this.from_date === ''
      const g = this.to_date === ''
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
  watch: {
    from_date() {
      this.listFiltering(1)
    },
    to_date() {
      this.listFiltering(1)
    },
  },
  methods: {
    listFiltering(this: any, page = 1) {
      this.$nextTick(() => {
        const from_date = this.from_date ? this.dateFormat(this.from_date) : ''
        const to_date = this.to_date ? this.dateFormat(this.to_date) : ''
        this.$emit('cont-filtering', {
          ...{ page, from_date, to_date },
          ...this.form,
        })
      })
    },
    resetForm() {
      this.form.status = '2'
      this.form.order_group = ''
      this.form.unit_type = ''
      this.form.building = ''
      this.form.registed = ''
      this.from_date = ''
      this.to_date = ''
      this.form.ordering = '-created_at'
      this.form.search = ''
      this.listFiltering(1)
    },
  },
})
</script>
