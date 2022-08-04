<template>
  <CTableRow>
    <CTableDataCell>
      <CFormSelect v-model="form.pay_sort" required>
        <option value="">종류선택</option>
        <option value="1">계약금</option>
        <option value="2">중도금</option>
        <option value="3">잔금</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.pay_code"
        placeholder="납입회차 코드"
        type="number"
        min="0"
        required
        @keypress.enter="formCheck(form.pay_code !== payOrder.pay_code)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.pay_time"
        placeholder="납부순서"
        type="number"
        min="0"
        required
        @keypress.enter="formCheck(form.pay_time !== payOrder.pay_time)"
      />
    </CTableDataCell>

    <CTableDataCell>
      <CCol class="pt-2 pl-3">
        <CFormSwitch
          v-model="form.is_pm_cost"
          :checked="payOrder.is_pm_cost === true"
        />
      </CCol>
    </CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model="form.pay_name"
        placeholder="납부회차 명"
        required
        @keypress.enter="formCheck(form.pay_name !== payOrder.pay_name)"
      />
    </CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model="form.alias_name"
        placeholder="회차 별칭"
        required
        @keypress.enter="formCheck(form.alias_name !== payOrder.alias_name)"
      />
    </CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model="form.pay_due_date"
        v-maska="'####-##-##'"
        placeholder="납부기한일"
        required
        @keypress.enter="formCheck(form.pay_due_date !== payOrder.pay_due_date)"
      />
    </CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model="form.extra_due_date"
        v-maska="'####-##-##'"
        placeholder="납부유예일"
        required
        @keypress.enter="
          formCheck(form.extra_due_date !== payOrder.extra_due_date)
        "
      />
    </CTableDataCell>

    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        :disabled="formsCheck"
        @click="onUpdatePayOrder"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeletePayOrder">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cil-warning" />
      층별 타입 삭제
    </template>
    <template #default>
      이 타입에 종속된 분양가 데이터가 있는 경우 해당 데이터를 모두 제거한 후
      삭제가능 합니다. 해당 층별 타입을 삭제 하시겠습니까?
    </template>
    <template #footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { maska } from 'maska'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'PayOrder',
  directives: { maska },
  components: { ConfirmModal, AlertModal },
  props: ['payOrder'],
  data() {
    return {
      form: {
        pay_sort: '',
        pay_code: null,
        pay_time: null,
        pay_name: '',
        alias_name: '',
        is_pm_cost: false,
        pay_due_date: null,
        extra_due_date: null,
      },
      validated: false,
    }
  },
  created(this: any) {
    if (this.payOrder) {
      this.resetForm()
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.pay_sort === this.payOrder.pay_sort
      const b = this.form.pay_code === this.payOrder.pay_code
      const c = this.form.pay_time === this.payOrder.pay_time
      const d = this.form.pay_name === this.payOrder.pay_name
      const e = this.form.alias_name === this.payOrder.alias_name
      const f = this.form.is_pm_cost === this.payOrder.is_pm_cost
      const g = this.form.pay_due_date === this.payOrder.pay_due_date
      const h = this.form.extra_due_date === this.payOrder.extra_due_date
      return a && b && c && d && e && f && g && h
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    formCheck(bool: boolean) {
      if (bool) this.onUpdatePayOrder()
      return
    },
    onUpdatePayOrder(this: any) {
      if (
        this.superAuth ||
        (this.staffAuth && this.staffAuth.project === '2')
      ) {
        const pk = this.payOrder.pk
        this.$emit('on-update', { ...{ pk }, ...this.form })
      } else {
        this.$refs.alertModal.callModal()
        this.resetForm()
      }
    },
    onDeletePayOrder(this: any) {
      if (this.superAuth) this.$refs.confirmModal.callModal()
      else {
        this.$refs.alertModal.callModal()
        this.resetForm()
      }
    },
    modalAction(this: any) {
      this.$emit('on-delete', this.payOrder.pk)
      this.$refs.confirmModal.visible = false
    },
    resetForm() {
      this.form.pay_sort = this.payOrder.pay_sort
      this.form.pay_code = this.payOrder.pay_code
      this.form.pay_time = this.payOrder.pay_time
      this.form.pay_name = this.payOrder.pay_name
      this.form.alias_name = this.payOrder.alias_name
      this.form.is_pm_cost = this.payOrder.is_pm_cost
      this.form.pay_due_date = this.payOrder.pay_due_date
      this.form.extra_due_date = this.payOrder.extra_due_date
    },
  },
})
</script>
