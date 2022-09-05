import { State } from '@/store'
import { User, LockedUser, Todo } from '@/store/types/accounts'

export declare interface AccountsState extends State {
  accessToken: string
  userInfo: User | null
  lockedUser: LockedUser | null
  todoList: Todo[]
}

const state: AccountsState = {
  accessToken: '',
  userInfo: null,
  lockedUser: null,
  todoList: [],
}

export default state
