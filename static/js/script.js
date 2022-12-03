// 네비게이션 햄버거
const toggleBtn = document.querySelector('.navbar__togleBtn');
const links = document.querySelector('.navbar__links');

toggleBtn.addEventListener('click', () => {
    links.classList.toggle('active');
});

// 마이페이지 라디오버튼
document.getElementById('radioform').addEventListener("click",  function() {
  var check_id = Array.from(radioform).find(radio => radio.checked).getAttribute('id').replace('radio', '');
  console.log(check_id)
  var radios = document.getElementsByName('menu');
  for (var i=1; i<=radios.length; i++)
  {
      // 체크된 라디오가 현재 인덱스의 id와 같다면
      // -> show
      if (check_id === String(i)) {
      document.querySelector('#cab'+String(i)).setAttribute('style', 'display: block')
      }
      // 다르다면
      // -> hide
      else {
      document.querySelector('#cab'+String(i)).setAttribute('style', 'display: none')
      }
  }
  })