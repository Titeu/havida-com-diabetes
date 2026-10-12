# Portão de qualidade — não entregar sem passar

Marque cada item. Falhou algum → volte à etapa 4 e corrija.

## Medição (skill `lighthouse-audit`, build de produção: `npm run build && npm run preview`)

Meta do modelo: **Performance 95+ · Acessibilidade 100 · Boas práticas 100 · SEO 100**, em mobile.
Se não atingir, registre o motivo e o que foi tentado.

- [ ] LCP até 2,5 s · CLS até 0,1 · INP bom
- [ ] Sem erro no console e sem requisição quebrada (404)- [ ] **Sem salto de layout em tela alguma (desktop e celular):** meça o CLS no site **publicado** com `PerformanceObserver` de `layout-shift` (ou Lighthouse). Elementos que o JavaScript reorganiza (hero com cenas, carrosséis) devem **nascer no tamanho final**: aplique a classe/altura final no HTML (script inline curto) e deixe o JS só refinar. Lição do site da Elaine: o hero nascia empilhado e encolhia quando o script rodava (CLS 0,64 → 0,02, nota desktop 77 → 96+).
- [ ] Sem rolagem horizontal: `window.scrollTo(300,0)` deve continuar em `scrollX = 0` (carrosséis com cartões fora da tela precisam de `overflow-x: clip` no contêiner; `overflow-x: clip` também no `html`)

## Performance

- [ ] Imagens em AVIF/WebP, com `width`/`height`, `lazy` abaixo da dobra, a principal prioritária
- [ ] No máximo 2 famílias de fonte, só os pesos usados, `font-display: swap`
- [ ] Zero JavaScript desnecessário; nenhuma biblioteca grande para efeito simples
- [ ] Se há React/Next: `/vercel-react-best-practices` rodada e itens críticos/altos corrigidos
- [ ] `npm run build` sem avisos, `npx astro check` sem erros e `npm audit --omit=dev` sem falha alta/crítica
- [ ] Nenhuma imagem acima de ~200 KB sem motivo
- [ ] **Imagens responsivas:** nada baixa bem maior do que exibe (o PageSpeed acusa "Melhorar a entrega de imagens"). Gere variantes (ex.: `foto-500.webp` + original) e use `srcset`/`sizes`; logos e ícones pequenos no tamanho exibido × 2.
- [ ] **CSS sem bloqueio:** `build.inlineStylesheets: "always"` no `astro.config.mjs` e regras `@font-face` embutidas no `<head>` (CSS pequeno cabe no HTML); mantenha o `preload` das 2 fontes principais. Resultado no site da Elaine: 87 → 96/99 no desktop.

## Acessibilidade (confira com `/web-design-guidelines`)

- [ ] Contraste do texto: 4,5:1 (3:1 para texto grande)
- [ ] Foco visível em tudo que se clica (`:focus-visible`), sem `outline: none` solto
- [ ] Navegação completa por teclado; link "Pular para o conteúdo"
- [ ] Um único `<h1>`; títulos em ordem; `<button>` para ação e `<a>` para navegação
- [ ] Imagens com `alt` (ou `alt=""` se decorativas); campos com `<label>`
- [ ] `prefers-reduced-motion` respeitado; nenhuma animação só decorativa que atrapalhe a leitura
- [ ] Zoom liberado (sem `user-scalable=no`); alvos de toque com pelo menos 44 px

## SEO e compartilhamento

- [ ] Checklist completo de [`seo-geo.md`](seo-geo.md) cumprido (SEO técnico, JSON-LD, `llms.txt`, robôs de IA, respostas citáveis, autoria) e auditado com `/seo-audit` e `/ai-seo`

- [ ] `<title>` e `meta description` únicos por página; `lang="pt-BR"`
- [ ] `canonical` com o domínio real (`site:` no `astro.config.mjs`)
- [ ] Open Graph e imagem de compartilhamento (1200×630) testados
- [ ] `robots.txt`, `sitemap` e favicon corretos
- [ ] Dados estruturados quando fizer sentido (LocalBusiness, Person, FAQ)

## Conteúdo e legal

- [ ] Nenhum "lorem ipsum" ou `[a confirmar]` restante
- [ ] Telefone, WhatsApp, e-mail, endereço e redes testados um a um
- [ ] Registro profissional e regras do conselho da categoria cumpridos
- [ ] Política de privacidade (LGPD) se houver formulário, analytics ou cookies; aviso de cookies se necessário
- [ ] Nenhum dado pessoal de terceiros exposto

## Fidelidade ao DNA

- [ ] Paleta, fontes e fundo conferem com o `DNA.md`
- [ ] Fotos e ilustrações seguem a direção fotográfica
- [ ] Texto na voz da marca; nada que o DNA lista como anti-padrão
- [ ] A pessoa olhou em celular e em computador e aprovou

## Referência de site (se houver)

- [ ] Ordem das seções, grade, espaçamentos e proporções conferem com a referência (capturas lado a lado, 1440 e 390 px)
- [ ] Nada copiado da referência: textos, imagens, logotipo, identidade e código são do cliente

## Responsivo

- [ ] Testado em 360, 390, 768, 1024 e 1280 px; sem rolagem horizontal
