$(document).ready(function(){
	//fdahead-nav
	$('.fdahead-nav-toggle').click(function () {
		$('.fdahead-nav').toggleClass('active', 300);
		if ($('.fdahead-nav').is(':hidden')) {
			$('.fdahead-nav-toggle').html('<span>show navigation</span>');
			
		} else {
			$('.fdahead-nav-toggle').html('<span>hide navigation</span>');
		}
		$('.nav').removeClass('active');
		$('.nav-toggle').html('show nav box');
	});
	
	$( ".fda-tabs-interface" ).tabs();
	$( ".fda-accordion-interface" ).accordion({
		collapsible: true,
		heightStyle: "content"
	});
});
  
    // search bar functionality
    var searchOptions = ['search_labels', 'search_events', 'search_enforcements'];

    // search go button onclick handler
    $("#search-category").click(function() {
        var url_category = $('#select-category').val();
        var search_term = $('#search-term').val();

        // stop the click event if the search term or category is falsey.
        if(!search_term || !url_category) {
            return false;
        }

        if (url_category === 'search_labels') {
            $('form').attr("action", "/search/labels/").submit();
        }
        else if (url_category === 'search_events') {
            $('form').attr("action", "/search/events/").submit();
        }
        else if (url_category === 'search_enforcements') {
            $('form').attr("action", "/search/enforcements/").submit();
        }
        else if (url_category === 'search_manufacturers') {
            $('form').attr("action", "/search/manufacturers/").submit();
        }
        else {
            console.log('unknown category' + url_category);
            return false;
        }
    });

    // functionality to support expand/collapse of divs for large bodies of text
        $(".panel-title a").click(function() {
            var panelTitle = this;
            setTimeout(function() {
                $(panelTitle).parents('.panel').first().find('.cell').each(function () {
                    var cell = this;
                    var text = $(cell).find(".text");
                    var more = $(cell).find(".more");
                    var less = $(cell).find(".less");

                    // correct for resizing
                    if ($(text).height() < 55) {
                        $(more).hide();
                        $(text).removeClass("text");
                    }

                    $(more).click(function () {
                        $(cell).addClass("expanded");
                        $(more).toggle();
                        $(less).toggle();
                    });

                    $(less).click(function () {
                        $(cell).removeClass("expanded");
                        $(more).toggle();
                        $(less).toggle();
                    });
                });
            }, 0);
        });
