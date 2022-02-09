<template>
  <CTableRow>
    <CTableDataCell :rowspan="1" class="text-center">
      {{ order.order_group_name }}
    </CTableDataCell>
    <CTableDataCell :rowspan="1" class="text-center"> 74</CTableDataCell>
    <CTableDataCell> 21층 이상</CTableDataCell>
    <CTableDataCell>
      <CFormInput type="number" min="0" placeholder="건물가" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput type="number" min="0" placeholder="대지가" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput type="number" min="0" placeholder="부가세" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput type="number" min="0" placeholder="공급가격" />
    </CTableDataCell>
    {{ order }}
  </CTableRow>

  <!--  {{ orderGroupList }}-->

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
import { mapActions, mapState } from 'vuex'

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
  props: ['order', 'price'],
  created(this: any) {
    if (this.price) {
      // this.form.start_floor = this.price.start_floor
      // this.form.end_floor = this.price.end_floor
      // this.form.alias_name = this.price.alias_name
    }
  },
  watch: {
    type(this: any) {
      // this.form.start_floor = this.price.start_floor
      // this.form.end_floor = this.price.end_floor
      // this.form.alias_name = this.price.alias_name
    },
  },
  computed: {
    orders() {
      return ['1차조합원']
    },
    // formsCheck(this: any) {
    // const a = this.form.start_floor === this.price.start_floor
    // const b = this.form.end_floor === this.price.end_floor
    // const c = this.form.alias_name === this.price.alias_name
    // return a && b && c
    // },
    ...mapState('contract', ['orderGroupList']),
    ...mapState('project', ['typeList']),
  },
  methods: {
    formCheck(bool: boolean) {
      if (bool) this.onUpdateFloor()
      return
    },
    onUpdateFloor(this: any) {
      const pk = this.price.pk
      this.$emit('on-update', { ...{ pk }, ...this.form })
    },
    onDeleteFloor(this: any) {
      this.$refs.confirmModal.callModal()
    },
    modalAction(this: any) {
      this.$emit('on-delete', this.price.pk)
      this.$refs.confirmModal.visible = false
    },
    ...mapActions('contract', ['fetchOrderGroupList']),
  },
})
</script>
