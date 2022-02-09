<template>
  <CTableRow>
    <CTableDataCell class="text-center">
      {{ condTexts.orderText }}
    </CTableDataCell>
    <CTableDataCell class="text-center">
      {{ condTexts.typeText }}
    </CTableDataCell>
    <CTableDataCell> {{ floor.alias_name }}</CTableDataCell>

    <CTableDataCell>
      <CFormInput type="number" min="0" placeholder="타입별 건물가" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput type="number" min="0" placeholder="타입별 대지가" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput type="number" min="0" placeholder="타입별 부가세" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput type="number" min="0" placeholder="타입별 공급가격" />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton color="success" size="sm">저장</CButton>
      <CButton color="danger" size="sm">삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <!--  <ConfirmModal ref="confirmModal">-->
  <!--    <template v-slot:header>-->
  <!--      <CIcon name="cil-warning" />-->
  <!--      층별 타입 삭제-->
  <!--    </template>-->
  <!--    <template v-slot:default>-->
  <!--      이 타입에 종속된 분양가 데이터가 있는 경우 해당 데이터를 모두 제거한 후-->
  <!--      삭제가능 합니다. 해당 층별 타입을 삭제 하시겠습니까?-->
  <!--    </template>-->
  <!--    <template v-slot:footer>-->
  <!--      <CButton color="danger" @click="modalAction">삭제</CButton>-->
  <!--    </template>-->
  <!--  </ConfirmModal>-->
</template>

<script lang="ts">
import { defineComponent } from 'vue'
// import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'Price',
  // components: { ConfirmModal },
  data() {
    return {
      form: {
        floorId: null,
        price_build: null,
        price_land: null,
        price_tax: null,
        price: null,
      },
    }
  },
  // created() {},
  props: {
    condTexts: {
      type: Object,
    },
    queryIds: {
      type: Object,
    },
    floor: {
      type: Object,
    },
  },
  computed: {
    ...mapState('cash', ['priceList']),
  },
})
</script>
