var swiper = new Swiper(".newsSwipper", {
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});

var categoriesSwipper = new Swiper(".categoriesSwipper", {
  slidesPerView: 5,
  spaceBetween: 30,
});

$(document).ready(function () {
  $(".phone_menu, .language").hide();

  $(".phone_items button").click(function (event) {
    event.stopPropagation();
    $(".phone_menu").slideToggle(200);
    $(".language").slideUp(200);
  });

  $(".language_menu button").click(function (event) {
    event.stopPropagation();
    $(".language").slideToggle(200);
    $(".phone_menu").slideUp(200);
  });

  $(document).click(function () {
    $(".phone_menu, .language").slideUp(200);
  });

  $(".phone_menu, .language").click(function (event) {
    event.stopPropagation();
  });

  $("#catalog_main_toggle").click(function () {
    $(".catalog_content").toggleClass("active");
    $("svg").toggleClass("rotated");
  });
});
