# TravelMaker (Expo React Native) — 프로젝트 안내 & 실행 가이드

> 이 문서는 **처음 보는 사람도 바로 실행/수정할 수 있게** “이 프로젝트가 무엇인지 / 파일들이 무슨 역할인지 / 코드 구조가 어떻게 돌아가는지 / VS Code에서 Expo Go로 어떻게 실행하는지”를 최대한 쉽게 풀어쓴 README입니다.

---

## 1) 이 프로젝트는 무엇인가요?

**TravelMaker**는 사용자가 여행을 만들고(기간/링크/옵션 입력) → 로딩을 거쳐 → **여행 일정(Itinerary)을 리스트/지도 화면으로 보고 편집**하며 → **보관함(History)에 저장/불러오기**까지 할 수 있는 **Expo(React Native) 기반 모바일 앱**입니다.

현재 코드 기준으로는 “AI로 자동 생성된 일정”을 실제로 호출하진 않고, 로딩 화면에서 **빈 일정(places = [])**을 만들어 전달한 뒤, 일정 화면에서 사용자가 직접 장소를 추가/정렬하며 완성해 나가는 흐름으로 구성되어 있습니다.

---

## 2) 기술 스택 / 핵심 라이브러리

- **Expo SDK**: 프로젝트 실행/빌드, Expo Go 연동
- **React Native**
- **React Navigation**
  - Bottom Tabs (`@react-navigation/bottom-tabs`)
  - Stack (`@react-navigation/stack`)
- **지도**
  - `react-native-maps` (마커/경로(Polyline) 표시)
- **드래그 정렬**
  - `react-native-draggable-flatlist` (일정 순서 변경)

---

## 3) 빠른 실행(팀원이 가장 많이 하는 것)

### A. 사전 준비물

1. **Node.js (LTS 권장)** 설치
2. **Expo Go 앱** 설치
   - iOS: App Store → “Expo Go”
   - Android: Play Store → “Expo Go”
3. (권장) **VS Code** 설치

> ⚠️ 주의  
> 본 프로젝트에서 사용하는 지도(`react-native-maps`), 네비게이션, 드래그 정렬 등은  
> **모두 npm 라이브러리로 관리되며**, 별도의 프로그램 설치는 필요 없습니다.  
> 팀원은 `npm install` 또는 `npm ci`만 실행하면 모든 의존성이 자동으로 설치됩니다.

---

### B. VS Code에서 Expo Go로 실행하기 (가장 표준)

1. VS Code에서 프로젝트 폴더 열기

   - 최상위에 `package.json`, `App.js`, `app.json`이 있는 폴더가 프로젝트 루트입니다.
   - cd TravelMaker

2. 터미널( VS Code: Terminal → New Terminal )에서 실행

```bash
# 1) 의존성 설치
npm install
# 또는 lock 기반으로 더 재현성 있게:
# npm ci

# 2) 개발 서버 실행 (권장 옵션)
npx expo start -c --tunnel
# (-c: 캐시 초기화 / --tunnel: 네트워크 환경 상관없이 기기 연결)
```

3. 실행하면 터미널/브라우저에 **QR 코드**가 뜹니다.
   - **Android**: Expo Go 앱에서 “Scan QR Code”
   - **iOS**: 기본 카메라로 QR 스캔 → Expo Go로 열기

#### 자주 쓰는 실행 스크립트

```bash
npm run start    # expo start
npm run android  # expo start --android (에뮬레이터가 있으면 자동 시도)
npm run ios      # expo start --ios (맥에서 시뮬레이터)
npm run web      # 웹으로 실행
```

#### 캐시 문제/이상한 에러가 날 때 (강력 추천)

```bash
npx expo start -c --tunnel
# 💡 대부분의 실행 오류(네트워크, 캐시, 기기 연결 문제)는
# 위 명령어로 해결됩니다.
# 문제가 생기면 항상 이 명령부터 다시 실행하세요.
```

---

## 4) 폴더/파일 구조 (무엇이 어디에 있나요?)

아래는 실제 프로젝트의 주요 구조입니다(핵심만):

```
TravelMaker/
├─ App.js
├─ package.json
├─ app.json
├─ assets/
├─ src/
│  ├─ navigation/
│  │  └─ AppNavigator.js
│  ├─ screens/
│  │  ├─ HomeScreen.js
│  │  ├─ SetupLinkScreen.js
│  │  ├─ SetupOptionsScreen.js
│  │  ├─ LoadingScreen.js
│  │  ├─ ItineraryScreen.js
│  │  ├─ HistoryScreen.js
│  │  └─ TripContext.js
│  └─ components/
│     └─ TimelineItem.js
├─ components/           # (expo 템플릿 잔여) themed-view 등
├─ constants/            # (expo 템플릿 잔여)
├─ hooks/                # (expo 템플릿 잔여)
└─ app_backup/           # (expo-router 템플릿 백업)
```

