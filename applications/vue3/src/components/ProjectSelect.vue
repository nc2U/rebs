<template>
  <CRow>
    <CCol md="4">
      <CFormSelect @change="$emit('on-change', $event)">
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
      return this.project ? this.project.id : ''
    },
    ...mapGetters('project', ['projSelect']),
  },

  methods: {
    ...mapActions('project', ['fetchProjectList']),
  },
})
</script>
