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
        epsilon_closure = self.epsilon_closure()
        queue = deque([epsilon_closure[0]]) # 모든 상태의 ε-closure를 deque로 가져옴 내부의 값은 모두 frozenset dfa의 상태들의 모임
        
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
        #3. 결과 반환
        dfa_final = set()
        for key, value in state_map.items():
            if self.final_states & key:
                dfa_final.update(value)
        dfa_alphabet = self.alphabet
        if 'ε' in dfa_alphabet:
            dfa_alphabet.remove('ε')
        return nfa(
            states=[chr(80+i) for i in range(len(state_map))],
            alphabet=dfa_alphabet,
            delta=dfa_delta,
            start_state=state_map[dfa_start],
            final_states=dfa_final
        )          
        
    def minimize(self):
        
    # 1. 초기 상태 분할
        final_states = {state for state in self.states if state in self.final_states}
        non_final_states = set(self.states) - final_states
        partitions = [final_states, non_final_states]

        # 2. 상태 분할 반복
        
        while True:
            new_partitions = []
            for states in partitions:
                symbol_to_states = {}
                for state in states:
                    # 입력 심볼에 따라 전이 결과를 키로 사용
                    key = tuple(
                        frozenset(self.delta.get((state, al), None)) if self.delta.get((state, al), None) else None
                        for al in self.alphabet
                    )
                    symbol_to_states.setdefault(key, set()).add(state)
                new_partitions.extend(symbol_to_states.values())

            if new_partitions == partitions:  # 분할이 안정화되면 종료
                break
            partitions = new_partitions
        #partitions = [{'p,'q'},{'r'}]
        
        # 3. 최소화된 DFA 생성
        # 상태 매핑 생성
        state_map = {}
        for i, states in enumerate(partitions):
            state_map[frozenset(states)] = chr(80+i)
            
        reduced_delta = dict()
        
        for states in partitions:
            state = list(states)[0]  # 그룹에서 하나의 상태 선택 하나의 상태가 곧 그룹의 상태이기 때문
            for al in self.alphabet:
                if (state, al) in self.delta:
                    value = self.delta[(state, al)]  # 현재 상태에서 입력 심볼로 이동한 결과
                    target_state = next(
                        (states for states in partitions if value & states),  # target_set이 group과 교집합이 있으면 해당 그룹 선택
                        None  # 없으면 None 반환
                    )
                    if target_state:
                        reduced_delta[(state_map[frozenset(states)], al)] = state_map[frozenset(target_state)]
        
        reduced_start = state_map[frozenset(next(state for state in partitions if self.start_state in state))]
        reduced_final = set()
    
        for state in partitions:
            if self.final_states & state:
                reduced_final.update(state_map[frozenset(state)])
        
        # 최소화된 DFA 반환
        return nfa(
            states=list(state_map.values()),
            alphabet=self.alphabet,
            delta=reduced_delta,
            start_state=reduced_start,
            final_states=reduced_final
        )


    
        
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

# Q=['q0','q1','q2']
# sigma = ['a','b']
# delta = {
#     ('q0','a') : {'q0','q1'},
#     ('q0','b') : {'q0'},
#     ('q1','b') : {'q2'}}
# start = {'q0'}
# final = {'q2'}

FM = nfa(Q,sigma,delta,start,final)
DFA = FM.to_dfa()
print(f"상태 : {DFA.states}", 
      f"알파벳 : {DFA.alphabet}")
print("전이함수 : ")
for i in DFA.delta:
    print(i)
print(f"시작상태 : {DFA.start_state}",
      f"종료상태 : {DFA.final_states}",sep='\n')
print("--------------------------------------------------------")
print("DFA 최소화")

DFA = DFA.minimize()

print(f"상태 : {DFA.states}", 
      f"알파벳 : {DFA.alphabet}")
print("전이함수 : ")
for i in DFA.delta:
    print(i)
print(f"시작상태 : {DFA.start_state}",
      f"종료상태 : {DFA.final_states}",sep='\n')