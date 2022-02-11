<template>
  <CTableRow>
    <CTableDataCell>
      <CFormSelect v-model.number="form.pay_sort" required>
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
        @click="onUpdateFloor"
        :disabled="formsCheck"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteFloor">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-warning" />
      층별 타입 삭제
    </template>
    <template v-slot:default>
      이 타입에 종속된 분양가 데이터가 있는 경우 해당 데이터를 모두 제거한 후
      삭제가능 합니다. 해당 층별 타입을 삭제 하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import { maska } from 'maska'

export default defineComponent({
  name: 'PayOrder',
  directives: { maska },
  components: { ConfirmModal },
  data() {
    return {
      form: {
        pay_sort: '',
        pay_code: null,
        pay_time: null,
        pay_name: '',
        alias_name: '',
        is_pm_cost: false,
        pay_due_date: '',
        extra_due_date: '',
      },
      validated: false,
    }
  },
  props: ['payOrder'],
  created(this: any) {
    if (this.payOrder) {
      this.form.pay_sort = this.payOrder.pay_sort
      this.form.pay_code = this.payOrder.pay_code
      this.form.pay_time = this.payOrder.pay_time
      this.form.pay_name = this.payOrder.pay_name
      this.form.alias_name = this.payOrder.alias_name
      this.form.is_pm_cost = this.payOrder.is_pm_cost
      this.form.pay_due_date = this.payOrder.pay_due_date
      this.form.extra_due_date = this.payOrder.extra_due_date
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
  },
  methods: {
    formCheck(bool: boolean) {
      if (bool) this.onUpdateFloor()
      return
    },
    onUpdateFloor(this: any) {
      const pk = this.floor.pk
      this.$emit('on-update', { ...{ pk }, ...this.form })
    },
    onDeleteFloor(this: any) {
      this.$refs.confirmModal.callModal()
    },
    modalAction(this: any) {
      this.$emit('on-delete', this.floor.pk)
      this.$refs.confirmModal.visible = false
    },
  },
})
</script>
