"""
L0 ↔ L1 인터페이스 구현

L0 (NeuralDynamicsCore)와 L1 (StateManifoldEngine) 간의 데이터 계약 및 통합.

핵심 원칙:
- L1의 위험도/상태 → L0의 입력/바이어스로 매핑
- L0의 수렴/진동/불안정 → L1의 상태 변화/경고/집중으로 해석

Author: GNJz (Qquarts)
Version: 0.1.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any, Callable
import sys
from pathlib import Path

# L0 (NeuralDynamicsCore) import
try:
    # Cognitive_Kernel에서 import
    cognitive_kernel_path = Path(__file__).parent.parent.parent.parent.parent.parent / "Cognitive_Kernel" / "src"
    if cognitive_kernel_path.exists():
        sys.path.insert(0, str(cognitive_kernel_path))
    from cognitive_kernel.engines.dynamics import (
        NeuralDynamicsCore,
        ContinuousDynamicsConfig,
    )
    L0_AVAILABLE = True
except ImportError:
    L0_AVAILABLE = False
    NeuralDynamicsCore = None
    ContinuousDynamicsConfig = None

from .models import StateManifold


# ============================================================================
# L0 입력/출력 타입 정의
# ============================================================================

@dataclass
class L0Input:
    """L0 (NeuralDynamicsCore) 입력"""
    I: List[float]  # 외부 입력 벡터 I(t)
    W: Optional[List[List[float]]] = None  # 연결 행렬 (옵션, 없으면 기존 W 사용)
    b: Optional[List[float]] = None  # 바이어스 벡터 (옵션)
    x0: Optional[List[float]] = None  # 초기 상태 (없으면 현재 상태 사용)
    noise_scale: float = 0.0  # 노이즈 스케일
    dt: float = 0.01  # 시간 스텝
    T: float = 1.0  # 시뮬레이션 시간
    tau: float = 0.1  # 시간 상수


@dataclass
class L0Output:
    """L0 (NeuralDynamicsCore) 출력"""
    x_trajectory: List[List[float]]  # x(t) 궤적
    x_final: List[float]  # 최종 상태
    converged: bool  # 수렴 여부
    steps: int  # 실제 시뮬레이션 스텝 수
    energy_trajectory: Optional[List[float]] = None  # energy(t) (옵션)
    final_energy: Optional[float] = None  # 최종 에너지 (옵션)


# ============================================================================
# L1 → L0 매핑 규칙
# ============================================================================

def map_risk_to_input(risk_map: Dict[str, float]) -> List[float]:
    """
    L1의 위험도 맵을 L0의 외부 입력 I(t)로 변환
    
    규칙: 위험도가 높으면 회피 신호 (음수 입력)
          위험도가 낮으면 탐색 신호 (양수 입력)
    
    Args:
        risk_map: 조건 서명 → 위험도 (0~1)
    
    Returns:
        I: 외부 입력 벡터
    """
    I = []
    for condition, risk in risk_map.items():
        # 위험도 → 입력 변환: risk=1.0 → I=-1.0, risk=0.0 → I=+0.5
        I_value = -risk + 0.5 * (1.0 - risk)
        I.append(I_value)
    return I


def map_state_to_bias(state_vector: List[float]) -> List[float]:
    """
    L1의 상태 벡터를 L0의 바이어스 b로 변환
    
    Args:
        state_vector: L1 상태 벡터
    
    Returns:
        b: 바이어스 벡터 (스케일 조정)
    """
    # 상태 벡터를 정규화하여 바이어스로 사용
    return [v * 0.5 for v in state_vector]


def apply_importance_gate(I: List[float], importance: List[float]) -> List[float]:
    """
    중요도에 따라 입력을 게이팅
    
    Args:
        I: 원본 입력
        importance: 중요도 벡터 (0~1)
    
    Returns:
        gated_I: 게이팅된 입력
    """
    if len(I) != len(importance):
        raise ValueError(f"Input length {len(I)} != importance length {len(importance)}")
    return [I[i] * importance[i] for i in range(len(I))]


# ============================================================================
# L0 → L1 역방향 피드백 규칙
# ============================================================================

def interpret_convergence(l0_output: L0Output) -> Dict[str, Any]:
    """
    L0의 수렴 결과를 L1이 해석할 수 있는 형태로 변환
    
    Args:
        l0_output: L0 출력
    
    Returns:
        {
            "stability": "stable" | "unstable" | "oscillating",
            "attractor_id": Optional[int],  # 어트랙터 식별자
            "confidence": float,  # 안정성 신뢰도 (0~1)
            "warning": Optional[str]  # 경고 메시지
        }
    """
    if l0_output.converged:
        # 수렴했으면 안정 상태
        # 어트랙터 ID는 최종 상태의 해시로 식별
        attractor_id = hash(tuple(round(v, 6) for v in l0_output.x_final))
        # 빠르게 수렴할수록 신뢰도 높음
        confidence = max(0.0, min(1.0, 1.0 - (l0_output.steps / 1000.0)))
        
        return {
            "stability": "stable",
            "attractor_id": attractor_id,
            "confidence": confidence,
            "warning": None
        }
    else:
        # 수렴하지 않았으면 불안정 또는 진동
        # 궤적 분석으로 진동 여부 판단
        if len(l0_output.x_trajectory) > 10:
            last_10 = l0_output.x_trajectory[-10:]
            variance = sum(
                sum((last_10[i][j] - last_10[i-1][j])**2 for j in range(len(last_10[0])))
                for i in range(1, len(last_10))
            ) / len(last_10)
            
            if variance > 0.1:
                return {
                    "stability": "oscillating",
                    "attractor_id": None,
                    "confidence": 0.3,
                    "warning": "System is oscillating, may need attention"
                }
        
        return {
            "stability": "unstable",
            "attractor_id": None,
            "confidence": 0.1,
            "warning": "System did not converge"
        }


def interpret_energy_change(l0_output: L0Output) -> float:
    """
    에너지 변화를 집중 신호로 변환
    
    Args:
        l0_output: L0 출력
    
    Returns:
        attention_signal: 0~1, 에너지가 크게 감소하면 높음
    """
    if l0_output.energy_trajectory and len(l0_output.energy_trajectory) > 1:
        initial_energy = l0_output.energy_trajectory[0]
        final_energy = l0_output.energy_trajectory[-1]
        
        if abs(initial_energy) > 1e-10:
            energy_reduction = (initial_energy - final_energy) / abs(initial_energy)
            return max(0.0, min(1.0, energy_reduction * 2.0))  # 스케일 조정
    
    return 0.5  # 기본값


# ============================================================================
# 통합 인터페이스 클래스
# ============================================================================

class L0L1Interface:
    """L0와 L1 간의 인터페이스"""
    
    def __init__(
        self,
        neural_core: Optional[NeuralDynamicsCore] = None,
        state_manifold: Optional[StateManifold] = None,
        default_n_neurons: int = 4
    ):
        """
        Args:
            neural_core: L0 (NeuralDynamicsCore) 인스턴스
            state_manifold: L1 (StateManifold) 인스턴스
            default_n_neurons: L0가 없을 때 기본 뉴런 수
        """
        if not L0_AVAILABLE:
            raise ImportError(
                "NeuralDynamicsCore is not available. "
                "Please ensure Cognitive_Kernel is installed and accessible."
            )
        
        self.l0 = neural_core
        self.l1 = state_manifold
        
        # L0가 없으면 기본 네트워크 생성
        if self.l0 is None:
            # 기본 대칭 연결 행렬 (Hopfield-style)
            W = [[0.5] * default_n_neurons for _ in range(default_n_neurons)]
            for i in range(default_n_neurons):
                W[i][i] = 1.0  # 자기 연결
            
            cfg = ContinuousDynamicsConfig(dt=0.01, tau=0.1, activation="tanh")
            self.l0 = NeuralDynamicsCore(W=W, b=[0.0] * default_n_neurons, config=cfg)
    
    def l1_to_l0(
        self,
        risk_map: Dict[str, float],
        state_vector: Optional[List[float]] = None,
        importance: Optional[List[float]] = None
    ) -> L0Input:
        """
        L1 출력을 L0 입력으로 변환
        
        Args:
            risk_map: 조건 서명 → 위험도 맵
            state_vector: L1 상태 벡터 (옵션)
            importance: 중요도 벡터 (옵션)
        
        Returns:
            L0Input: L0 입력
        """
        # 위험도 → 입력
        I = map_risk_to_input(risk_map)
        
        # 중요도 게이팅
        if importance:
            I = apply_importance_gate(I, importance)
        
        # 상태 벡터 → 바이어스
        if state_vector:
            b = map_state_to_bias(state_vector)
        else:
            b = [0.0] * len(I)
        
        # L0 뉴런 수와 맞추기
        n_neurons = self.l0.n
        if len(I) != n_neurons:
            # 패딩 또는 자르기
            if len(I) < n_neurons:
                I = I + [0.0] * (n_neurons - len(I))
                b = b + [0.0] * (n_neurons - len(b))
            else:
                I = I[:n_neurons]
                b = b[:n_neurons]
        
        return L0Input(
            I=I,
            b=b,
            noise_scale=0.0,
            dt=0.01,
            T=1.0,
            tau=0.1
        )
    
    def l0_to_l1(self, l0_output: L0Output) -> Dict[str, Any]:
        """
        L0 출력을 L1이 해석할 수 있는 형태로 변환
        
        Args:
            l0_output: L0 출력
        
        Returns:
            L1 피드백 딕셔너리
        """
        convergence_info = interpret_convergence(l0_output)
        attention_signal = interpret_energy_change(l0_output)
        
        return {
            **convergence_info,
            "attention": attention_signal,
            "final_state": l0_output.x_final,
            "trajectory_length": len(l0_output.x_trajectory)
        }
    
    def run_integrated(
        self,
        risk_map: Dict[str, float],
        state_vector: Optional[List[float]] = None,
        importance: Optional[List[float]] = None,
        compute_energy: bool = False
    ) -> Tuple[L0Output, Dict[str, Any]]:
        """
        L1 → L0 → L1 통합 실행
        
        Args:
            risk_map: 조건 서명 → 위험도 맵
            state_vector: L1 상태 벡터 (옵션)
            importance: 중요도 벡터 (옵션)
            compute_energy: 에너지 궤적 계산 여부
        
        Returns:
            (L0Output, L1 피드백)
        """
        # L1 → L0
        l0_input = self.l1_to_l0(risk_map, state_vector, importance)
        
        # L0 실행
        x0 = l0_input.x0 if l0_input.x0 else [0.0] * self.l0.n
        if len(x0) != self.l0.n:
            x0 = x0[:self.l0.n] if len(x0) > self.l0.n else x0 + [0.0] * (self.l0.n - len(x0))
        
        steps = int(l0_input.T / l0_input.dt)
        
        # 입력 스케줄 (고정 입력)
        def input_schedule(t: int) -> List[float]:
            return l0_input.I
        
        trajectory = self.l0.run(
            x0=x0,
            steps=steps,
            input_schedule=input_schedule,
            stop_tol=1e-6,
            return_trajectory=True
        )
        
        x_final = trajectory[-1] if trajectory else x0
        converged = len(trajectory) < steps
        
        # 에너지 궤적 계산 (옵션)
        energy_trajectory = None
        final_energy = None
        if compute_energy:
            energy_trajectory = []
            for x in trajectory:
                energy = self.l0.hopfield_energy(x)
                energy_trajectory.append(energy)
            final_energy = energy_trajectory[-1] if energy_trajectory else None
        
        l0_output = L0Output(
            x_trajectory=trajectory,
            x_final=x_final,
            energy_trajectory=energy_trajectory,
            converged=converged,
            steps=len(trajectory) - 1,
            final_energy=final_energy
        )
        
        # L0 → L1
        l1_feedback = self.l0_to_l1(l0_output)
        
        return l0_output, l1_feedback

