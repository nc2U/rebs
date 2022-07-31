<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

const selected = ref()
const store = useStore()
const props = defineProps({ project: { type: Object, default: null } })
const emit = defineEmits(['projSelect'])

const projSelect = computed(() => store.getters['project/projSelect'])
const initProjId = computed(() => store.getters['accounts/initProjId'])
const projId = computed(() =>
  props.project ? props.project.pk : initProjId.value,
)

const fetchProjectList = () => store.dispatch('project/fetchProjectList')

onMounted(() => {
  fetchProjectList()
  selected.value = projId.value
})
</script>

<template>
  <CRow class="m-0">
    <CFormLabel class="col-lg-1 col-form-label">프로젝트</CFormLabel>
    <CCol md="6" lg="3">
      <CFormSelect v-model="selected" @change="$emit('proj-select', $event)">
        <option value="">프로젝트선택</option>
        <option
          v-for="proj in projSelect"
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
