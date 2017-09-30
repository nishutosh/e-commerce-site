$('.side-nav-li').hover(function(){
  $(this).children('.side-nav-sub-list').slideDown();
},function(){
  $(this).children('.side-nav-sub-list').slideUp();
}
);

// $('.side-nav-li').mouseleave(function(){
//   $(this).children('.side-nav-sub-list').slideUp();
// });
