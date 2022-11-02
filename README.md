# DjangoCustomUser
페이징 기능 구현<br>
로그인 되어있을때 로그인 페이지로 가면 로그아웃이 뜨도록 설정<br>
게시판 리스트 댓글 유저 이름 보이기<br>
정렬기능 추가<br>
	-> (기본)최근 생성일 순<br>
	-> 오래된 생성일 순<br>
	-> 좋아요 오름차 순서<br>
	-> 좋아요 내림차 순서<br>
검색기능 추가<br>
	-> 게시판 이름 기준으로 검색<br>
	-> 작성자 이름 기준으로 검색<br>
메인페이지 추가 <br>
시간 수정<br>
	-> 한국 시간 기준으로 변경<br>
유저 이름 중복 출력<br>
회원가입 체크<br>
유저 정보 수정 추가<br>
	-> 유효성 검증 로직 회원가입과 공유<br>
조회수 기능 추가<br>
	-> model visit(int) 값 추가 <br>
	-> 조회수 오름차순 정렬 추가<br>
	-> 조회수 내림차순 정렬 추가<br>
	-> 블로그에 조회수 표시<br>
	-> 블로그 내부에 조회수 표시<br>
다른 로그인일때 접근시 해당 유저 정보 표시<br>
	-> following, followers 추가<br>
	-> 팔로우, 취소 기능 추가 <br>
블로그 페이지 표시 수정<br>
	-> 작성자 링크 추가<br>
이미지 저장<br>
	-> html로 변환하는 로직 추가 <br>
	-> 템플릿 유저 수정페이지 이미지 등록 구현<br>
	-> setting image url 추가<br>
	-> 게시판에 image 추가<br>
	-> 프로필 수정 페이지 이미지 업로드 추가<br>
	-> 프로필 사진 자동 삭제 적용<br>
테그 추가<br>
	-> model tag 추가<br>
	-> tag 테이블 추가<br>
	-> tag 추가 로직 생성<br>
	-> 생성시 tag 추가<br>
	-> tag 에러 로직 추가<br>
	-> tag 중복 체크<br>
	-> 편집 tag 추가<br>
검색 기능 수정<br>
	-> 유저 이름 필터링 수정<br>
	-> 블로그 제목 필터링 수정<br>
<br>
테스트 코드에서 object.create => post(‘create_user’) 으로 변경<br>
테스트 코드 setUpClass 유저 생성 로직 구현<br>
테스트 코드 생성된 테스트 계정 출력<br>
테스트 코드 유저 생성 테스트 구현<br>
테스트 코드 로그인 테스트 (cookie)<br>
테스트 코드 유저 정보 수정 테스트 (기존 유저값과 수정된 유저값 비교)<br>
	-> 수정후 저장되지 않은 부분 수정<br>
테스트 코드 블로그 생성 (로그인 유지 하면서 블로그 생성)<br>
	-> 테스트시에 HTTP_REFERER 에러 해결<br>
