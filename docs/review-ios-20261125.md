# iOS 등록용 개인정보처리방침

사용자가 기존 Android 자료를 참고해 가능한 iOS 등록 작업을 진행하도록 요청했다. 기존 Android 정책7언어/루트 URL을 유지하고 별도 iOS 한국어·영어 정책과 bilingual privacy-ios.html을 추가한다. iOS1.0.0의 DeviceMediaLibrary·MediaRecovery·PremiumStore·AdsModel, 번들 Google Mobile Ads13.9.0/UMP3.1.0 PrivacyInfo.xcprivacy와 공개 SDK 안내를 근거로 쓴다. 센서·추론 제한이나 새 수집 동작을 추가하지 않는다. 촬영/얼굴 데이터의 기기 내 처리와 Google 광고/Apple 구매/사용자 공유/호스팅 처리를 구분한다. 문의 주소는 기존 mgfrind@gmail.com이며 확인하지 않은 이름·주소·보존기간·연령 수치를 만들지 않는다.

1차 검토: 앱 로컬 사본과 Photos 공개/삭제·권한·UNKNOWN 복구, 기기 내 MediaPipe/Vision, 일회성 StoreKit 구매/복원과 앱 계정 부재를 코드와 대조한다.
2차 검토: 한국어·영어 조항 ID/정보 처리 의미를 대조하고 Android MediaStore/Google Play/ML Kit 문구를 iOS 정책에 섞지 않는다. 광고 SDK의 외부 처리·기기 식별자·진단/상호작용·IP 기반 대략 위치를 숨기지 않는다.
3차 검토: JSON/HTML 링크·날짜·단일 H1·스크립트/외부 폰트 부재·모바일 가로 넘침과 공개 URL 갱신을 확인한다. 기존 Android URL/7언어 본문은 변경하지 않는다. 이 게시만으로 App Store 개인정보 설문 제출까지 완료했다고 표시하지 않는다.

실행 결과: JSON12개 조항의 한/영 ID 순서·HTML3개와 진입 페이지의 상대 링크/단일 H1/스크립트 부재·git diff 검사가 통과했다. 실제 Chrome390×844/1280×844의3페이지, 총6조합에서 가로 넘침0을 확인했다. 한국어 제목의 단어 단위 줄바꿈을 보완했다. 기존 Android 정책 생성 결과는 diff가 없고 루트 진입 페이지에 iPhone 정책 링크만 추가했다. 앱 등록용 정책 URL은 https://hyunjunyim81.github.io/vora-extension/privacy-ios.html 이다. 게시 후 HTTP응답/본문 유지 여부는 별도로 확인한다.

후속 수정: iOS 전용 줄바꿈 CSS를 추가할 때 생성기의 f-string 중괄호 이스케이프 오류가 발생했다. 생성기를 수정하고 전체 정책 생성·Python 컴파일·6개 브라우저 조합을 다시 실행해 통과했다. 공개 HTML 내용은 정적 문서이며 생성기 오류가 런타임 스크립트로 실행되지는 않는다.
