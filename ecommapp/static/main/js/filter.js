$(document).ready(function(){
  var width = $(this).width();
  if(width<420)
  {
    $(".filter-list").hide();
  }
});

$(".filter-toggle-btn").click(function(){
  $(".filter-list").slideToggle();
});
