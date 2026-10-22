#!/usr/bin/env python3
"""Gera o blog "Espaço Saúde" do site Há vida com diabetes.

Uso (na pasta havida-pagina):  python -X utf8 scripts/build_blog.py

- Lê os artigos .docx de  ../Artigos  (um arquivo por artigo; a ordem e os metadados estão em POSTS abaixo).
- Reaproveita fontes, cores, nav e rodapé do index.html (o visual do blog acompanha o do site).
- Escreve  blog/index.html, blog/<slug>/index.html, assets/blog.<hash>.css e atualiza sitemap.xml.

Para publicar um artigo novo: salve o .docx em Artigos, acrescente uma entrada em POSTS, foto em assets/img/blog/
(variantes -480, -900 e -og, em WebP) e rode de novo.
"""
import hashlib, html, json, math, re, sys, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
ARTIGOS = ROOT.parent / "Artigos"
SITE = "https://havidacomdiabetes.com.br"
BLOG_NAME = "Espaço Saúde"
HOJE = "2026-10-21"

POSTS = [
    dict(slug="diabetes-e-saude-mental-cansaco-emocional", curto="Quando cuidar cansa", docx="Diabetes e saúde mental quando cuidar todos os dias se torna emocionalmente cansativo.docx",
         cat="Saúde emocional", img="blog-diabetes-saude-mental-cansaco-emocional", pub=HOJE,
         seo_title="Diabetes e saúde mental: quando o cuidado cansa",
         desc="Entenda o sofrimento relacionado ao diabetes (diabetes distress), como diferenciá-lo da depressão e quando a rotina de cuidados pede mais apoio.",
         alt="Mulher olhando pensativa pela janela, em um momento de cansaço e reflexão"),
    dict(slug="aceitacao-do-diabetes-act", curto="Aceitar sem se resignar", docx="Aceitação do diabetes como a ACT pode ajudar a construir uma vida com sentido.docx",
         cat="ACT", img="blog-aceitacao-diabetes-act-vida-com-sentido", pub=HOJE,
         seo_title="Aceitação do diabetes: como cuidar de si mesmo",
         desc="O que é aceitação na ACT, por que ela não é resignação e como valores e passos viáveis ajudam a viver com diabetes sem se cobrar além do possível.",
         alt="Mulher de costas em um campo de lavanda ao pôr do sol"),
    dict(slug="diabetes-tipo-2-e-culpa", curto="Culpa não é tratamento", docx="Diabetes tipo 2 e culpa como cuidar da saúde sem transformar o diagnóstico em julgamento.docx",
         cat="Estigma e culpa", img="blog-diabetes-tipo-2-culpa-estigma", pub=HOJE,
         seo_title="Diabetes tipo 2 e culpa: cuidar sem julgamento",
         desc="Diabetes tipo 2 tem múltiplos fatores. Entenda o estigma, a autocobrança e como transformar culpa em perguntas úteis para conversar com a equipe de saúde.",
         alt="Mulher mais velha verificando a glicemia com um glicosímetro no sofá de casa"),
    dict(slug="diabetes-na-familia-apoio-e-autonomia", curto="Apoio sem vigilância", docx="Diabetes na família como oferecer apoio e preservar a autonomia.docx",
         cat="Família", img="blog-diabetes-na-familia-apoio-autonomia", pub=HOJE,
         seo_title="Diabetes na família: apoio sem vigilância",
         desc="Como a família pode apoiar quem tem diabetes sem vigiar: conversas, acordos e divisão de tarefas que respeitam a autonomia de adultos, crianças e adolescentes.",
         alt="Mãe e filha conversando na cozinha; a menina usa um sensor de glicose no braço"),
    dict(slug="medo-de-hipoglicemia", curto="O medo que limita", docx="Medo de hipoglicemia quando a preocupação começa a limitar a vida.docx",
         cat="Hipoglicemia", img="blog-medo-de-hipoglicemia-vida-limitada", pub=HOJE,
         seo_title="Medo de hipoglicemia: quando limita a vida",
         desc="O medo de hipoglicemia pode limitar sono, passeios e exercícios. Veja quando ele merece atenção, como organizar a segurança e onde a ACT entra.",
         alt="Homem mais velho caminhando em um parque no outono"),
]

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


# ---------------------------------------------------------------- leitura do .docx
def ler_docx(path):
    z = zipfile.ZipFile(path)
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("word/_rels/document.xml.rels"))}
    doc = ET.fromstring(z.read("word/document.xml"))

    def runs(el):
        out = ""
        for ch in el:
            if ch.tag == W + "r":
                rpr = ch.find(W + "rPr")
                b = rpr is not None and rpr.find(W + "b") is not None and rpr.find(W + "b").get(W + "val") not in ("0", "false")
                s = "".join((x.text or "") if x.tag == W + "t" else "" for x in ch)
                out += f"**{s}**" if (b and s.strip()) else s
            elif ch.tag == W + "hyperlink":
                url = rels.get(ch.get(R + "id"), "")
                inner = runs(ch).replace("**", "")
                out += f"[{inner}]({url})" if url else inner
        return out.replace("****", "")

    paras = []
    for p in doc.iter(W + "p"):
        ppr = p.find(W + "pPr")
        lista = ppr is not None and ppr.find(W + "numPr") is not None
        t = runs(p).strip()
        if t:
            paras.append((lista, t))
    return paras


def esc(t):
    return html.escape(t, quote=False)


