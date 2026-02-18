# StateManifoldEngine

> **"상태 공간을 구성하고 위험 지형을 추적해, L0 동역학이 안정 어트랙터로 수렴하도록 입력/바이어스를 조절하는 메타-상태 엔진"**

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/qquartsco-svg/StateManifold_Engine)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

상태 공간을 구성하고 위험 지형을 추적하여, L0 동역학이 안정 어트랙터로 수렴하도록 입력/바이어스를 조절하는 엔진.

---

## 🎯 StateManifoldEngine이 정확히 하는 일

### 입력 → 처리 → 출력

**StateManifoldEngine**은 다음 3가지 작업을 수행합니다:

#### 1. 상태 공간 구축 (`build_state_space`)

**입력**: 여러 난제 엔진의 `SearchBias` 딕셔너리
```python
biases = {
    "three_body": SearchBias(risk_map={...}),
    "navier_stokes": SearchBias(risk_map={...}),
}
```

**처리**:
- 각 난제의 위험도 맵(`risk_map`)을 하나의 상태 공간으로 통합
- 난제 쌍 간의 **유기적 연결 가중치** 계산 (공통 위험 조건이 많을수록 강한 연결)
- 여러 난제에서 동시에 위험한 조건을 **통합 붕괴 영역**으로 식별

**출력**: `StateManifold` 객체
- `dimensions`: 각 난제의 SearchBias
- `organic_connections`: 난제 쌍 → 연결 강도
- `collapse_zones`: 통합 붕괴 영역 리스트

---

#### 2. 안정 경로 탐색 (`flow_through_space`)

**입력**: 
- `value`: 공간을 통과할 값 (어떤 타입이든 가능)
- `start`: 시작 조건 서명 (문자열)
- `goal`: 목표 조건 서명 (문자열)

**처리**:
- 시작 → 목표까지의 경로를 찾음 (위험도가 낮은 경로 우선)
- 경로의 **흐름 에너지** 계산 (경로상 위험도의 합)
- **형태 보존도** 계산 (값이 경로를 따라 변형되지 않았는지)
- **안정성** 계산 (경로상 최대 위험도의 역수)

**출력**: `FlowResult` 객체 또는 `None` (경로 없음)
- `path`: 조건 서명 리스트 (경로)
- `flow_energy`: 흐름 에너지 (낮을수록 좋음)
- `form_preservation`: 형태 보존도 (0.0~1.0)
- `stability`: 안정성 점수 (0.0~1.0)

---

#### 3. 상태 공간 유지 (`maintain_life`)

**입력**: 
- `fluctuation_scale`: 미세 요동 크기 (기본 0.01)

**처리**:
- 상태 공간의 각 조건에 대해 위험도를 **약간 감소**시킴 (장벽 완화)
- 여러 차원에서 동시에 높은 위험을 가지는 조건은 더 강하게 조정
- 이미 낮은 위험도는 거의 건드리지 않음

**출력**: 없음 (상태 공간 내부 수정)

---

### L0 통합 기능 (`L0L1Interface`)

**L1 → L0 매핑**:
- 위험도 맵 → L0 입력 벡터 `I` 변환
- 상태 벡터 → L0 바이어스 `b` 변환

**L0 → L1 피드백**:
- L0 수렴 여부 → L1 상태 해석
- L0 에너지 변화량 → L1 주의 신호

---

### 핵심 요약

**StateManifoldEngine**은:
1. 여러 난제의 위험 지형을 **하나로 통합**하는 도구
2. 통합된 지형에서 **안전한 경로를 찾는** 도구 (그리디 방식: 위험도가 낮은 쪽으로 이동)
3. 상태 공간을 **미세하게 조정**하여 유지하는 도구

---

### ⚠️ 현재 제한사항: "판단" 능력 없음

**StateManifoldEngine**은 **"보고 판단"하는 능력이 없습니다**.

**현재 동작 방식**:
- ✅ **계산**: 위험도를 합산하고 평균을 냄
- ✅ **선택**: 위험도가 가장 낮은 경로를 선택 (그리디)
- ✅ **임계값 비교**: 위험도가 0.8 이상이면 경로 탐색 중단
- ❌ **판단 없음**: 상황을 분석하여 "이 경로가 안전한가?"를 판단하지 않음
- ❌ **학습 없음**: 과거 경험을 기억하거나 학습하지 않음
- ❌ **적응 없음**: 새로운 상황에 맞춰 전략을 바꾸지 않음

**예시**:
```python
# 현재: 단순 계산
best_next = min(candidates, key=lambda c: self.manifold.get_risk(c))

# 만약 "판단" 능력이 있다면:
# - 이 경로가 실제로 도달 가능한가?
# - 과거에 이 경로로 실패한 적이 있는가?
# - 현재 상황에서 이 경로가 최선인가?
# → 이런 질문을 스스로 하지 않음
```

**결론**: StateManifoldEngine은 **"계산기"**이지 **"판단 엔진"**이 아닙니다.

---

