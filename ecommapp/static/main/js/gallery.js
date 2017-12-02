$(document).ready(function(){
  $(".small-image").click(function(){
    var source;
    var image = document.getElementById("mainImage");
    $(".small-image").removeClass("active");
    $(this).addClass("active");
    source = $(this).children("img").attr("src");
    image.src = source;
  });
});
