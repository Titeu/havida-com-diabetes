---
name: lighthouse-audit
description: Mede o site com o Lighthouse (desempenho, acessibilidade, boas práticas, SEO) em mobile e desktop e devolve as falhas com a causa provável. Use na etapa 5 (QA) e depois do deploy, ou quando pedirem "rode o Lighthouse", "meça a performance", "nota do site".
metadata:
  argument-hint: <url-opcional>
---

# Lighthouse — medição do site

Mede a página **rodando**. Complementa `web-design-guidelines` (que lê o código): esta skill dá notas e
tempos; aquela confere boas práticas de interface. Meta do modelo (mobile): **Performance 95+ ·
Acessibilidade 100 · Boas práticas 100 · SEO 100** (ver `intelligence/reference/quality-checklist.md`).

## Passo a passo

1. **Servir o build de produção** (nunca o `npm run dev`):
   `cd site && npm run build && npx astro preview --port 4321` (em segundo plano).
   Se o usuário passou uma URL (ex.: o site já no ar), use-a e pule este passo.
2. **Rodar mobile e desktop** (Chrome headless; sem instalar nada: usa `npx`):
   ```bash
   mkdir -p "$TEMP/lh" && cd "$TEMP/lh"
   npx --yes lighthouse http://localhost:4321/ --only-categories=performance,accessibility,best-practices,seo --chrome-flags="--headless=new" --output=json --output-path=mobile.json --quiet
   npx --yes lighthouse http://localhost:4321/ --preset=desktop --only-categories=performance,accessibility,best-practices,seo --chrome-flags="--headless=new" --output=json --output-path=desktop.json --quiet
   ```
   Rode também **uma página interna** de cada tipo (serviço, artigo, política) se o site tiver.
3. **Ler o JSON** com Python (notas, LCP, TBT, CLS e auditorias com score < 0,9). Pontos que mais
   explicam as notas: `largest-contentful-paint-element`, `lcp-breakdown-insight`, `bootup-time`,
   `third-party-summary`, `image-delivery-insight`, `render-blocking-insight`, `errors-in-console`,
   `color-contrast`, `heading-order`.
4. **Olhar a página** no navegador do Claude (preview) para conferir o visual depois de qualquer correção.
5. **Corrigir** o que for do site, rodar o build e **medir de novo**. Registrar antes/depois.
6. Parar o servidor de preview ao terminar (`taskkill //F //PID <pid>`).

## Ruído que NÃO é problema do site (explique ao usuário, não "corrija")

- **"Requisições inseguras" e erros de CORS em `localhost`:** somem em HTTPS. Reteste na URL final.
- **Scripts de antivírus** (ex.: `kaspersky-labs.com`) e extensões inflam TBT e peso. Confira
  `bootup-time`; se aparecem, a nota local está poluída: meça no PageSpeed Insights (pagespeed.web.dev).
- **Google Tag Manager / GA4 / Ads** pesam no mobile simulado. Se o cliente exige, carregue depois da
  primeira interação; não remova sem avisar.
- **Texto com revelação por rolagem** (começa esmaecido) aparece em `color-contrast`: falso positivo do efeito.
- A nota oscila entre rodadas (±5). Compare tendências, não um número isolado.
- **Link do PageSpeed é uma foto antiga:** `pagespeed.web.dev/analysis/...` guarda aquela análise para sempre. Depois de corrigir, o usuário deve abrir o PageSpeed, colar a URL e clicar em **Analisar** (a API pública costuma estourar a cota; nesse caso rode o Lighthouse local contra a URL publicada).
- **Medir o site publicado a partir da máquina do usuário:** o DNS local pode estar em cache. Use `--chrome-flags="--host-resolver-rules='MAP dominio.com.br IP_DA_VERCEL'"` e `--blocked-url-patterns="*kaspersky*"` para isolar o ruído do antivírus. Rode 2 a 3 vezes.
- **CLS alto no desktop com tudo mais verde:** descubra a origem com um `PerformanceObserver({type:"layout-shift"})` injetado por `evaluateOnNewDocument` e leia `sources[].previousRect/currentRect` (mostra qual elemento mudou de tamanho).
- A nota oscila entre rodadas (±5). Compare tendências, não um número isolado.

## Saída

Tabela mobile × desktop (4 notas), LCP/TBT/CLS, lista curta de falhas reais com `arquivo` provável e o
que foi corrigido (antes/depois). Se a meta não foi atingida, registre o motivo.

## Limites

Não publicar nem commitar sem pedido. Não instalar Lighthouse como dependência do `site/`: use `npx`.
