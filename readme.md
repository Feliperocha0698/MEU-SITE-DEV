# Felipe Rocha Maia — FelipeCode

Site profissional estático em HTML5, CSS3 e JavaScript puro. Atendimento remoto no Brasil e no exterior. Domínio de produção: https://felipercode0698.com/.

Esta modernização está em desenvolvimento local na branch `modernizacao-site-profissional`. Nenhum comando deste guia faz commit, push, merge ou publicação.

## Visualização local

Na pasta do projeto, execute:

```powershell
python tools/preview_site.py
```

Abra http://127.0.0.1:8001/index.html?lang=pt-BR. A prévia local usa `Cache-Control: no-store` para carregar os arquivos atuais entre revisões. Se o navegador ainda mostrar uma versão antiga ou a porta estiver ocupada, use `python tools/preview_site.py --port 8002` e abra o endereço exibido. Para encerrar o servidor, pressione Ctrl+C.

Alternativa sem servidor: abra `index.html` diretamente no navegador. O conteúdo e os links de idiomas são estáticos; a persistência de preferência em URLs `file:` varia entre navegadores. A integração de e-mail deve ser testada por HTTP/HTTPS.

## Páginas e idiomas

| Página | Português (pt-BR) | Inglês (en) | Espanhol (es) |
| --- | --- | --- | --- |
| Início | index.html | en/index.html | es/index.html |
| Sobre Mim | sobre-mim.html | en/about.html | es/sobre-mi.html |
| Portfólio | portfolio.html | en/portfolio.html | es/portafolio.html |
| Serviços | servicos.html | en/services.html | es/servicios.html |
| Contato | contato.html | en/contact.html | es/contacto.html |

O seletor aponta para a página equivalente em cada idioma e salva a escolha manual no armazenamento local, quando permitido. A primeira entrada em português usa a preferência salva ou o primeiro idioma compatível do navegador; sem correspondência, mantém português. Uma URL explícita em inglês/espanhol e a seleção manual são respeitadas. O parâmetro `?lang=pt-BR` permite abrir a versão portuguesa sem detecção automática. A navegação interna permanece no idioma atual.

As páginas têm conteúdo traduzido no próprio HTML, canonical próprio, hreflang recíproco e `x-default` em português. Referência: [versões localizadas no Google Search Central](https://developers.google.com/search/docs/specialty/international/localized-versions). O sitemap lista as 15 URLs; não há versões canônicas de parâmetros de busca/idioma. O HTTPS e os redirecionamentos entre www, domínio sem www e index.html deverão ser conferidos na hospedagem somente em uma futura etapa autorizada.

## Organização e manutenção

- `assets/css/home.css`: base visual da home aprovada, compartilhada pelo site.
- `assets/css/site.css`: páginas internas e componentes adicionais.
- `assets/i18n/{pt-BR,en,es}.json`: conteúdo e mensagens de cada idioma.
- `assets/icons/`: bandeiras SVG locais; ícones de serviços estão incorporados no HTML.
- `js/home.js`: idiomas, pesquisa, filtros, teclado e ano do rodapé.
- `js/contact.js`: validação e integração opcional Web3Forms.
- `js/contact-config.js`: configuração pública do formulário, inicialmente desativada.
- `tools/build_site.py`: gera HTML, sitemap e robots a partir dos textos e do template compartilhado.
- `tools/check_site.py` e `tools/check_behavior.cjs`: verificações locais.
- `review/`: relatório e capturas de revisão; não faz parte das páginas do site.

Para alterar conteúdo, edite os três JSON e o template em `tools/build_site.py`, conforme a necessidade, e gere novamente:

```powershell
python tools/build_site.py
python tools/check_site.py
node tools/check_behavior.cjs
```

Python é uma ferramenta opcional de manutenção, não uma dependência da hospedagem. As páginas prontas funcionam sem build, frameworks, instalação de pacotes ou CDN. Evite editar apenas um HTML gerado: uma nova geração substituirá essa alteração.

Os CSS antigos (`reset.css`, `style.css`, `media_queries.css`) e scripts antigos (`script.js`, `pesquisa.js`) foram preservados como arquivos legados e não são carregados pelas páginas modernizadas. Os originais versionados continuam no histórico Git e na branch main. Imagens originais e links de projetos foram preservados.

## Formulário de contato

Não há FormSubmit nas páginas. O formulário tem nome completo, e-mail, WhatsApp internacional, serviço e descrição. Há validação localizada, associação de erros aos campos, foco no primeiro erro, honeypot, bloqueio de envios simultâneos e timeout no fluxo preparado de envio.

**O envio está habilitado na cópia local. O teste de entrega aguarda autorização.** Sem JavaScript, os campos permanecem desativados e os contatos diretos continuam disponíveis.

Configuração e teste de entrega:

1. No Web3Forms, usar o formulário `Felipercode0698` vinculado a `felipercode0698@gmail.com`. A chave desse formulário define o destinatário. O site envia com o assunto “Novo orçamento recebido - FelipeCode” nos três idiomas.
2. A Access Key pública está em `js/contact-config.js`, com `enabled: true` na cópia local.
3. Após autorização, enviar um orçamento de teste pela prévia HTTP/HTTPS. Conferir a resposta da API e confirmar a chegada da mensagem na caixa de entrada ou no spam.

O código só mostra confirmação se uma requisição real retornar HTTP bem-sucedido **e** `success: true`. Erros, respostas inválidas e timeout não limpam os dados preenchidos. Não existem respostas de sucesso simuladas nos testes.

Referências: [API Web3Forms](https://docs.web3forms.com/getting-started/api-reference) e [instalação Web3Forms](https://docs.web3forms.com/getting-started/installation).

## SEO e privacidade

- HTML semântico e conteúdo estático traduzido; metadados, Open Graph e dados estruturados Person, WebSite e WebPage.
- As qualificações são as informadas pelo profissional; não há avaliações, clientes, estatísticas ou certificações inventadas.
- Nenhum Google Analytics, rastreador, tag de Google Ads ou campanha foi instalado.
- A única preferência persistida é o idioma. O formulário atual não usa armazenamento local para dados pessoais.
- Não há garantias de posicionamento, conversão ou resultados de anúncios.
- Políticas de tratamento de dados, headers de segurança, HTTPS e desempenho de produção dependem de revisão futura na hospedagem; não foram configurados remotamente.

## Revisão antes de uma futura publicação

Revisar textos e aparência; confirmar contatos e disponibilidade dos links externos; configurar e testar o formulário; conferir HTTPS/canonical/redirecionamentos na hospedagem e medir desempenho em produção. Publicação, commit, push e merge dependem de autorização separada.
