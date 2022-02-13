<template>
  <CSmartTable
    clickableRows
    :tableProps="{
      striped: false,
      hover: true,
    }"
    :tableHeadProps="{
      color: 'default',
    }"
    :activePage="1"
    header
    :items="items"
    :columns="columns"
    columnFilter
    tableFilter
    cleaner
    itemsPerPageSelect
    :itemsPerPage="5"
    columnSorter
    pagination
  >
    <template #status="{ item }">
      <td>
        <CBadge :color="getBadge(item.status)">{{ item.status }}</CBadge>
      </td>
    </template>

    <template #show_details="{ item, index }">
      <td class="py-2">
        <CButton color="primary" variant="outline" square size="sm">
          <!--          @click="toggleDetails(item, index)"-->
          <!--        >-->
          {{ Boolean(item._toggled) ? 'Hide' : 'Show' }}
        </CButton>
      </td>
    </template>

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

export default defineComponent({
  name: 'ContractList',
  data: () => {
    return {
      columns: [
        {
          key: 'name',
          _style: { width: '40%' },
          _props: { color: 'primary', className: 'fw-semibold' },
        },
        'registered',
        { key: 'role', filter: false, sorter: false, _style: { width: '20%' } },
        { key: 'status', _style: { width: '20%' } },
        // {
        //   key: 'show_details',
        //   label: '',
        //   _style: { width: '1%' },
        //   filter: false,
        //   sorter: false,
        //   _props: { color: 'primary', className: 'fw-semibold' },
        // },
      ],
      // details: [],
      items: [
        {
          name: 'John Doe',
          registered: '2018/01/01',
          role: 'Guest',
          status: 'Pending',
        },
        {
          name: 'Samppa Nori',
          registered: '2018/01/01',
          role: 'Member',
          status: 'Active',
          // _props: { color: 'primary', align: 'middle' },
        },
        {
          name: 'Estavan Lykos',
          registered: '2018/02/01',
          role: 'Staff',
          status: 'Banned',
          // _cellProps: {
          // all: { className: 'fw-semibold' },
          // name: { color: 'info' },
          // },
        },
        {
          name: 'Chetan Mohamed',
          registered: '2018/02/01',
          role: 'Admin',
          status: 'Inactive',
        },
        {
          name: 'Derick Maximinus',
          registered: '2018/03/01',
          role: 'Member',
          status: 'Pending',
        },
        {
          name: 'Friderik Dávid',
          registered: '2018/01/21',
          role: 'Staff',
          status: 'Active',
        },
        {
          name: 'Yiorgos Avraamu',
          registered: '2018/01/01',
          role: 'Member',
          status: 'Active',
        },
        {
          name: 'Avram Tarasios',
          registered: '2018/02/01',
          role: 'Staff',
          status: 'Banned',
          // _props: { color: 'warning', align: 'middle' },
        },
        {
          name: 'Quintin Ed',
          registered: '2018/02/01',
          role: 'Admin',
          status: 'Inactive',
        },
        {
          name: 'Enéas Kwadwo',
          registered: '2018/03/01',
          role: 'Member',
          status: 'Pending',
        },
        {
          name: 'Agapetus Tadeáš',
          registered: '2018/01/21',
          role: 'Staff',
          status: 'Active',
        },
        {
          name: 'Carwyn Fachtna',
          registered: '2018/01/01',
          role: 'Member',
          status: 'Active',
        },
        {
          name: 'Nehemiah Tatius',
          registered: '2018/02/01',
          role: 'Staff',
          status: 'Banned',
        },
        {
          name: 'Ebbe Gemariah',
          registered: '2018/02/01',
          role: 'Admin',
          status: 'Inactive',
        },
        {
          name: 'Eustorgios Amulius',
          registered: '2018/03/01',
          role: 'Member',
          status: 'Pending',
        },
        {
          name: 'Leopold Gáspár',
          registered: '2018/01/21',
          role: 'Staff',
          status: 'Active',
        },
        {
          name: 'Pompeius René',
          registered: '2018/01/01',
          role: 'Member',
          status: 'Active',
        },
        {
          name: 'Paĉjo Jadon',
          registered: '2018/02/01',
          role: 'Staff',
          status: 'Banned',
        },
        {
          name: 'Micheal Mercurius',
          registered: '2018/02/01',
          role: 'Admin',
          status: 'Inactive',
        },
        {
          name: 'Ganesha Dubhghall',
          registered: '2018/03/01',
          role: 'Member',
          status: 'Pending',
        },
        {
          name: 'Hiroto Šimun',
          registered: '2018/01/21',
          role: 'Staff',
          status: 'Active',
        },
        {
          name: 'Vishnu Serghei',
          registered: '2018/01/01',
          role: 'Member',
          status: 'Active',
        },
        {
          name: 'Zbyněk Phoibos',
          registered: '2018/02/01',
          role: 'Staff',
          status: 'Banned',
        },
        {
          name: 'Aulus Agmundr',
          registered: '2018/01/01',
          role: 'Member',
          status: 'Pending',
        },
        {
          name: 'Ford Prefect',
          registered: '2001/05/25',
          role: 'Alien',
          status: "Don't panic!",
        },
      ],
    }
  },
  methods: {
    getBadge(status: any) {
      switch (status) {
        case 'Active':
          return 'success'
        case 'Inactive':
          return 'secondary'
        case 'Pending':
          return 'warning'
        case 'Banned':
          return 'danger'
        default:
          'primary'
      }
    },
    // toggleDetails(item) {
    //   if (this.details.includes(item._id)) {
    //     this.details = this.details.filter(_item => _item !== item._id)
    //     return
    //   }
    //   this.details.push(item._id)
    // },
  },
})
</script>
