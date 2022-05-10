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
          <CDropdown placement="bottom-start">
            <CDropdownToggle class="py-0 btn-link" :caret="false">
              <CImage rounded thumbnail fluid :src="imgUrl" />
              <CCol
                class="bg-white text-high-emphasis position-absolute rounded-2 px-2 py-1 left-0 bottom-0 ml-1 mb-1 border"
              >
                <CIcon name="cilPencil" />
                Edit
              </CCol>
            </CDropdownToggle>
            <CDropdownMenu class="ml-2 py-1">
              <CDropdownItem @click="browse"> Upload a photo...</CDropdownItem>
            </CDropdownMenu>
          </CDropdown>
        </CCol>
      </CRow>
    </CCol>
  </CRow>

  <CropperModal
    ref="cropModal"
    :modal-img="modalImg"
    @image-del="delModalImg"
    @file-upload="fileUpload"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import CropperModal from './CropperModal.vue'

export default defineComponent({
  name: 'AvatarInput',
  components: { CropperModal },
  props: {
    defaultSrc: String,
  },
  data() {
    return {
      imgUrl: this.defaultSrc || '/static/dist/img/NoImage.jpeg',
      modalImg: null,
    }
  },
  methods: {
    browse(this: any) {
      this.$refs.file.$el.click()
    },
    change(this: any, event: any) {
      const image = event.target.files[0]
      this.$emit('file-upload', image)
      let reader = new FileReader()
      reader.readAsDataURL(image)
      reader.onload = (e: any) => {
        this.modalImg = e.target.result
        if (this.modalImg !== null) {
          this.$refs.cropModal.callModal()
        }
      }
    },
    fileUpload(image: any) {
      // this.$emit('file-upload', image)
      let reader = new FileReader()
      reader.readAsDataURL(image)
      reader.onload = (e: any) => {
        this.imgUrl = e.target.result
      }
      console.log(image)
    },
    delModalImg() {
      this.modalImg = null
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
