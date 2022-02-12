<template>
  <ContentHeader :page-title="'신규 프로젝트'" :nav-menu="['프로젝트 관리']" />

  <ContentBody>
    <component
      :is="compName"
      :userInfo="userInfo"
      :project="project"
      :update="update"
      @to-create="toCreate"
      @to-update="toUpdate"
      @reset-form="resetForm"
      @create-form="createForm"
      @update-form="updateForm"
    />
  </ContentBody>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import IndexForm from '@/views/projects/List/components/IndexForm.vue'
import IndexDetail from '@/views/projects/List/components/IndexDetail.vue'
import { mapActions, mapState } from 'vuex'

export default defineComponent({
  name: 'ProjectsIndex',
  components: {
    ContentHeader,
    ContentBody,
    IndexForm,
    IndexDetail,
  },
  data() {
    return {
      compName: 'IndexForm',
      update: false,
    }
  },
  computed: {
    ...mapState('accounts', ['userInfo']),
    ...mapState('project', ['project']),
  },
  watch: {
    project() {
      this.compName = 'IndexDetail'
    },
  },
  methods: {
    createForm() {
      this.update = false
      this.compName = 'IndexForm'
    },
    updateForm() {
      this.update = true
      this.compName = 'IndexForm'
    },
    resetForm() {
      this.update = false
      this.compName = 'IndexDetail'
    },
    toCreate(payload: any) {
      this.createProject(payload)
    },
    toUpdate(payload: any) {
      this.updateProject(payload)
    },
    ...mapActions('project', ['createProject', 'updateProject']),
  },
})
</script>
