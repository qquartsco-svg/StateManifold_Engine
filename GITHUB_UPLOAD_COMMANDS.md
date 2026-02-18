# GitHub 업로드 명령어

**작성일**: 2026-02-04  
**버전**: 0.2.0

---

## 📋 업로드 전 확인

### 현재 상태
- ✅ 모든 파일 스테이징 완료
- ✅ 블록체인 서명 검증 완료
- ✅ 주석/개념/수식 검증 완료
- ✅ 테스트 검증 완료

---

## 🚀 업로드 명령어

### 1. 디렉토리 이동
```bash
cd ~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/StateManifoldEngine
```

### 2. 최종 확인
```bash
git status
```

### 3. 커밋
```bash
git commit -m "feat: StateManifoldEngine v0.2.0 - 메타 상태 공간 엔진

- 상태 공간 구축 기능 구현
- 값이 공간을 통과하는 기능 구현
- 생명 유지 메커니즘 추가 (maintain_life)
- 퍼텐셜 우물 공간 개념 구현
- PHAM 블록체인 서명 완료 (TxID: BC570B5A94D0C2AA)

버전: 0.2.0
PHAM 서명: 2026-02-04"
```

### 4. 태그 생성
```bash
git tag -a v0.2.0 -m "StateManifoldEngine v0.2.0

메타 상태 공간 엔진 - 퍼텐셜 우물 공간 구축
PHAM 서명: BC570B5A94D0C2AA (2026-02-04)"
```

### 5. GitHub에 푸시
```bash
# 메인 브랜치 푸시
git push origin main

# 태그 푸시
git push origin v0.2.0
```

---

## 🔍 원격 저장소 정보

- **Repository**: `https://github.com/qquartsco-svg/BDS_Engine.git`
- **Branch**: `main`
- **Tag**: `v0.2.0`

---

## ✅ 업로드 후 확인

### 1. 커밋 확인
```bash
git log --oneline -1
```

### 2. 태그 확인
```bash
git tag -l "v0.2.0"
```

### 3. 원격 저장소 확인
GitHub 웹사이트에서 확인:
- https://github.com/qquartsco-svg/BDS_Engine

---

## 📝 참고사항

### 만약 index.lock 파일 오류가 발생하면:
```bash
# 상위 디렉토리로 이동
cd ~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine

# lock 파일 제거
rm -f .git/index.lock

# 다시 StateManifoldEngine으로 이동
cd Unsolved_Problems_Engines/StateManifoldEngine
```

### 만약 인증 오류가 발생하면:
```bash
# GitHub 인증 확인
git config --global user.name
git config --global user.email

# 필요시 SSH 키 사용
git remote set-url origin git@github.com:qquartsco-svg/BDS_Engine.git
```

---

**작성자**: AI Assistant  
**작성일**: 2026-02-04  
**상태**: 업로드 명령어 준비 완료

