<template>
  <CCallout color="danger" class="pb-0 mb-4">
    <CRow>
      <CCol>
        <CRow>
          <CCol md="4" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="search"
                placeholder="계약자, 비고, 계약 일련번호"
                @keydown.enter="searchContractor"
                aria-label="Search"
                aria-describedby="addon-wrapping"
              />
              <CInputGroupText @click="searchContractor">
                계약 건 찾기
              </CInputGroupText>
            </CInputGroup>
          </CCol>
          <CCol
            color="warning"
            class="p-1 pl-3"
            v-if="contractorList && contractorList.length > 0"
          >
            <CButton
              type="button"
              color="dark"
              v-for="contractor in contractorList"
              :key="contractor.pk"
              @click="
                setContractor(contractor.pk, contractor.contractorrelease)
              "
              variant="outline"
              size="sm"
            >
              {{ `${contractor.name}(${contractor.contract.serial_number})` }}
            </CButton>
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
import { mapMutations, mapState } from 'vuex'

export default defineComponent({
  name: 'ContController',
  data() {
    return {
      search: '',
    }
  },
  computed: {
    ...mapState('contract', ['contractorList']),
  },
  methods: {
    searchContractor() {
      this.$emit('search-contractor', this.search)
    },
    setContractor(pk: number, release: number | null) {
      this.$router.push({ name: '계약해지 관리', query: { contractor: pk } })
      if (release !== null) this.$emit('update-confirm', release)
      else this.FETCH_CONT_RELEASE(null)

      this.search = ''
      this.FETCH_CONTRACTOR_LIST([])
    },
    ...mapMutations('contract', [
      'FETCH_CONT_RELEASE',
      'FETCH_CONTRACTOR_LIST',
    ]),
  },
})
</script>
