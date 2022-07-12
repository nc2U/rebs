<template>
  <CCallout color="primary" class="pb-0 mb-4">
    <CRow>
      <CCol lg="7">
        <CRow>
          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect
              v-model="form.limit"
              @change="listFiltering(1)"
              disabled
            >
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
                v-for="dong in buildingList"
                :value="dong.pk"
                :key="dong.pk"
              >
                {{ dong.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="4" class="mb-3">
            <CFormSelect v-model="form.ordering" @change="listFiltering(1)">
              <option value="contractor__name">계약자명 올림차순</option>
              <option value="-contractor__name">계약자명 내림차순</option>
              <option value="contractor__contract_date">
                계약일자 올림차순
              </option>
              <option value="-contractor__contract_date">
                계약일자 내림차순
              </option>
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
          <CCol md="6" class="pt-1 mb-3 text-primary light-yellow">
            <strong>{{ now_order }}</strong>
          </CCol>
          <CCol md="6" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                @change="listFiltering(1)"
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
  props: {
    now_order: String,
  },
  data() {
    return {
      form: {
        limit: '',
        order_group: '',
        unit_type: '',
        building: '',
        ordering: 'contractor__name',
        search: '',
      },
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.limit === ''
      const b = this.form.order_group === ''
      const c = this.form.unit_type === ''
      const d = this.form.building === ''
      const e = this.form.ordering === 'contractor__name'
      const f = this.form.search === ''
      return a && b && c && d && e && f
    },
    ...mapState('contract', ['orderGroupList', 'contractsCount']),
    ...mapGetters('project', ['simpleTypes']),
    ...mapState('project', ['buildingList']),
  },
  methods: {
    listFiltering(this: any, page = 1) {
      this.$nextTick(() => {
        this.$emit('list-filtering', {
          ...{ page },
          ...this.form,
        })
      })
    },
    resetForm() {
      this.form.limit = ''
      this.form.order_group = ''
      this.form.unit_type = ''
      this.form.building = ''
      this.form.ordering = 'contractor__name'
      this.form.search = ''
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
