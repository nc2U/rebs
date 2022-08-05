<script lang="ts" setup>
import { ref } from 'vue'
import CropperModal from './CropperModal.vue'

const props = defineProps({
  defaultSrc: { type: String, default: '' },
})

const emit = defineEmits(['file-upload'])

const imgUrl = ref(props.defaultSrc || '/static/dist/img/NoImage.jpeg')
const modalImg = ref(null)
const cropModal = ref()

const browse = () => {
  let fu = document.getElementById('file')
  if (fu !== null) fu.click()
}

const change = (event: any) => {
  const image = event.target.files[0]
  emit('file-upload', image)
  let reader = new FileReader()
  reader.readAsDataURL(image)
  reader.onload = (e: any) => {
    modalImg.value = e.target.result
    if (modalImg.value !== null) {
      cropModal.value.callModal()
    }
  }
}

const fileUpload = (image: any) => {
  emit('file-upload', image)
  let reader = new FileReader()
  reader.readAsDataURL(image)
  reader.onload = (e: any) => {
    imgUrl.value = e.target.result
  }
}
const delModalImg = () => {
  modalImg.value = null
}
</script>

<template>
  <CRow class="mb-4">
    <CCol>
      <h6>Profile picture</h6>
      <input
        id="file"
        type="file"
        class="form-control"
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
