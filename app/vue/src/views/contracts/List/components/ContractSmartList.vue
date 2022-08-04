<template>
  <CSmartTable
    clickable-rows
    :table-props="{
      striped: false,
      hover: true,
    }"
    :table-head-props="{
      color: 'dark',
    }"
    :active-page="1"
    clickable-rows
    :items="contractIndex"
    :columns="columns"
    column-filter
    table-filter
    cleaner
    items-per-page-select
    :items-per-page="10"
    items-per-page-label="페이지당 표시 건수"
    column-sorter
    pagination
  >
    <template #serial_number="{ item }">
      <td>
        <router-link to="#">{{ item.serial_number }}</router-link>
      </td>
    </template>

    <template #is_registed="{ item }">
      <td>
        <CBadge :color="getBadge(item.is_registed)">
          {{ item.is_registed ? '인가완료' : '미 인 가' }}
        </CBadge>
      </td>
    </template>

    <!--    <template #show_details="{ item, index }">-->
    <!--      <td class="py-2">-->
    <!--        <CButton color="primary" variant="outline" square size="sm">-->
    <!--          &lt;!&ndash;          @click="toggleDetails(item, index)"&ndash;&gt;-->
    <!--          &lt;!&ndash;        >&ndash;&gt;-->
    <!--          {{ Boolean(item._toggled) ? 'Hide' : 'Show' }}-->
    <!--        </CButton>-->
    <!--      </td>-->
    <!--    </template>-->

    <!--    <template #details="{ item }">-->
    <!--      <CCollapse :visible="this.details.includes(item._id)">-->
    <!--        <CCardBody>-->
    <!--          <h4>-->
    <!--            {{ item.username }}-->
    <!--          </h4>-->
    <!--          <p class="text-muted">User since: {{ item.registered }}</p>-->
    <!--          <CButton size="sm" color="info" class=""> User Settings</CButton>-->
    <!--          <CButton size="sm" color="danger" class="ml-1"> Delete</CButton>-->
    <!--        </CCardBody>-->
    <!--      </CCollapse>-->
    <!--    </template>-->
  </CSmartTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapActions, mapGetters } from 'vuex'

export default defineComponent({
  name: 'ContractList',
  data: () => {
    return {
      columns: [
        {
          key: 'serial_number',
          label: '일련번호',
          _style: { width: '10%' },
        },
        {
          key: 'order_group',
          label: '차수',
          _style: { width: '10%' },
        },
        {
          key: 'unut_type',
          label: '타입',
          _style: { width: '10%' },
        },
        {
          key: 'unit_number',
          label: '동호수',
          _style: { width: '10%' },
        },
        {
          key: 'contractor',
          label: '계약자',
          _style: { width: '10%' },
        },
        {
          key: 'is_registed',
          label: '인가등록여부',
          _style: { width: '10%' },
        },
        {
          key: 'address',
          label: '주소',
          _style: { width: '25%' },
          filter: true,
          sorter: true,
        },
        {
          key: 'cell_phone',
          label: '연락처',
          _style: { width: '15%' },
        },
      ],
    }
  },
  created() {
    this.fetchContractList({ project: this.initProjId })
  },
  computed: {
    ...mapGetters('contract', ['contractIndex']),
    ...mapGetters('accounts', ['initProjId']),
  },
  methods: {
    getBadge(is_registed: any) {
      return is_registed ? 'success' : 'danger'
    },
    // toggleDetails(item) {
    //   if (this.details.includes(item._id)) {
    //     this.details = this.details.filter(_item => _item !== item._id)
    //     return
    //   }
    //   this.details.push(item._id)
    // },
    ...mapActions('contract', ['fetchContractList']),
  },
})
</script>
