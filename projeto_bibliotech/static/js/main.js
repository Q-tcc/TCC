document.addEventListener('DOMContentLoaded', () => {


    const botaoTema = document.getElementById('tema-do-botao');
    const htmlElement = document.documentElement;


    const salvarTema = localStorage.getItem('tema-claro');
    if (salvarTema) {
        htmlElement.setAttribute('tema-claro-escuro', salvarTema);
    }


    botaoTema.addEventListener('click', () => {

        let temas = htmlElement.getAttribute('tema-claro-escuro');
        
        if (temas === 'dark') {
            htmlElement.setAttribute('tema-claro-escuro', 'light');
            localStorage.setItem('tema-claro', 'light');
        } else {
            htmlElement.setAttribute('tema-claro-escuro', 'dark');
            localStorage.setItem('tema-claro', 'dark');
        }
    });


    const hamburgerButton = document.querySelector('.hamburger-button');
    const hamburgerMenu = document.querySelector('.hamburger-menu');

    if (hamburgerButton && hamburgerMenu) {
        hamburgerButton.addEventListener('click', () => {

            hamburgerMenu.classList.toggle('is-active');
        });
    }
});