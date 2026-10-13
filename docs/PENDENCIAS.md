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
