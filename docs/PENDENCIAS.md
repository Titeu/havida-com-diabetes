# Pendências — site Há vida com diabetes (atualizado em 12/10/2026)

## Já feito
Auditoria completa (SEO/GEO, desempenho, acessibilidade, LGPD), domínio havidacomdiabetes.com.br ativo, preço R$ 39,90 no Pix à vista (cartão R$ 41,65 à vista ou 12x de R$ 3,99), pagamento pela loja InfinitePay, depoimentos reais com primeiro nome, "de R$ 59,00" riscado mantido, fundo contínuo, faixas azuis com borboletas. PageSpeed (antes das últimas mudanças): computador 100, celular 86.

## Falta publicar
- [ ] **Deploy das últimas mudanças** (fundo contínuo + faixas azuis + imagem menor no celular; commits 8c14bc2 e 9fb5130 no GitHub). No Prompt de Comando, uma linha por vez:
  `cd /d "C:SERSERNADOWNLOADSAAA CLAUDEHAVIDA-PAGINA"` e depois `npx vercel deploy --prod --yes --scope ha-vida-com-diabetes`
- [ ] Conferir no celular e no computador o visual novo (intensidade das borboletas e das transições).
- [ ] Rodar o PageSpeed no celular em https://havidacomdiabetes.com.br/ (meta: 90+; estava 86).

## Você (precisa da sua conta)
- [ ] Enviar `https://havidacomdiabetes.com.br/sitemap.xml` ao **Google Search Console** (verificar o domínio) e ao **Bing Webmaster Tools**.
- [ ] **Vercel ↔ GitHub:** autorizar o repositório `Titeu/havida-com-diabetes` no app da Vercel (github.com/settings/installations → Vercel → Configure → adicionar o repositório) ou Vercel → projeto → Settings → Git → Connect. Depois cada push na `main` publica sozinho. (Avisar Claude para rodar `vercel git connect`.)
- [ ] **InfinitePay:** renomear a loja `eubella_21_18` para algo como "havidacomdiabetes" (se a opção existir) e passar o novo link; trocar em `CONFIG.nubankLink` no `index.html`.
- [ ] Conferir se o link da loja cobra os mesmos valores do site (R$ 39,90 Pix; cartão em 12x).

## Claude, amanhã
- [ ] Trocar o link da loja quando o nome for alterado; conectar o Git quando autorizado.
- [ ] Rodar o Lighthouse/PageSpeed no domínio depois do deploy e fechar a nota no relatório.
- [ ] Ajustar a intensidade das borboletas / transições, se pedido.
- [ ] Opcional: teste mensal de GEO (perguntar a ChatGPT/Perplexity/Gemini sobre o livro) e Google Perfil da Empresa, se aplicável.
- [ ] Opcional: depoimentos sem o campo de cargo "Endocrinologista" se quiser só primeiro nome; confirmar se Facebook/YouTube existem para reativar os ícones.

## Atualização de 13/10/2026
- PageSpeed (Google, 13/10 08:45, antes do último deploy): computador 84 (TBT 370 ms) · celular 89 (FCP 2,0 s, LCP 3,5 s) · demais notas 100.
- Feito: cartão do Henrique sem "Endocrinologista"; faixas azuis viraram brancas com borboletas suaves; animações 3D (livro e carrossel de leitores) só rodam quando visíveis (reduz TBT).
- Git ↔ Vercel: ainda falha (Vercel sem acesso ao repositório). Precisa autorizar no GitHub (Settings → Applications → Vercel → Configure → adicionar `havida-com-diabetes`).
- Link da loja InfinitePay: aguardando o novo nome.

## Atualização de 13/10/2026 (tarde)
- Deploy feito: fundo todo branco, CRP 06/127648 corrigido, imagens menores no celular.
- Search Console (psicologaalphaville.elainerosapsi.com.br): sitemap-index.xml ENVIADO (status inicial "não foi possível buscar", costuma resolver sozinho em algumas horas; conferir).
- Search Console (havidacomdiabetes.com.br): propriedade de domínio adicionada; registro TXT google-site-verification criado no DNS da Vercel (rec_f65287d759ffa8da94cdc196). FALTA clicar em VERIFICAR no Search Console e depois enviar `sitemap.xml`.
- GitHub ↔ Vercel: o GitHub pediu confirmação por e-mail (modo sudo) para abrir as configurações do app Vercel; falta o usuário confirmar e adicionar o repositório `havida-com-diabetes`.

## Atualização de 13/10/2026 (noite)
- Loja InfinitePay nova: https://loja.infinitepay.io/fernando_rosa-vv7 (livro a R$ 39,90). A antiga (eubella_21_18) foi trocada no site.
- Vendedor no rodapé e nas políticas: 48.952.092 FERNANDO LUIZ ROSA, CNPJ 48.952.092/0001-36, Jandira/SP (dados conferidos na BrasilAPI; o cadastro não traz rua/número).
- Novas páginas: troca-e-arrependimento.html (7 dias, CDC art. 49), 404.html; FAQ "Posso desistir da compra?"; ano de publicação 2018.
- Celular: botão "Quero meu livro" visível na primeira tela.
- Falta (usuário): código de e-mail no GitHub + adicionar repositório; configurar na loja InfinitePay o aviso de "pedido recebido"; decidir Analytics/Pixel (precisa do ID); revisar rua/endereço do vendedor se quiser mostrar.

## 13/10/2026 — equipe Vercel renomeada
- A equipe agora é "FR AI Creator Studio", URL `fr-ai-creator-studio` (antes ha-vida-com-diabetes). Deploy: `cd /d "C:\Users\ferna\Downloads\AAA Claude\havida-pagina"` e depois `npx vercel deploy --prod --yes --scope fr-ai-creator-studio`.
- Conferido: havidacomdiabetes.com.br e psicologaalphaville.elainerosapsi.com.br seguem 200; projetos intactos.
- Pendente: deploy das URLs limpas (commit d195a80); GitHub e Vercel; aviso pós-compra no InfinitePay.
- Git conectado em 13/10/2026: repositório Titeu/havida-com-diabetes ligado ao projeto na Vercel; cada push na `main` agora publica sozinho (não precisa mais do `npx vercel deploy`).
