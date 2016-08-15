$(document).ready(function() {
    $('a[rel="blank"]').attr("target", "_blank");

    $('input#busca-keyword').resetDefaultValue("Digite a sua busca..");
    $('input#newsletter-nome').resetDefaultValue("Digite o seu nome..");
    $('input#newsletter-email').resetDefaultValue("Digite o seu e-mail..");

    $('#newsletter-form').submit(function() {
        $.ajax({
          url: $('#newsletter-form').attr('action'),
          type: 'POST',
          data: $('#newsletter-form').serialize(),
          success: function(data) {
            var json = jQuery.parseJSON(data);
            if (json.success) {
                $('#form-status')
                    .fadeOut('fast')
                    .html('Você foi cadastrado com sucesso!')
                    .removeClass('error')
                    .addClass('success')
                    .fadeIn();
                $('#newsletter-nome').val("Digite o seu nome..");
                $('#newsletter-email').val("Digite o seu e-mail..");
            } else {
                $('#form-status')
                    .fadeOut('fast')
                    .html(json.errors[0][1])
                    .removeClass('success')
                    .addClass('error')
                    .fadeIn();
            }
          }
        });
        return false;
    });

    $('#contato-form').submit(function() {
        $('#contato-form .spinner').css('display', 'block');
        
        $.ajax({
          url: $('#contato-form').attr('action'),
          type: 'POST',
          data: $('#contato-form').serialize(),
          complete: function() {
              $('#contato-form .spinner').css('display', 'none');
          },
          success: function(data) {
            var json = jQuery.parseJSON(data);

            $('#contato-form p.error').remove();
            $('#contato-form .errored').removeClass('errored');

            if (json.success) {
                $('#form-status')
                    .fadeOut('fast')
                    .html('Contato enviado com sucesso!')
                    .removeClass('error')
                    .addClass('success')
                    .fadeIn();
                    
                jQuery('#contato-form input[type="text"], #contato-form textarea').val('');
            } else {
                $('#form-status')
                    .fadeOut('fast')
                    .html("Por favor, corrija os erros abaixo.")
                    .removeClass('success')
                    .addClass('error')
                    .fadeIn();
                
                $("#nome").focus();
                $.each(json.errors, function(index, value) {
                    $("#"+value[0]).addClass('errored');
                    $('<p class="error">'+value[1]+'</p>').insertAfter("#"+value[0]);
                })
            }
          }
        });
        return false;
    });
    
    $('#exibe-servicos').click(function(){
        $("#exibe-produtos").parent().parent().removeClass("selected");
        $(this).parent().parent().addClass("selected");
        $('#destaques-produtos').removeClass("mostra-destaque");
        $('#destaques-servicos').addClass("mostra-destaque");
        ajustaSetas();
        return false;
    });
    
    $('#exibe-produtos').click(function(){
        $("#exibe-servicos").parent().parent().removeClass("selected");
        $(this).parent().parent().addClass("selected");
        $('#destaques-servicos').removeClass("mostra-destaque");
        $('#destaques-produtos').addClass("mostra-destaque");
        ajustaSetas();
        return false;
    });
    
    $('.seta-esquerda').click(function() {
        moveSlider('backwards');
        return false;
    });

    $('.seta-direita').click(function() {
        moveSlider('forwards');
        return false;
    });
    
    function moveSlider(direction) {
         
         el = $('.scroller-wrap:visible .scroller');
         data = el.parent().data("scroller");
         seta_direita = $('a.seta-direita');
         seta_esquerda = $('a.seta-esquerda');
         
        if (direction == 'forwards') {
            data.proximaPagina = data.paginaAtual + 1;
            data.paginaAnterior = data.paginaAtual - 1;
        } else {
            data.proximaPagina = data.paginaAtual - 1;
            data.paginaAnterior = data.paginaAtual + 1;
        }

        /* Apenas faça as operações se esta não for a última(única) pagina */
        if ((direction == 'forwards' && data.paginaAtual < data.totalPaginas) || (direction == 'backwards' && data.paginaAtual > 1)) {
            data.paginaAtual = data.proximaPagina;

            ajustaSetas();

            /* Manipulando a animação */
            el.animate({
                'margin-left': 596 * ((data.proximaPagina-1) * -1)
            }, 350);
        }
    }
    
    function ajustaSetas() {
        
        el = $('.scroller-wrap:visible .scroller');
        data = el.parent().data("scroller");
        seta_direita = $('a.seta-direita');
        seta_esquerda = $('a.seta-esquerda');
        
        if (data.totalPaginas > 1) {
            if (data.paginaAtual == 1) {
                seta_esquerda.addClass('seta-esquerda-inactive');
                seta_direita.removeClass('seta-direita-inactive');
            } else if (data.paginaAtual == data.totalPaginas) {
                seta_esquerda.removeClass('seta-esquerda-inactive');
                seta_direita.addClass('seta-direita-inactive');
            } else {
                seta_esquerda.removeClass('seta-esquerda-inactive');
                seta_direita.removeClass('seta-direita-inactive');
            }
        } else {
            seta_esquerda.addClass('seta-esquerda-inactive');
            seta_direita.addClass('seta-direita-inactive');
        }
        
    }
    
});