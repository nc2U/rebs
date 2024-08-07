<script lang="ts" setup>
import { type PropType, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { IssueProject } from '@/store/types/work'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const props = defineProps({
  project: { type: Object as PropType<IssueProject>, required: true },
})

const RefProjectCloseConfirm = ref()
const RefProjectDeleteConfirm = ref()
const idForDelete = ref('')

const router = useRouter()

const projectClose = () => {
  alert('close!!')
  RefProjectCloseConfirm.value.close()
}

const projectDelete = () => {
  if (idForDelete.value === (props.project?.slug as string)) {
    alert('delete!!')
    RefProjectDeleteConfirm.value.close()
  } else idForDelete.value = ''
}
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>개요</h5>
    </CCol>

    <CCol class="text-right">
      <span class="mr-2 form-text">
        <v-icon icon="mdi-bookmark-multiple" color="primary" size="sm" />
        <router-link to="" class="ml-1">북마크 추가</router-link>
      </span>

      <span>
        <CDropdown color="secondary" variant="input-group" placement="bottom-end">
          <CDropdownToggle
            :caret="false"
            color="light"
            variant="ghost"
            size="sm"
            shape="rounded-pill"
          >
            <v-icon icon="mdi-dots-horizontal" class="pointer" color="grey-darken-1" />
            <v-tooltip activator="parent" location="top">Actions</v-tooltip>
          </CDropdownToggle>
          <CDropdownMenu>
            <CDropdownItem class="form-text">
              <router-link :to="{ name: '프로젝트 - 추가', query: { parent: project?.pk } }">
                <v-icon icon="mdi-plus-circle" color="success" size="sm" />
                새 하위 프로젝트
              </router-link>
            </CDropdownItem>
            <CDropdownItem class="form-text" @click="RefProjectCloseConfirm.callModal()">
              <router-link to="">
                <v-icon icon="mdi-lock" color="warning" size="sm" />
                닫기
              </router-link>
            </CDropdownItem>
            <CDropdownItem class="form-text" @click="RefProjectDeleteConfirm.callModal()">
              <router-link to="">
                <v-icon icon="mdi-trash-can-outline" color="danger" size="sm" />
                삭제
              </router-link>
            </CDropdownItem>
            <CDropdownItem class="form-text" @click="router.push({ name: '(설정)' })">
              <router-link to="">
                <v-icon icon="mdi-cog" color="secondary" size="sm" />
                설정
              </router-link>
            </CDropdownItem>
          </CDropdownMenu>
        </CDropdown>
      </span>
    </CCol>
  </CRow>

  <ConfirmModal ref="RefProjectCloseConfirm">
    <template #icon>
      <v-icon icon="mdi-arrow-right-bold-box" color="warning" class="mr-2" />
    </template>
    <template #default>
      '{{ project?.name }}' 프로젝트를 닫고 읽기 전용 프로젝트로 만드시겠습니까?
    </template>
    <template #footer>
      <CButton color="warning" @click="projectClose">확인</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="RefProjectDeleteConfirm">
    <template #icon>
      <v-icon icon="mdi-arrow-right-bold-box" color="danger" class="mr-2" />
    </template>
    <template #default>
      <div class="bg-amber-lighten-4 p-4 text-center">
        <h6>{{ project?.name }}</h6>
        <p>이 프로젝트를 삭제하고 모든 데이터를 삭제하시겠습니까?</p>
        <p>
          삭제를 진행하려면, 이 프로젝트의 식별자 (<strong>{{ project?.slug }}</strong
          >)를 입력하여 주십시요.
        </p>
        <CRow>
          <CFormLabel for="identifier" class="col-sm-2 col-form-label">식별자</CFormLabel>
          <CCol sm="10">
            <CFormInput v-model="idForDelete" id="identifier" />
          </CCol>
        </CRow>
      </div>
    </template>
    <template #footer>
      <CButton color="danger" @click="projectDelete">삭제</CButton>
    </template>
  </ConfirmModal>
</template>
