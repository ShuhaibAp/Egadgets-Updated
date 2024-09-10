  (function($) {
        "use strict";

        // Mobile Nav toggle
        var menuToggle = $('.menu-toggle > a');
        if(menuToggle.length > 0) {
          menuToggle.on('click', function (e) {
            e.preventDefault();
            $('#responsive-nav').toggleClass('active');
          });
        }

        // Fix cart dropdown from closing
        var cartDropdown = $('.cart-dropdown');
        if(cartDropdown.length > 0) {
          cartDropdown.on('click', function (e) {
            e.stopPropagation();
          });
        }

        /////////////////////////////////////////

        // Products Slick
        $('.products-slick').each(function() {
          var $this = $(this),
              $nav = $this.attr('data-nav');

          $this.slick({
            slidesToShow: 4,
            slidesToScroll: 1,
            autoplay: true,
            infinite: true,
            speed: 300,
            dots: false,
            arrows: true,
            appendArrows: $nav ? $nav : false,
            responsive: [{
                breakpoint: 991,
                settings: {
                  slidesToShow: 2,
                  slidesToScroll: 1,
                }
              },
              {
                breakpoint: 480,
                settings: {
                  slidesToShow: 1,
                  slidesToScroll: 1,
                }
              },
            ]
          });
        });

        // Products Widget Slick
        $('.products-widget-slick').each(function() {
          var $this = $(this),
              $nav = $this.attr('data-nav');

          $this.slick({
            infinite: true,
            autoplay: true,
            speed: 300,
            dots: false,
            arrows: true,
            appendArrows: $nav ? $nav : false,
          });
        });

        /////////////////////////////////////////

        // Product Main img Slick
        var productMainImg = $('#product-main-img');
        if (productMainImg.length > 0) {
          productMainImg.slick({
            infinite: true,
            speed: 300,
            dots: false,
            arrows: true,
            fade: true,
            asNavFor: '#product-imgs',
          });
        }

        // Product imgs Slick
        var productImgs = $('#product-imgs');
        if (productImgs.length > 0) {
          productImgs.slick({
            slidesToShow: 3,
            slidesToScroll: 1,
            arrows: true,
            centerMode: true,
            focusOnSelect: true,
            centerPadding: 0,
            vertical: true,
            asNavFor: '#product-main-img',
            responsive: [{
                breakpoint: 991,
                settings: {
                  vertical: false,
                  arrows: false,
                  dots: true,
                }
              },
            ]
          });
        }

        // Product img zoom
        var zoomMainProduct = document.getElementById('product-main-img');
        if (zoomMainProduct) {
          $('#product-main-img .product-preview').zoom();
        }

        /////////////////////////////////////////

        // Input number increment and decrement
        $('.input-number').each(function() {
          var $this = $(this),
              $input = $this.find('input[type="number"]'),
              up = $this.find('.qty-up'),
              down = $this.find('.qty-down');

          down.on('click', function () {
            var value = parseInt($input.val()) - 1;
            value = value < 1 ? 1 : value;
            $input.val(value);
            $input.change();
            updatePriceSlider($this , value);
          });

          up.on('click', function () {
            var value = parseInt($input.val()) + 1;
            $input.val(value);
            $input.change();
            updatePriceSlider($this , value);
          });
        });

        var priceInputMax = document.getElementById('price-max'),
            priceInputMin = document.getElementById('price-min');

        if(priceInputMax && priceInputMin) {
          priceInputMax.addEventListener('change', function(){
            updatePriceSlider($(this).parent(), this.value);
          });

          priceInputMin.addEventListener('change', function(){
            updatePriceSlider($(this).parent(), this.value);
          });
        }

        function updatePriceSlider(elem , value) {
          if ( elem.hasClass('price-min') ) {
            priceSlider.noUiSlider.set([value, null]);
          } else if ( elem.hasClass('price-max')) {
            priceSlider.noUiSlider.set([null, value]);
          }
        }

        // Price Slider
        var priceSlider = document.getElementById('price-slider');
        if (priceSlider) {
          noUiSlider.create(priceSlider, {
            start: [1, 999],
            connect: true,
            step: 1,
            range: {
              'min': 1,
              'max': 999
            }
          });

          priceSlider.noUiSlider.on('update', function(values, handle) {
            var value = values[handle];
            handle ? priceInputMax.value = value : priceInputMin.value = value;
          });
        }

      })(jQuery);