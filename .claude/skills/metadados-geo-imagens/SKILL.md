---
name: metadados-geo-imagens
description: Padrão obrigatório de metadados GEO para TODA imagem publicada no site (nome do arquivo, Título, Assunto, Marcas, Comentários, Autores, Direitos Autorais, gravados dentro do arquivo, mais alt). Use sempre que uma imagem entrar no site ou for trocada (build, manutenção, carrossel, hero, foto nova, imagem gerada por IA), quando pedirem "metadados das imagens", "GEO das imagens", "nomear imagens", ou na etapa 5 para verificar o portão de imagens.
metadata:
  argument-hint: <preparar | aplicar | verificar | imagem enviada para análise>
---

# Metadados GEO das imagens

Toda imagem que vai para o site passa por este processo. É regra do ecossistema, não um passo opcional:
**nenhuma imagem é publicada sem nome no padrão, os 7 campos gravados no arquivo e `alt`.**

- Padrão completo (regras de cada campo): [`reference/padrao.md`](reference/padrao.md). **Leia antes de preencher.**
- Exemplo preenchido (psicologia, Elaine Rosa — só exemplo, nunca copiar para outro cliente):
  [`reference/exemplo-elaine-rosa.md`](reference/exemplo-elaine-rosa.md).
- Script (só Python padrão): `scripts/imagens_geo.py` com `preparar`, `aplicar` e `verificar`.

## De onde vêm os dados

As **referências institucionais e geográficas, palavras-chave, autoria e direitos são do cliente atual**:
saem de `cliente/FICHA-DO-CLIENTE.md` (seção "Metadados GEO das imagens") e do `DNA.md`. Nunca reaproveite os
termos do exemplo (Elaine Rosa, ACT, Alphaville, Edifício Pravda...) em outro cliente. Dado que falta → a ficha
fica `[a confirmar]`, pergunte à pessoa; o script bloqueia a gravação enquanto houver pendência.

## Fluxo (por imagem nova ou trocada)

Ordem obrigatória: **otimizar → nomear → manifesto → aplicar → alt/schema → verificar**. Qualquer reconversão
(redimensionar, trocar formato, recomprimir) apaga os metadados: rode `aplicar` de novo depois.

1. **Otimizar** a imagem final (WebP; variantes de tamanho para `srcset`) e colocar em `site/public/img/...`.
   Não use `astro:assets`/`<Image>` para essas imagens: ele reprocessa no build da Vercel e **apaga os metadados**.
   AVIF não recebe metadados neste processo: publique em WebP.
2. **Nomear** no padrão `palavra-chave-contexto-cidade-uf[-largura].webp` (minúsculas, sem acento, hífens).
   Ao renomear, atualize todas as referências no código (`src`, `srcset`, OG, JSON-LD, `llms.txt`).
3. **Manifesto** `site/imagens-geo.json` (uma entrada por imagem; variantes de tamanho na mesma entrada por
   curinga, ex.: `img/hero/hero-consultorio-alphaville-barueri-sp-*.webp`):
   ```bash
   python .claude/skills/metadados-geo-imagens/scripts/imagens_geo.py preparar
   ```
   Cria as entradas que faltam com `[preencher]`. Preencha o bloco `padrao` (autoria, direitos, crédito,
   cidade/UF, `marcas_base`) uma vez por cliente, e por imagem: `titulo`, `assunto`, `marcas`, `comentarios`, `alt`,
   `origem` (`foto` ou `ia`). **Olhe a imagem** antes de descrever: nada que ela não mostra.
4. **Aplicar** (grava XMP + EXIF dentro do arquivo, sem reprocessar a imagem):
   ```bash
   python .claude/skills/metadados-geo-imagens/scripts/imagens_geo.py aplicar
   ```
5. **Alt e schema:** use no HTML o `alt` do manifesto (o alt descreve a imagem para quem não vê; os Comentários
   são o texto longo do arquivo; não são a mesma coisa). Imagens principais (hero, retrato, local) entram no JSON-LD
   como `ImageObject` com os mesmos dados (skill `schema`): `contentUrl`, `name` (Título), `description`
   (Comentários), `creator`, `copyrightNotice`, `creditText`.
6. **Verificar** (portão; também na etapa 5 e antes de cada publicação):
   ```bash
   npm --prefix site run build
   python .claude/skills/metadados-geo-imagens/scripts/imagens_geo.py verificar --html site/dist
   ```
   Só segue com **APROVADO**. Ele confere: toda imagem de `public/` tem entrada, nome no padrão, os campos gravados
   no arquivo, nenhuma pendência, `alt` no manifesto e no HTML.

## Quando a pessoa envia uma imagem "para análise"

Responda **sempre** com os 7 campos, nesta ordem e formato (é o formato do padrão), e depois aplique no site:

```text
filename: [nome-otimizado.webp]
Título: [título descritivo]
Assunto: [cluster semântico]
Marcas: [entidades e referências geográficas pertinentes]
Comentários: [descrição autônoma, contextualizada e citável]
Autores: [autoria confirmada e identificação profissional]
Direitos Autorais: [declaração de direitos confirmada]
```
Acrescente o `alt` sugerido. Campo sem confirmação → `[a confirmar]` + pergunta (não invente).

## Regras que não mudam

- Específico por imagem; nada de descrição duplicada em lote.
- Só termos que a imagem e os serviços reais justificam; sem encher de palavra-chave.
- Registro profissional (CRP, CRM, OAB...) só se confirmado. Autoria da foto ≠ responsabilidade pelo conteúdo:
  se o fotógrafo é outro, use `credito` ("Foto: Nome") e não atribua a foto ao cliente.
- Imagem gerada por IA: `origem: "ia"` (grava o tipo IPTC *trainedAlgorithmicMedia*) e nunca descrever como
  foto real do local, do cliente ou de atendimento.
- Não prometa que metadados garantem indexação, ranking ou citação por IA. Eles reforçam nome, autoria, direitos e
  local; quem pesa mais é nome do arquivo, `alt`, texto da página e dados estruturados — por isso o processo cobre os quatro.
- O manifesto vai para o git (só dados públicos). Nada de dado pessoal de terceiros nas descrições.
