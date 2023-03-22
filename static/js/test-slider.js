function ChangeSlideMargin(s) {
  if ((s.width - (s.slides.length + 1) * 60) > 0){
      var margin = "0px";
  }
  else {
      var margin = "auto";
  }
  for (let index = 0; index < s.slides.length; index++) {
    s.slides[index].style.marginLeft=margin;
  }
}

var test_swiper = new Swiper(".test-slider", {
    simulateTouch: false,
    speed:0,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
      renderBullet: function (index, className) {
        return '<div class="swiper-slide ' + className + '">' + (index + 1) + '</div>';
      },
    },
  });
var pagination_swiper = new Swiper(".pagination-slider", {
    slidesPerView: 1,
    slidesPerGroup: 1,
    spaceBetween: 20,
    resistance: false,
    roundLengths: true,
    setWrapperSize: true,
    simulateTouch: false,
    centerInsufficientSlides: false,
    wrapperClass: 'swiper-pagination',
    navigation: {
    nextEl: ".pagination-slider_control.right",
    prevEl: ".pagination-slider_control.left",
    },
    breakpointsBase: 'container',
    breakpoints: {
      60: {
        slidesPerView: 1,
        slidesPerGroup: 1
      },
      120: {
        slidesPerView: 2,
        slidesPerGroup: 2
      },
      180: {
        slidesPerView: 3,
        slidesPerGroup: 3
      },
      240: {
        slidesPerView: 4,
        slidesPerGroup: 4
      },
      300: {
        slidesPerView: 5,
        slidesPerGroup: 5
      },
      360: {
        slidesPerView: 6,
        slidesPerGroup: 6
      },
      420: {
        slidesPerView: 7,
        slidesPerGroup: 7
      },
      480: {
        slidesPerView: 8,
        slidesPerGroup: 8
      },
      540: {
        slidesPerView: 9,
        slidesPerGroup: 9
      },
      600: {
        slidesPerView: 10,
        slidesPerGroup: 10
      },
      660: {
        slidesPerView: 11,
        slidesPerGroup: 11
      },
      720: {
        slidesPerView: 12,
        slidesPerGroup: 12
      },
      780: {
        slidesPerView: 13,
        slidesPerGroup: 13
      },
      840: {
        slidesPerView: 14,
        slidesPerGroup: 14
      },
      900: {
        slidesPerView: 15,
        slidesPerGroup: 15
      },
      960: {
        slidesPerView: 16,
        slidesPerGroup: 16
      },
      1120: {
        slidesPerView: 17,
        slidesPerGroup: 17
      },
      1180: {
       slidesPerView: 18,
        slidesPerGroup: 18
      },
      1240: {
        slidesPerView: 19,
        slidesPerGroup: 19
      },
      1300: {
        slidesPerView: 20,
        slidesPerGroup: 20
      },
      1360: {
        slidesPerView: 21,
        slidesPerGroup: 21
      }
    },
    on: {
      init: function () {
        ChangeSlideMargin(this);
      },
    },
  });

pagination_swiper.on('resize', function () {
  ChangeSlideMargin(this);
});