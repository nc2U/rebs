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
        ref="cropper"
        class="cropper"
        :stencil-component="$options.components.CircleStencil"
        :default-size="{
          width: 1000,
          height: 1000,
        }"
        :src="modalImg"
      />
    </CModalBody>
    <CModalFooter class="d-grid gap-2">
      <CButton color="success" @click="crop"> Set new profile picture</CButton>
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
        this.$emit('image-del', null)
      }
    },
  },
  methods: {
    callModal() {
      this.visible = true
    },
    close() {
      this.visible = false
    },
    crop(this: any) {
      const { canvas } = this.$refs.cropper.getResult()
      if (canvas) {
        canvas.toBlob((blob: any) => {
          this.$emit('file-upload', blob)
        })
      }
      this.close()
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
