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

from typing import List, Optional, Dict, Any, Set
from .models import StateManifold, FlowResult, CollapseZone

# UP 엔진들의 SearchBias 타입 (타입 힌트용)
try:
    from three_body_boundary_engine.failure_bias_converter import SearchBias
except ImportError:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from typing import Any as SearchBias


class StateManifoldEngine:
    """메타 상태 공간 엔진
    
    여러 UP 엔진의 붕괴 영역 선언을 겹쳐서 상태 공간 형성.
    값이 이 공간을 통과하여 안정적으로 출력.
    
    핵심 원리:
    1. 각 UP 엔진의 SearchBias를 차원으로 받음
    2. 차원들을 겹쳐서 상태 공간 형성
    3. 유기적 연결 가중치 계산
    4. 값이 공간을 통과하여 흐름
    """
    
    def __init__(
        self,
        problem_engines: Optional[List[Any]] = None
    ):
        """
        Args:
            problem_engines: UP 엔진 리스트 (선택적)
        """
        self.problem_engines = problem_engines or []
        self.manifold: Optional[StateManifold] = None
    
    def build_state_space(
        self,
        biases: Dict[str, 'SearchBias']
    ) -> StateManifold:
        """상태 공간 구축
        
        여러 UP 엔진의 SearchBias를 겹쳐서 상태 공간 형성.
        
        Args:
            biases: 차원별 SearchBias 딕셔너리
                   예: {"three_body": SearchBias, "navier_stokes": SearchBias}
        
        Returns:
            통합된 상태 공간 (StateManifold)
        """
        # 차원별 위험 지형 저장
        dimensions = biases.copy()
        
        # 유기적 연결 가중치 계산
        organic_connections = self._calculate_organic_connections(biases)
        
        # 통합 붕괴 영역 식별
        collapse_zones = self._identify_collapse_zones(biases)
        
        self.manifold = StateManifold(
            dimensions=dimensions,
            organic_connections=organic_connections,
            collapse_zones=collapse_zones
        )
        
        return self.manifold
    
    def flow_through_space(
        self,
        value: Any,
        start: str,  # ConditionSignature
        goal: str    # ConditionSignature
    ) -> Optional[FlowResult]:
        """값이 상태 공간을 통과
        
        값이 여러 난제의 붕괴 조건을 동시에 고려하여
        공간의 결을 따라 흐름.
        
        Args:
            value: 공간을 통과할 값
            start: 시작 조건 서명
            goal: 목표 조건 서명
        
        Returns:
            흐름 결과 (형태 보존, 안정적 출력)
        """
        if not self.manifold:
            raise ValueError("상태 공간이 구축되지 않았습니다. build_state_space()를 먼저 호출하세요.")
        
        # 통합 위험 지형 기반으로 경로 찾기
        path = self._find_flow_path(start, goal)
        
        if not path:
            return None
        
        # 흐름 에너지 계산 (통합 위험도 기반)
        flow_energy = self._calculate_flow_energy(path)
        
        # 형태 보존도 계산
        form_preservation = self._calculate_form_preservation(path, value)
        
        # 안정성 계산
        stability = self._calculate_stability(path)
        
        return FlowResult(
            value=value,
            path=path,
            flow_energy=flow_energy,
            form_preservation=form_preservation,
            stability=stability
        )
    
    def _calculate_organic_connections(
        self,
        biases: Dict[str, 'SearchBias']
    ) -> Dict[tuple, float]:
        """유기적 연결 가중치 계산
        
        여러 난제의 위험 지형이 겹치는 구역에서
        유기적 증폭을 계산.
        
        Args:
            biases: 차원별 SearchBias 딕셔너리
        
        Returns:
            유기적 연결 가중치 (난제 쌍 → 가중치)
        """
        connections = {}
        dimension_names = list(biases.keys())
        
        # 모든 난제 쌍에 대해 유기적 연결 계산
        for i, dim1 in enumerate(dimension_names):
            for dim2 in dimension_names[i+1:]:
                bias1 = biases[dim1]
                bias2 = biases[dim2]
                
                # 공통 조건 서명 찾기
                common_conditions = set(bias1.risk_map.keys()) & set(bias2.risk_map.keys())
                
                if not common_conditions:
                    connections[(dim1, dim2)] = 0.0
                    continue
                
                # 유기적 연결 강도 계산
                # 두 난제에서 동시에 위험한 조건이 많을수록 강한 연결
                high_risk_pairs = sum(
                    1 for cond in common_conditions
                    if bias1.get_risk(cond) > 0.7 and bias2.get_risk(cond) > 0.7
                )
                
                connection_strength = high_risk_pairs / len(common_conditions) if common_conditions else 0.0
                connections[(dim1, dim2)] = connection_strength
        
        return connections
    
    def _identify_collapse_zones(
        self,
        biases: Dict[str, 'SearchBias']
    ) -> List[CollapseZone]:
        """통합 붕괴 영역 식별
        
        여러 난제의 붕괴 조건이 겹쳐진 영역을 식별.
        
        Args:
            biases: 차원별 SearchBias 딕셔너리
        
        Returns:
            통합 붕괴 영역 리스트
        """
        collapse_zones = []
        
        # 모든 차원의 조건 서명 수집
        all_conditions = set()
        for bias in biases.values():
            all_conditions.update(bias.risk_map.keys())
        
        # 각 조건에 대해 통합 위험도 계산
        for condition in all_conditions:
            dimension_risks = {}
            for dim_name, bias in biases.items():
                risk = bias.get_risk(condition)
                if risk > 0.5:  # 위험한 조건만 고려
                    dimension_risks[dim_name] = risk
            
            if not dimension_risks:
                continue
            
            # 유기적 위험도 계산
            base_risk = sum(dimension_risks.values()) / len(dimension_risks)
            
            # 여러 차원에서 동시에 위험한 경우 증폭
            if len(dimension_risks) > 1:
                organic_boost = 1.0 + (len(dimension_risks) - 1) * 0.2
                organic_risk = min(1.0, base_risk * organic_boost)
            else:
                organic_risk = base_risk
            
            # 붕괴 영역으로 식별 (유기적 위험도가 높은 경우)
            if organic_risk > 0.7:
                collapse_zones.append(CollapseZone(
                    condition_signature=condition,
                    dimensions=dimension_risks,
                    organic_risk=organic_risk
                ))
        
        return collapse_zones
    
    def _find_flow_path(
        self,
        start: str,
        goal: str
    ) -> Optional[List[str]]:
        """흐름 경로 찾기
        
        통합 위험 지형을 기반으로 경로 찾기.
        (간단한 구현, 향후 개선 가능)
        
        Args:
            start: 시작 조건 서명
            goal: 목표 조건 서명
        
        Returns:
            경로 (조건 서명 리스트)
        """
        if not self.manifold:
            return None
        
        # 간단한 그리디 방식으로 경로 찾기
        current = start
        path = [current]
        visited: Set[str] = {current}
        max_iterations = 100
        
        for _ in range(max_iterations):
            if current == goal:
                return path
            
            # 다음 조건 후보 찾기 (통합 위험도가 낮은 순서로)
            candidates = self._get_next_candidates(current, visited)
            
            if not candidates:
                break
            
            # 통합 위험도가 가장 낮은 후보 선택
            best_next = min(
                candidates,
                key=lambda c: self.manifold.get_risk(c)
            )
            
            # 위험도가 너무 높으면 중단
            if self.manifold.get_risk(best_next) > 0.8:
                break
            
            current = best_next
            path.append(current)
            visited.add(current)
        
        return None
    
    def _get_next_candidates(
        self,
        current: str,
        visited: Set[str]
    ) -> List[str]:
        """다음 조건 후보 찾기"""
        candidates = []
        
        # 모든 차원의 조건 서명 수집
        for bias in self.manifold.dimensions.values():
            if hasattr(bias, 'risk_map'):
                for condition in bias.risk_map.keys():
                    if condition not in visited:
                        candidates.append(condition)
        
        # 중복 제거
        return list(set(candidates))
    
    def _calculate_flow_energy(
        self,
        path: List[str]
    ) -> float:
        """흐름 에너지 계산
        
        통합 위험도 기반으로 흐름 에너지 계산.
        """
        if not path:
            return float('inf')
        
        total_risk = sum(self.manifold.get_risk(condition) for condition in path)
        flow_energy = total_risk / len(path)
        
        return flow_energy
    
    def _calculate_form_preservation(
        self,
        path: List[str],
        value: Any
    ) -> float:
        """형태 보존도 계산
        
        경로를 따라가면서 형태가 얼마나 보존되는지 계산.
        """
        if not path:
            return 0.0
        
        # 평균 위험도가 낮을수록 형태 보존도 높음
        avg_risk = sum(self.manifold.get_risk(condition) for condition in path) / len(path)
        form_preservation = 1.0 - avg_risk
        
        return max(0.0, min(1.0, form_preservation))
    
    def _calculate_stability(
        self,
        path: List[str]
    ) -> float:
        """안정성 계산
        
        경로의 안정성을 계산.
        """
        if not path:
            return 0.0
        
        # 위험도가 낮을수록 안정성 높음
        max_risk = max(self.manifold.get_risk(condition) for condition in path)
        stability = 1.0 - max_risk
        
        return max(0.0, min(1.0, stability))

    # 생명 유지 메커니즘 -------------------------------------------------
    
    def maintain_life(
        self,
        fluctuation_scale: float = 0.01,
        max_iterations: int = 1
    ) -> None:
        """생명 유지: 최소 에너지로 상태 공간을 '살아있는' 상태로 유지
        
        이 메서드는 별도의 큰 연산을 수행하지 않고,
        이미 구축된 상태 공간 위에서 **은은한 에너지 흐름**을 모사한다.
        
        개념적 역할:
        - 브라운 운동 / 열적 요동과 유사한 미세 플럭추에이션을 모사
        - 통합 위험도가 지나치게 높은 조건을 자연스럽게 정리
        - 작은 교란은 흡수하고, 잠재적으로 불안정한 조건은 완만하게 밀어냄
        
        구현 원칙:
        - 상태 공간이 없으면 아무 것도 하지 않음
        - SearchBias 자체를 파괴하지 않음 (가벼운 가중치 조정만 수행)
        - 한 번 호출은 "한 번의 미세한 숨결"에 해당 (루프/스레드 없음)
        
        Args:
            fluctuation_scale: 미세 요동의 크기 (0.0 ~ 1.0, 기본 0.01)
            max_iterations: 내부 미세 조정 반복 횟수 (기본 1)
        """
        if not self.manifold:
            # 아직 상태 공간이 없으면 생명 유지 개념이 적용되지 않음
            return
        
        if fluctuation_scale <= 0.0 or max_iterations <= 0:
            return
        
        # 너무 큰 값으로 설정되는 것을 방지
        fluctuation_scale = min(fluctuation_scale, 0.1)
        
        for _ in range(max_iterations):
            self._apply_minimal_fluctuations(fluctuation_scale)
    
    def _apply_minimal_fluctuations(
        self,
        fluctuation_scale: float
    ) -> None:
        """상태 공간에 미세한 요동을 적용하여 '살아있는' 상태를 유지
        
        구현 전략:
        - 각 차원의 SearchBias에서 위험도가 극단적으로 높은 조건을 완만하게 낮춤
        - 여러 차원에서 동시에 높은 위험을 가지는 조건은 조금 더 강하게 조정
        - 이미 낮은 위험도를 가진 조건은 거의 건드리지 않음
        
        이는 실제 물리 계에서의 열 잡음/브라운 운동이
        퍼텐셜 우물 바닥 주변을 탐색하게 만드는 것에 해당한다.
        """
        if not self.manifold:
            return
        
        # 모든 조건 서명 수집
        all_conditions: Set[str] = set()
        for bias in self.manifold.dimensions.values():
            if hasattr(bias, "risk_map"):
                all_conditions.update(bias.risk_map.keys())
        
        if not all_conditions:
            return
        
        for condition in all_conditions:
            # 차원별 위험도 수집
            dimension_risks: Dict[str, float] = {}
            for dim_name, bias in self.manifold.dimensions.items():
                if hasattr(bias, "get_risk") and hasattr(bias, "set_risk"):
                    risk = bias.get_risk(condition)
                    dimension_risks[dim_name] = risk
            
            if not dimension_risks:
                continue
            
            # 여러 차원에서 동시에 높은 위험을 가지는 조건일수록 더 강하게 완화
            high_risk_dims = [
                name for name, risk in dimension_risks.items()
                if risk > 0.8
            ]
            
            for dim_name, risk in dimension_risks.items():
                bias = self.manifold.dimensions[dim_name]
                
                # 너무 낮은 위험도는 건드리지 않음
                if risk < 0.2:
                    continue
                
                # 기본 완화 계수
                attenuation = fluctuation_scale
                
                # 여러 차원에서 동시에 높은 위험을 가지면 조금 더 강하게 완화
                if dim_name in high_risk_dims and len(high_risk_dims) > 1:
                    attenuation *= 1.5
                
                # 위험도를 약간 감소시켜, 장벽을 완만하게 다듬는다
                new_risk = max(0.0, risk - attenuation * risk)
                
                # SearchBias의 risk_map을 직접 수정 (set_risk 메서드가 없을 경우 대비)
                if hasattr(bias, 'set_risk'):
                    bias.set_risk(condition, new_risk)
                elif hasattr(bias, 'risk_map') and isinstance(bias.risk_map, dict):
                    # risk_map을 직접 수정
                    bias.risk_map[condition] = new_risk

