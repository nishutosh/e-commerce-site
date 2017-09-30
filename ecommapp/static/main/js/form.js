// styling input elements
$(document).ready(function(){
  styleInput();
});

$("input").change(function(){
  styleInput();
});

function styleInput()
{
  $("input").each(function(){
    if($(this).val()!== "")
    {
      $(this).siblings(".control-label").css({
        "top":"-20px"
      });
    }
    if($(this).attr("type")== "checkbox")
    {
      $(this).siblings(".orange-line").hide();
      $(this).siblings(".control-label").css({
        "top":"0px"
      });
    }
  });
}
