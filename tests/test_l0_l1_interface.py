"""
L0 ↔ L1 인터페이스 테스트

L0 (NeuralDynamicsCore)와 L1 (StateManifoldEngine) 간의 통합 테스트.
"""

import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Cognitive_Kernel 경로 추가
cognitive_kernel_path = project_root.parent.parent.parent.parent / "Cognitive_Kernel" / "src"
if cognitive_kernel_path.exists():
    sys.path.insert(0, str(cognitive_kernel_path))

import pytest

try:
    from state_manifold_engine.l0_l1_interface import (
        L0L1Interface,
        L0Input,
        L0Output,
        map_risk_to_input,
        map_state_to_bias,
        apply_importance_gate,
        interpret_convergence,
        interpret_energy_change,
    )
    from cognitive_kernel.engines.dynamics import (
        NeuralDynamicsCore,
        ContinuousDynamicsConfig,
    )
    INTERFACE_AVAILABLE = True
except ImportError as e:
    INTERFACE_AVAILABLE = False
    pytest.skip(f"L0L1Interface not available: {e}", allow_module_level=True)


class TestL1ToL0Mapping:
    """L1 → L0 매핑 테스트"""
    
    def test_map_risk_to_input(self):
        """위험도 → 입력 변환"""
        risk_map = {
            "cond1": 0.0,  # 낮은 위험 → 양수 입력
            "cond2": 0.5,  # 중간 위험 → 0 근처
            "cond3": 1.0,  # 높은 위험 → 음수 입력
        }
        
        I = map_risk_to_input(risk_map)
        
        assert len(I) == 3
        assert I[0] > 0  # 낮은 위험 → 양수
        assert abs(I[1]) < 0.5  # 중간 위험 → 0 근처
        assert I[2] < 0  # 높은 위험 → 음수
    
    def test_map_state_to_bias(self):
        """상태 벡터 → 바이어스 변환"""
        state = [1.0, -0.5, 0.3]
        b = map_state_to_bias(state)
        
        assert len(b) == 3
        assert b[0] == 0.5  # 1.0 * 0.5
        assert b[1] == -0.25  # -0.5 * 0.5
        assert b[2] == 0.15  # 0.3 * 0.5
    
    def test_apply_importance_gate(self):
        """중요도 게이팅"""
        I = [1.0, -0.5, 0.3]
        importance = [1.0, 0.5, 0.0]
        
        gated = apply_importance_gate(I, importance)
        
        assert len(gated) == 3
        assert gated[0] == 1.0  # 중요도 1.0 → 그대로
        assert gated[1] == -0.25  # 중요도 0.5 → 절반
        assert gated[2] == 0.0  # 중요도 0.0 → 0


class TestL0ToL1Feedback:
    """L0 → L1 피드백 테스트"""
    
    def test_interpret_convergence_stable(self):
        """수렴한 경우 해석"""
        l0_output = L0Output(
            x_trajectory=[[0.0, 0.0], [0.1, 0.1], [0.99, 0.99], [0.99, 0.99]],
            x_final=[0.99, 0.99],
            converged=True,
            steps=3
        )
        
        result = interpret_convergence(l0_output)
        
        assert result["stability"] == "stable"
        assert result["attractor_id"] is not None
        assert result["confidence"] > 0.5
        assert result["warning"] is None
    
    def test_interpret_convergence_unstable(self):
        """수렴하지 않은 경우 해석"""
        l0_output = L0Output(
            x_trajectory=[[0.0, 0.0], [0.1, 0.1], [0.2, 0.2]],
            x_final=[0.2, 0.2],
            converged=False,
            steps=2
        )
        
        result = interpret_convergence(l0_output)
        
        assert result["stability"] in ["unstable", "oscillating"]
        assert result["confidence"] < 0.5
        assert result["warning"] is not None
    
    def test_interpret_energy_change(self):
        """에너지 변화 해석"""
        l0_output = L0Output(
            x_trajectory=[[0.0, 0.0], [0.1, 0.1], [0.99, 0.99]],
            x_final=[0.99, 0.99],
            energy_trajectory=[10.0, 5.0, 1.0],  # 에너지 감소
            converged=True,
            steps=2
        )
        
        attention = interpret_energy_change(l0_output)
        
        assert 0.0 <= attention <= 1.0
        assert attention > 0.5  # 에너지가 크게 감소했으므로 높은 집중


class TestL0L1Interface:
    """통합 인터페이스 테스트"""
    
    def test_interface_initialization(self):
        """인터페이스 초기화"""
        # L0 없이 초기화 (기본 네트워크 생성)
        interface = L0L1Interface(default_n_neurons=4)
        
        assert interface.l0 is not None
        assert interface.l0.n == 4
    
    def test_l1_to_l0_conversion(self):
        """L1 → L0 변환"""
        interface = L0L1Interface(default_n_neurons=3)
        
        risk_map = {
            "cond1": 0.2,
            "cond2": 0.5,
            "cond3": 0.8,
        }
        state_vector = [0.5, -0.3, 0.1]
        
        l0_input = interface.l1_to_l0(risk_map, state_vector)
        
        assert len(l0_input.I) == 3
        assert len(l0_input.b) == 3
        assert l0_input.I[0] > l0_input.I[2]  # 위험도 낮은 것 → 더 큰 입력
    
    def test_run_integrated(self):
        """통합 실행"""
        interface = L0L1Interface(default_n_neurons=2)
        
        risk_map = {
            "cond1": 0.3,
            "cond2": 0.7,
        }
        
        l0_output, l1_feedback = interface.run_integrated(
            risk_map,
            compute_energy=True
        )
        
        # L0 출력 검증
        assert len(l0_output.x_final) == 2
        assert l0_output.steps > 0
        assert len(l0_output.x_trajectory) > 1
        
        # L1 피드백 검증
        assert "stability" in l1_feedback
        assert "attention" in l1_feedback
        assert "final_state" in l1_feedback
        assert 0.0 <= l1_feedback["attention"] <= 1.0

