// Ativa animações JS
document.documentElement.classList.add('js-ativado');

// Scroll suave para âncoras internas
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const targetSelector = this.getAttribute('href');
    const target = document.querySelector(targetSelector);
    if (target && targetSelector !== "#") {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Animação ao rolar a página
const elementosRevelar = document.querySelectorAll(
  '.subtitulo, .paragrafo, .projeto, .servico, .contato, .foto-container, .item-lista, .formulario-contato, .novos-projetos'
);

function revelarElementos() {
  elementosRevelar.forEach(el => {
    const topo = el.getBoundingClientRect().top;
    const alturaJanela = window.innerHeight;
    if (topo < alturaJanela - 100) {
      el.classList.add('ativo');
    }
  });
}

window.addEventListener('scroll', revelarElementos);
window.addEventListener('load', revelarElementos);

// Validação do formulário de contato
function validarEmail(email) {
  const regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  return regex.test(email);
}

const form = document.querySelector('.form-contato');
if (form) {
  form.addEventListener('submit', function (e) {
    const nome = form.querySelector('input[name="nome"]').value.trim();
    const email = form.querySelector('input[name="email"]').value.trim();
    const mensagem = form.querySelector('textarea[name="mensagem"]').value.trim();

    if (!nome || !email || !mensagem) {
      e.preventDefault();
      alert('Todos os campos são obrigatórios.');
    } else if (!validarEmail(email)) {
      e.preventDefault();
      alert('Por favor, insira um endereço de email válido.');
    }
  });
}

// Log de cliques em links externos
document.querySelectorAll('a[target="_blank"]').forEach(link => {
  link.addEventListener('click', function () {
    console.log(`Link externo clicado: ${this.href}`);
  });
});