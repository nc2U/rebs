<template>
  <CRow>
    <CFormLabel class="col-lg-1 col-form-label">프로젝트</CFormLabel>
    <CCol md="6" lg="3">
      <CFormSelect @change="$emit('proj-select', $event)">
        <option value="">프로젝트선택</option>
        <option
          v-for="proj in projSelect"
          :value="proj.value"
          :key="proj.value"
          :selected="proj.value === projId"
        >
          {{ proj.text }}
        </option>
      </CFormSelect>
    </CCol>
  </CRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapActions, mapGetters } from 'vuex'

export default defineComponent({
  name: 'ProjectSelect',
  created() {
    this.fetchProjectList()
  },
  props: {
    project: {
      type: Object,
    },
  },
  computed: {
    projId() {
      return this.project ? this.project.pk : this.initProjId
    },
    ...mapGetters('project', ['projSelect']),
    ...mapGetters('accounts', ['initProjId']),
  },

  methods: {
    ...mapActions('project', ['fetchProjectList']),
  },
})
</script>
