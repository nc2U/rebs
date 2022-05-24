<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CModalBody class="p-4">
      <div>
        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">거래일자</CFormLabel>
              <CCol sm="8">
                <DatePicker
                  v-model="form.deal_date"
                  required
                  placeholder="거래일자"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">구분</CFormLabel>
              <CCol sm="8">
                <CFormSelect v-model="form.sort" required @change="sort_change">
                  <!--                  :disabled="imprest && imprest.sort !== ''"-->
                  <option value="">---------</option>
                  <option value="1">입금</option>
                  <option value="2">출금</option>
                  <option value="3">대체</option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                계정[상위분류]
              </CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model="form.project_account_d1"
                  @change="d1_change"
                  :required="!form.is_separate"
                  :disabled="form.sort === '' || form.is_separate"
                >
                  <option value="">---------</option>
                  <option
                    v-for="d1 in formAccD1List"
                    :value="d1.pk"
                    :key="d1.pk"
                  >
                    {{ d1.name }}
                  </option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                계정[하위분류]
              </CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model="form.project_account_d2"
                  :required="!form.is_separate"
                  :disabled="form.project_account_d1 === '' || form.is_separate"
                >
                  <option value="">---------</option>
                  <option
                    v-for="d2 in formAccD2List"
                    :value="d2.pk"
                    :key="d2.pk"
                  >
                    {{ d2.name }}
                  </option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">적요</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.content"
                  placeholder="거래 내용"
                  :disabled="form.sort === ''"
                />
              </CCol>
            </CRow>
          </CCol>
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">거래처</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model="form.trader"
                  v-c-tooltip="{
                    content:
                      '분양대금(분담금) 수납 건인 경우 반드시 해당 계좌에 기재된 입금자를 기재',
                    placement: 'top',
                  }"
                  placeholder="거래처 (수납자)"
                  required
                  :disabled="form.sort === ''"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">
                {{ !imprest && form.sort === '3' ? '출금' : '거래' }}계좌
              </CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model="form.bank_account"
                  required
                  :disabled="form.sort === ''"
                >
                  <option value="">---------</option>
                  <option
                    v-for="ba in imprestBAccount"
                    :value="ba.pk"
                    :key="ba.pk"
                  >
                    {{ ba.alias_name }}
                  </option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow v-if="form.sort === '2'">
              <CFormLabel class="col-sm-4 col-form-label">지출증빙</CFormLabel>
              <CCol sm="8">
                <CFormSelect v-model="form.evidence" required>
                  <option value="">---------</option>
                  <option value="0">증빙 없음</option>
                  <option value="1">세금계산서</option>
                  <option value="2">계산서(면세)</option>
                  <option value="3">카드전표/현금영수증</option>
                  <option value="4">간이영수증</option>
                  <option value="5">거래명세서</option>
                  <option value="6">입금표</option>
                  <option value="7">지출결의서</option>
                </CFormSelect>
              </CCol>
            </CRow>

            <CRow v-if="!imprest && form.sort === '3'">
              <CFormLabel class="col-sm-4 col-form-label">입금계좌</CFormLabel>
              <CCol sm="8">
                <CFormSelect
                  v-model="form.bank_account_to"
                  required
                  :disabled="form.sort !== '3'"
                >
                  <option value="">---------</option>
                  <option
                    v-for="ba in imprestBAccount"
                    :value="ba.pk"
                    :key="ba.pk"
                  >
                    {{ ba.alias_name }}
                  </option>
                </CFormSelect>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">출금액</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.outlay"
                  type="number"
                  min="0"
                  placeholder="출금 금액"
                  :required="form.sort === '2'"
                  :disabled="form.sort === '1' || form.sort === ''"
                />
              </CCol>
            </CRow>
          </CCol>

          <CCol sm="6">
            <CRow>
              <CFormLabel class="col-sm-4 col-form-label">입금액</CFormLabel>
              <CCol sm="8">
                <CFormInput
                  v-model.number="form.income"
                  type="number"
                  min="0"
                  placeholder="입금 금액"
                  :required="form.sort === '1'"
                  :disabled="form.sort === '2' || form.sort === ''"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="12">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">비고</CFormLabel>
              <CCol sm="10">
                <CFormTextarea
                  v-model.number="form.note"
                  placeholder="특이사항"
                  :disabled="form.sort === ''"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow>
          <CCol class="text-medium-emphasis">
            <CFormCheck
              v-model="form.is_separate"
              label="별도 분리기록 거래 건 - 여러 계정 항목이 1회에 입·출금되어 별도 분리 기록이 필요한 거래인 경우."
              :disabled="sepDisabled"
            />
          </CCol>
        </CRow>
      </div>

      <div v-if="form.is_separate && imprest">
        <hr v-if="imprest.sepItems.length > 0" />
        <CRow class="mb-3" v-if="imprest.sepItems.length > 0">
          <CCol>
            <strong>
              <CIcon name="cilDescription" class="mr-2" />
              {{
                sepSummary[0] ? `입금액 합계 : ${numFormat(sepSummary[0])}` : ''
              }}
              {{
                sepSummary[1] ? `출금액 합계 : ${numFormat(sepSummary[1])}` : ''
              }}
            </strong>
          </CCol>
        </CRow>

        <CRow
          v-for="(sep, i) in imprest.sepItems"
          :key="sep.pk"
          class="mb-1"
          :class="
            sep.pk === sepPk ? 'text-success text-decoration-underline' : ''
          "
        >
          <CCol sm="1">{{ i + 1 }}</CCol>
          <CCol sm="2">{{ sep.trader }}</CCol>
          <CCol sm="5">{{ cutString(sep.content, 20) }}</CCol>
          <CCol sm="2" class="text-right">
            {{ sep.income ? numFormat(sep.income) : numFormat(sep.outlay) }}
          </CCol>
          <CCol sm="2" class="text-right">
            <CButton
              @click="sepUpdate(sep)"
              type="button"
              color="success"
              size="sm"
            >
              수정
            </CButton>
          </CCol>
        </CRow>
        <hr />
        <CRow class="mb-3">
          <CCol sm="1"></CCol>
          <CCol sm="11">
            <CRow>
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    계정[상위분류]
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormSelect
                      v-model="sepItem.project_account_d1"
                      @change="sepD1_change"
                      required
                    >
                      <option value="">---------</option>
                      <option
                        v-for="d1 in formAccD1List"
                        :value="d1.pk"
                        :key="d1.pk"
                      >
                        {{ d1.name }}
                      </option>
                    </CFormSelect>
                  </CCol>
                </CRow>
              </CCol>
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    계정[하위분류]
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormSelect
                      v-model="sepItem.project_account_d2"
                      :disabled="sepItem.project_account_d1 === ''"
                      required
                    >
                      <option value="">---------</option>
                      <option
                        v-for="d2 in formAccD2List"
                        :value="d2.pk"
                        :key="d2.pk"
                      >
                        {{ d2.name }}
                      </option>
                    </CFormSelect>
                  </CCol>
                </CRow>
              </CCol>
            </CRow>
          </CCol>
        </CRow>
        <CRow class="mb-3">
          <CCol sm="1"></CCol>
          <CCol sm="11">
            <CRow>
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    적요
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormInput
                      v-model="sepItem.content"
                      placeholder="거래 내용"
                    />
                  </CCol>
                </CRow>
              </CCol>
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    거래처
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormInput
                      v-model="sepItem.trader"
                      v-c-tooltip="{
                        content:
                          '분양대금(분담금) 수납 건인 경우 반드시 해당 계좌에 기재된 입금자를 기재',
                        placement: 'top',
                      }"
                      placeholder="거래처 (수납자)"
                      required
                    />
                  </CCol>
                </CRow>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="1"></CCol>
          <CCol sm="11">
            <CRow>
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    거래계좌
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormSelect
                      v-model="sepItem.bank_account"
                      readonly
                      required
                    >
                      <option value="">---------</option>
                      <option
                        v-for="ba in imprestBAccount"
                        :value="ba.pk"
                        :key="ba.pk"
                      >
                        {{ ba.alias_name }}
                      </option>
                    </CFormSelect>
                  </CCol>
                </CRow>
              </CCol>

              <CCol sm="6">
                <CRow v-if="form.sort === '2'">
                  <CFormLabel class="col-sm-4 col-form-label">
                    지출증빙
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormSelect v-model="sepItem.evidence" required>
                      <option value="">---------</option>
                      <option value="0">증빙 없음</option>
                      <option value="1">세금계산서</option>
                      <option value="2">계산서(면세)</option>
                      <option value="3">카드전표/현금영수증</option>
                      <option value="4">간이영수증</option>
                      <option value="5">거래명세서</option>
                      <option value="6">입금표</option>
                      <option value="7">지출결의서</option>
                    </CFormSelect>
                  </CCol>
                </CRow>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="1"></CCol>
          <CCol sm="11">
            <CRow>
              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    출금액
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormInput
                      v-model="sepItem.outlay"
                      type="number"
                      min="0"
                      placeholder="출금 금액"
                      :required="form.sort === '2'"
                      :disabled="form.sort !== '2'"
                    />
                  </CCol>
                </CRow>
              </CCol>

              <CCol sm="6">
                <CRow>
                  <CFormLabel class="col-sm-4 col-form-label">
                    입금액
                  </CFormLabel>
                  <CCol sm="8">
                    <CFormInput
                      v-model="sepItem.income"
                      type="number"
                      min="0"
                      placeholder="입금 금액"
                      :required="form.sort === '1'"
                      :disabled="form.sort !== '1'"
                    />
                  </CCol>
                </CRow>
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CCol sm="1"></CCol>
          <CCol sm="11">
            <CRow>
              <CFormLabel class="col-sm-2 col-form-label">비고</CFormLabel>
              <CCol sm="10">
                <CFormTextarea v-model="sepItem.note" placeholder="특이사항" />
              </CCol>
            </CRow>
          </CCol>
        </CRow>
      </div>
    </CModalBody>

    <CModalFooter>
      <CButton type="button" color="light" @click="$emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
          type="submit"
          :color="imprest ? 'success' : 'primary'"
          :disabled="formsCheck && requireItem"
        >
          저장
        </CButton>
        <CButton
          v-if="imprest"
          type="button"
          color="danger"
          @click="deleteConfirm"
        >
          삭제
        </CButton>
      </slot>
    </CModalFooter>
  </CForm>

  <ConfirmModal ref="delModal">
    <template v-slot:header>
      <CIcon name="cilWarning" />
      운영비(전도금) 거래 정보 삭제
    </template>
    <template v-slot:default>
      삭제한 데이터는 복구할 수 없습니다. 해당 입출금 거래 정보를
      삭제하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent, ref, reactive } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'ProImprestForm',
  components: { DatePicker, ConfirmModal, AlertModal },
  props: {
    imprest: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const sepPk = ref(null)
    let sepItem = reactive({
      project: '',
      sort: '',
      project_account_d1: '',
      project_account_d2: '',
      content: '',
      trader: '',
      bank_account: '',
      income: null,
      outlay: null,
      evidence: '',
      note: '',
      deal_date: '',
      is_separate: false,
      separated: null,
      is_imprest: true,
    })

    if (props.imprest) {
      // eslint-disable-next-line vue/no-setup-props-destructure
      sepItem.project = props.imprest.project
      // eslint-disable-next-line vue/no-setup-props-destructure
      sepItem.sort = props.imprest.sort
      // eslint-disable-next-line vue/no-setup-props-destructure
      sepItem.bank_account = props.imprest.bank_account
      // eslint-disable-next-line vue/no-setup-props-destructure
      sepItem.deal_date = props.imprest.deal_date
      // eslint-disable-next-line vue/no-setup-props-destructure
      sepItem.separated = props.imprest.pk
    }

    return {
      sepPk,
      sepItem,
    }
  },
  data() {
    return {
      form: {
        project: '',
        sort: '',
        project_account_d1: '',
        project_account_d2: '',
        content: '',
        trader: '',
        bank_account: '',
        income: null,
        outlay: null,
        evidence: '',
        note: '',
        deal_date: new Date(),
        is_separate: false,
        separated: null,
        is_imprest: true,
      },
      validated: false,
    }
  },
  created() {
    if (this.imprest) {
      this.form.project = this.imprest.project
      this.form.sort = this.imprest.sort
      this.form.project_account_d1 = this.imprest.project_account_d1
      this.form.project_account_d2 = this.imprest.project_account_d2
      this.form.content = this.imprest.content
      this.form.trader = this.imprest.trader
      this.form.bank_account = this.imprest.bank_account
      this.form.income = this.imprest.income
      this.form.outlay = this.imprest.outlay
      this.form.evidence = this.imprest.evidence
      this.form.note = this.imprest.note
      this.form.deal_date = new Date(this.imprest.deal_date)
      this.form.is_separate = this.imprest.is_separate
      this.form.separated = this.imprest.separated
    }
    this.callAccount()
  },
  computed: {
    requireItem() {
      return (
        this.form.project_account_d1 !== '' &&
        this.form.project_account_d2 !== ''
      )
    },
    sepDisabled() {
      const disabled =
        this.form.project_account_d1 !== '' ||
        this.form.project_account_d2 !== ''
      return this.imprest
        ? disabled || this.imprest.sepItems.length > 0
        : disabled
    },
    formsCheck() {
      if (this.imprest) {
        const a = this.form.project === this.imprest.project
        const b = this.form.sort === this.imprest.sort
        const c =
          this.form.project_account_d1 === this.imprest.project_account_d1
        const d =
          this.form.project_account_d2 === this.imprest.project_account_d2
        const e = this.form.content === this.imprest.content
        const f = this.form.trader === this.imprest.trader
        const g = this.form.bank_account === this.imprest.bank_account
        const h = this.form.income === this.imprest.income
        const i = this.form.outlay === this.imprest.outlay
        const j = this.form.evidence === this.imprest.evidence
        const k = this.form.note === this.imprest.note
        const l =
          this.form.deal_date.toString() ===
          new Date(this.imprest.deal_date).toString()
        const m = this.form.is_separate === this.imprest.is_separate

        return a && b && c && d && e && f && g && h && i && j && k && l && m
      } else return false
    },
    sepSummary() {
      const inc =
        this.imprest.sepItems.length !== 0
          ? this.imprest.sepItems
              .map((s: any) => s.income)
              .reduce((res: any, el: any) => res + el)
          : 0
      const out =
        this.imprest.sepItems.length !== 0
          ? this.imprest.sepItems
              .map((s: any) => s.outlay)
              .reduce((res: any, el: any) => res + el)
          : 0
      return [inc, out]
    },
    pageManageAuth() {
      return (
        this.superAuth ||
        (this.staffAuth && this.staffAuth.project_cash === '2')
      )
    },
    allowedPeriod(this: any) {
      return this.superAuth || this.diffDate(this.imprest.deal_date) <= 30
    },
    ...mapState('proCash', ['formAccD1List', 'formAccD2List']),
    ...mapGetters('proCash', ['imprestBAccount']),
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    sort_change(event: any) {
      if (event.target.value === '1') this.form.outlay = null
      if (event.target.value === '2') this.form.income = null
      if (event.target.value === '3') {
        this.form.project_account_d1 = '17'
        this.form.project_account_d2 = '62'
      } else {
        this.form.project_account_d1 = ''
        this.form.project_account_d2 = ''
      }
      this.callAccount()
    },
    d1_change() {
      this.form.project_account_d2 = ''
      this.callAccount()
    },
    sepD1_change() {
      this.sepItem.project_account_d2 = ''
      this.$nextTick(() => {
        const sort = this.form.sort
        const d1 = this.sepItem.project_account_d1
        this.fetchProFormAccD1List(sort)
        this.fetchProFormAccD2List({ sort, d1 })
      })
    },
    callAccount() {
      this.$nextTick(() => {
        const sort = this.form.sort
        const d1 = this.form.project_account_d1
        this.fetchProFormAccD1List(sort)
        this.fetchProFormAccD2List({ sort, d1 })
      })
    },
    sepUpdate(sep: any) {
      this.sepPk = sep.pk
      this.sepItem.project_account_d1 = sep.project_account_d1
      this.sepItem.project_account_d2 = sep.project_account_d2
      this.sepItem.content = sep.content
      this.sepItem.trader = sep.trader
      this.sepItem.evidence = sep.evidence
      this.sepItem.outlay = sep.outlay
      this.sepItem.income = sep.income
      this.sepItem.note = sep.note
    },
    createConfirm(this: any, payload: any) {
      if (this.pageManageAuth) this.multiSubmit(payload)
      else this.$refs.alertModal.callModal()
    },
    updateConfirm(this: any, payload: any) {
      if (this.pageManageAuth)
        if (this.allowedPeriod) this.multiSubmit(payload)
        else
          this.$refs.alertModal.callModal(
            null,
            '거래일로부터 30일이 경과한 건은 수정할 수 없습니다. 관리자에게 문의바랍니다.',
          )
      else this.$refs.alertModal.callModal()
    },
    deleteConfirm(this: any) {
      if (this.pageManageAuth)
        if (this.allowedPeriod) this.$refs.delModal.callModal()
        else
          this.$refs.alertModal.callModal(
            null,
            '거래일로부터 30일이 경과한 건은 삭제할 수 없습니다. 관리자에게 문의바랍니다.',
          )
      else this.$refs.alertModal.callModal()
    },
    onSubmit(this: any, event: any) {
      const form = event.currentTarget
      if (form.checkValidity() === false) {
        event.preventDefault()
        event.stopPropagation()

        this.validated = true
      } else {
        let formData = {}
        if (!this.formsCheck) {
          this.form.deal_date = this.dateFormat(this.form.deal_date)
          if (!this.imprest) formData = { ...this.form }
          else formData = { ...{ ...{ pk: this.imprest.pk }, ...this.form } }
        }
        let sepData = {}
        if (this.form.is_separate) {
          if (!this.sepPk) sepData = { ...this.sepItem }
          else sepData = { ...{ ...{ pk: this.sepPk }, ...this.sepItem } }
        }
        if (this.imprest || this.sepPk)
          this.updateConfirm({ formData, sepData })
        else this.createConfirm({ formData, sepData })
      }
    },
    multiSubmit(multiPayload: any) {
      this.$emit('multi-submit', multiPayload)
      this.$emit('close')
    },
    deleteObject(this: any) {
      this.$emit('on-delete', {
        project: this.imprest.project,
        pk: this.imprest.pk,
      })
      this.$refs.delModal.visible = false
      this.$emit('close')
    },
    ...mapActions('proCash', [
      'fetchProFormAccD1List',
      'fetchProFormAccD2List',
    ]),
  },
})
</script>
