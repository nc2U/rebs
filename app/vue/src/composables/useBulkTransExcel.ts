import { ref } from 'vue'
import ExcelJS from 'exceljs'
import {
  CODE_TO_EVIDENCE_MAP,
  EVIDENCE_TYPE_MAP,
  extractCellNumber,
  extractCellValue,
} from '@/composables/useExcelUpload'

/**
 * 다수 은행거래 + 회계 계정 대량 입력용 엑셀 템플릿 / 파서
 *
 * 시트 구조: 1행 = 회계 계정 1건. 같은 '그룹번호'가 연속된 행은 하나의 은행거래로 묶이며,
 * 은행거래 정보(거래일자~입출금액)는 그룹의 첫 행 값을 사용한다.
 */

interface Option {
  value: number | null | undefined
  label: string
}

export type BulkSystemType = 'project' | 'company'

export interface BulkParseOptions {
  bankAccounts: Option[]
  accounts: Array<{ value: number; label: string; is_cate_only?: boolean }>
  // 프로젝트: 계약자 후보 / 본사: 관계회사(프로젝트) 후보
  contracts: Array<{ value: number; label: string }>
  systemType?: BulkSystemType
}

// 시스템별 '연관 대상' 열 이름 (프로젝트=계약자, 본사=관계회사(프로젝트))
export const relatedLabelOf = (t: BulkSystemType = 'project') =>
  t === 'project' ? '계약자' : '관계회사(프로젝트)'

export interface BulkEntry {
  rowNumber: number
  account: number | null
  account_name: string
  trader: string
  amount: number
  evidence_type: '' | '0' | '1' | '2' | '3' | '4' | '5' | '6'
  contract: number | null // 프로젝트: 계약자 ID / 본사: 관계회사(affiliate) ID
  contract_name: string
  errors: string[]
  warnings: string[]
}

export interface BulkTransaction {
  key: string
  firstRow: number
  bankForm: {
    deal_date: string
    bank_account: number | null | ''
    bank_account_name: string
    sort: 1 | 2
    amount: number | null
    content: string
    note: string
  }
  entries: BulkEntry[]
  entryTotal: number
  isBalanced: boolean
  errors: string[]
  warnings: string[]
  isValid: boolean
}

export interface BulkParseResult {
  transactions: BulkTransaction[]
  summary: {
    transactionCount: number
    validTransactions: number
    invalidTransactions: number
    entryCount: number
  }
  isValid: boolean
}

export const BULK_COLUMNS = [
  // 화면 폼(거래일자 → 메모 → 거래계좌 → 적요 → 입출금액 → 계정 → 거래처 → 분류금액 → 지출증빙) 순서와 동일
  { header: '그룹번호', key: 'key', width: 12 },
  { header: '거래일자', key: 'deal_date', width: 14 },
  { header: '메모', key: 'note', width: 20 },
  { header: '거래계좌', key: 'bank_account', width: 22 },
  { header: '적요', key: 'content', width: 30 },
  { header: '구분(입금/출금)', key: 'sort', width: 16 },
  { header: '입출금액', key: 'amount', width: 16 },
  { header: '계정이름', key: 'account_name', width: 25 },
  { header: '__RELATED__', key: 'contract_name', width: 22 },
  { header: '거래처', key: 'trader', width: 25 },
  { header: '분류금액', key: 'entry_amount', width: 16 },
  { header: '지출증빙', key: 'evidence_type', width: 22 },
] as const

const SORT_MAP: Record<string, 1 | 2> = { 입금: 1, 출금: 2, '1': 1, '2': 2 }

// 엑셀 셀 값(Date/문자열/숫자)을 YYYY-MM-DD 로 정규화
const normalizeDate = (cell: ExcelJS.Cell): string => {
  const val = cell.value
  if (val instanceof Date) {
    // ExcelJS 는 날짜를 UTC 기준으로 반환하므로 UTC 요소를 사용
    const y = val.getUTCFullYear()
    const m = String(val.getUTCMonth() + 1).padStart(2, '0')
    const d = String(val.getUTCDate()).padStart(2, '0')
    return `${y}-${m}-${d}`
  }
  const str = extractCellValue(cell)
  const digits = str.replace(/[.\-/\s]/g, '')
  if (/^\d{8}$/.test(digits)) {
    return `${digits.slice(0, 4)}-${digits.slice(4, 6)}-${digits.slice(6, 8)}`
  }
  const m = str.match(/^(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})$/)
  if (m) return `${m[1]}-${m[2].padStart(2, '0')}-${m[3].padStart(2, '0')}`
  return str
}

const isValidDate = (s: string) => {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return false
  const d = new Date(`${s}T00:00:00Z`)
  return !isNaN(d.getTime()) && d.toISOString().slice(0, 10) === s
}

