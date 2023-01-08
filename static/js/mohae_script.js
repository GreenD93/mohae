  $(document).ready(function() {
    // 화면에 따라 메뉴바 active 클래스 추가
    var screen = $("#screen_check").val();
    if (screen == 'project_description') {
      $("#nav_project").addClass("active");
    } else if (screen == 'consultant'){
      $("#nav_consultant").addClass("active");
    }

    // 프로젝트 캐러셀 관련 옵션
    $('.my-1 > .owl-carousel').owlCarousel({
      stagePadding:100,
      autoplay:true,
      autoplayTimeout:2000,
      autoplayHoverPause:true,
      loop:true,
      margin:0,
      nav:true,
      navText:['<i class="fas fa-angle-left"></i>', '<i class="fas fa-angle-right"></i>'],
      responsive:{
          0:{
              items:1
          }
      }
    });

    // 견적문의 화면 관련 자동완성 옵션 off
    $(".form-control_new").prop("autocomplete", "off");
    $(".form-input").prop("autocomplete", "off");
    $(".dform").prop("autocomplete", "off");

    // 날짜 입력란 이벤트 옵션 설정
    $('.datepicker').datepicker({
      changeMonth: true, // 월을 바꿀수 있는 셀렉트 박스를 표시한다.
      changeYear: true, // 년을 바꿀 수 있는 셀렉트 박스를 표시한다.
      minDate: '-100y', // 현재날짜로부터 100년이전까지 년을 표시한다.
      nextText: '다음 달', // next 아이콘의 툴팁.
      prevText: '이전 달', // prev 아이콘의 툴팁.
      numberOfMonths: [1,1], // 한번에 얼마나 많은 월을 표시할것인가. [2,3] 일 경우, 2(행) x 3(열) = 6개의 월을 표시한다.
      stepMonths: 1, // next, prev 버튼을 클릭했을때 얼마나 많은 월을 이동하여 표시하는가.
      yearRange: 'c-5:c+5', // 년도 선택 셀렉트박스를 현재 년도에서 이전, 이후로 얼마의 범위를 표시할것인가.
      showButtonPanel: true, // 캘린더 하단에 버튼 패널을 표시한다.
      currentText: '오늘 날짜' , // 오늘 날짜로 이동하는 버튼 패널
      closeText: '닫기',  // 닫기 버튼 패널
      dateFormat: "yy-mm-dd", // 텍스트 필드에 입력되는 날짜 형식.
      showAnim: "slide", //애니메이션을 적용한다.
      showMonthAfterYear: true , // 월, 년순의 셀렉트 박스를 년,월 순으로 바꿔준다.
      dayNamesMin: ['월', '화', '수', '목', '금', '토', '일'], // 요일의 한글 형식.
      monthNamesShort: ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월'], // 월의 한글 형식
      //yearRange: "2022:2023" //연도 범위
    });

    // checkbox 기타 입력란 감지 이벤트 start
    $("#facility_category_etc").on('keyup', function (){
      $("#facility_category").prop('checked',true);
      if ($("#facility_category_etc").val().length == 0) {
          $("#facility_category").prop('checked',false);
      }
    })
    $("#expand_type_etc").on('keyup', function (){
      $("#expand_type5").prop('checked',true);
      if ($("#expand_type_etc").val().length == 0) {
          $("#expand_type5").prop('checked',false);
      }
    })
    $("#sash_type_etc").on('keyup',function (){
      $("#sash_type4").prop('checked',true);
      if ($("#sash_type_etc").val().length == 0) {
          $("#sash_type4").prop('checked',false);
      }
    })
    $("#floor_type_etc").on('keyup',function (){
      $("#floor_5").prop('checked',true);
      if ($("#floor_type_etc").val().length == 0) {
          $("#floor_5").prop('checked',false);
      }
    })
    $("input[name='floor_type']").on("change", function() {
      $("#floor_type_etc").val("");
    })
    // checkbox 기타 입력란 감지 이벤트 end
});

// 견적문의 제출 버튼 클릭
function submitButton2(){
  // 제출 확인 팝업
  Swal.fire({
      title: '견적문의를 제출하시겠습니까?',
      text: "제출 시 초기화면으로 이동합니다.",
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: '제출',
      cancelButtonText: '취소'
  }).then((result) => {
    $(document).off('focusin.modal');
      if (result.isConfirmed) {
        var valid = validFields();
        $(".dform").attr('disabled', true);
        if (valid == "submit") {
          $("#contactForm").submit();
          //location.href="http://172.30.1.15:5000/#home";
        } else {
          Swal.fire({
            icon: 'error',
            title: $("#label_"+valid+"").text()+'을(를) 확인하세요.',
          })
        }
      }
  });
}

// 유효성 검사 관련 함수
function validateEmail(email) {

    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;

    return re.test(email);
}

function telValidator(args) {

    const msg = '유효하지 않는 전화번호입니다.';

    if (/^[0-9]{8,13}/.test(args)) {
        return true;
    }
    return false;
}

function validFields() {
    var valid = "submit";
    var frm = $("#contactForm :input");       // 전체 input 태그 목록
    var chk_ele = ['name', 'phone', 'email']; // valid 대상 태그 Array

    // 주소 1줄로 합치기
    address = $("#sample6_postcode").val() + " \n        "
              + $("#sample6_address").val() + " "
              + $("#sample6_detailAddress").val() + " \n        "
              + $("#sample6_extraAddress").val();

    if( $("#sample6_postcode").val() == null ||  $("#sample6_postcode").val() == "") {
      $("#hid_address").val("미등록");
    } else {
      $("#hid_address").val(address);
    }

    frm.each(function(idx, ele) {
      var name = $(ele).attr("name");
      var value = $(ele).val();
      var result = true;
      // valid 체크 대상 목록 중 값이 없으면 입력 권고
      if (chk_ele.includes(name)) {

        if (value == "" || value == null) {
            result = false;
        } else if (name=="phone"){
            result = telValidator(value)
        } else if (name=="email"){
            result = validateEmail(value)
        }

        if (result == false) {
            valid = name;
            return false
        }
      }
		});
		return valid;
	}
