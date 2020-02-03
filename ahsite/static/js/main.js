(function($) {
    "use strict";

    $('.navbar').on('click', '.collapse.in .noop', function() {
        $(this)
            .parent()
            .siblings()
                .removeClass('expand')
                .end()
            .toggleClass('expand');
    });

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

    $('.selected-langugage').click(function(e) {
        e.preventDefault();
    });

    $('.language-switcher').click(function(e) {
        e.preventDefault();
        var $el = $(this);
        var target = $el.data('lang');
        $el
            .parents('form')
                .children('[name=language]')
                    .val(target)
                    .end()
                .submit();
    });
    $( ".mapboxgl-marker" ).mouseover(function() {
        var id = $( this ).data("id");
        $(".list-item-"+id).css("border-color","rgb(41, 162, 199)")
    }).mouseout(function(){
        var id = $( this ).data("id");
        $(".list-item-"+id).css({"border-color":"#D7D6D6",});
    });
})(jQuery);
