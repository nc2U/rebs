<script lang="ts" setup>
import { onBeforeMount, reactive, ref } from 'vue'
import Relation from '@/views/projects/SiteOwner/components/Relation.vue'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteOwnerForm from '@/views/projects/SiteOwner/components/SiteOwnerForm.vue'

const props = defineProps({
  owner: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['relation-update', 'multi-submit', 'on-delete'])

const form = reactive({
  pk: null,
  project: null,
  owner: '',
  date_of_birth: null as string | null,
  phone1: '',
  phone2: '',
  zipcode: '',
  address1: '',
  address2: '',
  address3: '',
  own_sort: '',
  own_sort_desc: '',
  sites: [],
  relations: [],
  counsel_record: '',
})

const updateFormModal = ref()
const showDetail = () => updateFormModal.value.callModal()
const relationUpdate = (payload: any) => emit('relation-update', payload)
const multiSubmit = (payload: any) => emit('multi-submit', payload)
const onDelete = (payload: any) => emit('on-delete', payload)

onBeforeMount(() => {
  if (props.owner) {
    form.pk = props.owner.pk
    form.project = props.owner.project
    form.owner = props.owner.owner
    form.date_of_birth = props.owner.date_of_birth
    form.phone1 = props.owner.phone1
    form.phone2 = props.owner.phone2
    form.zipcode = props.owner.zipcode
    form.address1 = props.owner.address1
    form.address2 = props.owner.address2
    form.address3 = props.owner.address3
    form.own_sort = props.owner.own_sort
    form.own_sort_desc = props.owner.own_sort_desc
    form.sites = props.owner.sites
    form.relations = props.owner.relations
    form.counsel_record = props.owner.counsel_record
  }
})
</script>

<template>
  <CTableRow
    v-for="(rel, i) in owner.relations"
    :key="rel.pk"
    class="text-center"
  >
    <Relation
      :owner="owner"
      :relation="rel"
      :index="i"
      @show-detail="showDetail"
      @relation-update="relationUpdate"
      @multi-submit="multiSubmit"
      @on-delete="onDelete"
    />
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>
      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />
      부지 소유자 정보 관리
    </template>
    <template #default>
      <SiteOwnerForm
        :owner="owner"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