### 4.1 App.js (앱 진입점)

- 앱이 시작될 때 최초로 실행되는 **Root Component**
- 전역 상태 관리(Context)인 `TripProvider`로 앱을 감싸고,
- 화면 전환을 담당하는 `AppNavigator`를 렌더링합니다.

핵심 역할:

- 전역 저장소 제공: `TripProvider`
- 네비게이션 렌더링: `AppNavigator`
- 상태바 설정: `StatusBar`

---

### 4.2 src/navigation/AppNavigator.js (화면 이동 전체 설계)

여기서 앱의 “화면 흐름”이 결정됩니다.

구성 요약:

- **Bottom Tab Navigator (하단 탭)**

  - Home 탭: `TripCreationStack` (스택 네비게이션)
  - Schedule 탭: `ItineraryScreen` (단독)
  - History 탭: `HistoryScreen` (단독)

- **TripCreationStack (Home 탭 내부 스택)**
  - `HomeScreen` → `SetupLinkScreen` → `SetupOptionsScreen` → `LoadingScreen` → `ItineraryScreen`

즉, “여행 생성 과정”은 Home 탭 안에서 **스택으로 단계별 진행**되고,  
생성 이후에는 탭(Schedule/History)으로 이동하여 보기/편집/저장이 가능합니다.

---

### 4.3 src/screens/TripContext.js (전역 상태 저장소)

여행 데이터를 앱 어디서나 공유하기 위해 Context API를 사용합니다.

관리하는 상태(핵심):

- `history`: 저장된 여행 목록(보관함)
- `recentTrip`: “지금 보고/편집 중인 여행” (가장 중요)

제공하는 함수(핵심):

- `addToHistory(trip)`: 보관함에 저장(동일 id면 업데이트)
- `removeFromHistory(id)`: 보관함에서 삭제
- `setRecentTrip(trip)`: 현재 여행 바꾸기

사용 방법:

```js
import { useTrip } from './TripContext';

const { history, addToHistory, recentTrip, setRecentTrip } = useTrip();
```

---

## 5) 화면(Screen)별 역할 — “사용자 흐름”을 기준으로 이해하기

### 5.1 HomeScreen (홈)

- 여행 만들기 시작점
- “여행 만들기” 버튼을 누르면 다음 단계(링크 입력)으로 이동하는 구조

### 5.2 SetupLinkScreen (링크 입력)

- 유튜브/블로그 등 여행 콘텐츠 링크를 입력하는 UI
- 현재 코드 기준으로 **링크를 실제로 분석/전송하는 API 호출은 없음**  
  (추후 AI/서버 연동 시 여기에서 링크를 넘기는 방식으로 확장 가능)

### 5.3 SetupOptionsScreen (옵션 선택)

- 여행 기간(1일/2일/3일/직접입력), 이동수단, 페이스 등 옵션 선택
- “일정 생성하기”를 누르면 `LoadingScreen`으로 이동하면서 `totalDays`를 전달

### 5.4 LoadingScreen (로딩)

- 3초 진행바 애니메이션을 보여주고
- 종료 시점에 **초기 여행 데이터(빈 일정)** 를 생성하여 `recentTrip`에 저장
- 이후 Schedule 탭(Itinerary 화면)으로 이동

초기 데이터 형태(요약):

```js
{
  id: "timestamp-string",
  title: "여행 일정 (YYYY. M. D.)",
  date: "YYYY. M. D. • N일 코스",
  totalDays: N,
  places: [],
  dailyPaths: []
}
```

### 5.5 ItineraryScreen (일정 보기/편집 — 가장 큰 화면)

이 화면이 앱의 핵심입니다.

기능 요약:

- **리스트 보기 / 지도 보기 전환**
- **장소 추가**
  - 검색창에 텍스트 입력 → Bucket(임시 보관함)에 추가
  - Bucket 아이템을 선택한 Day 일정에 추가
- **드래그 앤 드롭으로 일정 순서 변경**
- **지도에 마커/경로(Polyline) 표시**
- **저장(Save)**
  - `addToHistory()`로 보관함 저장
- **recentTrip 실시간 동기화**
  - 편집 중인 내용이 `recentTrip`에 반영되어 탭 이동 후에도 유지

#### places 데이터(중요)

ItineraryScreen에서 다루는 장소 항목의 형태는 대략 아래와 같습니다:

