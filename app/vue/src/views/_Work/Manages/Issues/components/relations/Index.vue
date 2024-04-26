<script lang="ts" setup>
import { type PropType, ref } from 'vue'
import { isValidate } from '@/utils/helper'
import { cutString } from '@/utils/baseMixins'
import type { IssueRelation } from '@/store/types/work'
import Multiselect from '@vueform/multiselect'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const props = defineProps({
  issuePk: { type: Number, required: true },
  addRIssue: { type: Boolean, default: false },
  relatedIssues: { type: Array as PropType<IssueRelation[]>, default: () => [] },
  getIssues: { type: Array as PropType<{ value: number; label: string }[]>, default: () => [] },
})

const emit = defineEmits(['add-rel-issue', 'add-form-ctl'])

const relIssue = ref<IssueRelation>({
  issue: props.issuePk,
  issue_to: null,
  relation_type: 'relates',
  delay: null,
})

const delRelRef = ref()
const validated = ref(false)

const addFormCtl = (bool: boolean) => emit('add-form-ctl', bool)

const addRelIssue = (event: Event) => {
  if (isValidate(event)) validated.value = true
  else emit('add-rel-issue', { ...relIssue.value })
  relIssue.value.issue_to = null
  relIssue.value.relation_type = 'relates'
  relIssue.value.delay = null
}

const relationUnLink = (pk: number) => {
  // child.value = pk
  delRelRef.value.callModal()
}

const unLinkRelConfirm = (pk: number) => {
  // workStore.updateIssueRelation(props.issue?.pk, { del_child: child.value })
  // child.value = null
  delRelRef.value.close()
}
</script>

