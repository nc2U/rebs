export interface ProjectAccountD1 {
  sort: string
  sort_desc: string
  name: string
  description: string
}

export interface ProjectAccountD2 {
  d1: ProjectAccountD1
  code: string
  sub_title: string
  name: string
  description: string
}

export interface ProjectCashState {
  d1: ProjectAccountD1
  d2: ProjectAccountD2
  d1List: ProjectAccountD1[]
  d2List: ProjectAccountD2[]
}

const state = {
  d1: null,
  d2: null,
  d1List: [],
  d2List: [],
}

export default state
