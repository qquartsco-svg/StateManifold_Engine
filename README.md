# StateManifoldEngine

> **"상태 공간 내 안정 어트랙터를 설계하는 메타 인지 엔진"**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/qquartsco-svg/StateManifold_Engine)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

상태 공간을 구축하고 위험 지형을 추적하여 안정적인 어트랙터를 설계하는 엔진.

---

## 🎯 핵심 가치 제안

### 메타 인지 엔진

**StateManifoldEngine**은 여러 난제 엔진(UP-1, UP-2 등)의 출력을 통합하여  
**하나의 통합된 상태 공간(State Manifold)**을 구축하고,  
**안정적인 어트랙터(Attractor)**를 설계하는 메타 인지 엔진입니다.

### 주요 특징

- ✅ **상태 공간 구축**: 여러 SearchBias를 통합하여 StateManifold 생성
- ✅ **위험 지형 추적**: 붕괴 영역(Collapse Zone) 식별 및 회피
- ✅ **안정 어트랙터 설계**: 에너지 최소 경로 탐색
- ✅ **L0 통합**: NeuralDynamicsCore와의 인터페이스 제공
- ✅ **생명 유지 메커니즘**: 미세한 에너지 흐름으로 상태 공간 활성화

---

## 🏛️ 아키텍처 위치

### 뇌 모델 레이어 (Brain Model Layer)

**L1: 상태 공간 엔진 (State Manifold Engine)**

```
L0: NeuralDynamicsCore (신경 동역학 코어)
    ↓
L1: StateManifoldEngine (상태 공간 엔진) ← 여기
    ↓
L2: HistoricalDataReconstructor (스토리라인 재구성)
```

---

## 🚀 빠른 시작

### 설치

```bash
pip install state-manifold-engine
```

### 기본 사용법

```python
from state_manifold_engine import StateManifoldEngine, StateManifold
from three_body_boundary_engine.failure_bias_converter import SearchBias

# 엔진 초기화
engine = StateManifoldEngine()

# SearchBias 수집 (예: UP-1에서)
search_biases = [
    SearchBias(condition="condition_1", risk=0.8, importance=0.9),
    SearchBias(condition="condition_2", risk=0.3, importance=0.5),
]

# StateManifold 구축
manifold = engine.build_manifold(search_biases)

# 안정 경로 탐색
flow_path = engine.find_flow_path(
    start_state=[0.5, 0.3],
    target_state=[0.8, 0.6],
    manifold=manifold
)

print(f"안정 경로: {flow_path.path}")
print(f"에너지: {flow_path.energy}")
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

# 인터페이스 생성
interface = L0L1Interface(neural_core=l0_core)

# L1 → L0 매핑
l0_input = interface.l1_to_l0(
    risk_map={"condition_1": 0.8},
    state_vector=[0.5, 0.3]
)

# L0 실행 후 L1 피드백
l1_feedback = interface.l0_to_l1(l0_output)
```

---

## 📊 핵심 개념

### StateManifold (상태 다양체)

여러 SearchBias를 통합하여 만든 상태 공간:

```python
@dataclass
class StateManifold:
    dimensions: Dict[str, SearchBias]  # 각 차원의 SearchBias
    risk_map: Dict[str, float]  # 조건 → 위험도
    flow_energy: float  # 흐름 에너지
    form_preservation: float  # 형태 보존도
```

### FlowPath (흐름 경로)

안정적인 어트랙터를 따라가는 경로:

```python
@dataclass
class FlowPath:
    path: List[Vector]  # 경로 점들
    energy: float  # 경로 에너지
    stability: float  # 안정성 점수
```

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

### v1.0.0 (2026-02-05)
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
