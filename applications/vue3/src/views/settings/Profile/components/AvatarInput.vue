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
      <div class="relative inline-block">
        <CImage rounded thumbnail fluid :src="imgUrl" />

        <div
          class="absolute top-0 h-full w-full bg-black rounded-full bg-opacity-25 flex items-center justify-center"
        >
          <button type="button" @click="browse">Browse</button>
          <button type="button" @click="remove" v-if="image">Remove</button>
        </div>
      </div>
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
      image: null,
      imgUrl: this.defaultSrc,
    }
  },
  methods: {
    browse(this: any) {
      this.$refs.file.$el.click()
    },
    remove() {
      this.image = null
      this.imgUrl = this.defaultSrc
      this.$emit('file-upload', this.image)
    },
    change(this: any, event: any) {
      this.image = event.target.files[0]
      this.$emit('file-upload', this.image)
      let reader = new FileReader()
      reader.readAsDataURL(this.image)
      reader.onload = (e: any) => {
        this.imgUrl = e.target.result
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
