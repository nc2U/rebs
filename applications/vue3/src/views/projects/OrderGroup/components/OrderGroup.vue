<template>
  <CTableRow>
    <CTableDataCell>
      <CFormInput
        type="number"
        v-model="form.order_number"
        min="1"
        required
        placeholder="등록차수"
        @keypress.enter="onUpdateOrder(form)"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect
        v-model="form.sort"
        :options="sorts"
        :selected="sorts.value == form.sort"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.order_group_name"
        @keypress.enter="onUpdateOrder(form)"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton color="success" size="sm" @click="onUpdateOrder(form)">
        수정
      </CButton>
      <CButton color="danger" size="sm">삭제</CButton>
    </CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'OrderGroup',
  data() {
    return {
      sorts: [
        { label: '일반분양', value: '1' },
        { label: '조합모집', value: '2' },
      ],
      form: {
        order_number: null,
        sort: '',
        order_group_name: '',
      },
      validated: false,
    }
  },
  props: {
    order: {
      type: Object,
    },
  },
  created(this: any) {
    this.form.order_number = this.order.order_number
    this.form.sort = this.order.sort
    this.form.order_group_name = this.order.order_group_name
  },
  methods: {
    onUpdateOrder(this: any, form: any) {
      const pk = this.order.pk
      this.$emit('on-update', { ...{ pk }, ...form })
    },
  },
})
</script>
