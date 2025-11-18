document.addEventListener('DOMContentLoaded', () => {
    const botaoTema = document.getElementById('tema-do-botao');
    const htmlElement = document.documentElement;

    const salvarTema = localStorage.getItem('tema-claro');
    if (salvarTema) {
        htmlElement.setAttribute('tema-claro-escuro', salvarTema);
    }

    if (botaoTema) {
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
    }

    const hamburgerButton = document.querySelector('.hamburger-button');
    const hamburgerMenu = document.querySelector('.hamburger-menu');

    if (hamburgerButton && hamburgerMenu) {
        hamburgerButton.addEventListener('click', () => {
            hamburgerMenu.classList.toggle('is-active');
        });
    }


    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    if (searchInput && searchResults) {
        searchInput.addEventListener('input', function() {
            const query = this.value;

            if (query.length > 0) { 
                fetch(`/api/buscar-livros/?q=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        searchResults.innerHTML = ''; 
                        
                        if (data.results.length > 0) {
                            searchResults.style.display = 'block'; 
                            
                            data.results.forEach(livro => {
                                const item = document.createElement('a');
                                item.href = `/livro/${livro.id}/`; 
                                item.classList.add('search-item');
                                    
                                item.innerHTML = `
                                    <img src="${livro.capa_url}" alt="${livro.titulo}">
                                    <div class="search-info">
                                        <h4>${livro.titulo}</h4>
                                        <p>${livro.autor}</p>
                                    </div>
                                `;
                                searchResults.appendChild(item);
                            });
                        } else {
                              searchResults.style.display = 'none';
                        }
                    });
            } else {
                searchResults.style.display = 'none'; 
            }
        });

        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });
    }
});

function scrollCarousel(gridId, direction) {
    const gridElement = document.getElementById(gridId);
    if (!gridElement) {
        console.error("Erro no Carrossel: Elemento do grid não encontrado:", gridId);
        return;
    }

    const scrollAmount = gridElement.clientWidth * 0.8; 

    gridElement.scrollBy({
        left: scrollAmount * direction,
        behavior: 'smooth'
    });
}