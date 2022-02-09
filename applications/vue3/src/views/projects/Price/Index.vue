<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-justify-center" />
      <strong class="pl-1"> {{ pageTitle }}</strong>
    </CCardHeader>

    <CCardBody>
      <HeaderNav :menus="navMenu" />

      <ProjectSelect :project="project" @proj-select="projSelect" />
    </CCardBody>
  </CCard>

  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-notes" />
      <strong class="pl-1"> {{ $route.name }}</strong>
    </CCardHeader>

    <CCardBody class="pb-5" v-if="project">
      <PriceSelectForm
        @on-order-select="orderSelect"
        @on-type-select="typeSelect"
        @on-floor-select="floorSelect"
        :selected="selected"
      />
      <PriceFormList
        @on-update="onUpdatePrice"
        @on-delete="onDeletePrice"
        :selected="selected"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import ProjectSelect from '@/components/ProjectSelect/Index.vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ProjectMixin from '@/views/projects/projectMixin'
import PriceSelectForm from '@/views/projects/Price/components/PriceSelectForm.vue'
import PriceFormList from '@/views/projects/Price/components/PriceFormList.vue'
import { mapActions } from 'vuex'

export default defineComponent({
  name: 'ProjectsPriceSet',
  mixins: [HeaderMixin, ProjectMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    PriceSelectForm,
    PriceFormList,
  },
  methods: {
    orderSelect(this: any, payload: any) {
      const project = this.project.pk
      const order = payload
      const type = ''
      if (payload !== '') {
        this.fetchOrderGroup(payload)
      } else {
        this.$store.state.contract.orderGroup = null
      }
      console.log({ project, order, type })
    },
    typeSelect(this: any, payload: any) {
      const project = this.project.pk
      const type = payload
      console.log({ project, type })
      if (payload !== '') {
        this.fetchType(payload)
      } else {
        this.$store.state.project.unitType = null
      }
    },
    floorSelect() {
      return
    },
  },
})
</script>
