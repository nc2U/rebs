<template>
  <CCard>
    <CCardBody>
      <CRow>
        <CCol class="pt-2">
          <CTable hover responsive>
            <colgroup>
              <col width="15%" />
              <col width="30%" />
              <col width="15%" />
              <col width="40%" />
            </colgroup>
            <CTableHead>
              <CTableRow>
                <CTableHeaderCell scope="col"></CTableHeaderCell>
                <CTableHeaderCell scope="col"></CTableHeaderCell>
                <CTableHeaderCell scope="col"></CTableHeaderCell>
                <CTableHeaderCell scope="col"></CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              <CTableRow>
                <CTableHeaderCell scope="row" color="dark">
                  프로젝트명
                </CTableHeaderCell>
                <CTableDataCell>
                  <span v-if="project">
                    {{ project.name }}
                    <span v-if="project.start_year">
                      ({{ project.start_year }}년도)
                    </span>
                  </span>
                </CTableDataCell>
                <CTableHeaderCell scope="row" color="dark">
                  프로젝트 종류
                </CTableHeaderCell>
                <CTableDataCell>
                  <span v-if="project">{{ project.kind_desc }}</span>
                </CTableDataCell>
              </CTableRow>

              <CTableRow>
                <CTableHeaderCell scope="row" color="dark">
                  현장주소(대표지번)
                </CTableHeaderCell>
                <CTableDataCell colspan="3">
                  <span v-if="project">
                    {{ project.local_address1 }} {{ project.local_address2 }}
                    {{ project.local_address3 }}
                  </span>
                </CTableDataCell>
              </CTableRow>
              <CTableRow>
                <CTableHeaderCell scope="row" color="dark">
                  용도지역지구
                </CTableHeaderCell>
                <CTableDataCell>
                  <span v-if="project">{{ project.area_usage }}</span>
                </CTableDataCell>
                <CTableHeaderCell scope="row" color="dark">
                  건축규모
                </CTableHeaderCell>
                <CTableDataCell>
                  <span v-if="project">{{ project.build_size }}</span>
                </CTableDataCell>
              </CTableRow>

              <CTableRow>
                <CTableHeaderCell scope="row" color="dark">
                  세대(호/실)수
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">
                    {{ numFormat(project.num_unit) }}
                    <span v-if="project.num_unit">세대(호/실)</span>
                  </span>
                </CTableDataCell>

                <CTableHeaderCell scope="row" color="dark">
                  대지매입면적
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">{{
                    areaM2PyFormat(project.buy_land_extent)
                  }}</span>
                </CTableDataCell>
              </CTableRow>

              <CTableRow>
                <CTableHeaderCell scope="row" color="dark">
                  계획대지면적
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">{{
                    areaM2PyFormat(project.scheme_land_extent)
                  }}</span>
                </CTableDataCell>
                <CTableHeaderCell scope="row" color="dark">
                  기부채납면적
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">{{
                    areaM2PyFormat(project.donation_land_extent)
                  }}</span>
                </CTableDataCell>
              </CTableRow>

              <CTableRow>
                <CTableHeaderCell scope="row" color="dark">
                  지상연면적
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">{{
                    areaM2PyFormat(project.on_floor_area)
                  }}</span>
                </CTableDataCell>
                <CTableHeaderCell scope="row" color="dark">
                  지하연면적
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">{{
                    areaM2PyFormat(project.under_floor_area)
                  }}</span>
                </CTableDataCell>
              </CTableRow>

              <CTableRow>
                <CTableHeaderCell scope="row" color="dark">
                  총 연면적
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">{{
                    areaM2PyFormat(project.total_floor_area)
                  }}</span>
                </CTableDataCell>
                <CTableHeaderCell scope="row" color="dark">
                  건축면적
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">{{
                    areaM2PyFormat(project.build_area)
                  }}</span>
                </CTableDataCell>
              </CTableRow>

              <CTableRow>
                <CTableHeaderCell scope="row" color="dark">
                  용적율
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">{{
                    ratioFormat(project.floor_area_ratio)
                  }}</span>
                </CTableDataCell>
                <CTableHeaderCell scope="row" color="dark">
                  건폐율
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">
                    {{ ratioFormat(project.build_to_land_ratio) }}
                  </span>
                </CTableDataCell>
              </CTableRow>

              <CTableRow>
                <CTableHeaderCell scope="row" color="dark">
                  법정주차대수
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">
                    {{ numFormat(project.num_legal_parking) }}
                    <span v-if="project.num_legal_parking">대</span>
                  </span>
                </CTableDataCell>
                <CTableHeaderCell scope="row" color="dark">
                  계획주차대수
                </CTableHeaderCell>
                <CTableDataCell class="text-right pr-3">
                  <span v-if="project">
                    {{ numFormat(project.num_planed_parking) }}
                    <span v-if="project.num_planed_parking">대</span>
                  </span>
                </CTableDataCell>
              </CTableRow>
            </CTableBody>
          </CTable>
        </CCol>
      </CRow>
    </CCardBody>

    <CCardFooter>
      <CRow class="justify-content-between">
        <CCol xs="auto">
          <CButton type="button" color="success" @click="toUpdate">
            <CIcon name="cil-check-circle" />
            수정하기
          </CButton>
        </CCol>
        <CCol xs="auto">
          <CButton type="button" color="primary" @click="toCreate">
            <CIcon name="cil-check-circle" />
            등록하기
          </CButton>
        </CCol>
      </CRow>
    </CCardFooter>
  </CCard>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/views/commonMixin'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ProjectDetail',
  mixins: [commonMixin],
  components: { AlertModal },
  props: {
    project: {
      type: Object,
      required: true,
    },
    userInfo: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    toCreate(this: any) {
      if (this.superAuth || (this.staffAuth && this.staffAuth.project === '2'))
        this.$emit('create-form')
      else this.$refs.alertModal.callModal()
    },
    toUpdate(this: any) {
      if (this.superAuth || (this.staffAuth && this.staffAuth.project === '2'))
        this.$emit('update-form')
      else this.$refs.alertModal.callModal()
    },
  },
})
</script>
