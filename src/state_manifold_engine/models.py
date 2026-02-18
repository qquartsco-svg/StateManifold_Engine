"""
StateManifoldEngine - 데이터 모델

메타 엔진: 여러 난제가 동시에 겹쳐진 상태 공간
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any


@dataclass
class CollapseZone:
    """붕괴 영역
    
    여러 난제의 붕괴 조건이 겹쳐진 영역.
    """
    condition_signature: str  # 조건 서명
    dimensions: Dict[str, float]  # 차원별 위험도 (예: {"three_body": 0.8, "navier_stokes": 0.7})
    organic_risk: float  # 유기적 위험도 (단순 합산이 아님)
    
    def get_total_risk(self) -> float:
        """통합 위험도 반환"""
        return self.organic_risk


@dataclass
class StateManifold:
    """상태 공간 (Manifold)
    
    여러 난제가 동시에 겹쳐진 고차원 공간.
    
    Attributes:
        dimensions: 차원별 위험 지형 (난제 이름 → SearchBias)
        organic_connections: 유기적 연결 가중치 (난제 쌍 → 가중치)
        collapse_zones: 통합 붕괴 영역
    """
    dimensions: Dict[str, Any] = field(default_factory=dict)  # 차원별 위험 지형
    organic_connections: Dict[Tuple[str, str], float] = field(default_factory=dict)  # 유기적 연결
    collapse_zones: List[CollapseZone] = field(default_factory=list)  # 통합 붕괴 영역
    
    def get_risk(
        self,
        condition_signature: str,
        dimension: Optional[str] = None
    ) -> float:
        """조건 서명에 대한 위험도 반환
        
        Args:
            condition_signature: 조건 서명
            dimension: 특정 차원만 (None이면 통합 위험도)
        
        Returns:
            위험도 (0.0 ~ 1.0)
        """
        if dimension:
            # 특정 차원의 위험도
            bias = self.dimensions.get(dimension)
            if bias and hasattr(bias, 'get_risk'):
                return bias.get_risk(condition_signature)
            return 0.0
        
        # 통합 위험도: 모든 차원의 위험도를 유기적으로 결합
        risks = []
        for dim_name, bias in self.dimensions.items():
            if bias and hasattr(bias, 'get_risk'):
                risk = bias.get_risk(condition_signature)
                risks.append((dim_name, risk))
        
        if not risks:
            return 0.0
        
        # 유기적 결합: 단순 평균이 아니라 가중 평균 + 유기적 증폭
        base_risk = sum(risk for _, risk in risks) / len(risks)
        
        # 유기적 증폭: 여러 차원에서 동시에 위험한 경우 증폭
        high_risk_count = sum(1 for _, risk in risks if risk > 0.7)
        if high_risk_count > 1:
            # 여러 차원에서 동시에 위험 → 유기적 증폭
            organic_boost = 1.0 + (high_risk_count - 1) * 0.2
            base_risk = min(1.0, base_risk * organic_boost)
        
        return base_risk


@dataclass
class FlowResult:
    """흐름 결과
    
    값이 상태 공간을 통과한 결과.
    """
    value: Any  # 통과한 값 (형태 보존)
    path: List[str]  # 경로 (조건 서명 리스트)
    flow_energy: float  # 흐름 에너지 (공간의 저항)
    form_preservation: float  # 형태 보존도 (0.0 ~ 1.0)
    stability: float  # 안정성 (0.0 ~ 1.0)
    
    def is_valid(self) -> bool:
        """유효한 결과인지 판정"""
        return (
            self.flow_energy >= 0.0 and
            self.form_preservation >= 0.0 and
            self.stability >= 0.0
        )

