  // Activer Flatpickr pour tous les champs avec un type 'date'
  flatpickr("input[type='date'], input.flatpickr", {
    dateFormat: "Y-m-d",
    allowInput: true,
    defaultDate: "today", // Par défaut, mettre la date d'aujourd'hui
});

// Bootstrap validation (optionnel)
(function () {
    'use strict'
    const forms = document.querySelectorAll('.needs-validation')
    Array.from(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            form.classList.add('was-validated')
        }, false)
    })
})()