<template>
  <div class="mt-2">
    <CRow v-for="rel in relatedIssues" :key="rel.pk">
      <CCol md="6">
        <span>{{ rel.type_display }} : </span>
        <span>
          <router-link :to="{ name: '(업무) - 보기', params: { issueId: rel.issue_to?.pk } }">
            기능 #{{ rel.issue_to?.pk }}
          </router-link>
          : {{ rel.issue_to?.subject }}
        </span>
      </CCol>
      <CCol class="col-sm-8 col-md-3 text-right">
        <span class="mr-3">{{ rel.issue_to?.status }}</span>
        <span v-if="rel.issue_to" class="mr-3">
          <router-link
            :to="{ name: '사용자 - 보기', params: { userId: rel.issue_to.assigned_to.pk } }"
          >
            {{ cutString(rel.issue_to.assigned_to.username, 9) }}
          </router-link>
        </span>
        <span class="mr-3">{{ rel.issue_to?.start_date }}</span>
      </CCol>
      <CCol class="col-sm-4 col-md-3 text-right">
        <span class="mr-3">
          <CProgress
            color="green-lighten-3"
            :value="rel.issue_to?.done_ratio"
            style="width: 100px; float: left; margin-top: 3px"
            height="14"
          />
        </span>
        <span class="mr-3" @click="relationUnLink(rel.issue_to?.pk as number)">
          <v-icon icon="mdi-link-variant-off" size="sm" color="grey" class="pointer" />
          <v-tooltip activator="parent" location="top"> 관계 지우기 </v-tooltip>
        </span>
        <span>
          <CDropdown color="secondary" variant="input-group" placement="bottom-end">
            <CDropdownToggle
              :caret="false"
              color="light"
              variant="ghost"
              size="sm"
              shape="rounded-pill"
            >
              <v-icon icon="mdi-dots-horizontal" class="pointer" color="grey-darken-1" />
              <v-tooltip activator="parent" location="top">Actions</v-tooltip>
            </CDropdownToggle>
            <CDropdownMenu>
              <CDropdownItem
                class="form-text"
                @click="
                  $router.push({
                    name: '(업무) - 보기',
                    params: { issueId: rel.issue_to?.pk },
                    query: { edit: '1' },
                  })
                "
              >
                <router-link to="">
                  <v-icon icon="mdi-pencil" color="amber" size="sm" />
                  편집
                </router-link>
              </CDropdownItem>
              <CDropdownItem class="form-text" disabled>
                <!--                    <router-link to="">-->
                <v-icon color="amber" size="sm" />
                유형
                <!--                    </router-link>-->
              </CDropdownItem>
              <CDropdownItem class="form-text" disabled>
                <v-icon color="amber" size="sm" />
                <!--                    <router-link to=""> -->
                우선순위
                <!--                    </router-link>-->
              </CDropdownItem>
              <CDropdownItem class="form-text" disabled>
                <v-icon color="amber" size="sm" />
                <!--                    <router-link to=""> -->
                담당자
                <!--                    </router-link>-->
              </CDropdownItem>
              <CDropdownItem class="form-text" disabled>
                <v-icon color="amber" size="sm" />
                <!--                    <router-link to=""> -->
                진척도
                <!--                    </router-link>-->
              </CDropdownItem>
              <CDropdownItem class="form-text" disabled>
                <!--                    <router-link to="">-->
                <v-icon icon="mdi-star" color="secondary" size="sm" />
                지켜보기
                <!--                    </router-link>-->
              </CDropdownItem>
              <CDropdownItem class="form-text" disabled>
                <!--                    <router-link to="">-->
                <v-icon icon="mdi-timer-edit-outline" color="grey" size="sm" />
                작업시간 기록
                <!--                    </router-link>-->
              </CDropdownItem>
              <CDropdownItem class="form-text" disabled>
                <!--                    <router-link to="">-->
                <v-icon icon="mdi-link-plus" color="grey" size="sm" />
                링크 복사
                <!--                    </router-link>-->
              </CDropdownItem>
              <CDropdownItem class="form-text" disabled>
                <!--                    <router-link to="">-->
                <v-icon icon="mdi-content-copy" color="grey" size="sm" />
                복사
                <!--                    </router-link>-->
              </CDropdownItem>
              <CDropdownItem class="form-text" disabled>
                <!--                    <router-link to="">-->
                <v-icon icon="mdi-trash-can-outline" color="grey" size="sm" />
                업무 삭제
                <!--                    </router-link>-->
              </CDropdownItem>
            </CDropdownMenu>
          </CDropdown>
        </span>
      </CCol>
    </CRow>

    <CForm class="needs-validation" novalidate :validated="validated" @submit.prevent="addRelIssue">
      <CRow v-if="addRIssue">
        <CCol sm="4" md="3" lg="2">
          <CFormSelect v-model="relIssue.relation_type">
            <option value="relates">다음 업무와 관련됨 :</option>
            <option value="duplicates">다음 업무에 중복됨 :</option>
            <option value="duplicated">중복된 업무 :</option>
            <option value="blocks">다음 업무의 해결을 막고 있음 :</option>
            <option value="blocked">다음 업무에게 막혀 있음 :</option>
            <option value="precedes">다음에 진행할 업무 :</option>
            <option value="follows">다음 업무를 우선 진행 :</option>
            <option value="copied_to">다음 업무로 복사됨 :</option>
            <option value="copied_from">다음 업무로부터 복사됨 :</option>
          </CFormSelect>
        </CCol>
        <CFormLabel for="colFormLabel" class="col-sm-1 col-form-label text-right">
          업무 #
        </CFormLabel>
        <CCol sm="4" md="3" lg="2">
          <Multiselect
            v-model="relIssue.issue_to"
            :options="getIssues"
            :classes="{
              caret: 'multiselect-caret mr-4',
              search: 'form-control multiselect-search',
              tagsSearch: 'form-control multiselect-tags-search',
            }"
            :attrs="relIssue.issue_to ? {} : { required: true }"
            placeholder="업무 검색"
            :add-option-on="['enter', 'tab']"
            searchable
          />
        </CCol>
        <template
          v-if="relIssue.relation_type === 'precedes' || relIssue.relation_type === 'follows'"
        >
          <CFormLabel for="colFormLabel" class="col-sm-1 col-form-label text-right">
            지연 :
          </CFormLabel>
          <CCol sm="3" md="2" lg="1">
            <CFormInput v-model="relIssue.delay" />
          </CCol>
          <CFormLabel class="col-sm-1 col-form-label"> 일</CFormLabel>
        </template>
        <CCol class="pt-1">
          <CButton type="submit" color="primary" size="sm">추가</CButton>
          <CButton color="light" size="sm" @click="addFormCtl(false)">취소</CButton>
        </CCol>
      </CRow>
    </CForm>
  </div>

  <ConfirmModal ref="delRelRef">
    <template #header>관계 지우기 확인</template>
    <template #default> 계속 진행하시겠습니까?</template>
    <template #footer>
      <CButton color="warning" @click="unLinkRelConfirm">확인</CButton>
    </template>
  </ConfirmModal>
</template>
