# PHAM 블록체인 서명 실행 가이드

## 서명 대상

**엔진**: StateManifoldEngine v0.2.0

## 서명할 파일 해시

1. `src/state_manifold_engine/state_manifold_engine.py`
   - SHA-256: `daf87e2d13b53d62776f299a86abd1e79e27b322361e8b0a5a0596ad4bbe8f94`

2. `src/state_manifold_engine/models.py`
   - SHA-256: `4a58d6e2b3441b00ef437c4ef3840dec6a06184b9befc286d6e089c48485b42d`

## 서명 실행 방법

PHAM 블록체인 서명 스크립트를 실행하여 다음 정보를 기록:

1. 파일 해시를 블록체인에 기록
2. 트랜잭션 ID (TxID) 획득
3. `PHAM_SIGNED.md` 파일에 TxID 업데이트

## 서명 후 작업

서명 완료 후:
1. `PHAM_SIGNED.md`에 TxID 업데이트
2. 버전 정보 업데이트 확인
3. GitHub 릴리스 준비 완료

