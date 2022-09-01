import { App } from 'vue'
import { CMultiSelect } from './CMultiSelect'

const CMultiSelectPlugin = {
  install: (app: App): void => {
    app.component(CMultiSelect.name, CMultiSelect)
  },
}

export { CMultiSelectPlugin, CMultiSelect }