export function useBulkTransExcel() {
  const isParsing = ref(false)

  /** 대량 입력 템플릿 다운로드 (예시 행 + 작성안내/참조목록 시트 포함) */
  const downloadBulkTemplate = async (ref_: {
    bankAccounts: Option[]
    accounts: Array<{ label: string; is_cate_only?: boolean }>
    systemType?: BulkSystemType
  }) => {
    const workbook = new ExcelJS.Workbook()
    const ws = workbook.addWorksheet('거래내역 대량입력')
    const relatedLabel = relatedLabelOf(ref_.systemType)
    ws.columns = BULK_COLUMNS.map(c => ({
      ...c,
      header: c.header === '__RELATED__' ? relatedLabel : c.header,
    }))

    const header = ws.getRow(1)
    header.font = { bold: true }
    header.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFE0E0E0' } }

    const firstBank = ref_.bankAccounts.find(b => b.value)?.label || '(거래계좌명)'
    const accounts = ref_.accounts.filter(a => !a.is_cate_only)
    const accA = accounts[0]?.label || '(계정이름)'
    const accB = accounts[1]?.label || accA

    // 예시: 1번 거래는 분류 2건, 2번 거래는 분류 1건
    // 열 순서: 그룹번호, 거래일자, 메모, 거래계좌, 적요, 구분, 입출금액, 계정이름, 계약자, 거래처, 분류금액, 지출증빙
    ws.addRow([1, '2026-01-15', '', firstBank, '예시 적요', '출금', 1500000, accA, '', '거래처A', 1000000, '증빙없음'])
    ws.addRow([1, '', '', '', '', '', '', accB, '', '거래처B', 500000, '세금계산서'])
    ws.addRow([2, '2026-01-16', '', firstBank, '예시 입금', '입금', 300000, accA, '', '거래처C', 300000, ''])
    ws.getColumn('deal_date').numFmt = '@'

    const guide = workbook.addWorksheet('작성안내')
    guide.columns = [{ width: 100 }]
    ;[
      '■ 작성 방법',
      '1. 1행 = 회계 계정(분류) 1건입니다. 시트 첫 번째 탭("거래내역 대량입력")에 입력하세요.',
      '2. [그룹번호]는 같은 은행거래에 속하는 행을 묶기 위한 엑셀 내 번호입니다. DB의 거래 번호(pk)가 아니며 저장되지 않습니다.',
      '   - 같은 그룹번호가 연속된 행은 하나의 은행거래로 묶입니다. (1, 2, 3 또는 A, B 등 아무 값이나 가능)',
      '   - 그룹번호를 비워 두면, 거래일자/거래계좌/적요/구분/입출금액 중 하나라도 입력된 행부터 새 은행거래로 인식합니다.',
      '3. 은행거래 정보(거래일자, 메모, 거래계좌, 적요, 구분, 입출금액)는 그룹의 첫 번째 행에만 입력하세요.',
      '4. 같은 그룹의 분류금액 합계는 입출금액과 반드시 일치해야 합니다.',
      '5. 거래일자는 YYYY-MM-DD 형식, 구분은 "입금" 또는 "출금"으로 입력하세요.',
      '6. 거래계좌/계정이름/' + relatedLabel + '은(는) 시스템에 등록된 이름과 정확히 일치해야 합니다. (참조목록 시트 확인)',
      '7. 지출증빙: ' + Object.keys(EVIDENCE_TYPE_MAP).join(', '),
      '8. 예시 행(1~3번 거래)은 삭제하고 입력하세요.',
    ].forEach(t => guide.addRow([t]))
    guide.getRow(1).font = { bold: true }

    const refSheet = workbook.addWorksheet('참조목록')
    refSheet.columns = [
      { header: '거래계좌', key: 'bank', width: 30 },
      { header: '계정이름', key: 'acc', width: 30 },
    ]
    refSheet.getRow(1).font = { bold: true }
    const bankNames = ref_.bankAccounts.filter(b => b.value).map(b => b.label)
    const rows = Math.max(bankNames.length, accounts.length)
    for (let i = 0; i < rows; i++) {
      refSheet.addRow({ bank: bankNames[i] || '', acc: accounts[i]?.label || '' })
    }

    const buffer = await workbook.xlsx.writeBuffer()
    const blob = new Blob([buffer], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `거래내역_대량입력_템플릿_${new Date().getTime()}.xlsx`
    link.click()
    URL.revokeObjectURL(url)
  }

  /** 대량 입력 엑셀 파싱 + 검증 */
  const parseBulkFile = async (file: File, opts: BulkParseOptions): Promise<BulkParseResult> => {
    isParsing.value = true
    try {
      const workbook = new ExcelJS.Workbook()
      await workbook.xlsx.load(await file.arrayBuffer())
      const ws = workbook.worksheets[0]
      if (!ws) throw new Error('엑셀 파일에 워크시트가 없습니다.')

      const transactions: BulkTransaction[] = []
      let current: BulkTransaction | null = null
      let lastKey = ''

      for (let i = 2; i <= ws.rowCount; i++) {
        const row = ws.getRow(i)
        // 열 순서: 그룹번호, 거래일자, 메모, 거래계좌, 적요, 구분, 입출금액, 계정이름, 계약자, 거래처, 분류금액, 지출증빙
        const key = extractCellValue(row.getCell(1))
        const dealDate = normalizeDate(row.getCell(2))
        const note = extractCellValue(row.getCell(3))
        const bankName = extractCellValue(row.getCell(4))
        const content = extractCellValue(row.getCell(5))
        const sortRaw = extractCellValue(row.getCell(6))
        const bankAmount = extractCellNumber(row.getCell(7))
        const accountName = extractCellValue(row.getCell(8))
        const contractName = extractCellValue(row.getCell(9))
        const trader = extractCellValue(row.getCell(10))
        const entryAmount = extractCellNumber(row.getCell(11))
        const rawEvidence = extractCellValue(row.getCell(12))

        // 빈 행 건너뛰기
        if (
          !key && !dealDate && !bankName && !sortRaw && !content && !note && !bankAmount &&
          !accountName && !trader && !entryAmount && !rawEvidence && !contractName
        ) {
          continue
        }

        // 새 그룹 시작: 그룹번호가 바뀌었거나, 그룹번호가 비어 있으면서 은행거래 정보가 입력된 경우
        const hasBankInfo = !!(dealDate || bankName || sortRaw || content || bankAmount)
        const startsNew = !current || (key ? key !== lastKey : hasBankInfo)

        if (startsNew) {
          const sort = SORT_MAP[sortRaw]
          const bank = opts.bankAccounts.find(b => b.value && b.label === bankName)
          current = {
            key: key || `행${i}`,
            firstRow: i,
            bankForm: {
              deal_date: dealDate,
              bank_account: bank?.value ?? '',
              bank_account_name: bankName,
              sort: sort ?? 2,
              amount: bankAmount || null,
              content,
              note,
            },
            entries: [],
            entryTotal: 0,
            isBalanced: false,
            errors: [],
            warnings: [],
            isValid: true,
          }
          if (!isValidDate(dealDate)) current.errors.push(`거래일자 '${dealDate}' 형식이 올바르지 않습니다. (YYYY-MM-DD)`)
          if (!bank) current.errors.push(`거래계좌 '${bankName}'을(를) 찾을 수 없습니다.`)
          if (!sort) current.errors.push(`구분 '${sortRaw}'은(는) 입금/출금이어야 합니다.`)
          if (!bankAmount || bankAmount <= 0) current.errors.push('입출금액은 0보다 큰 숫자여야 합니다.')
          if (!content) current.errors.push('적요는 필수 입력 항목입니다.')
          transactions.push(current)
          lastKey = key || current.key
        } else if (current && hasBankInfo) {
          current.warnings.push(`행 ${i}: 같은 그룹번호의 두 번째 이후 행에 입력된 은행거래 정보는 무시됩니다.`)
        }

        // 분류 항목
        const entry: BulkEntry = {
          rowNumber: i,
          account: null,
          account_name: accountName,
          trader,
          amount: entryAmount,
          evidence_type: '',
          contract: null,
          contract_name: contractName,
          errors: [],
          warnings: [],
        }

        const acc = opts.accounts.find(a => !a.is_cate_only && a.label === accountName)
        if (!acc) entry.errors.push(`계정명 '${accountName}'을(를) 찾을 수 없습니다.`)
        else entry.account = acc.value

        if (isNaN(entryAmount) || entryAmount <= 0) entry.errors.push('분류금액은 0보다 큰 숫자여야 합니다.')

        let code = EVIDENCE_TYPE_MAP[rawEvidence]
        if (!code && CODE_TO_EVIDENCE_MAP[rawEvidence]) code = rawEvidence
        if (rawEvidence && !code) entry.errors.push(`지출증빙 '${rawEvidence}'은(는) 유효하지 않습니다.`)
        else entry.evidence_type = (code || '') as BulkEntry['evidence_type']

        if (contractName) {
          const c = opts.contracts.find(o => o.label.includes(contractName))
          if (c) entry.contract = c.value
          else
            entry.warnings.push(
              `${relatedLabelOf(opts.systemType)} '${contractName}'을(를) 찾을 수 없음 - 업로드 후 선택 필요`,
            )
        }

        current!.entries.push(entry)
      }

      // 그룹별 합계/검증 집계
      for (const t of transactions) {
        t.entryTotal = t.entries.reduce((s, e) => s + (e.amount > 0 ? e.amount : 0), 0)
        t.isBalanced = !!t.bankForm.amount && Math.abs(t.entryTotal - t.bankForm.amount) < 0.01
        if (!t.isBalanced) {
          t.errors.push(
            `거래 금액(${(t.bankForm.amount ?? 0).toLocaleString()})과 분류 금액 합계(${t.entryTotal.toLocaleString()})가 일치하지 않습니다.`,
          )
        }
        t.isValid = t.errors.length === 0 && t.entries.every(e => e.errors.length === 0)
      }

      const validTransactions = transactions.filter(t => t.isValid).length
      return {
        transactions,
        summary: {
          transactionCount: transactions.length,
          validTransactions,
          invalidTransactions: transactions.length - validTransactions,
          entryCount: transactions.reduce((s, t) => s + t.entries.length, 0),
        },
        isValid: transactions.length > 0 && validTransactions === transactions.length,
      }
    } finally {
      isParsing.value = false
    }
  }

  return { isParsing, downloadBulkTemplate, parseBulkFile }
}
