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

  <CCard class="mb-4 pb-5">
    <CCardHeader>
      <CIcon name="cil-notes" />
      <strong class="pl-1"> {{ $route.name }}</strong>
    </CCardHeader>

    <CCardBody class="blank-body">
      <OrderForm @on-submit="onSubmit" />
      <OrderList :project="project" />
    </CCardBody>

    <!--    <CCardFooter>&nbsp;</CCardFooter>-->
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import HeaderNav from '@/components/HeaderNav.vue'
import HeaderMixin from '@/views/projects/_menu/headermixin2'
import ProjectMixin from '@/views/projects/projectMixin'
import ProjectSelect from '@/components/ProjectSelect/Index.vue'
import OrderForm from '@/views/projects/OrderGroup/components/OrderForm.vue'
import OrderList from '@/views/projects/OrderGroup/components/OrderList.vue'

export default defineComponent({
  name: 'ProjectsOrderSet',
  mixins: [HeaderMixin, ProjectMixin],
  components: {
    HeaderNav,
    ProjectSelect,
    OrderForm,
    OrderList,
  },
  methods: {
    onSubmit(payload: any) {
      console.log(payload)
    },
  },
})
</script>
