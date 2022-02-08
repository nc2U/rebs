<template>
  <CForm
    novalidate
    class="needs-validation"
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CRow class="p-2" color="success">
      <CCol md="3" class="mb-2">
        <CFormInput
          v-model="aa"
          placeholder="등록차수"
          type="number"
          required
        />
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormSelect v-model="bb" placeholder="aa">
          <option
            v-for="(s, i) in sort"
            :value="s.value"
            :key="i"
            :selected="s.value == ''"
          >
            {{ s.label }}
          </option>
        </CFormSelect>
      </CCol>

      <CCol md="3" class="mb-2">
        <CFormInput v-model="cc" placeholder="차수그룹 명칭" required />
      </CCol>

      <CCol md="3" class="d-grid gap-2 d-lg-block mb-3">
        <CButton color="primary">그룹추가</CButton>
      </CCol>
    </CRow>
  </CForm>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: '',
  data() {
    return {
      sort: [
        { label: '구분선택', value: '' },
        { label: '일반분양', value: '1' },
        { label: '조합모집', value: '2' },
      ],
      validated: false,
    }
  },
  props: {},
  computed: {},
  methods: {
    onSubmit() {
      this.$emit('on-submit', {})
    },
  },
})
</script>

<style lang="scss" scoped></style>
