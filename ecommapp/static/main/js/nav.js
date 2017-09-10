var showing = false;

$(".main-navbar-button").click(function(){

  if(showing === false)
    {
      $('#full-list').slideDown();
      showing = true;
    }
  else
    {
      $('#full-list').slideUp();
      showing = false;
    }
});


$(".mobile-list-link").click(function(){
  $('.mobile-list-sub:visible').slideUp();
      $(this).children('.mobile-list-sub:hidden').slideDown();

});
