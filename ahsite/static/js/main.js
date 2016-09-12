// Freelancer Theme JavaScript

(function($) {
    "use strict"; // Start of use strict

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a').click(function(){
        $('.navbar-toggle:visible').click();
    });

    // Offset for Main Navigation
    $('#mainNav').affix({
        offset: {
            top: 100
        }
    })

    // Floating label headings for the contact form
    $(function() {
        $("body").on("input propertychange", ".floating-label-form-group", function(e) {
            $(this).toggleClass("floating-label-form-group-with-value", !!$(e.target).val());
        }).on("focus", ".floating-label-form-group", function() {
            $(this).addClass("floating-label-form-group-with-focus");
        }).on("blur", ".floating-label-form-group", function() {
            $(this).removeClass("floating-label-form-group-with-focus");
        });
    });

    $('.noop').click(function(e) {
        e.preventDefault();
    });

    $('#newsletter-form').submit(function() {
        $.ajax({
          url: $('#newsletter-form').attr('action'),
          type: 'POST',
          dataType: 'json',
          data: $('#newsletter-form').serialize(),
          success: function(data) {
            if (data.success) {
                $('#form-status')
                    .fadeOut('fast')
                    .html('Você foi cadastrado com sucesso!')
                    .removeClass('error')
                    .addClass('success')
                    .fadeIn();
                $('#newsletter-form')[0].reset();
            } else {
                var msg = data.errors[0][1];
                if (msg === 'Este campo é obrigatório.') {
                    msg = 'Preencha todos os campos.';
                }

                $('#form-status')
                    .fadeOut('fast')
                    .html(msg)
                    .removeClass('success')
                    .addClass('error')
                    .fadeIn();
            }
          }
        });
        return false;
    });

})(jQuery); // End of use strict
