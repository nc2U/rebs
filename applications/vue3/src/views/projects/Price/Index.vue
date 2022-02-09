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
      <PriceSelectForm :selected="selected" @on-submit="onSubmit" />
      <PriceFormList
        @on-update="onUpdatePrice"
        @on-delete="onDeletePrice"
        :selected="selected"
        :project="project"
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
  created() {
    this.fetchPriceList(this.initProjId)
  },
  methods: {
    projSelect(event: any) {
      if (event.target.value !== '') {
        this.selected = true
        this.fetchProject(event.target.value)
        this.fetchPriceList(event.target.value)
      } else {
        this.selected = false
      }
    },
    onSubmit(payload: any) {
      // const project = this.project.pk
      // this.createPrice({ ...{ project }, ...payload })
      return
    },
    onUpdatePrice(payload: any) {
      const project = this.project.pk
      this.updatePrice({ ...{ project }, ...payload })
    },
    onDeletePrice(pk: number) {
      const project = this.project.pk
      this.deletePrice({ ...{ pk }, ...{ project } })
    },
    ...mapActions('cash', [
      'fetchPriceList',
      'createPrice',
      'updatePrice',
      'deletePrice',
    ]),
  },
})
</script>
