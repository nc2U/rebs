<template>
  <CRow class="mb-4">
    <CCol>
      <h6>Profile picture</h6>
      <CFormInput
        ref="file"
        type="file"
        accept="image/*"
        style="display: none"
        @change="change"
      />
      <CRow class="relative inline-block">
        <CCol>
          <CDropdown placement="bottom">
            <CDropdownToggle class="py-0 btn-link" :caret="false">
              <CImage rounded thumbnail fluid :src="imgUrl" />
              <!--          <button type="button" @click="browse">-->
              <!--            <CIcon name="cil-camera" />-->
              <!--          </button>-->
              <button type="button" @click="remove" v-if="changeImage">
                <CIcon name="cil-x" />
              </button>
            </CDropdownToggle>
            <CDropdownMenu class="pt-0">
              <CDropdownItem @click="browse">
                <strong>Upload a photo...</strong>
              </CDropdownItem>
            </CDropdownMenu>
          </CDropdown>
        </CCol>
      </CRow>
    </CCol>
  </CRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'AvatarInput',
  components: {},

  props: {
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
