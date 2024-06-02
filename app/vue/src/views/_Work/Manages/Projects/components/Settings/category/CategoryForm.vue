<script lang="ts" setup>
import { ref, onBeforeMount, inject, type ComputedRef, type PropType } from 'vue'
import { colorLight } from '@/utils/cssMixins'
import type { User } from '@/store/types/accounts'
import { isValidate } from '@/utils/helper'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps({
  memberList: { type: Array as PropType<{ pk: number; username: string }[]>, default: () => [] },
  category: { type: Object, default: () => null },
})

const emit = defineEmits(['aside-visible', 'create-category'])

const userInfo = inject<ComputedRef<User>>('userInfo')

const validated = ref(false)

const form = ref({
  project: '',
  name: '',
  assigned_to: null,
})

const [route, router] = [useRoute(), useRouter()]

const createCategory = (event: Event) => {
  if (isValidate(event)) {
    validated.value = true
  } else {
    emit('create-category', { ...form.value })
    validated.value = false
    router.push({ name: '(설정)' })
  }
}

onBeforeMount(async () => {
  emit('aside-visible', false)

  if (props.category) {
    form.value.project = props.category.project
    form.value.name = props.category.name
    form.value.assigned_to = props.category.assigned_to
  } else form.value.project = route.params.projId as string
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>새 업무 범주</h5>
    </CCol>
  </CRow>

  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="createCategory"
  >
    <CCard :color="colorLight" class="mb-3">
      <CCardBody>
        <CRow class="mb-3">
          <CFormLabel for="name" class="col-sm-2 col-form-label text-right required">
            이름
          </CFormLabel>

          <CCol sm="10" lg="6">
            <CFormInput v-model="form.name" placeholder="새 버전 이름" required />
          </CCol>
        </CRow>

        <CRow class="mb-3">
          <CFormLabel for="category-name" class="col-sm-2 col-form-label text-right">
            담당자
          </CFormLabel>
          <CCol sm="10" lg="6">
            <CFormSelect v-model.number="form.assigned_to">
              <option value="">---------</option>
              <option :value="userInfo?.pk">&lt;&lt; 나 &gt;&gt;</option>
              <option v-for="user in memberList" :value="user.pk" :key="user.pk">
                {{ user.username }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCardBody>
    </CCard>

    <CRow>
      <CCol>
        <CButton type="submit" color="primary">저장</CButton>
      </CCol>
    </CRow>
  </CForm>
</template>
