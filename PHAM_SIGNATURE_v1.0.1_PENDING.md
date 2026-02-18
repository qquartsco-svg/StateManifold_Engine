# PHAM 블록체인 서명 (v1.0.1) — PENDING

**엔진**: StateManifoldEngine  
**버전**: 1.0.1  
**상태**: ⚠️ PENDING (아직 PHAM 블록체인 TxID에 앵커링되지 않음)  
**작성일**: 2026-02-05  
**작성자**: GNJz (Qquarts)

---

## 왜 필요한가

v0.2.0은 PHAM 서명이 기록되어 있으나, 이번 v1.0.1은 다음 변경이 포함되어 **새 PHAM 서명이 필요**합니다.

- README 정합성 개선(다이어그램/예제/API 일치)
- `flow_through_space(manifold=...)` 옵션 추가(명시적 manifold 전달 지원)
- 패키지 버전 정렬 (`__version__`, badge 등)

---

## 서명 대상 파일 해시 (SHA-256)

아래 해시는 **현재 워킹 트리 기준**이며, PHAM 서명 실행 후 TxID가 확정되면 본 문서를 `SIGNED` 상태로 전환합니다.

```
README.md:
  f17591ddea283408038d445dbd2e065b6b67dba72be0366fae71246e3f3c9a33

src/state_manifold_engine/__init__.py:
  224370abdf7b58bbfcc200dc4f8ebbd2907823aa7092dc19ba798193bb92fb35

src/state_manifold_engine/state_manifold_engine.py:
  7f509cae87adc1ed5d8aaae05d77faee1d727ba55145dc1cf568809f972c2108

src/state_manifold_engine/models.py:
  4a58d6e2b3441b00ef437c4ef3840dec6a06184b9befc286d6e089c48485b42d

src/state_manifold_engine/l0_l1_interface.py:
  70ec472fa70464c3e60b913f9401a25a7fe4712746f09d7e9b4c7e3472d85c19

setup.py:
  c8f703313e618f0ce683594dba9a9e5e4b5a16149d928c34c753cb383158cc27
```

---

## PHAM 앵커링 정보 (추후 기록)

- **TxID**: (PENDING)
- **PHAM Hash**: (PENDING)
- **Timestamp**: (PENDING)


