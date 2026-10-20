<script lang="ts" setup>
import { type PropType, ref } from 'vue'
import type { Relation, SimpleSite, SiteOwner } from '@/store/types/project'
import Site from '@/views/projects/SiteOwner/components/Site.vue'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteOwnerForm from '@/views/projects/SiteOwner/components/SiteOwnerForm.vue'

const props = defineProps({
  owner: { type: Object as PropType<SiteOwner>, required: true },
  isReturned: { type: Boolean, default: false },
  isHighlight: { type: Boolean, default: false },
})

const emit = defineEmits(['relation-patch', 'multi-submit', 'on-delete'])

const updateFormModal = ref()
const isModalVisible = ref(false)

const showDetail = () => {
  isModalVisible.value = true
  updateFormModal.value.callModal()
}

const closeModal = () => {
  updateFormModal.value.close()
  isModalVisible.value = false
}

const relationPatch = (payload: Relation) => emit('relation-patch', payload)

const multiSubmit = (payload: SiteOwner) => {
  emit('multi-submit', payload)
  closeModal()
}

const onDelete = (payload: { pk: number; project: number }) => {
  emit('on-delete', payload)
  closeModal()
}
</script>

<template>
  <CTableRow
    v-for="(site, index) in owner.sites"
    :key="site.pk"
    class="text-center"
    :class="{ 'table-warning': props.isHighlight && index === 0 }"
    :data-site-owner-id="index === 0 ? owner.pk : null"
  >
    <Site
      :owner="owner"
      :site="site as SimpleSite"
      :index="index"
      :is-returned="isReturned"
      :is-highlight="isHighlight && index === 0"
      @show-detail="showDetail"
      @relation-patch="relationPatch"
      @multi-submit="multiSubmit"
      @on-delete="onDelete"
    />
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>부지 소유자 정보 관리</template>
    <template #default>
      <SiteOwnerForm
        v-if="isModalVisible"
        :owner="owner"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="closeModal"
      />
    </template>
  </FormModal>
</template>
