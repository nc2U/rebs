<script lang="ts" setup>
import MainChartExample from '@/views/_Dashboard/components/charts/MainChartExample.vue'
</script>

<template>
  <CRow>
    <CCol :md="12">
      <CCard class="mb-4">
        <CCardBody>
          <CRow>
            <CCol :sm="5">
              <h4 id="traffic" class="card-title mb-0">Traffic</h4>
              <div class="small text-medium-emphasis">January 2021</div>
            </CCol>
            <CCol :sm="7" class="d-none d-md-block">
              <CButton color="primary" class="float-end">
                <CIcon icon="cil-cloud-download" />
              </CButton>
              <CButtonGroup
                class="float-end me-3"
                role="group"
                aria-label="Basic outlined example"
              >
                <CButton color="secondary" variant="outline">Day</CButton>
                <CButton color="secondary" variant="outline" active
                  >Month
                </CButton>
                <CButton color="secondary" variant="outline">Year</CButton>
              </CButtonGroup>
            </CCol>
          </CRow>
          <CRow>
            <MainChartExample
              style="height: 300px; max-height: 300px; margin-top: 40px"
            />
          </CRow>
        </CCardBody>
        <CCardFooter>
          <CRow :xs="{ cols: 1 }" :md="{ cols: 5 }" class="text-center">
            <CCol class="mb-sm-2 mb-0">
              <div class="text-medium-emphasis">Visits</div>
              <strong>29.703 Users (40%)</strong>
              <CProgress
                class="mt-2"
                color="success"
                thin
                :precision="1"
                :value="40"
              />
            </CCol>
            <CCol class="mb-sm-2 mb-0 d-md-down-none">
              <div class="text-medium-emphasis">Unique</div>
              <strong>24.093 Users (20%)</strong>
              <CProgress
                class="mt-2"
                color="info"
                thin
                :precision="1"
                :value="20"
              />
            </CCol>
            <CCol class="mb-sm-2 mb-0">
              <div class="text-medium-emphasis">Pageviews</div>
              <strong>78.706 Views (60%)</strong>
              <CProgress
                class="mt-2"
                color="warning"
                thin
                :precision="1"
                :value="60"
              />
            </CCol>
            <CCol class="mb-sm-2 mb-0">
              <div class="text-medium-emphasis">New Users</div>
              <strong>22.123 Users (80%)</strong>
              <CProgress
                class="mt-2"
                color="danger"
                thin
                :precision="1"
                :value="80"
              />
            </CCol>
            <CCol class="mb-sm-2 mb-0 d-md-down-none">
              <div class="text-medium-emphasis">Bounce Rate</div>
              <strong>Average Rate (40.15%)</strong>
              <CProgress class="mt-2" :value="40" thin :precision="1" />
            </CCol>
          </CRow>
        </CCardFooter>
      </CCard>
    </CCol>
  </CRow>
</template>
