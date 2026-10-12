# Infraestrutura — Há vida com diabetes (conferido em 12/10/2026)

- **Site:** página única estática (HTML/CSS/JS puro, sem build). Raiz do repositório = raiz do site.
- **Pasta local:** `C:\Users\ferna\Downloads\AAA Claude\havida-pagina`
- **GitHub:** `Titeu/havida-com-diabetes` (branch `main`)
- **Vercel:** projeto `havida-com-diabetes`, equipe `ha-vida-com-diabetes` → https://havida-com-diabetes.vercel.app
- **Domínio próprio:** `havidacomdiabetes.com.br` ainda NÃO conectado (ao conectar: trocar canonical, og:url, sitemap, robots e llms.txt)
- **Publicar:** `vercel deploy --prod --yes --scope ha-vida-com-diabetes --cwd "<pasta>"` ou push na `main`
- **`.vercelignore`:** `docs`, `.claude`, `_orig` e `*.md` não vão ao ar.
- **Pagamento:** `CONFIG.nubankLink` no `index.html`. Loja InfinitePay https://loja.infinitepay.io/eubella_21_18 (preço na loja: R$ 39,90 — conferir com o site, R$ 49,90).
- **Pedido:** formulário monta mensagem de WhatsApp (5511996221013) com os dados; sem servidor/banco.
