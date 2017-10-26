$('.side-nav-li').hover(function(){
  $(this).children('.side-nav-sub-list').slideDown();
},function(){
  $(this).children('.side-nav-sub-list').slideUp();
}
);
