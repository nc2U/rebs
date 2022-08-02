<template>
  <CTableRow>
    <CTableDataCell>
      <CFormInput
        v-model="form.name"
        placeholder="동(건물)"
        @keypress.enter="formCheck(form.name !== building.name)"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        color="success"
        size="sm"
        :disabled="formsCheck"
        @click="onUpdateBuilding"
      >
        수정
      </CButton>
      <CButton color="danger" size="sm" @click="onDeleteBuilding">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cil-warning" />
      동(건물) 삭제
    </template>
    <template #default>
      이 동(건물)에 종속 데이터가 있는 경우 해당 데이터를 모두 제거한 후
      삭제가능 합니다. 해당 동(건물)을 삭제 하시겠습니까?
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
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'Building',
  components: { ConfirmModal, AlertModal },
  props: { building: { type: Object, default: null } },
  data() {
    return {
      form: {
        name: '',
      },
      validated: false,
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.name === this.building.name
      return a
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  created() {
    if (this.building) this.resetForm()
  },
  methods: {
    formCheck(bool: boolean) {
      if (bool) this.onUpdateBuilding()
      return
    },
    onUpdateBuilding(this: any) {
      if (
        this.superAuth ||
        (this.staffAuth && this.staffAuth.project === '2')
      ) {
        const pk = this.building.pk
        this.$emit('on-update', { ...{ pk }, ...this.form })
      } else {
        this.$refs.alertModal.callModal()
        this.resetForm()
      }
    },
    onDeleteBuilding(this: any) {
      if (this.superAuth) this.$refs.confirmModal.callModal()
      else {
        this.$refs.alertModal.callModal()
        this.resetForm()
      }
    },
    modalAction(this: any) {
      this.$emit('on-delete', this.building.pk)
      this.$refs.confirmModal.visible = false
    },
    resetForm() {
      this.form.name = this.building.name
    },
  },
})
</script>
