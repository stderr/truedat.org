$(document).ready(function() {
  // May as well offend some Seahawks fans while I'm at it. 
  $('a.btn-success,button.close').click(function() {
    opinion = $("#opinion");
    opinion.toggle();

    if(opinion.is(':visible')) {
      position = $(document).height()-$(window).height();
    }
    else {
      position = 0;
    }

    $('html, body').animate({scrollTop: position},1000,"swing");

  });

});

