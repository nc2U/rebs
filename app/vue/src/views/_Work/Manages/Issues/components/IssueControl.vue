<script lang="ts" setup>
const emit = defineEmits(['call-edit-form', 'go-time-entry'])

const callEditForm = () => emit('call-edit-form')
const goTimeEntry = () => emit('go-time-entry')
</script>

<template>
  <CCol class="text-right form-text">
    <span class="mr-2">
      <v-icon icon="mdi-pencil" color="amber" size="sm" />
      <router-link to="" class="ml-1" @click="callEditForm">편집</router-link>
    </span>

    <span class="mr-2">
      <v-icon icon="mdi-timer-edit-outline" color="grey" size="sm" />
      <router-link to="" class="ml-1" @click="goTimeEntry">작업시간 기록</router-link>
    </span>

    <span class="mr-2">
      <v-icon icon="mdi-star" color="amber" size="sm" />
      <router-link to="" class="ml-1">관심끄기</router-link>
    </span>

    <span class="mr-2">
      <v-icon icon="mdi-content-copy" color="grey" size="sm" />
      <router-link to="" class="ml-1">복사</router-link>
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
            <router-link to="">
              <v-icon icon="mdi-link-plus" color="grey" size="sm" />
              링크 복사
            </router-link>
          </CDropdownItem>
          <CDropdownItem class="form-text">
            <router-link to="">
              <v-icon icon="mdi-trash-can-outline" color="grey" size="sm" />
              업무 삭제
            </router-link>
          </CDropdownItem>
        </CDropdownMenu>
      </CDropdown>
    </span>
  </CCol>
</template>
