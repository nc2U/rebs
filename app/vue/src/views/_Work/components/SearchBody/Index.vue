<script setup lang="ts">
import { computed, type ComputedRef, inject, onBeforeMount, ref, watch } from 'vue'
import { navMenu } from '@/views/_Work/_menu/headermixin1'
import { useRoute } from 'vue-router'
import type { Company } from '@/store/types/settings'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'

const emit = defineEmits(['aside-visible'])

const cBody = ref()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)
const sideNavCAll = () => cBody.value.toggle()

const searchWord = ref('')
const searchAll = ref(true)
const searchSub = ref(false)

const route = useRoute()

watch(route, nVal => {
  if (nVal.query.q) searchWord.value = nVal.query.q as string
})

onBeforeMount(() => {
  emit('aside-visible', false)
  if (route.query.q) searchWord.value = route.query.q as string
})
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query" :aside="false">
    <template v-slot:default>
      <CRow class="py-2">
        <CCol>
          <h5>{{ $route.name }}</h5>
        </CCol>
      </CRow>

      <CCard color="light">
        <CCardBody>
          <CRow>
            <CCol sm="12" md="8" lg="6" xl="3">
              <CFormInput v-model="searchWord" />
            </CCol>
            <CCol class="pt-2">
              <CFormCheck v-model="searchAll" inline label="모든 단어" id="all-word" />

              <CFormCheck v-model="searchSub" inline label="제목에서만 찾기" id="only-subject" />
            </CCol>
          </CRow>

          <CRow>
            <CCol></CCol>
          </CRow>
        </CCardBody>
      </CCard>

      <CRow class="mt-3">
        <CCol>
          <h5>결과 (0)</h5>
        </CCol>
      </CRow>

      <CRow class="mt-3">
        <CCol> 결과들 ...</CCol>
      </CRow>
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
