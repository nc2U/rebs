<script lang="ts" setup>
import { ref, computed, onBeforeMount, nextTick } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useAccount } from '@/store/pinia/account'

const proj = ref()
const projectStore = useProject()
const accountStore = useAccount()

const props = defineProps({ project: { type: Object, default: null } })

const projSelectList = computed(() => projectStore.projSelect)
const initProjId = computed(() => accountStore.initProjId)

const emit = defineEmits(['header-select'])
const projSelect = (event: any) => {
  nextTick(() => emit('header-select', event.target.value))
}

onBeforeMount(() => {
  proj.value = initProjId.value
  projectStore.fetchProject(proj.value)
  projectStore.fetchProjectList()
})
</script>

<template>
  <CRow class="m-0">
    <CFormLabel class="col-lg-1 col-form-label text-body">프로젝트</CFormLabel>
    <CCol md="6" lg="3">
      <CFormSelect v-model="proj" @change="projSelect">
        <option value="">프로젝트선택</option>
        <option
          v-for="proj in projSelectList"
          :key="proj.value"
          :value="proj.value"
        >
          {{ proj.text }}
        </option>
      </CFormSelect>
    </CCol>
    <!--    <CCol md="6" lg="4" xl="3">-->
    <!--      <v-select-->
    <!--        v-model="selected"-->
    <!--        :items="projSelect"-->
    <!--        :hint="`${projSelect.value}, ${projSelect.text}`"-->
    <!--        item-title="text"-->
    <!--        item-value="value"-->
    <!--        label="프로젝트"-->
    <!--        density="comfortable"-->
    <!--        persistent-hint-->
    <!--        return-object-->
    <!--      />-->
    <!--      &lt;!&ndash;        @update:modelValue="emit('projSelect', selected)"&ndash;&gt;-->
    <!--    </CCol>-->
  </CRow>
</template>
