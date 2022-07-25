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
                  @keydown.enter="listFiltering(1)"
                  aria-label="Search"
                  aria-describedby="addon-wrapping"
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
      <CCol color="warning" class="p-2 pl-3" v-if="contractIndex.length !== 0">
        <CButton
            type="button"
            color="dark"
            v-for="cont in contractIndex"
            :key="cont.pk"
            @click="getContract(cont.pk)"
            variant="outline"
            size="sm"
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
              :to="{ name: '계약등록 관리', query: { contract: contract.pk } }"
              v-c-tooltip="'계약등록 관리'"
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
              :to="{ name: '계약등록 관리', query: { contract: contract.pk } }"
              v-c-tooltip="'계약등록 관리'"
          >
            계약자 : {{ contract.contractor.name }})
          </router-link>

          (
          <router-link to="" @click="get_print_payment">
            납부내역서 출력
          </router-link>
          )
        </strong>
      </CCol>
      <CCol class="text-right" v-if="contract">
        <router-link to="">
          <CIcon name="cilX" @click="removeContract"/>
        </router-link>
      </CCol>
    </CRow>
  </CAlert>
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import {maska} from 'maska'
import {mapGetters} from 'vuex'

export default defineComponent({
  name: 'ContChoicer',
  components: {},

  directives: {maska},
  props: {project: Object, contract: Object},
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
    ...mapGetters('contract', ['contractIndex']),
  },
  methods: {
    listFiltering(this: any, page = 1) {
      this.$nextTick(() => {
        if (this.form.search === '') this.pageInit()
        else this.$emit('list-filtering', {...{page}, ...this.form})
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
    get_print_payment() {
      const url = '/rebs/pdf-payments/'
      const project = this.project ? this.project.pk : ''
      const contract = this.contract ? this.contract.pk : ''
      location.href = `${url}?project=${project}&contract=${contract}`
    }
  },
})
</script>
