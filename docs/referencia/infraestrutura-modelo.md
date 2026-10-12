# Registro de infraestrutura (preencher na etapa 6, antes de dar o site por entregue)

Copie este modelo para `site/INFRAESTRUTURA.md` (vai no repositório; **sem senhas nem chaves**) e preencha com
valores **conferidos nos painéis e na CLI**, não de memória. Um site só está entregue quando este arquivo existe e está correto.

## Código (GitHub)
- Repositório (URL e visibilidade):
- Conta/organização dona:
- Branch de produção:

## Hospedagem (Vercel)
- Equipe (scope/slug e id):
- **Nome do projeto Vercel** e id (`prj_…`): *(confira com `vercel project inspect <nome> --scope <equipe>`; o nome pode ter sido alterado depois da criação)*
- Painel (URL):
- URL de produção `*.vercel.app`:
- Git conectado a qual repositório? Como o deploy é feito (push ou CLI)?
- Variáveis de ambiente cadastradas (só os nomes):
- Projetos parecidos na mesma equipe (para não confundir):

## Domínio
- Domínio final, onde está registrado, para onde o DNS aponta **hoje** (confira com `curl -sI`):
- O que falta para ativar:
- `site:` do `astro.config.mjs` confere com o domínio final?

## Trocar o domínio para a Vercel (lições do site da Elaine, 06/10/2026)
- Descubra **quem serve o DNS** (`nslookup -type=NS dominio`): o registrador (ex.: Registro.br) pode só registrar enquanto o DNS fica em outro serviço (ex.: Builderall `ns3/ns4.l4dns.com`). A edição é feita onde o DNS é servido.
- Se o domínio estiver "conectado a uma aplicação" no serviço antigo, desconecte-o lá antes de editar o registro. Faça só o registro do subdomínio; **não mexa em MX/e-mail**.
- Aponte o registro **A** para o IP indicado pela Vercel (`vercel domains inspect` / `vercel api` → `configuredBy: "A"`, `misconfigured: false`). TTL 300 enquanto testa.
- O certificado HTTPS deveria sair sozinho em minutos. Se passar de ~15 min sem HTTPS (`vercel certs ls` vazio), emita na mão: `vercel certs issue <dominio> --scope <equipe>` (saiu em ~17 s).
- Teste antes de o cache de DNS local atualizar: `curl --resolve dominio:443:IP_DA_VERCEL https://dominio/`.
- Depois de ativo: `sitemap-index.xml` no Search Console e no Bing; conferir URLs finais e conversão do Google Ads; migrar DNS e e-mail **antes** de cancelar o serviço antigo.

## Como publicar (comandos reais) e histórico de datas

## Regras
- Se algo for renomeado, movido ou reconectado, **atualize o arquivo no mesmo dia**.
- `.vercel/project.json` e textos genéricos de README/DEPLOY não são fonte de verdade: o registro é.
