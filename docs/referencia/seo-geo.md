# SEO e GEO — o que todo site do modelo precisa ter

**SEO** = ser encontrado no Google/Bing. **GEO** (Generative Engine Optimization, também AEO) = ser **citado** por
ChatGPT, Claude, Perplexity, Gemini e Google AI Overviews. A base é a mesma: conteúdo claro, estrutura legível por
máquina e autoridade comprovável. GEO é uma camada sobre o SEO, não um substituto.

## Skills do modelo (instaladas em `.claude/skills/`, só instruções, sem scripts nem chaves)

| Skill | Fonte | Quando | O que faz |
|---|---|---|---|
| `seo-audit` | coreyhaines31/marketingskills | Etapa 5 e depois do deploy | Audita SEO técnico e on-page: rastreio, indexação, títulos, descrições, headings, links internos, E-E-A-T |
| `ai-seo` | coreyhaines31/marketingskills | Etapas 2, 4 e 5 | **GEO/AEO**: `llms.txt`, robôs de IA no `robots.txt`, blocos de resposta, FAQ, autoridade e citações |
| `schema` | coreyhaines31/marketingskills | Etapa 4 e 5 | Dados estruturados JSON-LD (tipos, propriedades, validação) |

Chamar: `/seo-audit`, `/ai-seo`, `/schema` (ou pedir "audite o SEO e o GEO do site"). Lidas e revisadas em 06/10/2026;
nenhuma executa código. Atualizar com `npx skills update`.

**Limite importante:** `curl` e `web_fetch` **não enxergam** JSON-LD injetado por JavaScript. Em Astro estático o
schema vai no HTML, então dá para conferir no código-fonte do build (`dist/`); para o site no ar, confirme também no
[Teste de Resultados Ricos do Google](https://search.google.com/test/rich-results).

## Checklist do modelo (marque na etapa 4 e confira na 5)

### SEO técnico
- [ ] Um `<h1>` por página; hierarquia `h1 > h2 > h3` sem pular níveis
- [ ] `<title>` (até ~60 caracteres) e `meta description` (até ~155) **únicos** por página, com a cidade/serviço
- [ ] `canonical` em toda página, apontando para o **domínio final** (`site:` do `astro.config.mjs` conferido)
- [ ] `sitemap-index.xml` gerado (`@astrojs/sitemap`) e `public/robots.txt` com `Sitemap:` do domínio final
- [ ] Open Graph e imagem de compartilhamento absoluta por página; `lang="pt-BR"`
- [ ] URLs curtas, legíveis, sem acento; `alt` descritivo nas imagens de conteúdo; links internos entre serviços e artigos
  - **Páginas de serviço na raiz** (`/terapia-de-casal`, não `/servicos/terapia-de-casal`): mais curto e mantém a palavra-chave. Defina isso **antes** de publicar; se mudar depois, deixe redirect permanente (`/servicos/:slug` → `/:slug` no `vercel.json`) e atualize menu, rodapé, cartões, blog, `llms.txt` e sitemap.
- [ ] HTTPS, `www` ↔ raiz redirecionando, sem 404 nem cadeia de redirecionamentos

### Dados estruturados (JSON-LD, skill `schema`)
- [ ] Home: `Organization`/`LocalBusiness` (ou o subtipo certo, ex.: `Psychologist`, `Dentist`, `LegalService`) com nome, endereço, telefone, horário, `areaServed`, `sameAs` (redes e perfis oficiais)
- [ ] Profissional: `Person` com cargo e **registro profissional** (CRP, CRM, OAB…), formação e especialidades, só com dado real
- [ ] Páginas de serviço: `Service` (ou `MedicalBusiness`/equivalente) + `BreadcrumbList`
- [ ] Artigos: `Article` com autor, data de publicação e atualização + `FAQPage` quando houver FAQ visível na página
- [ ] O schema **reflete o que está visível**; nunca marcar avaliações, notas ou depoimentos que não existem

### GEO (skill `ai-seo`)
- [ ] `public/llms.txt` com resumo do negócio, quem atende, serviços, localização, contato e links das páginas principais (Markdown curto, só fatos)
- [ ] `robots.txt` **permite** os robôs de IA: `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `Applebot-Extended`. Decisão do cliente: se ele **não** quiser ser usado em treinamento, bloqueie só os de treinamento e mantenha os de busca. Registre a decisão
- [ ] Cada página responde a uma pergunta real logo no início, em **40 a 60 palavras** autocontidas (a "resposta citável"), e depois aprofunda
- [ ] Seção de **perguntas e respostas** (FAQ) nas páginas de serviço e artigos, com as dúvidas reais dos pacientes/clientes
- [ ] **Autoria visível**: nome, credencial e registro profissional na página e nos artigos; data de atualização
- [ ] **Fontes citadas** nos artigos (estudos, órgãos oficiais) e números com data
- [ ] Informação consistente em todo lugar (nome, endereço, telefone, especialidades) no site, no Google Perfil da Empresa e nas redes: IAs cruzam fontes
- [ ] Tabelas e listas para comparações e passo a passo; parágrafos curtos; sem texto escondido só para robôs

### Setores regulados (saúde, direito, finanças)
- Cumpra as regras de publicidade do **conselho profissional** (ex.: CFP, CFM, OAB). **Confira** o que o conselho permite sobre depoimentos de clientes, promessa de resultado e preços antes de marcar `Review` ou publicar relatos.
- Conteúdo de saúde exige autoria qualificada e fontes (E-E-A-T). Nunca prometa cura ou resultado.
- Respeite a LGPD em formulários, cookies e depoimentos.

## Fora do site (parte do trabalho, anote na ficha e entregue ao cliente)

- **Google Perfil da Empresa** (negócio local): categoria, serviços, horários, fotos, link do site, mesmo NAP do site
- **Google Search Console**: verificar o domínio, enviar o sitemap, acompanhar indexação
- **Bing Webmaster Tools** (alimenta ChatGPT e outros): importar do Search Console e enviar o sitemap
- Perfis consistentes (Instagram, LinkedIn, diretórios do conselho) com o mesmo nome e link do site
- **Teste mensal de GEO:** perguntar a ChatGPT, Perplexity, Gemini e Claude as perguntas que o cliente quer ganhar ("psicólogo em Alphaville", "terapia de casal Barueri") e anotar se o site é citado

## Vercel e GEO
SEO e GEO se fazem no código do site; a Vercel só hospeda. O que conferir nela:
- Domínio final ativo com HTTPS e redirecionamento `www` ↔ raiz
- Em **Firewall / Bot Protection**, confirmar que os robôs de IA e de busca **não estão bloqueados** (os nomes das opções mudam; confira no painel ao configurar)
- Após o deploy, testar `/robots.txt`, `/sitemap-index.xml` e `/llms.txt` na URL final
- Deploy Protection **desligada** em produção (senão buscadores e IAs recebem a tela de login)

## Como medir
- Search Console: impressões, cliques, páginas indexadas, erros
- Lighthouse (`/lighthouse-audit`): meta SEO 100 e acessibilidade
- Teste de GEO mensal (acima) registrado em `site/INFRAESTRUTURA.md` ou na ficha
