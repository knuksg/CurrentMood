const burger = document.querySelector(".burger");
const nav = document.querySelector(".nav-links");
const navlinks = document.querySelectorAll(".nav-links li");


const navAnimation = () => {
  navlinks.forEach((link, index) => {
    // 애니메이션이 있을 때
    if (link.style.animation) {
      // 애니메이션 비움
      link.style.animation = "";
    } else {
      // 애니메이션 없을 때 애니메이션을 추가
      // 딜레이 간격을 줘서 li가 하나씩 차례대로 나타나도록 설정
      link.style.animation = `navLinkFade 0.5s ease forwards ${
        index / 7 + 0.5
      }s`;
    }
  });
};
const handleNav = () => {
  nav.classList.toggle("nav-active");

  //nav Animation
  navAnimation();

  //burger Animation
  burger.classList.toggle("toggle");
};
const navSlide = () => {
  burger.addEventListener("click", handleNav);
};





const setNavTransition = (width) => {
  if (width > 768) {
    nav.style.transition = "";
  } else {
    nav.style.transition = "transform 0.5s ease-in";
  }
};

const handleResize = () => {
  const width = event.target.innerWidth;
  setNavTransition(width);
};




const init = () => {
  // Toggle Nav
  window.addEventListener("resize", handleResize);
  navSlide();
};

init();