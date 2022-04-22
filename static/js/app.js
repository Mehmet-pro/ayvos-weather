$(document).ready(function(){
    $(".location").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $($(this).parent().children("a")).filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });

  $(document).on("click",".accordion",function(){
    let content = $(this).next();
    if (content.css('height') != "0px") {
      content.css({'height':'0'});
    } else {
      content.css({'height':(content.prop('scrollHeight') +30)+ "px"}); ;
    }
  });

  $(document).ready(function() {
    $("#filter-form").validate({
        rules: {
            from: {
                required: {
                    depends: function(elem) {
                        return $("#till").val() != "";
                    }
                },
            },
            till: {
                required: {
                    depends: function(elem) {
                        return $("#from").val() != "";
                    }
                },
            }
        }
    });
});