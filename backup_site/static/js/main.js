(function ($) {
  "use strict";

  $(".navbar").on("click", ".collapse.in .noop", function () {
    $(this)
      .parent()
      .siblings()
      .removeClass("expand")
      .end()
      .toggleClass("expand");
  });

  $(function () {
    $("body")
      .on("input propertychange", ".floating-label-form-group", function (e) {
        $(this).toggleClass(
          "floating-label-form-group-with-value",
          !!$(e.target).val()
        );
      })
      .on("focus", ".floating-label-form-group", function () {
        $(this).addClass("floating-label-form-group-with-focus");
      })
      .on("blur", ".floating-label-form-group", function () {
        $(this).removeClass("floating-label-form-group-with-focus");
      });
  });

  $(".noop").click(function (e) {
    e.preventDefault();
  });

  $("#newsletter-form").submit(function () {
    $.ajax({
      url: $("#newsletter-form").attr("action"),
      type: "POST",
      dataType: "json",
      data: $("#newsletter-form").serialize(),
      success: function (data) {
        if (data.success) {
          $("#form-status")
            .fadeOut("fast")
            .html("Você foi cadastrado com sucesso!")
            .removeClass("error")
            .addClass("success")
            .fadeIn();
          $("#newsletter-form")[0].reset();
        } else {
          var msg = data.errors[0][1];
          if (msg === "Este campo é obrigatório.") {
            msg = "Preencha todos os campos.";
          }

          $("#form-status")
            .fadeOut("fast")
            .html(msg)
            .removeClass("success")
            .addClass("error")
            .fadeIn();
        }
      },
    });
    return false;
  });

  $(".selected-langugage").click(function (e) {
    e.preventDefault();
  });

  $(".language-switcher").click(function (e) {
    e.preventDefault();
    var $el = $(this);
    var target = $el.data("lang");
    $el.parents("form").children("[name=language]").val(target).end().submit();
  });
  $(".mapboxgl-marker")
    .mouseover(function () {
      var id = $(this).data("id");
      $(".list-item-" + id).css("border-color", "rgb(41, 162, 199)");
    })
    .mouseout(function () {
      var id = $(this).data("id");
      $(".list-item-" + id).css({ "border-color": "#D7D6D6" });
    });

  // Espera o DOM carregar completamente
  document.addEventListener("DOMContentLoaded", function () {
    // Navbar scroll effect
    const navbar = document.querySelector(".navbar");
    let lastScroll = 0;

    window.addEventListener("scroll", () => {
      const currentScroll = window.pageYOffset;

      if (currentScroll <= 0) {
        navbar.classList.remove("scroll-up");
        return;
      }

      if (
        currentScroll > lastScroll &&
        !navbar.classList.contains("scroll-down")
      ) {
        // Scroll Down
        navbar.classList.remove("scroll-up");
        navbar.classList.add("scroll-down");
      } else if (
        currentScroll < lastScroll &&
        navbar.classList.contains("scroll-down")
      ) {
        // Scroll Up
        navbar.classList.remove("scroll-down");
        navbar.classList.add("scroll-up");
      }
      lastScroll = currentScroll;
    });

    // Smooth scroll para links internos
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      });
    });

    // Animação de fade-in para elementos
    const fadeElements = document.querySelectorAll(".fade-in");
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = 1;
          entry.target.style.transform = "translateY(0)";
        }
      });
    });

    fadeElements.forEach((element) => {
      element.style.opacity = 0;
      element.style.transform = "translateY(20px)";
      element.style.transition = "opacity 0.5s ease, transform 0.5s ease";
      observer.observe(element);
    });

    // Dropdown hover effect para desktop
    const dropdowns = document.querySelectorAll(".dropdown");
    if (window.innerWidth > 768) {
      dropdowns.forEach((dropdown) => {
        dropdown.addEventListener("mouseenter", function () {
          this.querySelector(".dropdown-menu").classList.add("show");
        });

        dropdown.addEventListener("mouseleave", function () {
          this.querySelector(".dropdown-menu").classList.remove("show");
        });
      });
    }

    // Lazy loading para imagens
    const lazyImages = document.querySelectorAll("img[data-src]");
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute("data-src");
          imageObserver.unobserve(img);
        }
      });
    });

    lazyImages.forEach((img) => imageObserver.observe(img));

    // Validação de formulários
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
      form.addEventListener("submit", function (e) {
        if (!form.checkValidity()) {
          e.preventDefault();
          e.stopPropagation();
        }
        form.classList.add("was-validated");
      });
    });

    // Tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Popovers do Bootstrap
    const popoverTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl);
    });

    // Back to top button
    const backToTopButton = document.createElement("button");
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopButton.className = "back-to-top";
    document.body.appendChild(backToTopButton);

    window.addEventListener("scroll", () => {
      if (window.pageYOffset > 300) {
        backToTopButton.classList.add("show");
      } else {
        backToTopButton.classList.remove("show");
      }
    });

    backToTopButton.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });

    // Submenu dropdown
    document.addEventListener("DOMContentLoaded", function () {
      // Função para fechar todos os submenus
      function closeAllSubmenus() {
        document.querySelectorAll(".dropdown-menu").forEach((menu) => {
          menu.style.display = "none";
        });
      }

      // Gerenciar dropdowns em desktop
      if (window.innerWidth >= 768) {
        document.querySelectorAll(".dropend").forEach((dropdown) => {
          dropdown.addEventListener("mouseenter", function () {
            const submenu = this.querySelector(".dropdown-menu");
            if (submenu) {
              submenu.style.display = "block";
            }
          });

          dropdown.addEventListener("mouseleave", function () {
            const submenu = this.querySelector(".dropdown-menu");
            if (submenu) {
              submenu.style.display = "none";
            }
          });
        });
      }

      // Gerenciar dropdowns em mobile
      if (window.innerWidth < 768) {
        document
          .querySelectorAll(".dropend > .dropdown-toggle")
          .forEach((toggle) => {
            toggle.addEventListener("click", function (e) {
              e.preventDefault();
              e.stopPropagation();

              const submenu = this.nextElementSibling;
              const isVisible = submenu.style.display === "block";

              // Fecha todos os outros submenus
              closeAllSubmenus();

              // Toggle do submenu atual
              submenu.style.display = isVisible ? "none" : "block";
            });
          });
      }
    });
  });
})(jQuery);
