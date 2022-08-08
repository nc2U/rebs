<script lang="ts" setup>
const emit = defineEmits(['weekends-toggle'])
defineProps({
  calendarOptions: { type: Object, default: Function },
  currentEvents: { type: Array, default: Function },
})
</script>

<template>
  <CCol md="3" class="d-none d-md-block">
    <div class="demo-app-sidebar">
      <div class="demo-app-sidebar-section">
        <h2>
          <v-icon
            icon="mdi-alpha-i-circle"
            size="small"
            class="mr-2"
            color="indigo"
          />
          Instructions
        </h2>
        <ul>
          <li>날짜를 선택하면 새 이벤트를 생성하라는 메시지가 표시됩니다.</li>
          <li>드래그, 드롭 및 크기 조정 이벤트</li>
          <li>이벤트를 삭제하려면 클릭하세요.</li>
        </ul>
      </div>
      <div class="demo-app-sidebar-section">
        <label>
          <input
            type="checkbox"
            :checked="calendarOptions.weekends"
            @change="emit('weekends-toggle')"
          />
          주말 표시 여부
        </label>
      </div>
      <div class="demo-app-sidebar-section">
        <h2>월간 진행 일정 목록 ({{ currentEvents.length }})</h2>
        <ul>
          <li v-for="event in currentEvents" :key="event.id">
            <b>{{ event.start }}</b>
            <i class="ml-2">{{ event.title }}</i>
          </li>
        </ul>
      </div>
    </div>
  </CCol>
</template>

<style lang="scss" scoped>
h2 {
  margin: 0;
  font-size: 16px;
}

ul {
  margin: 0;
  padding: 0 0 0 1.5em;
}

li {
  margin: 1.5em 0;
  padding: 0;
}

b {
  /* used for event dates/times */
  margin-right: 3px;
}

.demo-app {
  //display: flex;
  min-height: 100%;
  width: 100%;
  font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
  font-size: 14px;
}

.demo-app-sidebar {
  width: 300px;
  line-height: 1.2;
  background: #eaf9ff;
  border-right: 1px solid #d3e2e8;
}

.demo-app-sidebar-section {
  padding: 2em;
}

.demo-app-main {
  flex-grow: 1;
  padding: 3em;
}

.fc {
  /* the calendar root */
  max-width: 1100px;
  margin: 0 auto;
}
</style>
