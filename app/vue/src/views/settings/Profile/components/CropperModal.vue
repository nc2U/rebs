<script lang="ts">
import { defineComponent, ref, watch } from 'vue'
import { CircleStencil, Cropper } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'
import 'vue-advanced-cropper/dist/theme.compact.css'

export default defineComponent({
  name: 'CropperModal',
  components: { CircleStencil, Cropper },
  props: {
    modalImg: { type: String, default: undefined },
  },
  setup(props, ctx) {
    const visible = ref(false)
    const cropper = ref()

    const close = () => {
      visible.value = false
      ctx.emit('image-del')
    }

    const crop = () => {
      const { canvas } = cropper.value.getResult()
      if (canvas) {
        canvas.toBlob((blob: Blob) => {
          const img = new File([blob], 'profile.png', { type: blob.type })
          ctx.emit('file-upload', img)
        })
      }
      close()
    }

    watch(visible, val => {
      if (!val) ctx.emit('image-del')
    })

    return {
      visible,
      cropper,
      close,
      crop,
    }
  },
})
</script>

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
