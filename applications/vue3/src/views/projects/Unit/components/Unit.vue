<template>
  <CTableRow>
    <CTableDataCell>
      <CFormInput
        v-model="form.name"
        placeholder="동(건물)"
        @keypress.enter="formCheck(form.name !== unit.name)"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        @click="onUpdateUnit"
        :disabled="formsCheck"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteUnit">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-warning" />
      동(건물) 삭제
    </template>
    <template v-slot:default>
      이 동(건물)에 종속 데이터가 있는 경우 해당 데이터를 모두 제거한 후
      삭제가능 합니다. 해당 동(건물)을 삭제 하시겠습니까?
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
  name: 'Unit',
  components: { ConfirmModal },
  data() {
    return {
      form: {
        name: '',
      },
      validated: false,
    }
  },
  props: ['unit'],
  created() {
    if (this.unit) {
      this.form.name = this.unit.name
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.name === this.unit.name
      return a
    },
  },
  methods: {
    formCheck(bool: boolean) {
      if (bool) this.onUpdateUnit()
      return
    },
    onUpdateUnit(this: any) {
      const pk = this.unit.pk
      this.$emit('on-update', { ...{ pk }, ...this.form })
    },
    onDeleteUnit(this: any) {
      this.$refs.confirmModal.callModal()
    },
    modalAction(this: any) {
      this.$emit('on-delete', this.unit.pk)
      this.$refs.confirmModal.visible = false
    },
  },
})
</script>
