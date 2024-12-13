class nfa:
    #states, alphabet은 리스트 데이터터형
    # start_states, final_states은 집합 데이터형
    #delta는 전이함수로 딕셔너리 데이터형
    def __init__(self, states, alphabet, delta, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.delta = delta
        self.start_state = start_state
        self.final_states = final_states
    
    def to_dfa(self):
        #1. ε-closure(S)의 원소가 바뀌지 않을 때까지 계속 모든 상태를 결합
        
        epsilon_closure=[set() for _ in range(len(self.states))]
        
        #epsilon_closure구하기
        for i, state in enumerate(self.states):
            closure = set([state]) #closure에 자기자신 추가
            stack = [state]
            
            while stack:
                current = stack.pop()
                if (current, 'ε') in self.delta:  # ε-전이가 존재하면
                    for next_state in self.delta[(current, 'ε')]:
                        if next_state not in closure:  # 이미 처리한 상태는 건너뜀
                            closure.add(next_state)
                            stack.append(next_state)

            epsilon_closure[i] = closure
        for i, val in enumerate(epsilon_closure):
            print(f"ε-closure({i}) : {val}")
        #2. epsilon_전이가 있는 NFA와 동등한 DFA 만들기
        # DFA_states는 chr(65+i)로 만들고 싶음
        
        DFA_start_state = epsilon_closure[0]
        
        
        
        
        # 
        # print("to_dfa",self.states)

#예시 nfa 생성
Q = [i for i in range(14)]
sigma = {'a','b','c','ε'}
delta = {
    (0,'ε'): {1,7},
    (1,'ε'): {2,4},
    (2,'a'): {3},
    (3,'ε'): {6},
    (4,'b'): {5},
    (5,'ε'): {6},
    (6,'ε'): {7},
    (7,'ε'): {8},
    (8,'a'): {9},
    (9,'ε'): {10},
    (10,'b'): {11},
    (11,'ε'): {12},
    (12,'b'): {13}
    }
start = {0}
final = {13}

FM = nfa(Q,sigma,delta,start,final)
FM.to_dfa()
print(FM.states,FM.alphabet,FM.delta,FM.start_state,FM.final_states,end='\n')