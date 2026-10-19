// Mobile menu
(function () {
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.textContent = open ? 'Close' : 'Menu';
    });
  }

  // Quote form. While the site is a draft (data-draft on the form), submissions are not sent
  // anywhere; the visitor sees how to reach the company instead. Remove data-draft once
  // form handling is set up with the chosen host.
  var form = document.getElementById('quote-form');
  if (form && form.hasAttribute('data-draft')) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = document.getElementById('form-status');
      if (status) {
        status.hidden = false;
        status.textContent = 'Preview only: this form is not connected yet. Once the site is live, requests will go straight to our customer care inbox. For now, please call 908-222-7111 or email innovativedisposablecsrcare@gmail.com.';
        status.scrollIntoView({ block: 'nearest' });
      }
    });
  }
})();
