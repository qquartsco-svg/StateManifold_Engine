"""
StateManifoldEngine 기본 사용 예제

메타 엔진: 여러 난제가 동시에 겹쳐진 상태 공간
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dataclasses import dataclass, field
from typing import Dict

# UP 엔진들의 SearchBias 타입 (테스트용)
@dataclass
class SearchBias:
    risk_map: Dict[str, float] = field(default_factory=dict)
    collapse_mode_risk: Dict[str, float] = field(default_factory=dict)
    total_risk_score: float = 0.0
    max_risk_score: float = 0.0
    
    def get_risk(self, condition_signature: str) -> float:
        return self.risk_map.get(condition_signature, 0.0)


from state_manifold_engine import StateManifoldEngine


def main():
    """기본 사용 예제"""
    
    print("=" * 60)
    print("StateManifoldEngine 기본 사용 예제")
    print("=" * 60)
    
    # 1. 여러 UP 엔진의 SearchBias 생성 (시뮬레이션)
    print("\n1. 여러 UP 엔진의 SearchBias 생성")
    
    # UP-1 (삼체 문제) 위험 지형
    three_body_bias = SearchBias(
        risk_map={
            "mass_1.0_dist_1.0_mismatch_0.1": 0.1,
            "mass_1.0_dist_1.0_mismatch_0.5": 0.5,
            "mass_1.0_dist_1.0_mismatch_0.9": 0.9,  # 붕괴 구역
        },
        max_risk_score=0.9
    )
    
    # UP-4 (스토크스) 위험 지형
    navier_stokes_bias = SearchBias(
        risk_map={
            "density_0.5_velocity_0.1": 0.2,
            "density_0.5_velocity_0.5": 0.6,
            "density_0.5_velocity_0.9": 0.9,  # 난류 구역
        },
        max_risk_score=0.9
    )
    
    print(f"   UP-1 (삼체): {len(three_body_bias.risk_map)}개 조건")
    print(f"   UP-4 (스토크스): {len(navier_stokes_bias.risk_map)}개 조건")
    
    # 2. 메타 엔진 생성 및 상태 공간 구축
    print("\n2. 상태 공간 구축")
    engine = StateManifoldEngine()
    
    biases = {
        "three_body": three_body_bias,
        "navier_stokes": navier_stokes_bias,
    }
    
    manifold = engine.build_state_space(biases)
    
    print(f"   차원 수: {len(manifold.dimensions)}")
    print(f"   유기적 연결 수: {len(manifold.organic_connections)}")
    print(f"   붕괴 영역 수: {len(manifold.collapse_zones)}")
    
    # 3. 값이 상태 공간을 통과
    print("\n3. 값이 상태 공간을 통과")
    
    test_value = {"data": "test"}
    result = engine.flow_through_space(
        value=test_value,
        start="mass_1.0_dist_1.0_mismatch_0.1",
        goal="density_0.5_velocity_0.1"
    )
    
    if result:
        print(f"   ✅ 흐름 성공!")
        print(f"   경로: {' → '.join(result.path)}")
        print(f"   흐름 에너지: {result.flow_energy:.3f}")
        print(f"   형태 보존도: {result.form_preservation:.3f}")
        print(f"   안정성: {result.stability:.3f}")
        print(f"   값: {result.value}")
    else:
        print("   ❌ 흐름 경로를 찾을 수 없음")
    
    # 4. 통합 위험도 확인
    print("\n4. 통합 위험도 확인")
    test_condition = "mass_1.0_dist_1.0_mismatch_0.5"
    integrated_risk = manifold.get_risk(test_condition)
    print(f"   조건: {test_condition}")
    print(f"   통합 위험도: {integrated_risk:.3f}")
    
    print("\n" + "=" * 60)
    print("예제 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()

