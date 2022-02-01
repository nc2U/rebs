<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />

      <CompanySelect :company="company" @on-change="onChange" />
    </CCardBody>
  </CCard>

  <component :is="compName" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import CompanySelect from '@/components/CompanySelect.vue'
import BlankComponent from '@/components/BlankComponent.vue'
import HeaderMixin from '@/views/cashes/_menu/headermixin'
import { mapActions, mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'CashesIndex',
  mixins: [HeaderMixin],
  components: {
    HeaderNav,
    CompanySelect,
    BlankComponent,
  },
  data() {
    return {
      compName: 'BlankComponent',
    }
  },
  created() {
    this.fetchCompany(this.initComId)
  },
  computed: {
    ...mapState('settings', ['company']),
    ...mapGetters('accounts', ['initComId']),
  },
  methods: {
    ...mapActions('settings', ['fetchCompany']),
  },
})
</script>

<style lang="scss" scoped></style>
