import { App } from 'vue'
import { CPagination } from './CPagination'
import { CPaginationItem } from './CPaginationItem'
import { CSmartPagination } from './CSmartPagination'

const CPaginationPlugin = {
  install: (app: App): void => {
    app.component(CPagination.name, CPagination)
    app.component(CPaginationItem.name, CPaginationItem)
    app.component(CSmartPagination.name, CSmartPagination)
  },
}

export { CPaginationPlugin, CPagination, CPaginationItem, CSmartPagination }
