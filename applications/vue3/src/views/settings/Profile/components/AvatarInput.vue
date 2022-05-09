<template>
  <CRow class="mb-4">
    <CCol>
      <h6>Profile picture</h6>
      <CFormInput
        type="file"
        accept="image/*"
        ref="file"
        style="display: none"
        @change="change"
      />
      <CRow class="relative inline-block">
        <CCol
          class="absolute top-0 h-full w-full bg-black rounded-full bg-opacity-25 flex items-center justify-center"
        >
          <CImage
            rounded
            thumbnail
            fluid
            :src="imgUrl"
            class="h-full w-full rounded-full object-cover"
          />
          <button type="button" @click="browse">
            <CIcon name="cil-camera" />
          </button>
          <button type="button" @click="remove" v-if="changeImage">
            <CIcon name="cil-x" />
          </button>
        </CCol>
      </CRow>
    </CCol>
  </CRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AvatarInput',
  props: {
    value: File,
    defaultSrc: String,
  },
  data() {
    return {
      imgUrl: this.defaultSrc || '/static/dist/img/NoImage.jpeg',
      changeImage: false,
    }
  },
  methods: {
    browse(this: any) {
      this.$refs.file.$el.click()
    },
    remove() {
      this.imgUrl = '/static/dist/img/NoImage.jpeg'
      this.changeImage = false
      this.$emit('file-upload', null)
    },
    change(this: any, event: any) {
      const image = event.target.files[0]
      this.$emit('file-upload', image)
      let reader = new FileReader()
      reader.readAsDataURL(image)
      reader.onload = (e: any) => {
        this.imgUrl = e.target.result
        this.changeImage = true
      }
    },
  },
})
</script>

<style lang="scss" scoped>
@media (min-width: 768px) {
  .flex-md-row {
    flex-direction: row !important;
  }
}

.flex-column-reverse {
  flex-direction: column-reverse;
}

.rounded {
  border-radius: 100px !important;
  width: 200px;
  height: 200px;
  overflow: hidden;
  cursor: pointer;
}
</style>
