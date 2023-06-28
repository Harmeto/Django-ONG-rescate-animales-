document.addEventListener('DOMContentLoaded', function() {
    const formContainer = document.getElementById('form-container');
    const solicitarBtn = document.getElementById('solicitar-btn');
    const cancelarBtn = document.getElementById('cancelar-btn')

    solicitarBtn.addEventListener('click', function() {
        formContainer.classList.remove('d-none');
        solicitarBtn.style.display = 'none';
    });

    cancelarBtn.addEventListener('click', ()=>{
        formContainer.classList.add('d-none');
        solicitarBtn.style.display = 'block';
    })
});