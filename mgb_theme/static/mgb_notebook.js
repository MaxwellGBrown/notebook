(function($) {
    var element = $('.follow-scroll'),
        originalY = element.offset().top;

    var topMargin = 20;
    
 
    element.css('position', 'relative');
    
    $(window).on('scroll', function(event) {
            var scrollTop = $(window).scrollTop();
            
            element.stop(false, false).animate({
                        top: scrollTop < originalY
                                ? 0
                                : scrollTop - originalY + topMargin
                    }, 300);
        });
})(jQuery);
