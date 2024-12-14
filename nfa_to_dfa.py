from collections import deque

class nfa:
    #states, alphabet은 리스트 데이터형
    # start_states, final_states은 집합 데이터형
    #delta는 전이함수로 딕셔너리 데이터형
    def __init__(self, states, alphabet, delta, start_state, final_states):
        self.states = states
        self.alphabet = [str(symbol) for symbol in alphabet]
        self.delta = {
        (state, str(symbol)): {str(next_state) for next_state in next_states}
        for (state, symbol), next_states in delta.items()
        }
        self.start_state = start_state
        self.final_states = final_states
    
    def epsilon_closure(self):
        #1. ε-closure(S)의 원소가 바뀌지 않을 때까지 계속 모든 상태를 결합
        epsilon_closure=[set() for _ in range(len(self.states))] #ε-closure(S)를 저장하는 리스트 변수
        #ε-closure구하기
        for i, state in enumerate(self.states):
            closure = set([state]) #closure에 자기자신 추가
            stack = [state]
            
            while stack:
                current = stack.pop()
                if (current, 'ε') in self.delta:  # 전이함수에 ε-전이가 존재하면
                    for next_state in self.delta[(current, 'ε')]: #다음 ε-전이가 있는 지 확인
                        if next_state not in closure:  # 이미 처리한 상태는 건너뜀
                            closure.add(next_state)
                            stack.append(next_state)
            epsilon_closure[i] = frozenset(closure) # frozenset으로 값을 상수화화
            
        return epsilon_closure
    def to_dfa(self):
        # 1. ε-closure를 미리 계산
        queue = deque(self.epsilon_closure()) # 모든 상태의 ε-closure를 deque로 가져옴 내부의 값은 모두 frozenset dfa의 상태들의 모임
        dfa_start=queue[0]
        dfa_delta = dict()
        state_map = dict()
        for i in queue:
            state_map[i] = chr(80+len(state_map))
        #2. dfa 상태, 전이함수 구하기
        while queue:
            current_state = queue.popleft() # {q0,q1}
            for al in sorted(set(self.alphabet) - {"ε"}) :
                new_state=set()
                for state in sorted(current_state):
                    
                    if (state,al) in self.delta:
                        new_state.update(self.delta[(state, al)]) 
                if new_state :
                    new_state = frozenset(sorted(new_state))
                    if new_state not in queue and new_state not in state_map: # new_state가 존재하고, 겹치지 않는다면
                        queue.append(frozenset(new_state)) # 상태를 추가
                        state_map[new_state] = chr(80 + len(state_map))  #new_state를 매핑 후 저장
                        
                    dfa_delta[(state_map[current_state], al)] = state_map[new_state] # new_state가 존재하지만 겹칠 때를 포함한 전이함수에 추가
                    
        #4. 결과 반환
        dfa_final = set()
        for key, value in state_map.items():
            if self.final_states & key:
                dfa_final.update(value)
        dfa_alphabet = self.alphabet
        dfa_alphabet.remove('ε')
        return nfa(
            states=[chr(80+i) for i in range(len(state_map))],
            alphabet=dfa_alphabet,
            delta=dfa_delta,
            start_state=state_map[dfa_start],
            final_states=dfa_final
        )          
        
    def minimize(self):
        
        return "boom"
        
#예시 nfa 생성
Q = ['q0','q1','q2']
sigma = ['0', '1', 'ε']
delta = {
    ('q0','ε'): {'q1'},
    ('q1',0): {'q1','q2'},
    ('q1',1): {'q1'}
    }
start = {'q0'}
final = {'q0','q2'}

FM = nfa(Q,sigma,delta,start,final)
DFA = FM.to_dfa()
print("상태 : ",DFA.states,
      "알파벳 : ",DFA.alphabet,
      "전이함수 : ",DFA.delta,
      "시작상태 : ",DFA.start_state,
      "종료상태 : ",DFA.final_states, sep ='\n')
