// ===============================
// Barra de Pesquisa Avançada
// ===============================

// Conteúdos indexados
const conteudos = [
  { titulo: "Sobre Mim", pagina: "sobre-mim.html", target: ".sobre-mim", descricao: "Informações sobre Felipe Rocha Maia" },
  { titulo: "Minha Trajetória", pagina: "sobre-mim.html", target: ".minha-trajetoria", descricao: "História acadêmica e profissional" },
  { titulo: "Meus Objetivos", pagina: "sobre-mim.html", target: ".meus-objetivos", descricao: "Metas e planos de carreira" },
  { titulo: "Minhas Habilidades", pagina: "sobre-mim.html", target: ".minhas-habilidades", descricao: "Competências técnicas e ferramentas" },
  { titulo: "Contato", pagina: "contato.html", target: ".formulario-contato", descricao: "Formas de entrar em contato" },
  { titulo: "Portfólio", pagina: "portfolio.html", target: ".projeto1", descricao: "Projetos desenvolvidos" },
  { titulo: "Serviços", pagina: "servicos.html", target: ".servico1", descricao: "Lista de serviços oferecidos" }
];

const campoPesquisa = document.querySelector('.campo-pesquisa');
const resultadosDiv = document.querySelector('.resultados-pesquisa');
const formularioPesquisa = document.querySelector('.barra-pesquisa');

// Intercepta envio do formulário (Enter ou botão)
if (formularioPesquisa) {
  formularioPesquisa.addEventListener('submit', function(e) {
    e.preventDefault();
    executarPesquisa();
  });
}

// Sugestões enquanto digita
campoPesquisa.addEventListener('input', function() {
  const termo = campoPesquisa.value.toLowerCase();
  resultadosDiv.innerHTML = "";

  if (termo.length > 1) {
    const resultados = conteudos.filter(item =>
      item.titulo.toLowerCase().includes(termo) ||
      item.descricao.toLowerCase().includes(termo)
    );

    resultados.forEach(item => {
      const sugestao = document.createElement('div');
      sugestao.classList.add('sugestao');
      sugestao.innerHTML = `<strong>${item.titulo}</strong> — ${item.descricao}`;
      sugestao.addEventListener('click', () => {
        navegarPara(item);
      });
      resultadosDiv.appendChild(sugestao);
    });
  }
});

// Executa pesquisa ao enviar
function executarPesquisa() {
  const termo = campoPesquisa.value.toLowerCase();
  const resultado = conteudos.find(item =>
    item.titulo.toLowerCase().includes(termo) ||
    item.descricao.toLowerCase().includes(termo)
  );

  if (resultado) {
    navegarPara(resultado);
  }

  // Limpa campo após pesquisa
  campoPesquisa.value = "";
  resultadosDiv.innerHTML = "";
}

// Navega para página ou rola até seção
function navegarPara(item) {
  if (!window.location.pathname.endsWith(item.pagina)) {
    window.location.href = item.pagina;
  } else {
    const target = document.querySelector(item.target);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  }
}