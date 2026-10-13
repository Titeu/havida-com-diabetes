# Infraestrutura — Há vida com diabetes (conferido em 12/10/2026)

- **Site:** página única estática (HTML/CSS/JS puro, sem build). Raiz do repositório = raiz do site.
- **Pasta local:** `C:\Users\ferna\Downloads\AAA Claude\havida-pagina`
- **GitHub:** `Titeu/havida-com-diabetes` (branch `main`)
- **Vercel:** projeto `havida-com-diabetes`, equipe `fr-ai-creator-studio` (nome "FR AI Creator Studio", renomeada em 13/10/2026; antes `ha-vida-com-diabetes`) → https://havidacomdiabetes.com.br
- **Domínio próprio:** `havidacomdiabetes.com.br` ativo (DNS na Vercel; www e http redirecionam para o domínio raiz). Canonical, sitemap, robots e llms usam esse domínio.
- **Publicar:** `vercel deploy --prod --yes --scope fr-ai-creator-studio --cwd "<pasta>"` ou push na `main`
- **`.vercelignore`:** `docs`, `.claude`, `_orig` e `*.md` não vão ao ar.
- **Pagamento:** `CONFIG.nubankLink` no `index.html`. Loja InfinitePay https://loja.infinitepay.io/eubella_21_18 (R$ 39,90 no Pix à vista; cartão até 9x com acréscimo).
- **Pedido:** formulário monta mensagem de WhatsApp (5511996221013) com os dados; sem servidor/banco.