def inline(t, externo=True):
    t = esc(t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener noreferrer">{m.group(1)}</a>', t)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)


def plain(t):
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", re.sub(r"\[([^\]]+)\]\(https?://[^)\s]+\)", r"\1", t))


def so_negrito(t):
    m = re.fullmatch(r"\*\*([^*]+)\*\*", t)
    return m.group(1) if m else None


def parse_artigo(paras):
    titulo = so_negrito(paras[0][1]) or plain(paras[0][1])
    sub = plain(paras[1][1])
    corpo, faq, refs, nota, proximo = [], [], [], "", ""
    modo = "corpo"
    for lista, t in paras[2:]:
        h = so_negrito(t)
        if h and h.lower().startswith("perguntas frequentes"):
            modo = "faq"; continue
        if h and h.lower().startswith("referências"):
            modo = "refs"; continue
        if modo == "corpo":
            if h:
                corpo.append(("h2", h))
            elif lista:
                if corpo and corpo[-1][0] == "ul": corpo[-1][1].append(t)
                else: corpo.append(("ul", [t]))
            elif t.startswith("“") and re.search(r"”\.?$", t):
                corpo.append(("quote", t))
            else:
                corpo.append(("p", t))
        elif modo == "faq":
            m = re.fullmatch(r"\*\*(.+?)\*\*(.+)", t)
            if m and m.group(2).strip():
                faq.append((m.group(1).strip(), m.group(2).strip()))
            else:
                proximo = t
        else:
            if lista: refs.append(t)
            else: nota = t
    palavras = sum(len(plain(x if isinstance(x, str) else " ".join(x)).split()) for _, x in corpo)
    palavras += sum(len(q.split()) + len(a.split()) for q, a in faq) + len(proximo.split())
    return dict(titulo=titulo, sub=sub, corpo=corpo, faq=faq, refs=refs, nota=nota, proximo=proximo,
                min=max(2, math.ceil(palavras / 190)))



# Trechos reescritos depois do .docx (o texto abaixo substitui a seção de mesmo título). Formato: "## título" + parágrafos.
SUBSTITUICOES = {
    "diabetes-e-saude-mental-cansaco-emocional": {
        "Como a ACT pode contribuir?": """## Como continuar se cuidando nos dias difíceis?

Um resultado de glicemia diferente do esperado pode trazer frustração, medo e pensamentos duros sobre si, como “eu nunca faço nada direito”. Em alguns momentos, isso pode aumentar a vontade de adiar uma consulta ou se afastar do cuidado.

Quando isso acontece, vale perceber o que esse resultado despertou e como você está reagindo. Um pensamento de fracasso, por mais convincente que pareça, não resume quem você é nem todo o esforço envolvido em conviver com o diabetes.

Você não precisa esperar a frustração passar para buscar apoio. Pode começar com perguntas como: **“O que preciso compreender sobre esse resultado? O que está dificultando meu cuidado? Qual passo é possível dar agora?”** Levar essas dúvidas à consulta ou compartilhar uma dificuldade com alguém de confiança pode ser um começo.

Esse olhar também inclui as condições da sua vida. Falta de dinheiro, informação, acesso ao tratamento ou apoio são dificuldades reais que precisam ser consideradas. Cuidar de si envolve encontrar caminhos possíveis dentro da sua realidade e buscar ajuda para enfrentar aquilo que você não consegue resolver sozinho.""",
    },
    "diabetes-na-familia-apoio-e-autonomia": {
        "Uma reflexão orientada pela ACT": """## Como apoiar quem você ama sem transformar o cuidado em cobrança

Quando alguém da família tem diabetes, o medo e a preocupação podem influenciar a maneira de conversar. Às vezes, a intenção é ajudar, mas o cuidado acaba aparecendo como insistência, vigilância ou crítica.

Nesses momentos, vale fazer uma pausa e se perguntar: **“Que familiar eu quero ser nesta conversa? Como posso demonstrar o carinho e o respeito que desejo oferecer?”**

Você não precisa deixar de sentir preocupação para agir com mais acolhimento. Pode reconhecer esse sentimento e, ainda assim, escolher escutar até o fim, perguntar se a pessoa gostaria de uma sugestão ou procurar entender o que está difícil antes de cobrar uma mudança. Uma pergunta como “O que posso fazer para ajudar?” pode abrir espaço para uma conversa em que ambos tenham voz.

Quem oferece apoio também precisa de cuidado. Reconhecer o próprio cansaço, pedir ajuda e compartilhar responsabilidades são formas de tornar essa participação mais sustentável. Conforme as necessidades e os acordos da família, um primeiro passo pode ser reunir dúvidas para uma consulta, caso a pessoa queira companhia, ou combinar quais tarefas cada um pode assumir.

O cuidado pode ser construído nesses pequenos gestos: estar disponível, respeitar a autonomia e encontrar, juntos, maneiras de lidar com as dificuldades do dia a dia.""",
    },
}


# Perguntas extras (somam-se às do .docx). Formato: (pergunta, resposta).
FAQ_EXTRAS = {
    "aceitacao-do-diabetes-act": [
        ("Aceitar significa desistir de querer que as coisas fossem diferentes?",
         "Não. Você pode reconhecer que o diabetes faz parte da sua realidade e continuar desejando que as coisas fossem diferentes. Pode sentir raiva das exigências do tratamento, tristeza pelas mudanças e cansaço das decisões diárias, e ainda assim encontrar maneiras de se cuidar."),
        ("O que fazer quando evitar o assunto traz alívio?",
         "Observe, sem se julgar: “O que fica mais fácil quando evito essa situação? E o que fica mais difícil depois?”. Essas perguntas ajudam a perceber as consequências das escolhas e a pensar no apoio necessário para um próximo passo."),
        ("Como contar à equipe que estou com medo ou vergonha?",
         "Você pode anotar as dúvidas, dizer que está com receio ou pedir a companhia de alguém de confiança. Preparar uma pergunta para a consulta ou compartilhar uma dificuldade já é uma forma de participar do próprio cuidado."),
        ("É normal voltar a sentir raiva ou tristeza depois de um tempo?",
         "Sim. Esses sentimentos podem reaparecer diante de mudanças no tratamento, novas dificuldades ou momentos de maior cansaço. Isso não apaga o que você aprendeu nem significa que todo o caminho foi perdido."),
        ("Falta de dinheiro ou de acesso a medicamentos é falta de aceitação?",
         "Não. Nem toda dificuldade com o tratamento está relacionada à maneira de lidar com o diagnóstico. Falta de dinheiro, de insumos, de informação clara ou de apoio são barreiras reais e precisam entrar na conversa com a equipe de saúde."),
        ("A ACT melhora a glicemia?",
         "Pesquisas investigam a contribuição da ACT para o cuidado em diabetes, com resultados que não são uniformes. Por isso, não é possível prometer que essa abordagem produzirá determinada mudança na glicemia de uma pessoa. A indicação da psicoterapia depende de avaliação individual."),
    ],
    "diabetes-e-saude-mental-cansaco-emocional": [
        ("Um resultado ruim significa que eu falhei?",
         "Não. Um resultado diferente do esperado é uma informação para ser compreendida com a equipe de saúde, não uma sentença sobre quem você é. Um pensamento de fracasso, por mais convincente que pareça, não resume todo o esforço envolvido em conviver com o diabetes."),
        ("Por que sinto vontade de adiar a consulta depois de um resultado difícil?",
         "Frustração, medo e pensamentos duros sobre si podem aumentar a vontade de se afastar do cuidado. Perceber o que o resultado despertou e como você está reagindo é um primeiro passo. Levar essa dificuldade à consulta também faz parte do tratamento."),
        ("Preciso esperar a frustração passar para pedir ajuda?",
         "Não. Você pode buscar apoio mesmo sentindo frustração ou medo. Perguntas como “O que preciso compreender sobre esse resultado?” e “Qual passo é possível dar agora?” ajudam a começar a conversa."),
        ("E se a dificuldade for falta de dinheiro, de informação ou de acesso ao tratamento?",
         "Essas dificuldades são reais e precisam ser consideradas, e não transformadas em culpa pessoal. Cuidar de si envolve encontrar caminhos possíveis dentro da sua realidade e buscar ajuda para enfrentar aquilo que você não consegue resolver sozinho."),
        ("Com quem posso compartilhar o que estou sentindo?",
         "Com a equipe que acompanha o seu diabetes, com um profissional de saúde mental ou com alguém de confiança. Não é necessário dar um nome ao sofrimento antes de pedir ajuda: uma frase simples, como “Preciso conversar sobre como estou me sentindo em relação ao diabetes”, já é um começo."),
    ],
    "diabetes-na-familia-apoio-e-autonomia": [
        ("Sentir preocupação com meu familiar significa que estou fazendo algo errado?",
         "Não. Preocupar-se é compreensível. Você pode reconhecer esse sentimento e, ainda assim, escolher como agir: escutar até o fim, perguntar se a pessoa quer uma sugestão ou tentar entender o que está difícil antes de cobrar uma mudança."),
        ("O que posso perguntar em vez de cobrar?",
         "Perguntas abertas costumam ajudar, como “O que posso fazer para ajudar?” ou “Você prefere que eu escute ou que pense em soluções com você?”. O ponto é abrir espaço para uma conversa em que as duas pessoas tenham voz."),
        ("E se a pessoa não quiser a minha ajuda?",
         "Em um adulto capaz de decidir, a participação da família deve respeitar as escolhas e os acordos construídos. Vale combinar quando e como a ajuda é bem-vinda e, se houver dúvidas sobre segurança ou tratamento, levar essa conversa à equipe de saúde."),
        ("Preciso acompanhar a pessoa nas consultas?",
         "Só se ela quiser companhia. Um primeiro passo pode ser reunir dúvidas para a consulta e combinar, juntos, como a família pode participar. Cada família chega a acordos diferentes, e eles podem mudar com o tempo."),
        ("Como dividir as tarefas do cuidado sem sobrecarregar ninguém?",
         "Comece por uma única tarefa e combine quem faz o quê e quando o acordo será revisto. Quem oferece apoio também precisa de cuidado: reconhecer o próprio cansaço, pedir ajuda e compartilhar responsabilidades torna a participação mais sustentável."),
        ("Quem apoia alguém com diabetes também pode buscar ajuda psicológica?",
         "Sim. O cansaço, o medo e a sobrecarga de quem acompanha também merecem atenção, mesmo que a pessoa com diabetes não esteja em acompanhamento psicológico."),
    ],
}


def art_de_md(path, base):
    """Artigo revisado em Markdown simples: '# título', '## seção', '* ref', '::proximo:: texto'. Mantém o subtítulo e as perguntas do .docx."""
    linhas = [l.rstrip() for l in Path(path).read_text(encoding="utf-8").split("\n")]
    titulo, corpo, refs, nota, proximo, modo = None, [], [], "", "", "corpo"
    for l in linhas:
        if not l.strip():
            continue
        if l.startswith("# "):
            titulo = l[2:].strip()
        elif l.startswith("## "):
            if l[3:].lower().startswith("referências"):
                modo = "refs"
            else:
                corpo.append(("h2", l[3:].strip()))
        elif modo == "refs":
            if l.startswith("* "):
                refs.append(l[2:].strip())
            else:
                nota = l.strip()
        elif l.startswith("::proximo::"):
            proximo = l[len("::proximo::"):].strip()
        elif l.startswith("“") and re.search(r"”\.?$", l):
            corpo.append(("quote", l.strip()))
        else:
            corpo.append(("p", l.strip()))
    art = dict(base)
    art.update(titulo=titulo, corpo=corpo, refs=refs, nota=nota, proximo=proximo)
    return art


def aplicar_substituicoes(slug, art):
    art["faq"] = art["faq"] + FAQ_EXTRAS.get(slug, [])
    for titulo_antigo, md in SUBSTITUICOES.get(slug, {}).items():
        corpo = art["corpo"]
        i = next(n for n, (tp, x) in enumerate(corpo) if tp == "h2" and x == titulo_antigo)
        j = next((n for n in range(i + 1, len(corpo)) if corpo[n][0] == "h2"), len(corpo))
        novos = []
        for bloco in md.strip().split("\n\n"):
            bloco = bloco.strip()
            novos.append(("h2", bloco[3:]) if bloco.startswith("## ") else ("p", bloco))
        art["corpo"] = corpo[:i] + novos + corpo[j:]


# ---------------------------------------------------------------- CSS e sprite herdados do index.html
def extrair_css_base():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
    css = css.replace("url(assets/", "url(/assets/").replace('url("assets/', 'url("/assets/')
    linhas = css.split("\n")
    pref = (".foot", ".sr-only", ".skip", "a:focus-visible", "@keyframes floatB", "html{background", "body{background",
            ".reveal", ".kicker", ".wrap", "::selection", ".progress", ".btn")
    out, i = [], 0
    # 1) fontes + tokens + base + botões + nav (até "SECTION DOTS")
    fim = next(n for n, l in enumerate(linhas) if "SECTION DOTS" in l)
    out += linhas[:fim]
    # 2) regras soltas do restante (rodapé, acessibilidade, reveal, fundo contínuo)
    n = fim
    while n < len(linhas):
        l = linhas[n]
        pega = l.startswith(pref) or (l.startswith("@media") and ".foot__" in l and "foot__main" in l)
        if pega:
            bloco = [l]
            while bloco[-1].count("{") + sum(x.count("{") for x in bloco[:-1]) > sum(x.count("}") for x in bloco) and n + 1 < len(linhas):
                n += 1; bloco.append(linhas[n])
            out += bloco
        n += 1
    return "\n".join(out)


def extrair_sprite():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    a = src.index('<svg width="0" height="0"')
    b = src.index("</svg>", src.index('<symbol id="i-quote"')) + len("</svg>")
    return src[a:b]


# ---------------------------------------------------------------- peças de página
def cabeca(title, desc, url, og_img, schema, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="{'article' if '/blog/' in url else 'website'}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Há vida com diabetes">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}{og_img}">
<link rel="icon" type="image/svg+xml" href="/assets/img/favicon.svg">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/fraunces-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/mulish-normal.woff2" as="font" type="font/woff2" crossorigin>
{extra_head}<link rel="stylesheet" href="/assets/{CSS_NAME}">
<noscript><style>.reveal{{opacity:1!important;transform:none!important}}</style></noscript>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body class="blog">
"""


def nav():
    return """<div class="progress" id="progress"></div>
<a href="#conteudo" class="skip">Pular para o conteúdo</a>
<nav class="nav" id="nav" aria-label="Principal">
  <a class="nav__brand" href="/" aria-label="Há vida com diabetes — página inicial">
    <svg class="logo-svg" viewBox="205 722 1620 624"><use href="#logo" x="205" y="722" width="1620" height="624"/></svg>
  </a>
  <div class="nav__menu">
    <ul class="nav__links">
      <li><a href="/">Início</a></li>
      <li><a href="/#autora">A autora</a></li>
      <li><a href="/#livro">O livro</a></li>
      <li><a href="/#depoimentos">Depoimentos</a></li>
      <li><a href="/blog" aria-current="page">Espaço Saúde</a></li>
      <li><a href="/#faq">Dúvidas</a></li>
    </ul>
    <a href="/#livro" class="btn btn--primary nav__cta">Comprar o livro</a>
  </div>
  <div class="nav__right">
    <div class="nav__social">
      <a href="https://instagram.com/havidacomdiabetes" target="_blank" rel="noopener" aria-label="Instagram"><svg><use href="#i-ig"/></svg></a>
    </div>
    <a href="/#livro" class="btn btn--primary nav__cta">Compre o livro</a>
    <button class="nav__burger" id="burger" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</nav>
"""


def rodape():
    return """<footer class="foot" id="contato">
  <div class="wrap">
    <div class="foot__cta reveal">
      <svg class="bf" viewBox="0 0 200 200"><use href="#bf"/></svg>
      <h2>Comece hoje a sua <em>travessia</em>.</h2>
      <p>Há vida com diabetes. E, com cuidado e acolhimento, ela pode ser extraordinária.</p>
      <a href="/#livro" class="btn btn--gold btn--lg"><svg><use href="#i-book"/></svg>Quero meu livro</a>
    </div>
    <div class="foot__main">
      <div class="foot__brand">
        <svg class="logo-svg logo-2t" viewBox="205 722 1620 624"><use href="#logo" x="205" y="722" width="1620" height="624"/></svg>
        <p>Um livro de Elaine Rosa sobre acolhimento, autoconhecimento e a coragem de viver bem — apesar do diabetes.</p>
        <div class="foot__social">
          <a href="https://instagram.com/havidacomdiabetes" target="_blank" rel="noopener" aria-label="Instagram"><svg><use href="#i-ig"/></svg></a>
        </div>
      </div>
      <div class="foot__col">
        <h3>Navegue</h3>
        <a href="/">Início</a>
        <a href="/#autora">A autora</a>
        <a href="/#livro">O livro</a>
        <a href="/#depoimentos">Depoimentos</a>
        <a href="/blog">Espaço Saúde</a>
      </div>
      <div class="foot__col">
        <h3>O livro</h3>
        <a href="/#livro">Comprar agora</a>
        <a href="/#faq">Perguntas frequentes</a>
        <a href="/troca-e-arrependimento">Troca e arrependimento</a>
        <span>Literare Books Int.</span>
        <span>ISBN 978-85-9455-117-7</span>
      </div>
      <div class="foot__col foot__contact">
        <h3>Contato</h3>
        <a href="https://wa.me/5511996221013" target="_blank" rel="noopener"><svg><use href="#i-phone"/></svg>(11) 99622-1013</a>
        <a href="https://instagram.com/havidacomdiabetes" target="_blank" rel="noopener"><svg><use href="#i-ig"/></svg>@havidacomdiabetes</a>
        <a href="mailto:havidacomdiabetes@gmail.com"><svg><use href="#i-mail"/></svg>havidacomdiabetes@gmail.com</a>
      </div>
    </div>
    <p class="foot__seller">Vendido por <b>48.952.092 Fernando Luiz Rosa</b> · CNPJ 48.952.092/0001-36 · Jandira/SP · WhatsApp (11) 99622-1013 · <a href="mailto:havidacomdiabetes@gmail.com">havidacomdiabetes@gmail.com</a></p>
    <div class="foot__bar">
      <span>© 2026 Há vida com diabetes · Elaine Rosa. Todos os direitos reservados. · <a href="/privacidade" style="text-decoration:underline">Privacidade</a> · <a href="/troca-e-arrependimento" style="text-decoration:underline">Troca e arrependimento</a></span>
      <span>Feito com <svg style="width:13px;height:13px;color:var(--blue-300);vertical-align:-2px"><use href="#i-heart"/></svg> e muita esperança.</span>
    </div>
  </div>
</footer>
"""


JS_BASE = """<script>
(function(){
  var nav=document.getElementById('nav'),bar=document.getElementById('progress'),b=document.getElementById('burger');
  function on(){nav.classList.toggle('scrolled',window.scrollY>40);var h=document.documentElement;bar.style.width=(h.scrollTop/Math.max(1,h.scrollHeight-h.clientHeight)*100)+'%'}
  window.addEventListener('scroll',on,{passive:true});on();
  b.addEventListener('click',function(){nav.classList.toggle('open')});
  var els=[].slice.call(document.querySelectorAll('.reveal'));
  if(!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')});return}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
  els.forEach(function(e){io.observe(e)});
})();
</script>
"""

PROC_JS = (Path(__file__).resolve().parent / "process.js").read_text(encoding="utf-8")

JS_BUSCA = """<script>
(function(){
  var norm=function(t){return t.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase()};
  var input=document.getElementById('busca'),status=document.getElementById('busca-status'),vazio=document.getElementById('busca-vazio'),limpar=document.getElementById('busca-limpar');
  var itens=[].slice.call(document.querySelectorAll('[data-busca]'));
  if(!input)return;
  function filtrar(){
    var termos=norm(input.value).split(/\\s+/).filter(Boolean),n=0;
    itens.forEach(function(el){var ok=termos.every(function(t){return (el.getAttribute('data-busca')||'').indexOf(t)>-1});el.hidden=!ok;if(ok)n++});
    limpar.hidden=termos.length===0;vazio.hidden=n>0;
    status.textContent=termos.length===0?'':(n===1?'1 artigo encontrado':n+' artigos encontrados');
  }
  input.addEventListener('input',filtrar);
  input.addEventListener('keydown',function(e){if(e.key==='Enter')e.preventDefault()});
  limpar.addEventListener('click',function(){input.value='';filtrar();input.focus()});
  var q=new URLSearchParams(location.search).get('q');if(q){input.value=q;filtrar()}
})();
</script>
"""


def img_tag(p, cls="", sizes="100%", eager=False, w=1600, h=1067):
    base = f"/assets/img/blog/{p['img']}"
    return (f'<img src="{base}-900.webp" srcset="{base}-480.webp 480w, {base}-900.webp 900w, {base}.webp 1600w" sizes="{sizes}" '
            f'alt="{html.escape(p["alt"])}" width="{w}" height="{h}" {"fetchpriority=\"high\"" if eager else "loading=\"lazy\""} decoding="async"{cls}>')


def data_br(iso):
    a, m, d = iso.split("-")
    return f"{d}/{m}/{a}"


# ---------------------------------------------------------------- páginas
def pagina_artigo(p, todos):
    a = p["art"]
    url = f"{SITE}/blog/{p['slug']}"
    outros = [x for x in todos if x["slug"] != p["slug"]]
    i = todos.index(p)
    rel = [todos[(i + 1) % len(todos)], todos[(i + 2) % len(todos)]]
    schema = [
        {"@context": "https://schema.org", "@type": "Article", "headline": a["titulo"], "description": p["desc"],
         "image": f"{SITE}/assets/img/blog/{p['img']}.webp", "datePublished": p["pub"], "dateModified": p["pub"],
         "inLanguage": "pt-BR", "mainEntityOfPage": url, "articleSection": p["cat"],
         "author": {"@type": "Person", "@id": f"{SITE}/#autora", "name": "Elaine Rosa",
                    "jobTitle": "Psicóloga (CRP 06/127648), educadora em diabetes e palestrante", "url": f"{SITE}/"},
         "publisher": {"@type": "Organization", "name": "Há vida com diabetes", "url": f"{SITE}/",
                       "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/apple-touch-icon.png"}},
         "isPartOf": {"@type": "Blog", "name": BLOG_NAME, "url": f"{SITE}/blog"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": BLOG_NAME, "item": f"{SITE}/blog"},
            {"@type": "ListItem", "position": 3, "name": a["titulo"]}]},
    ]
    if a["faq"]:
        schema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(r)}} for q, r in a["faq"]]})

    corpo = []
    for tipo, x in a["corpo"]:
        if tipo == "h2": corpo.append(f"<h2>{esc(x)}</h2>")
        elif tipo == "p": corpo.append(f"<p>{inline(x)}</p>")
        elif tipo == "quote": corpo.append(f'<blockquote class="aquote">{inline(x)}</blockquote>')
        elif tipo == "ul": corpo.append('<ul class="alist">' + "".join(f"<li>{inline(i)}</li>" for i in x) + "</ul>")
    faq = ""
    if a["faq"]:
        faq = '<section class="afaq"><h2>Perguntas frequentes</h2>' + "".join(
            f"<details><summary>{esc(q)}</summary><p>{inline(r)}</p></details>" for q, r in a["faq"]) + "</section>"
    prox = (f'<div class="anext"><div class="anext__label"><svg><use href="#bf"/></svg>Para levar com você</div>'
            f'<p>{inline(a["proximo"])}</p></div>') if a["proximo"] else ""
    refs = ""
    if a["refs"]:
        refs = '<section class="arefs"><h3>Referências e leituras para aprofundamento</h3><ul>' + "".join(
            f"<li>{inline(r)}</li>" for r in a["refs"]) + "</ul></section>"
    nota = f'<p class="anote">{inline(a["nota"])}</p>' if a["nota"] else ""

    relhtml = "".join(
        f'<a class="arel__card" href="/blog/{r["slug"]}"><img src="/assets/img/blog/{r["img"]}-480.webp" alt="{html.escape(r["alt"])}" width="480" height="320" loading="lazy" decoding="async">'
        f'<div><span class="cat">{esc(r["cat"])}</span><h3>{esc(r["art"]["titulo"])}</h3></div></a>' for r in rel)

    pre = f'<link rel="preload" as="image" href="/assets/img/blog/{p["img"]}-900.webp" imagesrcset="/assets/img/blog/{p["img"]}-480.webp 480w, /assets/img/blog/{p["img"]}-900.webp 900w, /assets/img/blog/{p["img"]}.webp 1600w" imagesizes="(max-width:1100px) 100vw, 1100px" fetchpriority="high">\n'
    h = cabeca(p["seo_title"] + " | " + BLOG_NAME, p["desc"], url, f"/assets/img/blog/{p['img']}-og.webp", schema, pre)
    h += SPRITE + nav() + f"""<main id="conteudo">
<article>
  <header class="ahead">
    <div class="wrap">
      <nav class="crumbs" aria-label="Você está aqui"><a href="/">Início</a><span>/</span><a href="/blog">{BLOG_NAME}</a><span>/</span><b>{esc(p['cat'])}</b></nav>
      <span class="cat">{esc(p['cat'])}</span>
      <h1>{esc(a['titulo'])}</h1>
      <p class="lead">{esc(a['sub'])}</p>
      <div class="byline">
        <div class="byline__who"><img src="/assets/img/author-120.webp" alt="Elaine Rosa" width="46" height="46"><div><b>Elaine Rosa</b>Psicóloga · CRP 06/127648 · Educadora em diabetes · Palestrante</div></div>
        <time class="byline__dot" datetime="{p['pub']}">{data_br(p['pub'])}</time>
        <span class="byline__dot">{a['min']} min de leitura</span>
      </div>
    </div>
  </header>
  <figure class="acover">{img_tag(p, sizes="(max-width:1100px) 100vw, 1100px", eager=True)}</figure>
  <div class="alayout">
    <div class="abody">
      {"".join(corpo)}
      {faq}
      {prox}
      {refs}
      {nota}
      <div class="asign">
        <img src="/assets/img/author-120.webp" alt="" width="64" height="64" loading="lazy" decoding="async">
        <div><strong>Elaine Rosa</strong><span>Psicóloga (CRP 06/127648), educadora em diabetes, palestrante e autora do livro <a href="/#livro">Há vida com diabetes</a>.</span>
        <a class="btn btn--ghost asign__btn" href="https://psicologaalphaville.elainerosapsi.com.br/" target="_blank" rel="noopener">Saiba mais sobre a autora →</a></div>
      </div>
    </div>
    <aside class="aside" aria-label="Sobre o livro">
      <div class="abook">
        <img src="/assets/img/livro-sem-fundo-420.webp" alt="Capa do livro Há vida com diabetes, de Elaine Rosa" width="420" height="482" loading="lazy" decoding="async">
        <h3>Há vida com diabetes</h3>
        <p>Um livro de Elaine Rosa sobre acolhimento, autoconhecimento e transformação para quem vive com diabetes e para quem caminha ao lado.</p>
        <a class="btn btn--gold" href="/#livro"><svg><use href="#i-book"/></svg>Conhecer o livro</a>
      </div>
      <div class="aautor">
        <p>Quer conhecer o trabalho de Elaine como psicóloga?</p>
        <a class="btn btn--ghost" href="https://psicologaalphaville.elainerosapsi.com.br/" target="_blank" rel="noopener">Saiba mais sobre a autora →</a>
      </div>
    </aside>
  </div>
</article>
<section class="arel"><div class="wrap">
  <span class="kicker">Continue lendo</span>
  <h2>Mais do {BLOG_NAME}</h2>
  <div class="arel__grid">{relhtml}</div>
  <p style="margin-top:26px"><a class="more" href="/blog">Ver todos os artigos <svg><use href="#i-arrow"/></svg></a></p>
</div></section>
</main>
""" + rodape() + JS_BASE + "</body></html>\n"
    return h


def pagina_indice(todos):
    url = f"{SITE}/blog"
    desc = ("Artigos de Elaine Rosa, psicóloga e educadora em diabetes, sobre saúde emocional, família, culpa, "
            "medo de hipoglicemia e aceitação para quem vive com diabetes.")
    schema = [
        {"@context": "https://schema.org", "@type": "Blog", "name": BLOG_NAME, "url": url, "inLanguage": "pt-BR",
         "description": desc,
         "author": {"@type": "Person", "@id": f"{SITE}/#autora", "name": "Elaine Rosa"},
         "publisher": {"@type": "Organization", "name": "Há vida com diabetes", "url": f"{SITE}/"},
         "blogPost": [{"@type": "BlogPosting", "headline": p["art"]["titulo"], "description": p["desc"],
                       "image": f"{SITE}/assets/img/blog/{p['img']}.webp", "datePublished": p["pub"],
                       "url": f"{SITE}/blog/{p['slug']}"} for p in todos]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": BLOG_NAME, "item": url}]},
    ]
    norm = lambda s: re.sub(r"[̀-ͯ]", "", __import__("unicodedata").normalize("NFD", s)).lower()
    busca = lambda p: html.escape(norm(" ".join([p["art"]["titulo"], p["desc"], p["cat"]])))
    resto = todos[4:]
    cards = "".join(
        f'<article class="bcard reveal" data-busca="{busca(p)}"><a href="/blog/{p["slug"]}">'
        f'<div class="bcard__img">{img_tag(p, sizes="(max-width:700px) 100vw, 560px", w=900, h=600)}</div>'
        f'<div class="bcard__body"><div class="bcard__meta"><span class="cat">{esc(p["cat"])}</span><span>{p["art"]["min"]} min de leitura</span></div>'
        f'<h3>{esc(p["art"]["titulo"])}</h3><p>{esc(p["art"]["sub"])}</p><span class="more">Leia o artigo <svg><use href="#i-arrow"/></svg></span></div></a></article>'
        for p in resto)
    link = lambda p, t: f'<a href="/blog/{p["slug"]}">{t}</a>'
    h = cabeca(f"{BLOG_NAME} | Blog Há vida com diabetes", desc, url, "/assets/img/og-cover.webp", schema)
    h += SPRITE + nav() + f"""<main id="conteudo">
<header class="bhero">
  <svg class="bf" viewBox="0 0 200 200" aria-hidden="true"><use href="#bf"/></svg>
  <svg class="bf bf--l" viewBox="0 0 200 200" aria-hidden="true"><use href="#bf"/></svg>
  <div class="wrap">
    <span class="kicker">{BLOG_NAME}</span>
    <h1>Cuidar do diabetes também é cuidar de <em>como você se sente</em>.</h1>
    <p class="lead">Textos de Elaine Rosa sobre o lado emocional de viver com diabetes: informação com cuidado, sem culpa e sem promessas fáceis.</p>
  </div>
</header>

<section class="bintro reveal">
  <h2>Um espaço para falar do que o exame não mostra</h2>
  <p>O {BLOG_NAME} reúne artigos que escrevo como psicóloga (CRP 06/127648) e educadora em diabetes. A ideia é traduzir, em linguagem clara, o que muita gente sente e raramente consegue dizer na consulta: o cansaço da rotina, a culpa depois de um resultado, o medo de passar mal e a dificuldade de aceitar uma condição que não escolhemos.</p>
  <p>A base é a Terapia de Aceitação e Compromisso (ACT), que trabalha a flexibilidade psicológica: perceber pensamentos e emoções difíceis sem ser dominado por eles e dar passos possíveis em direção ao que importa. Você encontra textos sobre {link(todos[0], "diabetes e saúde mental")}, {link(todos[1], "aceitação do diabetes")}, {link(todos[2], "diabetes tipo 2 e culpa")}, {link(todos[3], "diabetes na família")} e {link(todos[4], "medo de hipoglicemia")}.</p>
  <p>Os artigos são informativos e não substituem a avaliação da sua equipe de saúde nem o acompanhamento psicológico. Ajustes de medicação, metas e monitorização devem ser definidos com quem acompanha o seu tratamento. Em momentos de sofrimento intenso, o CVV atende gratuitamente, a qualquer hora, pelo 188.</p>
</section>

<section class="bsearch reveal" role="search" aria-label="Buscar artigos do blog">
  <label for="busca" class="sr-only">Buscar artigos</label>
  <div class="bsearch__box">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input id="busca" type="search" placeholder="Buscar por tema, ex.: família" autocomplete="off" enterkeyhint="search">
    <button type="button" id="busca-limpar" class="bsearch__clear" hidden>Limpar</button>
  </div>
  <p id="busca-status" class="bsearch__status" aria-live="polite"></p>
</section>

<section class="pin">
  <div class="pin__stick"><div class="wrap">
    <div class="proc__head">
      <div><span class="kicker">Comece por aqui</span><h2>Quatro textos para <em>respirar fundo</em>.</h2></div>
      <p>Cansaço, aceitação, culpa e família: por onde a conversa costuma começar.</p>
    </div>
    {proc_cards(todos, "/")}
  </div></div>
</section>

<section class="bpad"><div class="wrap"><span class="kicker" style="margin-bottom:22px">Mais do {BLOG_NAME}</span><div class="bgrid">{cards}</div>
  <p class="bvazio" id="busca-vazio" hidden>Nenhum artigo encontrado para essa busca. Tente outra palavra, como <b>família</b>, <b>culpa</b> ou <b>hipoglicemia</b>.</p>
</div></section>

<section class="bpad"><div class="wrap"><div class="bbook reveal">
  <img src="/assets/img/livro-sem-fundo-420.webp" alt="Capa do livro Há vida com diabetes, de Elaine Rosa" width="420" height="482" loading="lazy" decoding="async">
  <div>
    <span class="kicker">O livro</span>
    <h2>Há vida com diabetes, <em>e ela pode ser extraordinária</em>.</h2>
    <p>Se estes textos conversam com o que você vive, o livro vai além: uma narrativa real, acolhedora e honesta, para quem tem diabetes e para quem caminha ao lado.</p>
    <a class="btn btn--gold" href="/#livro"><svg><use href="#i-book"/></svg>Conhecer o livro</a>
  </div>
</div></div></section>
</main>
""" + rodape() + JS_BASE + JS_BUSCA + "<script>\n" + PROC_JS + "</script>\n</body></html>\n"
    return h




def proc_cards(todos, pre):
    """Quatro cartões no estilo 'processo': foto de fundo, número grande, título curto e resumo."""
    out = []
    for i, p in enumerate(todos[:4], 1):
        base = f"{pre}assets/img/blog/{p['img']}"
        out.append(
            f'<a class="proc__card" href="/blog/{p["slug"]}" data-busca="{busca_txt(p)}">'
            f'<img class="proc__img" src="{base}-900.webp" srcset="{base}-480.webp 480w, {base}-900.webp 900w" sizes="(max-width:900px) 78vw, 300px" width="900" height="600" loading="lazy" decoding="async" alt="{html.escape(p["alt"])}">'
            f'<p class="proc__num" aria-hidden="true">{i:02d}</p>'
            f'<span class="proc__cat">{esc(p["cat"])}</span><h3>{esc(p["curto"])}</h3><p>{esc(p["art"]["sub"])}</p>'
            f'<span class="proc__more">Ler o artigo <svg><use href="#i-arrow"/></svg></span></a>')
    return '<div class="proc reveal">' + "".join(out) + "</div>"


def busca_txt(p):
    import unicodedata
    n = unicodedata.normalize("NFD", " ".join([p["art"]["titulo"], p["desc"], p["cat"], p["curto"]]))
    return html.escape(re.sub(r"[̀-ͯ]", "", n).lower())


def secao_index(todos):
    return f'''<!-- BLOG:START -->
<section class="espaco pin" id="espaco-saude" data-dot="Espaço Saúde">
  <div class="pin__stick"><div class="wrap">
    <div class="proc__head">
      <div>
        <span class="kicker reveal">{BLOG_NAME}</span>
        <h2 class="reveal d1">Cuidar do diabetes também é cuidar de <em>como você se sente</em>.</h2>
      </div>
      <p class="reveal d2">Artigos de Elaine Rosa sobre o lado emocional de viver com diabetes: cansaço, culpa, medo e família.</p>
    </div>
    {proc_cards(todos, "")}
    <div class="espaco__cta reveal"><a class="btn btn--primary btn--lg" href="/blog">Ver todos os artigos <svg><use href="#i-arrow"/></svg></a></div>
  </div></div>
</section>
<!-- BLOG:END -->'''

# ---------------------------------------------------------------- execução
def main():
    global CSS_NAME, SPRITE
    SPRITE = extrair_sprite() + "\n"
    global PROC
    PROC = (ROOT / "scripts" / "process.css").read_text(encoding="utf-8")
    css = extrair_css_base() + "\n" + (ROOT / "scripts" / "blog-extra.css").read_text(encoding="utf-8") + "\n" + PROC
    CSS_NAME = f"blog.{hashlib.sha1(css.encode()).hexdigest()[:8]}.css"
    for velho in (ROOT / "assets").glob("blog.*.css"):
        velho.unlink()
    (ROOT / "assets" / CSS_NAME).write_text(css, encoding="utf-8")

    for p in POSTS:
        p["art"] = parse_artigo(ler_docx(ARTIGOS / p["docx"]))
        rev = ROOT / "scripts" / "artigos-revisados" / (p["slug"] + ".md")
        if rev.exists():
            p["art"] = art_de_md(rev, p["art"])
        aplicar_substituicoes(p["slug"], p["art"])
        a = p["art"]
        palavras = sum(len(plain(x if isinstance(x, str) else " ".join(x)).split()) for _, x in a["corpo"])
        palavras += sum(len(q.split()) + len(r.split()) for q, r in a["faq"]) + len(a["proximo"].split())
        a["min"] = max(2, math.ceil(palavras / 190))
        print(f"  {p['slug']}: {p['art']['min']} min, {len(p['art']['faq'])} FAQs, {len(p['art']['refs'])} refs")

    (ROOT / "blog").mkdir(exist_ok=True)
    (ROOT / "blog" / "index.html").write_text(pagina_indice(POSTS), encoding="utf-8")
    for p in POSTS:
        d = ROOT / "blog" / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(pagina_artigo(p, POSTS), encoding="utf-8")

    # seção do blog na página principal
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    idx = re.sub(r"/\* PROC:START \*/.*?/\* PROC:END \*/", lambda m: "/* PROC:START */\n" + PROC + "/* PROC:END */", idx, flags=re.S)
    procjs = "<!-- PROCJS:START -->\n<script>\n" + PROC_JS + "</script>\n<!-- PROCJS:END -->"
    idx = re.sub(r"<!-- PROCJS:START -->.*?<!-- PROCJS:END -->", lambda m: procjs, idx, flags=re.S)
    idx = re.sub(r"<!-- BLOG:START -->.*?<!-- BLOG:END -->", lambda m: secao_index(POSTS), idx, flags=re.S)
    (ROOT / "index.html").write_text(idx, encoding="utf-8")

    # sitemap
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sm = re.sub(r"\s*<url><loc>" + re.escape(SITE) + r"/blog[^<]*</loc>.*?</url>", "", sm)
    novas = [f"  <url><loc>{SITE}/blog</loc><lastmod>{HOJE}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>"]
    novas += [f"  <url><loc>{SITE}/blog/{p['slug']}</loc><lastmod>{p['pub']}</lastmod><priority>0.7</priority></url>" for p in POSTS]
    sm = sm.replace("</urlset>", "\n".join(novas) + "\n</urlset>")
    (ROOT / "sitemap.xml").write_text(sm, encoding="utf-8")
    print("ok:", CSS_NAME)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
