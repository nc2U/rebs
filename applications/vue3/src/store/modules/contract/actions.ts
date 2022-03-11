import api from '@/api'
import {
  FETCH_CONTRACT,
  FETCH_CONTRACT_LIST,
  FETCH_ORDER_GROUP_LIST,
  FETCH_SUBS_SUMMARY_LIST,
  FETCH_CONT_SUMMARY_LIST,
  FETCH_KEY_UNIT_LIST,
  FETCH_HOUSE_UNIT_LIST,
} from '@/store/modules/contract/mutations-types'
import router from '@/router'
import { message } from '@/utils/helper'

const actions = {
  fetchContractList: ({ commit }: any, payload?: any) => {
    const { project } = payload
    const status = payload.status ? payload.status : '2'
    let url = `/contract/?project=${project}&activation=true&contractor__status=${status}`
    if (payload.order_group) url += `&order_group=${payload.order_group}`
    if (payload.unit_type) url += `&unit_type=${payload.unit_type}`
    if (payload.building)
      url += `&keyunit__houseunit__building_unit=${payload.building}`
    if (payload.registed) url += `&contractor__is_registed=${payload.registed}`
    if (payload.from_date) url += `&from_contract_date=${payload.from_date}`
    if (payload.to_date) url += `&to_contract_date=${payload.to_date}`
    if (payload.ordering) url += `&ordering=${payload.ordering}`
    if (payload.search) url += `&search=${payload.search}`
    const page = payload.page ? payload.page : 1
    url += `&page=${page}`
    api
      .get(url)
      .then(res => {
        commit(FETCH_CONTRACT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchContract: ({ commit }: any, pk: number) => {
    api
      .get(`/contract/${pk}/`)
      .then(res => {
        commit(FETCH_CONTRACT, res.data)
      })
      .catch(console.log)
  },

  createContract: async (payload: any) => {
    // 1. 계약 생성
    api
      .post(`/contract/`, payload)
      .then(res => console.log(res.data))
      .catch(err => console.log(err.response.data))
  },

  patchKeyUnit: (payload: any) => {
    // 2. keyunit
    api
      .patch(`key-unit/${payload.keyUnitPk}/`, payload.contPk)
      .then(res => console.log(res.data))
      .catch(err => console.log(err.response.data))
  },

  patchHouseUnit: (payload: any) => {
    // 3. houseunit
    api
      .patch(`/house-unit/${payload.houseUnitPk}`, payload.keyUnitPk)
      .then(res => console.log(res.data))
      .catch(err => console.log(err.response.data))
  },

  createContractor: (payload: any) => {
    // 4. contractor
    api
      .post(`/contractor/`, payload)
      .then(res => console.log(res.data))
      .catch(err => console.log(err.response.data))
  },

  createAddress: (payload: any) => {
    // 5. address
    api
      .post(`/contractor-address/`, payload)
      .then(res => console.log(res.data))
      .catch(err => console.log(err.response.data))
  },

  createContact: (payload: any) => {
    // 6. contact
    api
      .post(`/contractor-contact/`, payload)
      .then(res => console.log(res.data))
      .catch(err => console.log(err.response.data))
  },

  createContractSet: async ({ dispatch }: any, payload: any) => {
    // 1. contract 생성
    const { project, order_group, unit_type, key_unit, ...rest1 } = payload
    const unit = key_unit.split(',')
    const serial_number = `${unit[1]}-${order_group}`
    const contractObj = await dispatch('createContract', {
      project,
      order_group,
      unit_type,
      serial_number,
    })

    // 2. 계약 유닛 연결 ( keyunit -> contract.pk)
    const keyUnitPk = key_unit[0]
    const contPk = contractObj.data.pk
    const keyunitObj = await dispatch('patchKeyUnit', { keyUnitPk, contPk })

    // 3. 동호수 연결
    const { houseunit, ...rest3 } = rest1
    const houseUnitPk = houseunit
    const houseunitObj = await dispatch('patchHouseUnit', {
      houseUnitPk,
      keyUnitPk,
    })

    // 4. 계약자 정보 테이블 입력
    const {
      name,
      birth_date,
      gender,
      is_registed,
      status,
      reservation_date,
      contract_date,
      note,
      ...rest4
    } = rest3
    const contractorObj = await dispatch('createContractor', {
      contract: contPk,
      name,
      birth_date,
      gender,
      is_registed,
      status,
      reservation_date,
      contract_date,
      note,
    })

    // 5. 계약자 주소 테이블 입력
    const contractor = contractorObj.data.pk
    const {
      id_zipcode,
      id_address1,
      id_address2,
      id_address3,
      dm_zipcode,
      dm_address1,
      dm_address2,
      dm_address3,
      ...rest5
    } = rest4
    const addressObj = await dispatch('createAddress', {
      contractor,
      id_zipcode,
      id_address1,
      id_address2,
      id_address3,
      dm_zipcode,
      dm_address1,
      dm_address2,
      dm_address3,
    })

    // 6. 계약자 연락처 테이블 입력
    const { cell_phone, home_phone, other_phone, email, ...rest6 } = rest5
    const contactObj = await dispatch('createContact', {
      contractor,
      cell_phone,
      home_phone,
      other_phone,
      email,
    })

    // 7. 계약금 - 수납 정보 테이블 입력
    const proCashObj = await dispatch('proCash/createPrCashBook', rest6, {
      root: true,
    })

    return {
      contractObj,
      keyunitObj,
      houseunitObj,
      contractorObj,
      addressObj,
      contactObj,
      proCashObj,
    }
  },

  fetchSubsSummaryList: ({ commit }: any, project?: number) => {
    api
      .get(`/subs-sum/?project=${project}`)
      .then(res => {
        commit(FETCH_SUBS_SUMMARY_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchContSummaryList: ({ commit }: any, project?: number) => {
    api
      .get(`/cont-sum/?project=${project}`)
      .then(res => {
        commit(FETCH_CONT_SUMMARY_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchOrderGroupList: ({ commit }: any, pk?: number) => {
    api
      .get(`/order-group/?project=${pk}`)
      .then(res => {
        commit(FETCH_ORDER_GROUP_LIST, res.data)
      })
      .catch(err => console.log(err))
  },

  createOrderGroup: ({ dispatch }: any, payload: any) => {
    api
      .post(`/order-group/`, payload)
      .then(res => {
        dispatch('fetchOrderGroupList', res.data.project)
        message()
      })
      .catch(err => {
        console.log(err.response.data)
        alert(
          `${Object.keys(err.response.data)[0]} : ${
            err.response.data[Object.keys(err.response.data)[0]]
          }`,
        )
      })
  },

  updateOrderGroup: ({ dispatch }: any, payload: any) => {
    const { pk, ...formData } = payload
    api
      .put(`/order-group/${pk}/`, formData)
      .then(res => {
        dispatch('fetchOrderGroupList', res.data.project)
        message()
      })
      .catch(err => {
        console.log(err.response.data)
        alert(
          `${Object.keys(err.response.data)[0]} : ${
            err.response.data[Object.keys(err.response.data)[0]]
          }`,
        )
      })
  },

  deleteOrderGroup: ({ dispatch }: any, payload: any) => {
    const { pk, projId } = payload
    api
      .delete(`/order-group/${pk}/`)
      .then(() => {
        dispatch('fetchOrderGroupList', projId)
        message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.')
      })
      .catch(err => {
        alert(
          '해당 그룹에 종속된 계약관련 데이터가 있는 경우 이 그룹을 삭제할 수 없습니다.',
        )
        ;(router as any).go()
      })
  },

  fetchKeyUnitList: ({ commit }: any, payload?: any) => {
    const { project } = payload
    const unit_type = payload.unit_type ? payload.unit_type : ''
    api
      .get(
        `/key-unit/?project=${project}&unit_type=${unit_type}&no_contract=true`,
      )
      .then(res => {
        commit(FETCH_KEY_UNIT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },

  fetchHouseUnitList: ({ commit }: any, payload?: any) => {
    const { project } = payload
    const unit_type = payload.unit_type ? payload.unit_type : ''
    api
      .get(
        `/house-unit/?project=${project}&unit_type=${unit_type}&is_hold=false&no_keyunit=true`,
      )
      .then(res => {
        commit(FETCH_HOUSE_UNIT_LIST, res.data)
      })
      .catch(err => console.log(err.response.data))
  },
}

export default actions
