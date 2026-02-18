# 빠른 업로드 가이드

**⚠️ 중요**: 홈 디렉토리(`~`)가 아니라 **데스크탑의 하위 폴더**로 이동해야 합니다!

---

## 🎯 정확한 경로

Git 저장소 위치:
```
~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine
```

---

## 📝 터미널에서 실행할 명령어 (복사해서 붙여넣기)

### 1단계: 디렉토리 이동
```bash
cd ~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine
```

### 2단계: 현재 위치 확인 (선택사항)
```bash
pwd
```
**결과**: `/Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine` 이 나와야 합니다.

### 3단계: Git 상태 확인
```bash
git status
```
**결과**: "현재 브랜치 main" 같은 메시지가 나와야 합니다.  
**오류**: "깃 저장소가 아닙니다" 메시지가 나오면 → 1단계를 다시 확인하세요.

### 4단계: 커밋 (아직 안 했다면)
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

### 5단계: 태그 생성
```bash
git tag -a v0.2.0 -m "StateManifoldEngine v0.2.0 - 메타 상태 공간 엔진"
```

### 6단계: GitHub에 푸시
```bash
git push origin main
git push origin v0.2.0
```

---

## ✅ 성공 확인

### 성공하면 이런 메시지가 나옵니다:
```
Enumerating objects: ...
Writing objects: ...
To https://github.com/qquartsco-svg/BDS_Engine.git
```

### 실패하면:
- "깃 저장소가 아닙니다" → 1단계 다시 확인
- "인증 오류" → GitHub 인증 확인 필요
- "권한 없음" → 저장소 권한 확인

---

## 🔍 현재 위치 확인 방법

터미널 프롬프트를 보세요:
- ❌ `~ %` → 홈 디렉토리 (잘못된 위치)
- ✅ `Brain_Disorder_Simulation_Engine %` → 올바른 위치

---

## 💡 팁

### 한 번에 실행하려면:
```bash
cd ~/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine && git status
```

### 경로가 기억나지 않으면:
```bash
cd ~/Desktop
ls
# 00_BRAIN 폴더가 보이면
cd 00_BRAIN/Brain_Disorder_Simulation_Engine
```

---

**작성일**: 2026-02-04  
**상태**: 빠른 업로드 가이드 준비 완료

