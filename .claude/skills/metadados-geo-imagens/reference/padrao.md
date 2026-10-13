# Padrão obrigatório de metadados GEO para imagens

> Padrão genérico do modelo. Os **valores** (entidade, abordagens, públicos, palavras-chave locais, referência
> geográfica, autoria, direitos) **dependem dos dados do cliente atual**: vêm da `cliente/FICHA-DO-CLIENTE.md`
> (seção "Metadados GEO das imagens") e do `DNA.md`. O exemplo da Elaine Rosa
> ([`exemplo-elaine-rosa.md`](exemplo-elaine-rosa.md)) mostra o padrão preenchido e **nunca** é copiado para outro cliente.

## 1. Objetivo

Padronizar os metadados de toda imagem publicada no site para fortalecer a identificação do profissional ou da
marca, o contexto do serviço e a relevância geográfica da região atendida, de forma verdadeira e consistente.

Sempre que uma imagem for enviada para análise ou entrar no site, gerar os campos abaixo, com exatamente estes
nomes e nesta ordem.

## 2. Campos obrigatórios

### filename
- Minúsculas, sem acento, palavras separadas por hífen.
- Priorizar a palavra-chave principal, o contexto da imagem e a localização, quando pertinentes.
- Não inserir informação que não corresponda à imagem ou à sua finalidade.
- Padrão: `palavra-chave-contexto-cidade-uf.webp` (variantes: `...-800.webp`, `...-1600.webp`).

### Título
- Descreve claramente a entidade, o assunto da imagem e a intenção contextual.
- Linguagem natural, específica e descritiva; nada genérico ou repetido entre imagens.

### Assunto
- Cluster semântico da imagem: tema principal, variações, contexto do serviço e localização, quando pertinentes.
- Sem palavra-chave sem relação direta com o conteúdo visual.

### Marcas
- Entidades e referências geográficas relevantes, **sem sugerir vínculo não confirmado**.
- **Referências institucionais e geográficas prioritárias: definidas por cliente** na ficha (nome do
  profissional/marca, abordagem ou especialidade, cidade/região, referência geográfica conhecida, como um
  edifício ou bairro). Incluir só as pertinentes à imagem e à página onde ela será publicada.
- Uma referência geográfica (prédio, bairro, ponto conhecido) pode constar como **referência**, mas só aparece
  como **endereço** do cliente se o endereço estiver confirmado na ficha.

### Comentários
Parágrafo autônomo, informativo e compreensível sem depender do resto da página. Deve:
- descrever o que a imagem **efetivamente** mostra;
- contextualizar o tema no campo de atuação do cliente, quando houver fundamento;
- relacionar o conteúdo à atuação do cliente **só quando a relação estiver confirmada**;
- incorporar a cidade/região quando a localização for pertinente;
- usar linguagem clara, técnica e acessível, favorecendo a recuperação semântica e a citação por buscadores e IAs;
- **não inventar** elementos visuais, serviços, especialidades, endereço ou informação clínica/técnica.

### Autores
- Padrão: `Nome — Profissão | Registro [número confirmado] | Especialidade` (+ cidade/UF quando pertinente).
- Registro profissional (CRP, CRM, OAB, CREA...) **só com o número confirmado**; sem confirmação, fica
  `[a confirmar]` e a imagem não é publicada.
- Não atribuir a autoria de uma **fotografia** ao cliente se ela não for confirmada: distinguir quem fez a foto
  (campo `credito`, ex.: "Foto: Nome do fotógrafo") da responsabilidade profissional pelo conteúdo.

### Direitos Autorais
- Padrão: `© Titular — Marca ou linha de atuação`.
- Aplicar só quando os direitos sobre a imagem estiverem com o cliente ou autorizados. Imagem de terceiros
  (banco de imagens, fotógrafo, parceiro): manter a atribuição e os direitos de quem detém.

## 3. Palavras-chave prioritárias (por cliente)

Montadas na etapa 1 e registradas na ficha, em quatro grupos. Escolher por imagem conforme o conteúdo real,
sem inserir todas indiscriminadamente:

| Grupo | O que entra | Exemplo genérico |
|---|---|---|
| Entidade profissional | nome, profissão, linha de atuação | "Nome Sobrenome", "nutricionista", "nutrição clínica" |
| Abordagens / especialidades | métodos e áreas **realmente** oferecidos | "nutrição esportiva", "reeducação alimentar" |
| Públicos e contextos | quem é atendido, **se for verdade** | "adultos", "atletas", "gestantes" |
| SEO local | serviço + cidade/bairro, região, referência geográfica | "nutricionista em Moema", "Moema – São Paulo/SP" |

