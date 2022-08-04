<template>
  <CRow>
    <CCol class="pl-4 pr-4">
      <CCallout color="warning" class="pb-1 mb-4">
        <CRow>
          <CCol>
            <CRow>
              <CCol md="5" class="mb-3">
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
          <CCol
            v-if="contractIndex.length !== 0"
            color="warning"
            class="p-2 pl-3"
          >
            <CButton
              v-for="cont in contractIndex"
              :key="cont.pk"
              type="button"
              color="dark"
              variant="outline"
              size="sm"
              @click="contMatching(cont)"
            >
              {{ `${cont.contractor}(${cont.serial_number})` }}
            </CButton>
          </CCol>
          <CCol v-else class="mt-3 m-2" :class="textClass">
            {{ msg }}
          </CCol>
        </CRow>
      </CCallout>

      <CAlert
        v-if="contractIndex.length !== 0"
        color="default"
        class="pt-0 pb-0"
      >
        상기 계약 건 중 아래 수납 항목을 매칭 등록할 계약 건을 클릭하여
        주십시요.
      </CAlert>

      <CAlert color="info">
        <span>
          {{
            `[입금자] : ${payment.trader}  | [입금액] : ${numFormat(
              payment.income,
            )} | [입금계좌] : ${payment.bank_account} | [입금일] : ${
              payment.deal_date
            }`
          }}
        </span>
      </CAlert>
    </CCol>
  </CRow>

  <ConfirmModal ref="confirmModal">
    <template #header>건별 수납 매칭</template>
    <template #default>
      해당 수납 항목을 이 계약 건 &lt;{{
        `${cont.contractor}(${cont.serial_number})`
      }}&gt; 에 등록하시겠습니까?
    </template>
    <template #footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ContChoicer',
  components: { ConfirmModal, AlertModal },
  props: { payment: Object },
  data() {
    return {
      form: {
        search: '',
      },
      cont: {},
      msg: '',
      textClass: '',
    }
  },
  created() {
    this.pageInit()
  },
  computed: {
    pageManageAuth() {
      return (
        this.superAuth || (this.staffAuth && this.staffAuth.payment === '2')
      )
    },
    ...mapState('project', ['project']),
    ...mapGetters('contract', ['contractIndex']),
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    listFiltering(this: any) {
      this.$nextTick(() => {
        if (this.form.search === '') this.pageInit()
        else {
          const project = this.project.pk
          this.fetchContractList({ ...{ project }, ...this.form })
        }
      })
      if (this.contractIndex.length === 0) {
        this.msg = `해당 검색어로 등록된 데이터가 없습니다.`
        this.textClass = 'text-danger'
      }
    },
    contMatching(this: any, cont: number) {
      if (this.pageManageAuth) {
        this.cont = cont
        this.$refs.confirmModal.callModal()
      } else this.$refs.alertModal.callModal()
    },
    modalAction(this: any) {
      const pk = this.payment.pk
      const is_contract_payment = true
      const contract = this.cont.pk
      const content = `${this.cont.contractor}[${this.cont.serial_number}] 대금납부`
      this.$emit('on-patch', { pk, is_contract_payment, contract, content })
      this.pageInit()
      this.$emit('close')
    },
    pageInit(this: any) {
      this.form.search = ''
      this.textClass = 'text-medium-emphasis'
      this.msg = '계약자 관련정보 또는 계약 일련변호를 입력하세요.'
      this.$store.state.contract.contractList = []
    },
    ...mapActions('contract', ['fetchContractList']),
  },
})
</script>
