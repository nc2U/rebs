<script setup lang="ts">
import { type PropType, ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  visibilityHeight: { type: Number as PropType<number>, default: 400 },
  backPosition: { type: Number, default: 0 },
  customStyle: {
    type: Object,
    default: () => ({
      right: '50px',
      bottom: '50px',
      width: '46px',
      height: '46px',
      'border-radius': '50%',
      'line-height': '46px', // Please keep consistent with height to center vertically
      background: 'rgba( 255, 255, 255, 0.3 )',
      boxShadow: '0 10px 35px rgba(0, 0, 0, 0.05), 0 2px 2px rgba(0, 0, 0, 0.1)',
    }),
  },
  transitionName: {
    type: String as PropType<string>,
    default: 'fade',
  },
})

const visible = ref(false)
const interval = ref<any>()
const isMoving = ref(false)

const handleScroll = () => (visible.value = window.scrollY > props.visibilityHeight)

const backToTop = () => {
  if (isMoving.value) return
  const start = window.scrollY
  let i = 0
  isMoving.value = true
  interval.value = setInterval(() => {
    const next = Math.floor(easeInOutQuad(10 * i, start, -start, 10))
    if (next <= props.backPosition) {
      window.scrollTo(0, props.backPosition as number)
      clearInterval(interval.value)
      isMoving.value = false
    } else {
      window.scrollTo(0, next)
    }
    i++
  }, 100)
}

const easeInOutQuad = (t: number, b: number, c: number, d: number) => {
  if ((t /= d / 2) < 1) return (c / 2) * t * t + b
  return (-c / 2) * (--t * (t - 2) - 1) + b
}

onMounted(() => window.addEventListener('scroll', handleScroll))

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
  if (interval.value) clearInterval(interval.value)
})
</script>

<template>
  <transition :name="transitionName">
    <div v-show="visible" :style="customStyle" class="back-to-ceiling" @click="backToTop">
      <svg
        width="16"
        height="16"
        viewBox="0 0 17 17"
        xmlns="http://www.w3.org/2000/svg"
        class="Icon Icon--backToTopArrow"
        aria-hidden="true"
        style="height: 16px; width: 16px"
      >
        <path
          d="M12.036 15.59a1 1 0 0 1-.997.995H5.032a.996.996 0 0 1-.997-.996V8.584H1.03c-1.1 0-1.36-.633-.578-1.416L7.33.29a1.003 1.003 0 0 1 1.412 0l6.878 6.88c.782.78.523 1.415-.58 1.415h-3.004v7.004z"
        />
      </svg>
    </div>
  </transition>
</template>

<style scoped>
.back-to-ceiling {
  position: fixed;
  display: inline-block;
  text-align: center;
  cursor: pointer;
}

.back-to-ceiling:hover {
  background: #d5dbe7;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.back-to-ceiling .Icon {
  fill: #9aaabf;
  background: none;
}
</style>
