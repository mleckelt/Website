jQuery(document).ready(function($){

 
/*==========================*/ 
/* Search show/hide */ 
/*==========================*/
$('.search-icon').click(function(){
    $('body').addClass('show-search');
    return false;
});

$('.close-search').click(function(){
    $('body').removeClass('show-search');
    return false;
});

/*==========================*/ 
/* Fix on Scroll */ 
/*==========================*/
$('.fix').theiaStickySidebar({
      // Settings
      additionalMarginTop: 90
    });

/*==========================*/  
/* Scroll on animate */  
/*==========================*/
function onScrollInit( items, trigger ) {
  items.each( function() {
    var osElement = $(this),
        osAnimationClass = osElement.attr('data-os-animation'),
        osAnimationDelay = osElement.attr('data-os-animation-delay');
      
        osElement.css({
          '-webkit-animation-delay':  osAnimationDelay,
          '-moz-animation-delay':     osAnimationDelay,
          'animation-delay':          osAnimationDelay
        });

        var osTrigger = ( trigger ) ? trigger : osElement;
        
        osTrigger.waypoint(function() {
          osElement.addClass('animated').addClass(osAnimationClass);
          },{
              triggerOnce: true,
              offset: '85%',
        });

// osElement.removeClass('fadeInUp');
  
  });

}

 onScrollInit( $('.os-animation') );
 onScrollInit( $('.staggered-animation'), $('.staggered-animation-container') );

 

$('.os-animation').each( function(index, element){
  $(element).waypoint({
      handler: function(){

        var osElementLoad = $(this),
        osAnimationClassLoad = osElementLoad.attr('data-os-animation'); 
          $(element).removeClass(osAnimationClassLoad);
      },offset: '200px'
  });
});


/*==========================*/  
/* Animated Number  */  
/*==========================*/   
  
  $('.timer').data('countToOptions', {
        formatter: function (value, options) {
          return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
        }
      });
 
      // start all the timers
      $('.timer').each(count);
 
      function count(options) {
        var $this = $(this);
        options = $.extend({}, options || {}, $this.data('countToOptions') || {});
        $this.countTo(options);
      }
    
   $('.stat-container .timer').waypoint(function() {
    $('.stat-container .timer').not('.animated').each(count);
  $('.stat-container .timer').addClass('animated');
},{offset: '95%'});
 

/*==========================*/  
/* Hero Slider */  
/*==========================*/
  var owlHero = $('.hero-slider');
  if (owlHero.length) {
    owlHero.on('initialized.owl.carousel', function(event) {
      owlHero.find('.owl-item.active').find('.animated').each(function() {
        $(this).addClass($(this).data('animate'));
      });
    });
    owlHero.owlCarousel({
      items: 1,
      loop: true,
      dots: true,
      nav: true,
      navText: ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
      autoplay:true,
      // autoplayHoverPause:true,
      autoplayTimeout: 4000
    });
    owlHero.on('changed.owl.carousel', function(event) {
      var owlItem = owlHero.find('.owl-item');
      owlItem.find('.animated').each(function() {
        $(this).removeClass($(this).data('animate'));
      });
      owlItem.eq(event.item.index).find('.animated').each(function() {
        $(this).addClass($(this).data('animate'));
      });
    });
  }


/*==========================*/  
/* Case Study Slider */  
/*==========================*/
var owlCase = $('.case-slider');
  if (owlCase.length) {
    owlCase.on('initialized.owl.carousel', function(event) {
      owlCase.find('.owl-item.active').find('.animated').each(function() {
        $(this).addClass($(this).data('animate'));
      });
    });
    owlCase.owlCarousel({
        center: true,
        loop:true,
        autoHeight:true,
        items:1,
        margin:35,
        stagePadding: 0,
        dots:true,
        nav:true,
     
    });
    owlCase.on('changed.owl.carousel', function(event) {
      var owlItem = owlCase.find('.owl-item');
      owlItem.find('.animated').each(function() {
        $(this).removeClass($(this).data('animate'));
      });
      owlItem.eq(event.item.index).find('.animated').each(function() {
        $(this).addClass($(this).data('animate'));
      });
    });
  }

 

/*==========================*/  
/* Testimonial Slider */  
/*==========================*/
 $('.testimonial-slider').owlCarousel({
    loop:true, 
     autoHeight:true,
    items:1,  
     dots:true,
     nav:false,
    
})

/*==========================*/  
/* Logo Slider */  
/*==========================*/
$('.logo-slider').owlCarousel({
    loop:true, 
     autoHeight:true,
    items:5,  
     dots:false,
     nav:false, 
     center: true,
      autoWidth:true, 
    loop:true,
    margin:100,
     autoplay:true,
    autoplayTimeout:3000,
    responsive:{
        600:{
            items:4
        }
    }
    
});


/*==========================*/  
/* Google Map */  
/*==========================*/
  if($('#map-canvas').length != 0){
    var map;
    function initialize() {
      var mapOptions = {
        zoom: 18,
        scrollwheel: false,
        center: new google.maps.LatLng(25.931743, 83.567199),
        styles: [
              {"stylers": [{ hue: "#00bcb4" },
              { saturation: 0 },
              { lightness: 0 }]},
              {
                "featureType": "road",
                "elementType": "labels",
                "stylers": [{"visibility": "off"}]
              },
              {
                "featureType": "road",
                "elementType": "geometry",
                "stylers": [{"lightness": 100},
                      {"visibility": "simplified"}]
              }
        ]
      };
      map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
      var image = 'include/images/map-marker.png';
      var myLatLng = new google.maps.LatLng(25.931743, 83.567199);
      var beachMarker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        icon: image
       });
    }

    google.maps.event.addDomListener(window, 'load', initialize);
  }

 
/*==========================*/  
/* Header fix */  
/*==========================*/
var scroll = $(window).scrollTop();

    if (scroll >= 10) {
        $("body").addClass("fixed");
    } else {
        $("body").removeClass("fixed");
    }
  
}); 

  

$(window).scroll(function() {    
    var scroll = $(window).scrollTop();

    if (scroll >= 10) {
        $("body").addClass("fixed");
    } else {
        $("body").removeClass("fixed");
    }


    
});
 
