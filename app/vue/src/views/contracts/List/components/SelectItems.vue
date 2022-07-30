<script lang="ts" setup>
import { ref } from 'vue'

const props = defineProps({
  project: { type: Boolean, default: false },
  visible: Boolean,
})

const emit = defineEmits(['print-items'])
const items = ref(['1', '2', '3', '4', '5', '6', '7', '8', '9', '14'])
</script>

<template>
  <v-alert v-show="visible" color="info" variant="tonal" class="info-tonal">
    <v-checkbox-btn
      v-model="items"
      label="일련번호"
      color="grey"
      value="1"
      readonly
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="인가여부"
      color="indigo-darken-3"
      value="2"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="차수"
      color="indigo-darken-3"
      value="3"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="타입"
      color="indigo-darken-3"
      value="4"
      hide-details
    />
    <v-checkbox-btn
      v-if="project"
      v-model="items"
      label="동호수"
      color="indigo-darken-3"
      value="5"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="계약자"
      color="indigo-darken-3"
      value="6"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="생년월일"
      color="indigo-darken-3"
      value="7"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="계약일자"
      color="indigo-darken-3"
      value="8"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="연락처[1]"
      color="indigo-darken-3"
      value="9"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="연락처[2]"
      color="indigo-darken-3"
      value="10"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="연락처[3]"
      color="indigo-darken-3"
      value="11"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="이메일"
      color="indigo-darken-3"
      value="12"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="주소[등본]"
      color="indigo-darken-3"
      value="13"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="주소[우편]"
      color="indigo-darken-3"
      value="14"
      hide-details
    />
    <v-checkbox-btn
      v-model="items"
      label="비고"
      color="indigo-darken-3"
      value="15"
      hide-details
    />
  </v-alert>
</template>

<style lang="scss" scoped>
.info-tonal {
  color: #0d47a1 !important;
}
</style>
