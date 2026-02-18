"""
StateManifoldEngine - 메타 상태 공간 엔진

엔진 번호: Meta (메타 엔진)
역할: 여러 난제 엔진의 붕괴 영역 선언을 겹쳐서 상태 공간 형성

핵심 철학:
- 여러 난제가 동시에 겹쳐진 고차원 공간 구현
- 유기적 배치와 흐름 허용
- 값이 공간 안으로 들어가서 혼돈/발산/수렴하지 않고 출력됨

Author: GNJz (Qquarts)
Version: 0.2.0
PHAM Signed: 2026-02-04
"""

from .state_manifold_engine import StateManifoldEngine
from .models import StateManifold, FlowResult

__all__ = [
    "StateManifoldEngine",
    "StateManifold",
    "FlowResult",
]

__version__ = "0.2.0"

