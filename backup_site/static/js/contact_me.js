console.log("contact_me.js carregado!");

// Função para inicializar o formulário
function initializeForm() {
  console.log("DOM carregado, inicializando formulário...");
  console.log("Procurando por #contactFormCompras...");
  console.log("Formulário encontrado:", $("#contactFormCompras").length);
  
  // Verificar se o plugin jqBootstrapValidation está disponível
  if (typeof $.fn.jqBootstrapValidation === 'undefined') {
    console.error("jqBootstrapValidation não está disponível!");
    console.log("jQuery disponível:", typeof $ !== 'undefined');
    console.log("jQuery.fn disponível:", typeof $.fn !== 'undefined');
    // Tentar novamente em 100ms
    setTimeout(initializeForm, 100);
    return;
  }
  
  console.log("jqBootstrapValidation disponível, continuando...");
  
  $(
    "#contactFormCompras input,#contactFormCompras textarea,#contactFormCompras select"
  ).jqBootstrapValidation({
    preventSubmit: true,
    submitError: function ($form, event, errors) {
      // additional error messages or events
      console.log("Erro de validação:", errors);
    },
    submitSuccess: function ($form, event) {
      console.log("submitSuccess chamado!");
      // Prevent spam click and default submit behaviour
      $("#btnSubmit").attr("disabled", true);
      event.preventDefault();

      var server_url = $form.data("url");
      console.log("Enviando formulário para:", server_url);

      // get values from FORM
      var name = $("input#name").val();
      var email = $("input#email").val();
      var phone = $("input#phone").val();
      var city = $("input#city").val();
      var destinatario = $("select#destinatario").val();
      var message = $("textarea#message").val();

      var firstName = name; // For Success/Failure Message
      // Check for white space in name for Success/Fail message
      if (firstName.indexOf(" ") >= 0) {
        firstName = name.split(" ").slice(0, -1).join(" ");
      }

      $.ajax({
        url: server_url,
        type: "POST",
        data: {
          name: name,
          phone: phone,
          email: email,
          city: city,
          destinatario: destinatario,
          message: message,
        },
        cache: false,
        success: function (data) {
          console.log("Resposta do servidor:", data);
          $("#btnSubmit").attr("disabled", false);
          // Remove mensagens antigas
          $form.find(".alert").remove();

          // Verifica se a resposta é JSON
          var responseData;
          try {
            responseData = typeof data === "string" ? JSON.parse(data) : data;
          } catch (e) {
            responseData = { success: true };
          }

          if (responseData.success) {
            // Mensagem de sucesso
            var successHtml =
              '<div class="alert alert-success alert-dismissible fade show" role="alert" style="margin-bottom: 1rem;">' +
              '<i class="fa fa-check-circle"></i> Obrigado! Sua mensagem foi enviada com sucesso.' +
              '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
              "</div>";
            $form.prepend(successHtml);
            //clear all fields
            $("#contactFormCompras").trigger("reset");
          } else {
            // Mensagem de erro do servidor
            var errorHtml =
              '<div class="alert alert-danger alert-dismissible fade show" role="alert" style="margin-bottom: 1rem;">' +
              '<i class="fa fa-exclamation-circle"></i> Erro: ' +
              (responseData.message || "Algo deu errado. Tente novamente.") +
              '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
              "</div>";
            $form.prepend(errorHtml);
          }
        },
        error: function (xhr, status, error) {
          console.log("Erro na requisição:", status, error);
          console.log("Resposta do servidor:", xhr.responseText);
          $("#btnSubmit").attr("disabled", false);
          $form.find(".alert").remove();
          var errorHtml =
            '<div class="alert alert-danger alert-dismissible fade show" role="alert" style="margin-bottom: 1rem;">' +
            '<i class="fa fa-exclamation-circle"></i> Desculpe ' +
            firstName +
            ", parece que algo de errado aconteceu. Por favor, tente novamente mais tarde!" +
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
            "</div>";
          $form.prepend(errorHtml);
        },
      });
    },
    filter: function () {
      return $(this).is(":visible");
    },
  });

  $('a[data-toggle="tab"]').click(function (e) {
    e.preventDefault();
    $(this).tab("show");
  });
  
  // Fallback: interceptar submit diretamente caso jqBootstrapValidation não funcione
  $("#contactFormCompras").on("submit", function(e) {
    console.log("Submit interceptado diretamente!");
    e.preventDefault();
    
    var $form = $(this);
    var server_url = $form.data("url");
    console.log("Enviando formulário para:", server_url);

    // get values from FORM
    var name = $("input#name").val();
    var email = $("input#email").val();
    var phone = $("input#phone").val();
    var city = $("input#city").val();
    var destinatario = $("select#destinatario").val();
    var message = $("textarea#message").val();

    // Validação básica
    if (!name || !email || !phone || !city || !destinatario || !message) {
      alert("Por favor, preencha todos os campos obrigatórios.");
      return false;
    }

    $("#btnSubmit").attr("disabled", true);

    $.ajax({
      url: server_url,
      type: "POST",
      data: {
        name: name,
        phone: phone,
        email: email,
        city: city,
        destinatario: destinatario,
        message: message,
      },
      cache: false,
      success: function (data) {
        console.log("Resposta do servidor:", data);
        $("#btnSubmit").attr("disabled", false);
        $form.find(".alert").remove();

        var responseData;
        try {
          responseData = typeof data === "string" ? JSON.parse(data) : data;
        } catch (e) {
          responseData = { success: true };
        }

        if (responseData.success) {
          var successHtml =
            '<div class="alert alert-success alert-dismissible fade show" role="alert" style="margin-bottom: 1rem;">' +
            '<i class="fa fa-check-circle"></i> Obrigado! Sua mensagem foi enviada com sucesso.' +
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
            "</div>";
          $form.prepend(successHtml);
          $("#contactFormCompras").trigger("reset");
        } else {
          var errorHtml =
            '<div class="alert alert-danger alert-dismissible fade show" role="alert" style="margin-bottom: 1rem;">' +
            '<i class="fa fa-exclamation-circle"></i> Erro: ' +
            (responseData.message || "Algo deu errado. Tente novamente.") +
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
            "</div>";
          $form.prepend(errorHtml);
        }
      },
      error: function (xhr, status, error) {
        console.log("Erro na requisição:", status, error);
        $("#btnSubmit").attr("disabled", false);
        $form.find(".alert").remove();
        var errorHtml =
          '<div class="alert alert-danger alert-dismissible fade show" role="alert" style="margin-bottom: 1rem;">' +
          '<i class="fa fa-exclamation-circle"></i> Desculpe, parece que algo de errado aconteceu. Por favor, tente novamente mais tarde!' +
          '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
          "</div>";
        $form.prepend(errorHtml);
      },
    });
  });
});

// When clicking on Full hide fail/success boxes
$("#name").focus(function () {
  $(".alert").remove();
});

// Inicializar quando o DOM estiver pronto
$(function () {
  initializeForm();
});