## 🏛️ 아키텍처 위치

### 뇌 모델 레이어 (Brain Model Layer)

**L1: 상태 공간 엔진 (State Manifold Engine)**  
L0와는 **양방향 결합(입력 조절 ↔ 수렴 해석)** 관계입니다.

```
L2: HistoricalDataReconstructor
            ↑
            │
L1: StateManifoldEngine
      ↕  (bidirectional)
L0: NeuralDynamicsCore
```

---

## 🚀 빠른 시작

### 설치

```bash
# 개발 모드 설치 (로컬)
pip install -e .

# 또는 GitHub에서 직접 설치
pip install git+https://github.com/qquartsco-svg/StateManifold_Engine.git
```

### 기본 사용법

```python
from state_manifold_engine import StateManifoldEngine

# SearchBias는 UP 엔진에서 생성 (예시용 최소 구조)
from dataclasses import dataclass
from typing import Dict

@dataclass
class SearchBias:
    condition: str
    risk_map: Dict[str, float]
    importance: float = 1.0
    
    def get_risk(self, condition: str) -> float:
        return self.risk_map.get(condition, 0.0)

# 엔진 초기화
engine = StateManifoldEngine()

# SearchBias 수집 (예: UP-1에서)
search_biases = {
    "three_body": SearchBias(
        condition="condition_1",
        risk_map={"condition_1": 0.8, "condition_2": 0.3},
        importance=0.9
    ),
}

# StateManifold 구축
manifold = engine.build_state_space(search_biases)

# 값이 공간을 통과
flow_result = engine.flow_through_space(
    manifold=manifold,
    value="example_value",
    start="condition_1",
    goal="condition_2"
)

if flow_result:
    print(f"경로: {flow_result.path}")
    print(f"흐름 에너지: {flow_result.flow_energy}")
    print(f"형태 보존도: {flow_result.form_preservation}")
```

---

## 🔗 L0 통합

### L0 ↔ L1 인터페이스

**파일**: `src/state_manifold_engine/l0_l1_interface.py`

**기능**:
- L1 → L0: 위험도 → 입력, 상태 → 바이어스 매핑
- L0 → L1: 수렴 해석, 에너지 변화 해석

**사용 예**:
```python
from state_manifold_engine.l0_l1_interface import L0L1Interface
from cognitive_kernel.engines.dynamics import NeuralDynamicsCore

# L0 코어 생성 (예시)
W = [[0.5, -0.3], [-0.3, 0.5]]  # 연결 가중치 행렬
b = [0.1, 0.1]  # 바이어스
l0_core = NeuralDynamicsCore(W=W, b=b)

# 인터페이스 생성
interface = L0L1Interface(neural_core=l0_core)

# L1 → L0 → L1 통합 실행
l0_output, l1_feedback = interface.run_integrated(
    risk_map={"condition_1": 0.8},
    state_vector=[0.5, 0.3],
    importance=None,
    compute_energy=True,
)

print("converged:", l0_output.converged)
print("final_energy:", l0_output.final_energy)
print("l1_feedback:", l1_feedback)
```

---

## 💡 활용 사례 및 시나리오

### 1. 뇌 모델링: 감각 피질과 전두엽의 연결 고리

**StateManifoldEngine**은 뇌 모델에서 **감각 피질(L0: 신경 동역학)**과 **전두엽(L2: 스토리라인 재구성)** 사이의 **메타 인지 계층** 역할을 합니다.

**시나리오**:
- L0가 신경 동역학으로 패턴을 인식
- L1이 여러 난제의 위험 지형을 통합하여 "안전한 인식 경로"를 제공
- L2가 스토리라인을 재구성하여 장기 기억 형성

**결과**: 뇌가 혼돈이나 붕괴 없이 안정적으로 정보를 처리할 수 있는 "내비게이션 시스템"

---

### 2. 다중 난제 환경에서의 안정 경로 탐색

**문제**: 여러 난제(삼체 문제, 나비에-스토크스 등)가 동시에 작용하는 복잡한 환경에서 안정적인 경로를 찾아야 함.

**해결**:
```python
# 여러 난제 엔진의 출력을 통합
biases = {
    "three_body": three_body_search_bias,      # UP-1
    "navier_stokes": navier_stokes_search_bias, # UP-4
    "butterfly": butterfly_search_bias,        # UP-3
}

# 통합된 상태 공간 구축
manifold = engine.build_state_space(biases)

# 안정 경로 탐색 (여러 난제를 동시에 고려)
flow_result = engine.flow_through_space(
    manifold=manifold,
    value=system_state,
    start="initial_condition",
    goal="target_condition"
)
```

**결과**: 단일 난제만 고려할 때 놓치던 "유기적 위험 증폭"을 감지하고 회피

---

### 3. L0 신경 동역학의 안정 수렴 유도

**문제**: L0 (NeuralDynamicsCore)가 혼돈이나 발산 없이 안정 어트랙터로 수렴하도록 입력/바이어스를 조절해야 함.

