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
      <DownPayAddForm
        :selected="selected"
        :orders="orderGroupList"
        :types="unitTypeList"
        @on-submit="onSubmit"
      />
      <DownPayFormList
        @on-update="onUpdateDownPay"
        @on-delete="onDeleteDownPay"
        :selected="selected"
        :orders="orderGroupList"
        :types="unitTypeList"
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
import DownPayAddForm from '@/views/projects/DownPay/components/DownPayAddForm.vue'
import DownPayFormList from '@/views/projects/DownPay/components/DownPayFormList.vue'
import { mapActions, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectsDownPaySet',
  mixins: [HeaderMixin, ProjectMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    DownPayAddForm,
    DownPayFormList,
  },
  created() {
    this.fetchDownPayList(this.initProjId)
    this.fetchOrderGroupList(this.initProjId)
    this.fetchTypeList(this.initProjId)
  },
  computed: {
    ...mapState('contract', ['orderGroupList']),
    ...mapState('project', ['unitTypeList']),
  },
  methods: {
    projSelect(event: any) {
      if (event.target.value !== '') {
        this.selected = true
        this.fetchProject(event.target.value)
        this.fetchDownPayList(event.target.value)
        this.fetchOrderGroupList(event.target.value)
        this.fetchTypeList(event.target.value)
      } else {
        this.selected = false
      }
    },
    onSubmit(payload: any) {
      const project = this.project.pk
      this.createDownPay({ ...{ project }, ...payload })
    },
    onUpdateDownPay(payload: any) {
      const project = this.project.pk
      this.updateDownPay({ ...{ project }, ...payload })
    },
    onDeleteDownPay(pk: number) {
      const project = this.project.pk
      this.deleteDownPay({ ...{ pk }, ...{ project } })
    },
    ...mapActions('cash', [
      'fetchDownPayList',
      'createDownPay',
      'updateDownPay',
      'deleteDownPay',
    ]),
    ...mapActions('contract', ['fetchOrderGroupList']),
    ...mapActions('project', ['fetchTypeList']),
  },
})
</script>
