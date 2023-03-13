<script lang="ts" setup>
defineProps({ contractor: { type: Object, default: null } })

const getStatus = (num: string) => {
  const status = [
    { code: '1', text: '청약' },
    { code: '2', text: '계약' },
    { code: '3', text: '해지신청' },
    { code: '4', text: '해지완료' },
  ]
  return status.filter(s => s.code === num).map(s => s.text)[0]
}
</script>

<template>
  <CAlert :color="contractor.status < '3' ? 'success' : 'danger'">
    <strong>
      <CIcon name="cilTask" />
      계약자명 :
      {{ contractor.name }}({{ contractor.__str__ }}) :::::: 현재상태 : [{{
        getStatus(contractor.status)
      }}]
    </strong>
  </CAlert>
</template>