## 4. Regras de qualidade para SEO + GEO

- Metadados gravados no arquivo **não substituem** o texto alternativo (`alt`), o título e a descrição da página
  nem os dados estruturados. O processo cobre os quatro.
- Descrições específicas para cada imagem, sem duplicação automática.
- Grafia consistente do nome profissional, da abordagem e da localização em todas as imagens e no site.
- Nada de palavra-chave só para tentar posicionar.
- Não prometer que os metadados garantem indexação, ranqueamento ou citação por IA.
- Entregar sempre os sete campos: filename, Título, Assunto, Marcas, Comentários, Autores e Direitos Autorais.
- Informação que não pode ser confirmada é sinalizada para validação, nunca inventada.
- **Comentários** é o principal campo descritivo para contexto semântico, sem deixar de otimizar o `alt` e o
  conteúdo da página.
- Imagem gerada por IA é declarada como tal (`origem: "ia"`) e não é descrita como foto real.

## 5. Formato obrigatório de entrega

```text
filename: [Nome do arquivo otimizado]
Título: [Título descritivo]
Assunto: [Cluster semântico da imagem]
Marcas: [Entidades e referências geográficas pertinentes]
Comentários: [Descrição autônoma, contextualizada e citável]
Autores: [Autoria confirmada e identificação profissional]
Direitos Autorais: [Declaração de direitos confirmada]
```

**Regra final:** todos os metadados são específicos à imagem, semanticamente coerentes, geograficamente
contextualizados quando pertinente e compatíveis com as informações profissionais **confirmadas do cliente**.

## 6. Onde cada campo é gravado (feito pelo script `aplicar`)

| Campo | XMP (padrão aberto, IPTC/Adobe) | EXIF (o que o Windows mostra em Propriedades › Detalhes) |
|---|---|---|
| filename | o próprio nome do arquivo | — |
| Título | `dc:title`, `photoshop:Headline` | `XPTitle`, `ImageDescription` |
| Assunto | termos em `dc:subject` | `XPSubject` |
| Marcas | `dc:subject` | `XPKeywords` |
| Comentários | `dc:description`, `exif:UserComment` | `XPComment` |
| Autores | `dc:creator` | `XPAuthor`, `Artist` |
| Direitos Autorais | `dc:rights`, `xmpRights:Marked` | `Copyright` |
| Crédito da foto (opcional) | `photoshop:Credit` | — |
| Cidade/UF/país | `photoshop:City/State/Country` | — |
| Origem (foto ou IA) | `Iptc4xmpExt:DigitalSourceType` | — |
| Página de direitos (opcional) | `xmpRights:WebStatement` | — |

Formatos: WebP, JPEG e PNG (sem reprocessar a imagem). AVIF não: publicar em WebP. O Google lê os campos IPTC de
autoria, crédito e direitos (`dc:creator`, `photoshop:Credit`, `dc:rights`) para a informação de licença no Google Imagens.

## 7. Manifesto `site/imagens-geo.json`

```json
{
  "padrao": {
    "autores": "Nome — Profissão | Registro 00/00000 | Especialidade",
    "direitos": "© Nome — Linha de atuação",
    "credito": "Foto: Nome do fotógrafo",
    "site_direitos": "https://dominio-do-cliente.com.br",
    "cidade": "Cidade", "estado": "UF", "pais": "Brasil",
    "marcas_base": ["Nome do cliente", "Cidade – UF"]
  },
  "ignorar": ["favicon*", "apple-touch-icon*", "icon-*"],
  "imagens": [
    {
      "arquivos": ["img/hero/palavra-chave-contexto-cidade-uf-*.webp"],
      "origem": "foto",
      "titulo": "...", "assunto": "termo; termo; termo", "marcas": ["..."],
      "comentarios": "...", "alt": "..."
    }
  ]
}
```

- Campos da imagem que ficarem vazios herdam do `padrao` (autores, direitos, crédito, cidade). `marcas_base` soma
  às `marcas` de cada imagem.
- `"decorativa": true` → imagem puramente decorativa (fica com `alt=""`, mas recebe metadados).
- `"decorativa_sem_metadados": true` → só para elementos gráficos sem conteúdo (texturas, ícones), com motivo.
