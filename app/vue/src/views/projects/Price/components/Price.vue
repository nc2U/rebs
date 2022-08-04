<template>
  <CTableRow>
    <CTableDataCell class="text-center">
      {{ condTexts.orderText }}
    </CTableDataCell>
    <CTableDataCell class="text-center">
      {{ condTexts.typeText }}
    </CTableDataCell>
    <CTableDataCell> {{ floor.alias_name }}</CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model.number="form.price_build"
        type="number"
        min="0"
        placeholder="타입별 건물가"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price_land"
        type="number"
        min="0"
        placeholder="타입별 대지가"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price_tax"
        type="number"
        min="0"
        placeholder="타입별 부가세"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price"
        type="number"
        min="0"
        placeholder="타입별 공급가격"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        :color="btnColor"
        size="sm"
        :disabled="formsCheck"
        @click="onStorePrice"
      >
        {{ btnTitle }}
      </CButton>
      <CButton
        color="danger"
        size="sm"
        :disabled="disabled"
        @click="deletePrice()"
      >
        삭제
      </CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template #header>
      <CIcon name="cil-warning" />
      공급가격 삭제
    </template>
    <template #default>
      이 그룹에 종속 데이터가 있는 경우 해당 데이터를 모두 제거한 후 삭제가능
      합니다. 해당 공급가격을 삭제 하시겠습니까?
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
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'Price',
  components: { ConfirmModal, AlertModal },
  props: { floor: Object, condTexts: Object, queryIds: Object },
  data() {
    return {
      form: {
        price_build: null,
        price_land: null,
        price_tax: null,
        price: null,
      },
      price: {},
    }
  },
  computed: {
    btnColor() {
      return this.price ? 'success' : 'primary'
    },
    btnTitle() {
      return this.price ? '수정' : '등록'
    },
    disabled() {
      return !this.price
    },
    formsCheck(this: any) {
      if (this.price) {
        const a = this.form.price_build == this.price.price_build
        const b = this.form.price_land == this.price.price_land
        const c = this.form.price_tax == this.price.price_tax
        const d = this.form.price == this.price.price
        return (a && b && c && d) || !this.price
      } else {
        return (
          !this.form.price_build &&
          !this.form.price_land &&
          !this.form.price_tax &&
          !this.form.price
        )
      }
    },

    ...mapState('payment', ['priceList']),
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  watch: {
    priceList() {
      this.resetForm()
    },
  },
  methods: {
    onStorePrice(this: any) {
      if (
        this.superAuth ||
        (this.staffAuth && this.staffAuth.project === '2')
      ) {
        const payload = {
          ...this.queryIds,
          ...{ unit_floor_type: this.floor.pk },
          ...this.form,
        }
        if (!this.price) this.$emit('on-create', payload)
        else {
          const updatePayload = { ...{ pk: this.price.pk }, ...payload }
          this.$emit('on-update', updatePayload)
        }
      } else {
        this.$refs.alertModal.callModal()
        this.resetForm()
      }
    },
    deletePrice(this: any) {
      if (this.superAuth) this.$refs.confirmModal.callModal()
      else {
        this.$refs.alertModal.callModal()
        this.resetForm()
      }
    },
    modalAction(this: any) {
      this.$emit('on-delete', this.price.pk)
      this.$refs.confirmModal.visible = false
    },
    resetForm(this: any) {
      const unit_floor_type = String(this.floor.pk)
      const { project, order_group, unit_type }: any = this.queryIds
      const price = this.priceList.filter(
        (p: any) =>
          p.project == project &&
          p.order_group == order_group &&
          p.unit_type == unit_type &&
          p.unit_floor_type == unit_floor_type,
      )[0]
      this.price = price
      this.form.price_build = price ? price.price_build : null
      this.form.price_land = price ? price.price_land : null
      this.form.price_tax = price ? price.price_tax : null
      this.form.price = price ? price.price : null
    },
  },
})
</script>
