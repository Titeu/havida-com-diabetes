# Auditoria — site Há vida com diabetes (12/10/2026)
Método: skills do modelo "Criação de site padrão Claude" (lighthouse-audit, seo-audit, ai-seo, schema, web-design-guidelines) + quality-checklist + seo-geo.

## Antes (site no ar)
Mobile: Desempenho 61 · Acessibilidade 88 · Boas práticas 100 · SEO 100 (LCP 19,8 s; 5,3 MB)
Desktop: 53 · 82 · 100 · 100 (LCP 4,0 s; TBT 360 ms)
Faltavam: `<h1>`, `main`, canonical, JSON-LD, robots.txt, sitemap, llms.txt, favicon.ico (404); fontes do Google bloqueando; imagens de 1,3 MB/889 KB; menu/modal com foco indevido.

## Depois (servidor local, sem compressão; medir de novo no ar)
Mobile: 73 · 100 · 81* · 100 (TBT 60 ms, CLS 0) — Desktop: 97 · 100 · 81* · 100 (LCP 1,0 s, CLS 0) · peso 1,5 MB
*Boas práticas 81 = só por rodar em http://localhost; no HTTPS da Vercel volta a 100.

## Corrigido
SEO: title/description novos, canonical, robots (IA liberada), sitemap.xml, llms.txt, JSON-LD (WebSite, Person, Book+Offer, FAQPage), FAQ em HTML estático.
Desempenho: imagens → WebP responsivas (-70%), fontes locais (sem Google Fonts), hero com fetchpriority, scripts após 1º desenho, cache longo e cabeçalhos de segurança (`vercel.json`).
Acessibilidade: h1, `main`, link "pular para o conteúdo", foco visível, ordem de títulos, modal com `inert`/foco/Esc, alvos de toque ≥24 px, botões com nome.
Código: aspas tortas na seção de depoimentos (classes quebradas), links `#` mortos (Facebook/YouTube/site), © 2024 → ano automático, mensagem do WhatsApp com `encodeURIComponent`, `src=""` do lightbox.
Legal: política de privacidade (`privacidade.html`) + aviso LGPD no formulário.

## PENDENTE — decisão do usuário
1. (RESOLVIDO em 12/10: usuário confirmou que são reais; só primeiro nome) ~~Depoimentos fictícios~~ (Mariana A., Dr. Henrique L. "Endocrinologista" etc., 5 estrelas). Publicar como reais fere o CFP e o CDC. Trocar por relatos reais autorizados ou remover a seção.
2. **Pagamento:** link InfinitePay reutilizável (Pix sem validade + cartão 9x).
3. (RESOLVIDO: o correto é CRP 06/127648) ~~CRP divergente:~~ anotações antigas dizem 126648; site da psicóloga mostra 06/127648. Confirmar antes de exibir.
4. Domínio `havidacomdiabetes.com.br`; Search Console + Bing; Google Perfil, se aplicável.
5. Não foi feito commit/push/deploy: revisar e publicar.
