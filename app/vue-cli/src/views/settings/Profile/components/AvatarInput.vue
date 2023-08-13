<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue'
import CropperModal from './CropperModal.vue'

const props = defineProps({
  image: { type: String, default: '/static/dist/img/NoImage.jpeg' },
})

const emit = defineEmits(['file-upload'])

const imgUrl = ref('')

const modalImg = ref()
const cropModal = ref()

const browse = () => {
  const fu = document.getElementById('file')
  if (!!fu) fu.click()
}

const loadFile = (payload: Event) => {
  const inputEl = payload.target as HTMLInputElement
  if (inputEl.files) {
    const img = inputEl.files[0]
    emit('file-upload', img)
    const reader = new FileReader()
    reader.readAsDataURL(img)
    reader.onload = e => {
      modalImg.value = e.target?.result
      if (!!modalImg.value) {
        cropModal.value.visible = true
      }
    }
  }
}

const fileUpload = (img: File) => {
  emit('file-upload', img)
  const reader = new FileReader()
  reader.readAsDataURL(img)
  reader.onload = e => {
    imgUrl.value = String(e.target?.result)
  }
}

const delModalImg = () => (modalImg.value = null)

watch(props, val => {
  if (val) {
    imgUrl.value = val.image
  }
})

onMounted(() => {
  if (props.image) {
    imgUrl.value = props.image
  }
})
</script>

<template>
  <CRow class="mb-4">
    <CCol>
      <h6>프로필 이미지</h6>
      <input
        id="file"
        type="file"
        class="form-control"
        accept="image/*"
        style="display: none"
        @change="loadFile"
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
