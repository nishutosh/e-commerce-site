$(".search-btn").click(function(){
  var searchUrl = $(this).attr("data-url");
  searchUrl = encodeURI(searchUrl + "?search_term="+ $('input[name=search_term]').val());
  $.get(searchUrl,function(data,status){
    console.log(data + "Is the response from server for elastic search");
  })
});

$("#filter-btn").click(function(){
  var filters = "";
  $(".filter-input:checked").each(
    function(){
      filters = filters + $(this).val();
    }
  );
  console.log(filters);
  var search_url = "/search";
  var updated_url = encodeURI(search_url + "?search_term="+ filters);
  $.get(updated_url,function(data,status){
    console.log(data + "Is the response from server for elastic search");
  })
});
