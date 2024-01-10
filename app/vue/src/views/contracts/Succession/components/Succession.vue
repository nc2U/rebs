<script lang="ts" setup>
import { computed, type PropType } from 'vue'
import { type Succession } from '@/store/types/contract'
import { useRouter } from 'vue-router'

const props = defineProps({
  succession: { type: Object as PropType<Succession>, required: true },
})
const emit = defineEmits(['call-form', 'on-submit'])

const done = computed(() => props.succession.is_approval)
const buttonColor = computed(() => (!done.value ? 'success' : 'secondary'))

const router = useRouter()

const callFormModal = () => {
  router.replace({
    name: '권리 의무 승계',
    query: { contractor: props.succession?.buyer.pk },
  })
  setTimeout(() => {
    emit('call-form', props.succession)
  }, 300)
}
</script>

<template>
  <CTableDataCell class="text-center">
    <router-link to="" @click="callFormModal">
      {{ succession.contract.serial_number }}
    </router-link>
  </CTableDataCell>
  <CTableDataCell class="text-center">
    <router-link to="" @click="callFormModal">
      {{ succession.seller.name }}
    </router-link>
  </CTableDataCell>
  <CTableDataCell class="text-center">
    <router-link to="" @click="callFormModal">
      {{ succession.buyer.name }}
    </router-link>
  </CTableDataCell>
  <CTableDataCell class="text-center">
    {{ succession.apply_date }}
  </CTableDataCell>
  <CTableDataCell class="text-center">
    {{ succession.trading_date }}
  </CTableDataCell>
  <CTableDataCell class="text-primary text-center fw-bold">
    {{ succession.approval_date }}
  </CTableDataCell>
  <CTableDataCell class="text-primary text-center fw-bold">
    {{ done ? '완료' : '' }}
  </CTableDataCell>
  <CTableDataCell class="text-center">
    <CButton type="button" :color="buttonColor" size="sm" @click="callFormModal"> 확인</CButton>
  </CTableDataCell>
</template>
