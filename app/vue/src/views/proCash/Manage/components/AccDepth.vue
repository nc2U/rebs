<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useProCash } from '@/store/pinia/proCash'
import { cutString } from '@/utils/baseMixins'
import AlertModal from '@/components/Modals/AlertModal.vue'

const dAccount = ref()

const proCashStore = useProCash()
const allAccD1List = computed(() => proCashStore.allAccD1List)
const allAccD3List = computed(() => proCashStore.allAccD3List)

const callModal = () => dAccount.value.callModal()

defineExpose({ callModal })
</script>

<template>
  <AlertModal ref="dAccount" size="lg">
    <template #header> 프로젝트 계정 분류 보기</template>
    <template #default>
      <CAccordion>
        <CAccordionItem
          v-for="d1 in allAccD1List"
          :key="d1.pk"
          :item-key="d1.pk"
        >
          <CAccordionHeader>
            {{ `[${d1.code}] ${d1.name} :: ${cutString(d1.description, 45)}` }}
          </CAccordionHeader>
          <CAccordionBody class="pl-3">
            <CRow
              v-for="d3 in allAccD3List.filter(d3 => d3.d1 === d1.pk)"
              :key="d3.pk"
              class="pl-2 mb-2"
            >
              <CCol>
                [{{ d3.code }}] {{ d3.name }} ::
                {{ cutString(d3.description, 38) }}
              </CCol>
            </CRow>
          </CAccordionBody>
        </CAccordionItem>
      </CAccordion>
    </template>
    <template #footer></template>
  </AlertModal>
</template>
