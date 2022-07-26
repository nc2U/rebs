<template>
  <div class="unit">
    <div
      class="unit-name"
      :class="{
        firstline: (isPiloti || unit) && line === 1,
        restline: (isPiloti || unit) && line !== 1,
        piloti: isPiloti,
      }"
      :style="`background-color: ${unit ? unit.color : ''}`"
    >
      <span v-if="unit">{{ unit.name }}</span>
    </div>

    <div
      class="status"
      :class="{
        firstline: unit && line === 1,
        restline: unit && line !== 1,
        firstPiloti: isPiloti && line === 1,
        restPiloti: isPiloti && line !== 1,
        piloti: isPiloti,
      }"
      :style="`background-color: ${statusColor};`"
    >
      <span v-if="unit && unit.key_unit && unit.key_unit.contract">
        <router-link
          :to="{
            name: '계약등록 관리',
            query: { contract: unit.key_unit.contract.pk },
          }"
        >
          {{ contractor }}
        </router-link>
      </span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Unit',
  props: { units: Array, floor: Number, line: Number },
  computed: {
    unit(this: any) {
      return this.units
        .filter((u: any) => u.line == this.line)
        .filter((u: any) => u.floor == this.floor)[0]
    },
    isPiloti(this: any) {
      return !this.unit && this.floor < 3
    },
    isContract() {
      return !!this.unit.key_unit?.contract
    },
    contractor() {
      return this.isContract ? this.unit.key_unit.contract.contractor.name : ''
    },
    status() {
      return this.isContract
        ? this.unit.key_unit.contract.contractor.status
        : ''
    },
    isHold() {
      return this.isContract ? this.unit.is_hold : ''
    },
    statusColor() {
      let color = ''
      if (this.unit && this.isContract) {
        if (this.status === '1') color = '#D5F1DE'
        if (this.status === '2') color = '#CBC7EC'
        if (this.isHold) color = '#555'
      }

      return color
    },
  },
})
</script>

<style lang="scss" scoped>
.unit {
  width: 40px;
  height: 40px;
  padding: 0;
  font-size: 10px;
  text-align: center;
  vertical-align: middle;
}

.unit-name {
  height: 20px;
  line-height: 20px;
  padding: 0;
}

.status {
  height: 20px;
  line-height: 20px;
  padding: 0;
}

.firstline {
  border-width: 1px 1px 0 1px;
  border-style: solid;
  border-color: #999;
}

.firstPiloti {
  border-width: 0 1px 0 1px;
  border-style: solid;
  border-color: #999;
}

.restline {
  border-width: 1px 1px 0 0;
  border-style: solid;
  border-color: #999;
}

.restPiloti {
  border-width: 0 1px 0 0;
  border-style: solid;
  border-color: #999;
}

.piloti {
  background-color: #ccc;
  border-color: #999;
}
</style>
