console.log("contact_me.js carregado!");
$(function () {
  console.log("DOM carregado, inicializando formulário...");
  console.log("Procurando por #contactFormCompras...");
  console.log("Formulário encontrado:", $("#contactFormCompras").length);
  
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

// ===== ANIMAÇÕES PARA PÁGINA "QUEM SOMOS" =====

// Animação das frases rotativas
function initRotatingText() {
  const texts = document.querySelectorAll('.rotating-text');
  let currentIndex = 0;
  
  if (texts.length === 0) return;
  
  function rotateText() {
    texts.forEach((text, index) => {
      text.classList.remove('active');
      if (index === currentIndex) {
        text.classList.add('active');
      }
    });
    
    currentIndex = (currentIndex + 1) % texts.length;
  }
  
  // Rotacionar a cada 4 segundos
  setInterval(rotateText, 4000);
}

// Animação das partículas
function initParticles() {
  const particles = document.querySelectorAll('.particle');
  
  particles.forEach((particle, index) => {
    // Posicionar partículas aleatoriamente
    const top = Math.random() * 100;
    const animationDuration = 6 + Math.random() * 4; // 6-10 segundos
    
    particle.style.top = `${top}%`;
    particle.style.animationDuration = `${animationDuration}s`;
    particle.style.animationDelay = `${index * 0.5}s`;
  });
}

// ===== FLIPBOOK - NOSSA HISTÓRIA =====

let currentPage = 1;
const totalPagesHistoria = 5;

function changePage(direction) {
  const newPage = currentPage + direction;
  
  if (newPage >= 1 && newPage <= totalPagesHistoria) {
    goToPage(newPage);
  }
}

function goToPage(pageNumber) {
  if (pageNumber < 1 || pageNumber > totalPagesHistoria) return;
  
  // Esconder página atual
  const currentPageElement = document.querySelector(`[data-page="${currentPage}"]`);
  if (currentPageElement) {
    currentPageElement.style.display = 'none';
  }
  
  // Mostrar nova página
  const newPageElement = document.querySelector(`[data-page="${pageNumber}"]`);
  if (newPageElement) {
    newPageElement.style.display = 'block';
    newPageElement.classList.add('page-transition');
    
    // Remover classe de transição após animação
    setTimeout(() => {
      newPageElement.classList.remove('page-transition');
    }, 800);
  }
  
  // Atualizar indicadores
  updatePageIndicators(pageNumber);
  updateNavigationButtons(pageNumber);
  
  currentPage = pageNumber;
}

function updatePageIndicators(pageNumber) {
  const dots = document.querySelectorAll('.page-dot');
  dots.forEach((dot, index) => {
    dot.classList.remove('active');
    if (index === pageNumber - 1) {
      dot.classList.add('active');
    }
  });
}

function updateNavigationButtons(pageNumber) {
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  
  if (prevBtn) {
    prevBtn.disabled = pageNumber === 1;
  }
  
  if (nextBtn) {
    nextBtn.disabled = pageNumber === totalPagesHistoria;
  }
}

// Inicializar flipbook quando a página carregar
function initFlipbook() {
  if (document.querySelector('.flipbook-container')) {
    updateNavigationButtons(1);
  }
}

// ===== INICIALIZAÇÃO GERAL =====

document.addEventListener('DOMContentLoaded', function() {
  // Inicializar animações da página "Quem Somos" apenas se estivermos nela
  if (document.querySelector('.about-hero-modern')) {
    initRotatingText();
    initParticles();
  }
  
  // Inicializar flipbook apenas se estivermos na página "Quem Somos"
  if (document.querySelector('.flipbook-container')) {
    initFlipbook();
  }
  
  // Adicionar efeito de scroll suave para links internos
  const internalLinks = document.querySelectorAll('a[href^="#"]');
  internalLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });
  
  // Adicionar animação de entrada para elementos
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in-up');
      }
    });
  }, observerOptions);
  
  // Observar elementos que devem ter animação de entrada
  const animatedElements = document.querySelectorAll('.about-card, .flipbook-page, .chapter-title');
  animatedElements.forEach(el => {
    observer.observe(el);
  });
});
