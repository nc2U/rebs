<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'

const activeKey = ref(1)

const updateActiveKey = (key: number) => {
  activeKey.value = key
}

const store = useStore()

const isDark = computed(() =>
  store.state.theme === 'dark' ? 'dark-theme' : 'bg-white',
)
const asideVisible = computed(() => store.state.asideVisible)
</script>

<template>
  <CSidebar
    color-scheme="light"
    self-hiding="xxl"
    size="lg"
    overlaid
    position="end"
    :visible="asideVisible"
    :class="isDark"
  >
    <CSidebarHeader class="bg-transparent p-0">
      <CNav variant="pills">
        <CNavItem>
          <CNavLink @click="updateActiveKey(1)">
            <CIcon icon="cil-List" alt="CoreUI Icons List" />
          </CNavLink>
        </CNavItem>
        <CNavItem>
          <CNavLink @click="updateActiveKey(2)">
            <CIcon icon="cil-speech" alt="CoreUI Icons Speech" />
          </CNavLink>
        </CNavItem>
        <CNavItem>
          <CNavLink @click="updateActiveKey(3)">
            <CIcon icon="cil-settings" alt="CoreUI Icons Settings" />
          </CNavLink>
        </CNavItem>
        <CNavItem class="ms-auto me-2 d-flex align-items-center">
          <CCloseButton @click="store.commit('toggleAside')" />
        </CNavItem>
      </CNav>
    </CSidebarHeader>
    <CTabContent>
      <CTabPane :visible="activeKey == 1">
        <CListGroup flush>
          <CListGroupItem
            class="list-group-item border-start-4 border-start-secondary bg-light text-center fw-bold text-medium-emphasis text-uppercase small"
          >
            Today
          </CListGroupItem>
          <CListGroupItem href="#" class="border-start-4 border-start-warning">
            <CAvatar :src="avatar7" size="lg" class="float-end" />
            <div>Meeting with <strong>Lucas</strong></div>
            <small class="text-medium-emphasis me-3">
              <CIcon icon="cil-calendar" />
              1 - 3pm
            </small>
            <small class="text-medium-emphasis">
              <CIcon icon="cil-location-pin" />
              Palo Alto, CA
            </small>
          </CListGroupItem>
          <CListGroupItem href="#" class="border-start-4 border-start-info">
            <CAvatar :src="avatar4" size="lg" class="float-end" />
            <div>Skype with <strong>Megan</strong></div>
            <small class="text-medium-emphasis me-3">
              <CIcon icon="cil-calendar" />
              4 - 5pm
            </small>
            <small class="text-medium-emphasis">
              <CIcon icon="cib-skype" />
              On-line
            </small>
          </CListGroupItem>
          <CListGroupItem
            class="border-start-4 border-start-secondary bg-light text-center fw-bold text-medium-emphasis text-uppercase small"
          >
            Tomorrow
          </CListGroupItem>
          <CListGroupItem
            accent="danger"
            href="#"
            class="border-start-4 border-start-danger"
          >
            <div>New UI Project - <strong>deadline</strong></div>
            <small class="text-medium-emphasis me-3">
              <CIcon icon="cil-calendar" />
              10 - 11pm
            </small>
            <small class="text-medium-emphasis">
              <CIcon icon="cil-home" />
              creativeLabs HQ
            </small>
            <div class="avatars-stack mt-2">
              <CAvatar :src="avatar2" size="sm" />
              <CAvatar :src="avatar3" size="sm" />
              <CAvatar :src="avatar4" size="sm" />
              <CAvatar :src="avatar5" size="sm" />
              <CAvatar :src="avatar6" size="sm" />
            </div>
          </CListGroupItem>
          <CListGroupItem href="#" class="border-start-4 border-start-success">
            <div><strong>#10 Startups.Garden</strong> Meetup</div>
            <small class="text-medium-emphasis me-3">
              <CIcon icon="cil-calendar" />
              1 - 3pm
            </small>
            <small class="text-medium-emphasis">
              <CIcon icon="cil-location-pin" />
              Palo Alto, CA
            </small>
          </CListGroupItem>
          <CListGroupItem
            href="#"
            class="border-start-4 border-start-primary border-bottom"
          >
            <div>
              <strong>Team meeting</strong>
            </div>
            <small class="text-medium-emphasis me-3">
              <CIcon icon="cil-calendar" />
              4 - 6pm
            </small>
            <small class="text-medium-emphasis">
              <CIcon icon="cil-home" />
              creativeLabs HQ
            </small>
            <div class="/avatars-stack mt-2">
              <CAvatar :src="avatar2" size="sm" />
              <CAvatar :src="avatar3" size="sm" />
              <CAvatar :src="avatar4" size="sm" />
              <CAvatar :src="avatar5" size="sm" />
              <CAvatar :src="avatar6" size="sm" />
              <CAvatar :src="avatar7" size="sm" />
              <CAvatar :src="avatar8" size="sm" />
            </div>
          </CListGroupItem>
        </CListGroup>
      </CTabPane>
      <CTabPane class="p-3" :visible="activeKey == 2">
        <div class="message">
          <div class="py-3 pb-5 me-3 float-start">
            <CAvatar :src="avatar7" status="success" size="md" />
          </div>
          <div>
            <small class="text-medium-emphasis">Lukasz Holeczek</small>
            <small class="text-medium-emphasis float-end mt-1">1:52 PM</small>
          </div>
          <div class="text-truncate fw-semibold">
            Lorem ipsum dolor sit amet
          </div>
          <small class="text-medium-emphasis">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
            eiusmod tempor incididunt...
          </small>
        </div>
        <hr />
        <div class="message">
          <div class="py-3 pb-5 me-3 float-start">
            <CAvatar :src="avatar7" status="success" size="md" />
          </div>
          <div>
            <small class="text-medium-emphasis">Lukasz Holeczek</small>
            <small class="text-medium-emphasis float-end mt-1">1:52 PM</small>
          </div>
          <div class="text-truncate fw-semibold">
            Lorem ipsum dolor sit amet
          </div>
          <small class="text-medium-emphasis">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
            eiusmod tempor incididunt...
          </small>
        </div>
        <hr />
        <div class="message">
          <div class="py-3 pb-5 me-3 float-start">
            <CAvatar :src="avatar7" status="success" size="md" />
          </div>
          <div>
            <small class="text-medium-emphasis">Lukasz Holeczek</small>
            <small class="text-medium-emphasis float-end mt-1">1:52 PM</small>
          </div>
          <div class="text-truncate fw-semibold">
            Lorem ipsum dolor sit amet
          </div>
          <small class="text-medium-emphasis">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
            eiusmod tempor incididunt...
          </small>
        </div>
        <hr />
        <div class="message">
          <div class="py-3 pb-5 me-3 float-start">
            <CAvatar :src="avatar7" status="success" size="md" />
          </div>
          <div>
            <small class="text-medium-emphasis">Lukasz Holeczek</small>
            <small class="text-medium-emphasis float-end mt-1">1:52 PM</small>
          </div>
          <div class="text-truncate fw-semibold">
            Lorem ipsum dolor sit amet
          </div>
          <small class="text-medium-emphasis">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
            eiusmod tempor incididunt...
          </small>
        </div>
        <hr />
        <div class="message">
          <div class="py-3 pb-5 me-3 float-start">
            <CAvatar :src="avatar7" status="success" size="md" />
          </div>
          <div>
            <small class="text-medium-emphasis">Lukasz Holeczek</small>
            <small class="text-medium-emphasis float-end mt-1">1:52 PM</small>
          </div>
          <div class="text-truncate fw-semibold">
            Lorem ipsum dolor sit amet
          </div>
          <small class="text-medium-emphasis">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
            eiusmod tempor incididunt...
          </small>
        </div>
      </CTabPane>
      <CTabPane class="p-3" :visible="activeKey == 3">
        <h6>Settings</h6>
        <div>
          <div class="clearfix mt-4">
            <CFormSwitch
              id="Option1"
              size="lg"
              label="Option 1"
              default-checked
            />
          </div>
          <div>
            <small class="text-medium-emphasis">
              Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </small>
          </div>
        </div>
        <div>
          <div class="clearfix mt-3">
            <CFormSwitch id="fOption2" size="lg" label="Option 2" />
          </div>
          <div>
            <small class="text-medium-emphasis">
              Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </small>
          </div>
        </div>
        <div>
          <div class="clearfix mt-3">
            <CFormSwitch id="Option3" size="lg" label="Option 3" />
          </div>
        </div>
        <div>
          <div class="clearfix mt-3">
            <CFormSwitch
              id="Option4"
              size="lg"
              label="Option 4"
              default-checked
            />
          </div>
        </div>
        <hr />
        <h6>System Utilization</h6>
        <div class="text-uppercase mb-1 mt-4">
          <small>
            <b>CPU Usage</b>
          </small>
        </div>
        <CProgress thin color="info-gradient" :value="25" />
        <small class="text-medium-emphasis">348 Processes. 1/4 Cores.</small>
        <div class="text-uppercase mb-1 mt-2">
          <small>
            <b>Memory Usage</b>
          </small>
        </div>
        <CProgress thin color="warning-gradient" :value="70" />
        <small class="text-medium-emphasis">11444GB/16384MB</small>
        <div class="text-uppercase mb-1 mt-2">
          <small>
            <b>SSD 1 Usage</b>
          </small>
        </div>
        <CProgress thin color="danger-gradient" :value="95" />
        <small class="text-medium-emphasis">243GB/256GB</small>
        <div class="text-uppercase mb-1 mt-2">
          <small>
            <b>SSD 2 Usage</b>
          </small>
        </div>
        <CProgress thin color="success-gradient" :value="10" />
        <small class="text-medium-emphasis">25GB/256GB</small>
      </CTabPane>
    </CTabContent>
  </CSidebar>
</template>
