export interface BankApiCredential {
  pk: number
  company_bank_account: number | null
  project_bank_account: number | null
  account_alias: string
  is_project: boolean
  company_id?: number | null
  company_name?: string | null
  project_id?: number | null
  project_name?: string | null
  is_imprest?: boolean
  directpay?: boolean
  auth_type?: 'cert' | 'fast'
  fast_business_number?: string
  connected_id: string
  bank_code: string
  account_number: string
  is_active: boolean
  last_scraped_at: string | null
  last_status: 'ready' | 'success' | 'error'
  last_error_message: string
  created_at: string
  updated_at: string
}

export interface RegisterFastAccountPayload {
  bank_code: string
  account_number: string
  business_number: string
  account_password: string
  target_type: 'project' | 'company'
  project_id?: number | null
  company_id?: number | null
  existing_account_id?: number | null
  alias_name?: string
  holder?: string
  is_imprest?: boolean
}

export interface RawBankTransaction {
  pk: number
  credential: number
  account_alias: string
  bank_code: string
  account_number: string
  is_project: boolean
  company_id?: number | null
  company_name?: string | null
  project_id?: number | null
  project_name?: string | null
  is_imprest?: boolean
  directpay?: boolean
  deal_date: string
  deal_time: string | null
  sort_type: 'deposit' | 'withdraw'
  amount: number
  balance: number | null
  client_name: string
  content: string
  branch_name: string
  status: 'pending' | 'ready' | 'confirmed' | 'ignored'
  confidence_score: number
  ai_reason: string
  suggested_company_account: number | null
  suggested_company_account_name: string | null
  suggested_project_account: number | null
  suggested_project_account_name: string | null
  suggested_contract: number | null
  suggested_contract_name: string | null
  confirmed_by: number | null
  confirmed_by_name: string | null
  confirmed_at: string | null
  created_company_transaction: number | null
  created_project_transaction: number | null
  created_at: string
  updated_at: string
}

export interface RawTransactionFilter {
  page?: number
  credential?: number | null
  company?: number | null
  project?: number | null
  is_imprest?: boolean | string
  status?: string
  deal_date?: string
  sort_type?: string
  search?: string
}

export interface BankDiscoveredAccount {
  account_number: string
  account_name: string
  holder: string
  balance: number | null
  matched_type: 'company' | 'project' | null
  matched_account_id: number | null
  matched_account_alias: string | null
  company_id: number | null
  project_id: number | null
  is_imprest: boolean
  is_already_registered: boolean
}

export interface RegisterCertificateResponse {
  connected_id: string
  bank_code: string
  accounts: BankDiscoveredAccount[]
}

export interface BatchLinkAccountItem {
  account_number: string
  account_name?: string
  holder?: string
  target_type: 'company' | 'project'
  company_id?: number | null
  project_id?: number | null
  is_imprest?: boolean
  existing_account_id?: number | null
  alias_name?: string
}

