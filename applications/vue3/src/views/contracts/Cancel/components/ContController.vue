<template>
  <CCallout color="info" class="pb-0 mb-4">
    <CRow>
      <CCol>
        <CRow>
          <CCol md="4" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                placeholder="계약자, 비고, 계약 일련번호"
                @keydown.enter="listFiltering(1)"
                aria-label="Search"
                aria-describedby="addon-wrapping"
              />
              <CInputGroupText @click="listFiltering(1)">
                계약 건 찾기
              </CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
    <CRow>
      <!--      <CCol color="warning" class="p-2 pl-3" v-if="contractIndex.length !== 0">-->
      <!--        <CButton-->
      <!--          type="button"-->
      <!--          color="dark"-->
      <!--          v-for="cont in contractIndex"-->
      <!--          :key="cont.pk"-->
      <!--          @click="getContract(cont.pk)"-->
      <!--          variant="outline"-->
      <!--          size="sm"-->
      <!--        >-->
      <!--          {{ `${cont.contractor}(${cont.serial_number})` }}-->
      <!--        </CButton>-->
      <!--      </CCol>-->
      <!--      <CCol v-else class="mt-3 m-2" :class="textClass">-->
      <!--        {{ msg }}-->
      <!--      </CCol>-->
    </CRow>
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ContController',
  components: {},
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {},
  methods: {},
})
</script>
