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

  <CAlert :color="contract ? 'info' : 'secondary'">
    <CRow>
      <CCol xs="10">
        <strong v-if="contract">
          [일련번호 :
          <router-link
            v-c-tooltip="'계약등록 관리'"
            :to="{ name: '계약등록 관리', query: { contract: contract.pk } }"
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
            v-c-tooltip="'계약등록 관리'"
            :to="{ name: '계약등록 관리', query: { contract: contract.pk } }"
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
  <TableTitleRow v-if="contract" pdf :url="paymentUrl" />
</template>

<script lang="ts">
import TableTitleRow from '@/components/TableTitleRow.vue'
import { defineComponent } from 'vue'
import { maska } from 'maska'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ContChoicer',
  components: { TableTitleRow },

  directives: { maska },
  props: { project: Object, contract: Object },
  data() {
    return {
      form: {
        search: '',
      },
      msg: '',
      textClass: '',
    }
  },
  created() {
    this.pageInit()
  },
  computed: {
    paymentUrl() {
      const url = '/rebs/pdf-payments/'
      const project = this.project ? this.project.pk : ''
      const contract = this.contract ? this.contract.pk : ''
      return `${url}?project=${project}&contract=${contract}`
    },
    ...mapGetters('contract', ['contractIndex']),
  },
  methods: {
    listFiltering(this: any, page = 1) {
      this.$nextTick(() => {
        if (this.form.search === '') this.pageInit()
        else this.$emit('list-filtering', { ...{ page }, ...this.form })
      })
      if (this.contractIndex.length === 0) {
        this.msg = `해당 검색어로 등록된 데이터가 없습니다.`
        this.textClass = 'text-danger'
      }
    },
    getContract(cont: number) {
      this.$emit('get-contract', cont)
      this.pageInit()
    },
    pageInit(this: any) {
      this.form.search = ''
      this.textClass = 'text-medium-emphasis'
      this.msg = '계약자 관련정보 또는 계약 일련변호를 입력하세요.'
      this.$store.state.contract.contractList = []
    },
    removeContract(this: any) {
      this.$store.state.contract.contract = null
      this.$store.state.payment.paymentList = []
    },
  },
})
</script>