```js
{
  id: "timestamp-string",
  day: 1,              // 1일부터 시작하는 날짜
  index: 0,            // 같은 day 내 순서(저장 시 재계산)
  title: "장소 이름",
  latitude: 37.5700,
  longitude: 126.9800,
  isBucket: true|false // Bucket(임시)인지 실제 일정인지
}
```

`places`가 바뀌면 `dailyPaths`(지도 경로용 좌표 리스트)를 다시 계산합니다.

### 5.6 HistoryScreen (보관함)

- `TripContext.history`를 목록으로 보여줍니다.
- 특정 여행을 누르면:
  1. `setRecentTrip(item)`으로 현재 여행 지정
  2. `Schedule` 탭(ItineraryScreen)으로 이동하면서 `savedData`를 파라미터로 전달

---

## 6) “왜 components/ constants/ hooks/ app_backup 이 있어요?” (템플릿 잔여 설명)

이 프로젝트는 Expo 템플릿(특히 expo-router 기반 템플릿)의 흔적이 남아 있습니다.

- `components/`, `constants/`, `hooks/`

  - 주로 expo-router 템플릿에서 제공하는 예제 컴포넌트/유틸입니다.
  - 현재 앱의 메인 흐름은 `src/` 아래의 화면과 네비게이션을 사용하므로,
    **이 폴더들은 “당장 실행에 필수는 아닌 잔여 템플릿”** 성격이 큽니다.

- `app_backup/`
  - expo-router 방식의 `app/` 라우팅 구조를 백업해 둔 폴더입니다.
  - 현재는 `App.js` + React Navigation 구조를 쓰기 때문에 **실행에 직접 사용되진 않습니다.**

> 헷갈리지 않도록:  
> **실제로 앱 로직을 수정할 때는 대부분 `src/` 폴더만 보면 됩니다.**

---

## 7) 트러블슈팅(팀 공유 시 자주 발생)

### 7.1 `node_modules` 관련 에러가 날 때

- ZIP에 `node_modules`가 포함되어 있더라도,
  팀원 환경(운영체제/Node버전)에 따라 깨질 수 있습니다.

해결:

```bash
rm -rf node_modules
npm ci   # package-lock.json 기반 재설치
# 또는 npm install
npx expo start -c
```

### 7.2 Expo Go 연결이 안 될 때

- 같은 와이파이인지 확인
- 회사/학교 네트워크는 mDNS/포트가 막힐 수 있음

해결:

- `npx expo start --tunnel` (느릴 수 있지만 연결 확률↑)
- 또는 개인 핫스팟 사용

### 7.3 iOS에서 react-native-maps 관련 문제

- Expo Go에서 `react-native-maps`는 대체로 동작하지만,
  특정 네이티브 설정이 필요해지는 순간(커스텀 빌드)에는 **Development Build**가 필요할 수 있습니다.
- 현재 구성은 Expo Go 기준 개발을 목표로 합니다.

---

## 8) 개발자 메모(확장 포인트)

- **AI/서버 연동을 하려면**

  - `LoadingScreen`에서 현재는 빈 데이터를 생성합니다.
  - 여기서 외부 API 호출(링크 분석/일정 생성)을 붙이고,
  - 응답으로 받은 `places`를 채워 `setRecentTrip()`에 넣으면 됩니다.

- **링크 입력 값 전달**
  - `SetupLinkScreen`에서 입력받은 링크를 `SetupOptionsScreen` → `LoadingScreen`으로 route params로 전달하도록 확장하면 자연스럽습니다.

---

## 9) 프로젝트에서 가장 중요한 파일 Top 5

1. `App.js` — 앱 진입점(Provider + Navigator)
2. `src/navigation/AppNavigator.js` — 화면 흐름 설계(탭/스택)
3. `src/screens/TripContext.js` — 전역 상태(보관함/현재여행)
4. `src/screens/ItineraryScreen.js` — 일정/지도/편집/저장 핵심 로직
5. `src/screens/HistoryScreen.js` — 보관함 목록/불러오기

---

## 10) 팀 공유 체크리스트

- [ ] `node_modules/`는 공유본에서 제거(가능하면)
- [ ] `.env` 같은 민감정보가 있다면 절대 커밋/공유 금지(현재 프로젝트에는 없음)
- [ ] 실행 방법: `npm install` → `npx expo start -c --tunnel` → Expo Go QR 스캔
- [ ] “수정은 src/ 폴더 중심”이라고 안내

---

### 부록) 최소 커맨드만 다시 정리

```bash
npm install
npx expo start -c --tunnel
```

---
