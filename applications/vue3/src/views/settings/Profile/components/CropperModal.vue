<template>
  <CModal :visible="visible" @close="() => close">
    <CModalHeader :close-button="false">
      <CModalTitle component="h6"> Crop your new profile picture</CModalTitle>
      <CButton
        type="button"
        aria-label="Close"
        class="btn btn-close"
        @click="close"
      />
    </CModalHeader>
    <CModalBody>
      <cropper
        class="cropper"
        :stencil-component="$options.components.CircleStencil"
        :default-size="{
          width: 1000,
          height: 1000,
        }"
        :src="modalImg"
        @change="change"
      />
    </CModalBody>
    <CModalFooter class="d-grid gap-2">
      <CButton color="success"> Set new profile picture</CButton>
    </CModalFooter>
    <CircleStencil v-if="false" />
  </CModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { CircleStencil, Cropper } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'
import 'vue-advanced-cropper/dist/theme.compact.css'

export default defineComponent({
  name: 'CropperModal',
  components: { CircleStencil, Cropper },
  props: {
    modalImg: String,
  },
  setup() {
    return {}
  },
  data() {
    return {
      visible: false,
    }
  },
  computed: {},
  watch: {
    visible(val) {
      if (val === false) {
        this.$emit('modal-img', null)
      }
    },
  },
  methods: {
    callModal() {
      this.visible = true
    },
    change({ coordinates, canvas }: any) {
      console.log(coordinates, canvas)
    },
    close() {
      this.visible = false
    },
  },
})
</script>

<style lang="scss" scoped>
.cropper {
  height: 320px;
  width: 470px;
  background: #ddd;
}

.line {
  border-style: dashed;
  border-color: red;
}
</style>
