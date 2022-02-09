<template>
  <CTableRow>
    <CTableDataCell>
      <CFormInput
        v-model="form.start_floor"
        placeholder="시작 층"
        type="number"
        min="0"
        required
        @keypress.enter="formCheck(form.start_floor !== floor.start_floor)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.end_floor"
        placeholder="종료 층"
        type="number"
        min="0"
        required
        @keypress.enter="formCheck(form.end_floor !== form.end_floor)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.alias_name"
        placeholder="층별 범위 명칭"
        required
        @keypress.enter="formCheck(form.alias_name !== floor.alias_name)"
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

export default defineComponent({
  name: 'Price',
  components: { ConfirmModal },
  data() {
    return {
      form: {
        start_floor: null,
        end_floor: null,
        alias_name: '',
      },
      validated: false,
    }
  },
  props: ['floor'],
  created(this: any) {
    if (this.floor) {
      this.form.start_floor = this.floor.start_floor
      this.form.end_floor = this.floor.end_floor
      this.form.alias_name = this.floor.alias_name
    }
  },
  watch: {
    type(this: any) {
      this.form.start_floor = this.floor.start_floor
      this.form.end_floor = this.floor.end_floor
      this.form.alias_name = this.floor.alias_name
    },
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.start_floor === this.floor.start_floor
      const b = this.form.end_floor === this.floor.end_floor
      const c = this.form.alias_name === this.floor.alias_name
      return a && b && c
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
