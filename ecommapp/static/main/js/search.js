$(".search-btn").click(function(){
  var searchUrl = $(this).attr("data-url");
  $.get(searchUrl,function(data,status){
    console.log(data + "Is the response from server for elastic search");
  })
});
