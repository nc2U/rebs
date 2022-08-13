<template>
  <div
    id="layer"
    ref="element_layer"
    :style="{
      display: displayVal,
      width: widthVal,
      height: heightVal,
      border: borderVal,
      left: leftVal,
      top: topVal,
    }"
  >
    <img
      id="btnCloseLayer"
      src="//t1.daumcdn.net/postcode/resource/images/close.png"
      alt="닫기 버튼"
      @click="closeLayer"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import store from '@/store'

export default defineComponent({
  name: 'DaumPostcode',
  props: {
    width: {
      type: Number,
      default: 450,
    },
    height: {
      type: Number,
      default: 415,
    },
    borderWidth: {
      type: Number,
      default: 5,
    },
    autoClose: {
      type: Boolean,
      default: false,
    },
    autoResize: {
      type: Boolean,
      default: false,
    },
    animation: {
      type: Boolean,
      default: false,
    },
    autoMapping: {
      type: Boolean,
      default: true,
    },
    shorthand: {
      type: Boolean,
      default: true,
    },
    pleaseReadGuide: {
      type: Number,
      default: 0,
    },
    pleaseReadGuideTimer: {
      type: Number,
      default: 1.5,
    },
    maxSuggestItems: {
      type: Number,
      default: 8,
    },
    showMoreHName: {
      type: Boolean,
      default: false,
    },
    hideMapBtn: {
      type: Boolean,
      default: false,
    },
    hideEngBtn: {
      type: Boolean,
      default: false,
    },
    alwaysShowEngAddr: {
      type: Boolean,
      default: false,
    },
    submitMode: {
      type: Boolean,
      default: true,
    },
    useSuggest: {
      type: Boolean,
      default: true,
    },
    componentStyle: {
      type: Object,
      default: null,
    },
    defaultQuery: {
      type: String,
      default: null,
    },
    scriptUrl: {
      type: String,
      default: '//t1.daumcdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js',
    },
  },
  emits: ['address-put'],
  data() {
    return {
      displayVal: 'none',
    }
  },
  computed: {
    widthVal() {
      return this.width + 'px'
    },
    heightVal() {
      return this.height + 'px'
    },
    borderVal() {
      return this.borderWidth + 'px solid'
    },
    leftVal() {
      return (
        ((window.innerWidth || document.documentElement.clientWidth) -
          this.width) /
          2 -
        this.borderWidth +
        'px'
      )
    },
    topVal() {
      return (
        ((window.innerHeight || document.documentElement.clientHeight) -
          this.height) /
          2 -
        this.borderWidth +
        'px'
      )
    },
    theme() {
      if (store.state.theme === 'dark') {
        return {
          searchBgColor: '#2A2B36', //검색창 배경색
          queryTextColor: '#FFFFFF', //검색창 글자색
        }
      } else {
        return null
      }
    },
  },
  mounted: function () {
    const scriptId = 'daum_postcode_script'
    const isExist = !!document.getElementById(scriptId)
    if (!isExist) {
      const script = document.createElement('script')
      script.src = this.scriptUrl
      script.id = scriptId
      document.body.appendChild(script)
    }
  },
  methods: {
    initiate(formNum = 1) {
      // eslint-disable-next-line @typescript-eslint/no-this-alias
      const vm: any = this
      ;(window as any).daum.postcode.load(() => {
        new (window as any).daum.Postcode({
          oncomplete: function oncomplete(data: any) {
            vm.$emit('address-put', { ...{ formNum }, ...data })
            vm.displayVal = 'none'
          },
          alwaysShowEngAddr: vm.alwaysShowEngAddr,
          animation: vm.animation,
          autoMapping: vm.autoMapping,
          autoResize: vm.autoResize,
          hideEngBtn: vm.hideEngBtn,
          hideMapBtn: vm.hideMapBtn,
          maxSuggestItems: vm.maxSuggestItems,
          pleaseReadGuide: vm.pleaseReadGuide,
          pleaseReadGuideTimer: vm.pleaseReadGuideTimer,
          shorthand: vm.shorthand,
          showMoreHName: vm.showMoreHName,
          submitMode: vm.submitMode,
          theme: vm.theme,
          useSuggest: vm.useSuggest,
          width: '100%',
          height: '100%',
        }).embed(vm.$refs.element_layer)

        // iframe을 넣은 element를 보이게 한다.
        vm.displayVal = 'block'
      })
    },
    closeLayer() {
      this.displayVal = 'none'
    },
  },
})
</script>

<style lang="scss" scoped>
#layer {
  position: fixed;
  overflow: hidden;
  z-index: 100;
  -webkit-overflow-scrolling: touch;
}

#btnCloseLayer {
  cursor: pointer;
  position: absolute;
  right: -3px;
  top: -3px;
  z-index: 100;
}
</style>