**해결**:
```python
# L1 → L0: 위험도 지형을 입력/바이어스로 변환
l0_input = interface.l1_to_l0(
    risk_map={"high_risk_condition": 0.9},
    state_vector=[0.5, 0.3]
)

# L0 실행
l0_output, l1_feedback = interface.run_integrated(
    risk_map={"condition_1": 0.8},
    compute_energy=True
)

# L0 → L1: 수렴 여부를 관측하여 피드백
if l1_feedback["converged"]:
    print("안정 어트랙터로 수렴 성공")
else:
    print("불안정 또는 진동 감지")
```

**결과**: L0가 혼돈에 빠지지 않고 안정적으로 수렴

---

### 4. 물리 시스템 설계: 안정 운전 영역 확보

**문제**: 엔진, 터빈, 로봇 등 물리 시스템에서 여러 실패 모드(분리, 스톨, 서지, 충격파)를 동시에 고려하여 안정 운전 영역을 설계해야 함.

**해결**:
- 각 실패 모드를 "난제"로 모델링
- StateManifoldEngine이 통합 위험 지형을 구축
- 안정 경로를 따라 시스템이 운전되도록 입력 스케줄 생성

**결과**: 패시브 안정성 확보 (능동 제어 없이도 안정적으로 운전)

---

### 5. 향후 확장: 감정/주의(Attention) 모듈 통합

**StateManifoldEngine**은 향후 감정이나 주의 모듈을 얹을 수 있는 **견고한 토대**를 제공합니다.

- **감정 모듈**: 위험도 지형에 감정 가중치를 추가하여 "공포 회피 경로" 생성
- **주의 모듈**: 중요도(importance) 지형을 활용하여 "집중 영역" 식별

---

## 📊 핵심 개념

### StateManifold (상태 다양체)

여러 SearchBias를 통합하여 만든 상태 공간:

```python
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class StateManifold:
    dimensions: Dict[str, SearchBias]  # 각 차원의 SearchBias (난제 이름 → SearchBias)
    organic_connections: Dict[Tuple[str, str], float]  # 유기적 연결 가중치
    collapse_zones: List[CollapseZone]  # 통합 붕괴 영역
```

**주요 메서드**:
- `get_risk(condition_signature, dimension=None) -> float`: 조건에 대한 위험도 반환

### FlowResult (흐름 결과)

값이 상태 공간을 통과한 결과:

```python
from typing import List, Any

@dataclass
class FlowResult:
    value: Any  # 통과한 값 (형태 보존)
    path: List[str]  # 경로 (조건 서명 리스트)
    flow_energy: float  # 흐름 에너지 (경로/상태의 비용 함수 값, 낮을수록 선호)
    form_preservation: float  # 형태 보존도 (UP-2 등에서 들어온 형태 보존 점수, 0.0~1.0)
    stability: float  # 안정성 점수 (0.0~1.0)
```

**참고**: `flow_energy`는 L1의 risk/importance 지형 기반으로 계산된 경로 비용이며, L0의 Hopfield 에너지와는 별개입니다.

---

## 📖 예제 및 데모

### 기본 사용 예제

```bash
# examples/basic_usage.py 실행
python examples/basic_usage.py
```

**예제 내용**:
- 여러 UP 엔진의 SearchBias 통합
- 상태 공간 구축 및 흐름 경로 탐색
- 통합 위험도 확인

### 통합 데모 (L0 → L1 → L2)

전체 파이프라인 데모는 상위 프로젝트의 `INTEGRATED_DEMO_L0_L1_L2.py`를 참조하세요.

---

## 🧪 테스트

```bash
# L0 ↔ L1 인터페이스 테스트
pytest tests/test_l0_l1_interface.py -v

# 전체 테스트
pytest tests/ -v
```

**테스트 결과**: ✅ 9개 테스트 통과

---

## 📚 문서

### 주요 문서
- `L0_L1_INTEGRATION_SPEC.md`: L0 ↔ L1 인터페이스 스펙
- `L0_L1_INTEGRATION_COMPLETE.md`: 통합 완료 문서
- `META_STATE_SPACE_ENGINE_DESIGN.md`: 메타 상태 공간 엔진 설계

---

## 🔧 의존성

### 필수 의존성
- Python 3.8+
- `cognitive-kernel` (L0: NeuralDynamicsCore)

### 선택적 의존성
- `three-body-boundary-engine` (UP-1: SearchBias 생성)

---

## 📈 버전 히스토리

### v1.0.1 (2026-02-05)
- ✅ StateManifoldEngine 기본 구현
- ✅ L0 ↔ L1 인터페이스 구현
- ✅ 통합 테스트 완료 (9개 테스트 통과)
- ✅ 문서화 완료

---

## 🤝 기여

기여를 환영합니다! 이슈를 열거나 Pull Request를 제출해주세요.

---

## 📄 라이선스

MIT License

---

## 👤 작성자

GNJz (Qquarts)

---

**상태**: ✅ 완성 (v1.0.0)
