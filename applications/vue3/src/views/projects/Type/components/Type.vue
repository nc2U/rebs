<template>
  <CTableRow>
    <CTableDataCell>
      <CFormInput
        v-model="form.name"
        placeholder="타입명칭"
        required
        @keypress.enter="formCheck(form.name !== type.name)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.color" title="타입색상" type="color" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.average_price"
        placeholder="평균가격"
        type="number"
        min="0"
        required
        @keypress.enter="formCheck(form.average_price !== type.average_price)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.num_unit"
        placeholder="세대수"
        type="number"
        min="0"
        required
        @keypress.enter="formCheck(form.num_unit !== type.num_unit)"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        @click="onUpdateType"
        :disabled="formsCheck"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteType">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-warning" />
      삭제 확인!
    </template>
    <template v-slot:default>
      이 타입에 종속 데이터가 있는 경우 해당 데이터를 모두 제거한 후 삭제가능
      합니다. 해당 타입을 삭제 하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="danger" @click="modalAction">삭제</CButton>
    </template>
  </ConfirmModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

export default defineComponent({
  name: 'UnitType',
  components: { ConfirmModal },
  data() {
    return {
      form: {
        name: '',
        color: '',
        average_price: null,
        num_unit: null,
      },
      validated: false,
    }
  },
  props: {
    type: {
      type: Object,
    },
  },
  created(this: any) {
    if (this.type) {
      this.form.name = this.type.name
      this.form.color = this.type.color
      this.form.average_price = this.type.average_price
      this.form.num_unit = this.type.num_unit
    }
  },
  watch: {
    type(this: any) {
      this.form.name = this.type.name
      this.form.color = this.type.color
      this.form.average_price = this.type.average_price
      this.form.num_unit = this.type.num_unit
    },
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.name === this.type.name
      const b = this.form.color === this.type.color
      const c = this.form.average_price === this.type.average_price
      const d = this.form.num_unit === this.type.num_unit
      return a && b && c && d
    },
  },
  methods: {
    formCheck(bool: boolean) {
      if (bool) this.onUpdateType()
      return
    },
    onUpdateType(this: any) {
      const pk = this.type.pk
      this.$emit('on-update', { ...{ pk }, ...this.form })
    },
    onDeleteType(this: any) {
      this.$refs.confirmModal.callModal()
    },
    modalAction(this: any) {
      this.$emit('on-delete', this.type.pk)
      this.$refs.confirmModal.visible = false
    },
  },
})
</script>
