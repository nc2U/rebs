<script lang="ts" setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  unitSet: { type: Boolean, default: false },
  visible: { type: Boolean, default: false },
})

const printItems = ref(['1', '3', '4', '5', '8', '9', '10'])
const emit = defineEmits(['print-items'])

watch(printItems, newVal => {
  emit('print-items', newVal)
})

watch(props, val => {
  if (val.unitSet && !printItems.value.includes('6-7')) printItems.value.splice(4, 0, '6-7')
})

onMounted(() => {
  if (props.unitSet && !printItems.value.includes('6-7')) printItems.value.splice(4, 0, '6-7')
})
</script>

<template>
  <CCollapse :visible="visible" class="bg-indigo-lighten-5">
    <v-container class="m-0" fluid>
      <v-row class="my-checkbox d-flex py-2">
        <v-checkbox-btn
          id="printItems1"
          v-model="printItems"
          color="grey"
          label="일련번호"
          readonly
          value="1"
          hide-details
        />
        <v-checkbox-btn
          id="printItems2"
          v-model="printItems"
          label="등록상태"
          value="2"
          color="indigo"
          inline
          hide-details
        />
        <v-checkbox-btn
          id="printItems3"
          v-model="printItems"
          label="차수"
          value="3"
          color="indigo"
          inline
          hide-details
        />
        <v-checkbox-btn
          id="printItems4"
          v-model="printItems"
          label="타입"
          value="4"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems5"
          v-model="printItems"
          label="계약자"
          value="5"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          v-if="unitSet"
          id="printItems6"
          v-model="printItems"
          label="동호수"
          value="6-7"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems8"
          v-model="printItems"
          label="계약일자"
          value="8"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems9"
          v-model="printItems"
          label="공급가액"
          value="9"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems10"
          v-model="printItems"
          label="납입금합계"
          value="10"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems11"
          v-model="printItems"
          label="회당계약금"
          value="11"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems12"
          v-model="printItems"
          label="회당중도금"
          value="12"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems13"
          v-model="printItems"
          label="회당잔금"
          value="13"
          color="indigo"
          hide-details
        />

        <v-checkbox-btn
          id="printItems14"
          v-model="printItems"
          label="생년월일"
          value="14"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems15"
          v-model="printItems"
          label="연락처[1]"
          value="15"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems16"
          v-model="printItems"
          label="연락처[2]"
          value="16"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems17"
          v-model="printItems"
          label="연락처[3]"
          value="17"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems18"
          v-model="printItems"
          label="이메일"
          value="18"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems19"
          v-model="printItems"
          label="주소[등본]"
          value="19-20-21-22"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems23"
          v-model="printItems"
          label="주소[우편]"
          value="23-24-25-26"
          color="indigo"
          hide-details
        />
        <v-checkbox-btn
          id="printItems27"
          v-model="printItems"
          label="비고"
          value="27"
          color="indigo"
          hide-details
        />
      </v-row>
    </v-container>
  </CCollapse>
</template>

<style lang="scss" scoped>
:deep(.my-checkbox .v-label) {
  font-size: 1em !important;
}
</style>
