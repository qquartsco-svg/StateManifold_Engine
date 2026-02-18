# StateManifoldEngine

> **"상태 공간을 구성하고 위험 지형을 추적해, L0 동역학이 안정 어트랙터로 수렴하도록 입력/바이어스를 조절하는 메타-상태 엔진"**

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/qquartsco-svg/StateManifold_Engine)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

상태 공간을 구성하고 위험 지형을 추적하여, L0 동역학이 안정 어트랙터로 수렴하도록 입력/바이어스를 조절하는 엔진.

---

## 🎯 핵심 가치 제안

### 메타 인지 엔진

**StateManifoldEngine**은 여러 난제 엔진(UP-1, UP-2 등)의 출력을 통합하여  
**하나의 통합된 상태 공간(State Manifold)**을 구성하고,  
**L0 동역학이 안정 어트랙터로 수렴하도록 입력/바이어스를 조절**하는 메타-상태 엔진입니다.

### 주요 특징

- ✅ **상태 공간 구축**: 여러 SearchBias를 통합하여 StateManifold 생성
- ✅ **위험 지형 추적**: 붕괴 영역(Collapse Zone) 식별 및 회피
- ✅ **안정 경로/입력 조건 산출**: (L1의 risk/importance 지형 기반) 안정 구간으로 유도하는 경로/입력 스케줄 생성
- ✅ **L0 통합**: NeuralDynamicsCore와의 인터페이스 제공 (L0 에너지 변화량 관측 및 피드백)
- ✅ **(프로토타입) 상태 공간 유지**: manifold의 risk 지형을 기준으로 미세 요동/완화(장벽 다듬기)를 수행

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
