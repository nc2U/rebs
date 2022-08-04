<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <component
      :is="compName"
      :user-info="userInfo"
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
import HeaderMixin from '@/views/projects/_menu/headermixin1'
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
  mixins: [HeaderMixin],
  data() {
    return {
      compName: 'IndexDetail',
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
