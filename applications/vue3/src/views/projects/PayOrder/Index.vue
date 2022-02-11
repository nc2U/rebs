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
      <PayOrderAddForm :selected="selected" @on-submit="onSubmit" />
      <PayOrderFormList
        @on-update="onUpdatePayOrder"
        @on-delete="onDeletePayOrder"
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
import PayOrderAddForm from '@/views/projects/PayOrder/components/PayOrderAddForm.vue'
import PayOrderFormList from '@/views/projects/PayOrder/components/PayOrderFormList.vue'
import { mapActions } from 'vuex'

export default defineComponent({
  name: 'ProjectsPayOrderSet',
  mixins: [HeaderMixin, ProjectMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    PayOrderAddForm,
    PayOrderFormList,
  },
  created() {
    this.fetchPayOrderList(this.initProjId)
  },
  methods: {
    projSelect(event: any) {
      if (event.target.value !== '') {
        this.selected = true
        this.fetchProject(event.target.value)
        this.fetchPayOrderList(event.target.value)
      } else {
        this.selected = false
      }
    },
    onSubmit(payload: any) {
      const project = this.project.pk
      this.createPayOrder({ ...{ project }, ...payload })
    },
    onUpdateFloor(payload: any) {
      const project = this.project.pk
      this.updatePayOrder({ ...{ project }, ...payload })
    },
    onDeleteFloor(pk: number) {
      const project = this.project.pk
      this.deletePayOrder({ ...{ pk }, ...{ project } })
    },
    ...mapActions('cash', [
      'fetchPayOrderList',
      'createPayOrder',
      'updatePayOrder',
      'deletePayOrder',
    ]),
  },
})
</script>
