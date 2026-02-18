# GitHub 업로드 단계별 가이드

**작성일**: 2026-02-04  
**버전**: 0.2.0

---

## ⚠️ 중요: 올바른 디렉토리로 이동

Git 저장소는 **상위 디렉토리**에 있습니다.  
반드시 아래 명령어로 이동한 후 실행하세요.

---

## 📍 1단계: 올바른 디렉토리로 이동

```bash
cd ~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine
```

또는

```bash
cd ~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/StateManifoldEngine
```

**확인**: `git status` 명령어가 정상 작동하는지 확인

---

## 📋 2단계: 현재 상태 확인

```bash
# 현재 위치 확인
pwd

# Git 상태 확인
git status

# 스테이징된 파일 확인
git status --short
```

---

## 💾 3단계: 커밋 (아직 안 했다면)

StateManifoldEngine 파일들이 이미 스테이징되어 있다면:

```bash
# 상위 디렉토리에서 커밋
cd ~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine

git commit -m "feat: StateManifoldEngine v0.2.0 - 메타 상태 공간 엔진

- 상태 공간 구축 기능 구현
- 값이 공간을 통과하는 기능 구현
- 생명 유지 메커니즘 추가 (maintain_life)
- 퍼텐셜 우물 공간 개념 구현
- PHAM 블록체인 서명 완료 (TxID: BC570B5A94D0C2AA)

버전: 0.2.0
PHAM 서명: 2026-02-04"
```

---

## 🏷️ 4단계: 태그 생성

```bash
# 상위 디렉토리에서 태그 생성
cd ~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine

git tag -a v0.2.0 -m "StateManifoldEngine v0.2.0

메타 상태 공간 엔진 - 퍼텐셜 우물 공간 구축
PHAM 서명: BC570B5A94D0C2AA (2026-02-04)"
```

---

## 🚀 5단계: GitHub에 푸시

```bash
# 상위 디렉토리에서 푸시
cd ~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine

# 메인 브랜치 푸시
git push origin main

# 태그 푸시
git push origin v0.2.0
```

---

## ✅ 6단계: 확인

```bash
# 커밋 확인
git log --oneline -1

# 태그 확인
git tag -l "v0.2.0"

# 원격 상태 확인
git status
```

---

## 🔍 현재 상태 요약

- **Git 저장소 위치**: `~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine`
- **원격 저장소**: `https://github.com/qquartsco-svg/BDS_Engine.git`
- **브랜치**: `main`
- **로컬 커밋**: origin/main보다 5개 앞서 있음
- **StateManifoldEngine 파일**: 스테이징 완료 (19개 파일)

---

## 📝 한 번에 실행하는 명령어

```bash
# 1. 디렉토리 이동
cd ~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine

# 2. 상태 확인
git status

# 3. 커밋 (아직 안 했다면)
git commit -m "feat: StateManifoldEngine v0.2.0 - 메타 상태 공간 엔진

- 상태 공간 구축 기능 구현
- 값이 공간을 통과하는 기능 구현
- 생명 유지 메커니즘 추가 (maintain_life)
- 퍼텐셜 우물 공간 개념 구현
- PHAM 블록체인 서명 완료 (TxID: BC570B5A94D0C2AA)

버전: 0.2.0
PHAM 서명: 2026-02-04"

# 4. 태그 생성
git tag -a v0.2.0 -m "StateManifoldEngine v0.2.0 - 메타 상태 공간 엔진"

# 5. 푸시
git push origin main
git push origin v0.2.0
```

---

**작성자**: AI Assistant  
**작성일**: 2026-02-04  
**상태**: 업로드 가이드 준비 완료

