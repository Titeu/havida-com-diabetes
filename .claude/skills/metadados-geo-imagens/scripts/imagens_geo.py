"""Metadados GEO das imagens do site: preparar, aplicar e verificar.

Grava os 7 campos do padrão (filename, Título, Assunto, Marcas, Comentários, Autores, Direitos Autorais)
DENTRO de cada arquivo de imagem (XMP + EXIF), sem reprocessar a imagem (não perde qualidade).
Formatos: WebP, JPEG e PNG. AVIF não é gravado por este script (avisa).

Uso (na raiz da pasta do cliente):
  python .claude/skills/metadados-geo-imagens/scripts/imagens_geo.py preparar
  python .claude/skills/metadados-geo-imagens/scripts/imagens_geo.py aplicar
  python .claude/skills/metadados-geo-imagens/scripts/imagens_geo.py verificar [--html site/dist]

Opções: --site <pasta do site> (padrão: site)  ·  --manifesto <arquivo> (padrão: <site>/imagens-geo.json)
        --public <pasta servida> (padrão: <site>/public; site em HTML puro sem build: --site . --public .)

Só usa a biblioteca padrão do Python (Pillow é opcional, só para ler o tamanho de WebP simples).
"""
import argparse
import fnmatch
import json
import re
import struct
import sys
import unicodedata
import zlib
from html.parser import HTMLParser
from pathlib import Path
from xml.sax.saxutils import escape

EXTS = {".webp", ".jpg", ".jpeg", ".png", ".avif"}
NOME_OK = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.(?:webp|jpe?g|png|avif)$")
PENDENTE = re.compile(r"\[(?:a confirmar|preencher)[^\]]*\]|lorem ipsum", re.I)
IA = "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"
FOTO = "http://cv.iptc.org/newscodes/digitalsourcetype/digitalCapture"
CAMPOS = ("titulo", "assunto", "marcas", "comentarios", "autores", "direitos")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ----------------------------------------------------------------------------- manifesto

def carregar(manifesto: Path) -> dict:
    if not manifesto.exists():
        return {"padrao": {}, "ignorar": ["favicon*", "apple-touch-icon*", "icon-*"], "imagens": []}
    return json.loads(manifesto.read_text(encoding="utf-8"))


def salvar(manifesto: Path, dados: dict) -> None:
    manifesto.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def imagens_do_site(public: Path, ignorar: list) -> list:
    out = []
    for p in sorted(public.rglob("*")):
        if p.is_file() and p.suffix.lower() in EXTS:
            rel = p.relative_to(public).as_posix()
            if not any(fnmatch.fnmatch(p.name, g) or fnmatch.fnmatch(rel, g) for g in ignorar):
                out.append(rel)
    return out


def arquivos_da_entrada(entrada: dict, todos: list) -> list:
    achados = []
    for padrao in entrada.get("arquivos", []):
        achados += [r for r in todos if fnmatch.fnmatch(r, padrao)]
    return sorted(set(achados))


def resolver(entrada: dict, padrao: dict) -> dict:
    """Campos finais da imagem: o que a entrada não define vem do bloco `padrao` do cliente."""
    r = {k: entrada.get(k) if entrada.get(k) not in (None, "", []) else padrao.get(k) for k in
         ("titulo", "assunto", "comentarios", "autores", "direitos", "credito", "origem",
          "cidade", "estado", "pais", "site_direitos")}
    marcas = list(entrada.get("marcas") or [])
    for m in padrao.get("marcas_base") or []:
        if m not in marcas:
            marcas.append(m)
    r["marcas"] = marcas
    return r


# ----------------------------------------------------------------------------- XMP e EXIF

def _alt(v):
    return f'<rdf:Alt><rdf:li xml:lang="x-default">{escape(v)}</rdf:li></rdf:Alt>'


def _seq(vs):
    return "<rdf:Seq>" + "".join(f"<rdf:li>{escape(v)}</rdf:li>" for v in vs) + "</rdf:Seq>"


def _bag(vs):
    return "<rdf:Bag>" + "".join(f"<rdf:li>{escape(v)}</rdf:li>" for v in vs) + "</rdf:Bag>"


def termos_assunto(assunto: str) -> list:
    return [t.strip() for t in re.split(r"[;,]", assunto or "") if t.strip()]


def montar_xmp(c: dict) -> bytes:
    palavras = []
    for t in termos_assunto(c["assunto"]) + list(c["marcas"]):
        if t not in palavras:
            palavras.append(t)
    autores = [a.strip() for a in (c["autores"] if isinstance(c["autores"], list) else [c["autores"]]) if a]
    props = [
        f"<dc:title>{_alt(c['titulo'])}</dc:title>",
        f"<dc:description>{_alt(c['comentarios'])}</dc:description>",
        f"<dc:subject>{_bag(palavras)}</dc:subject>",
        f"<dc:creator>{_seq(autores)}</dc:creator>",
        f"<dc:rights>{_alt(c['direitos'])}</dc:rights>",
        f"<photoshop:Headline>{escape(c['titulo'])}</photoshop:Headline>",
        f"<exif:UserComment>{_alt(c['comentarios'])}</exif:UserComment>",
        "<xmpRights:Marked>True</xmpRights:Marked>",
    ]
    if c.get("credito"):
        props.append(f"<photoshop:Credit>{escape(c['credito'])}</photoshop:Credit>")
    if c.get("site_direitos"):
        props.append(f"<xmpRights:WebStatement>{escape(c['site_direitos'])}</xmpRights:WebStatement>")
    for campo, tag in (("cidade", "City"), ("estado", "State"), ("pais", "Country")):
        if c.get(campo):
            props.append(f"<photoshop:{tag}>{escape(c[campo])}</photoshop:{tag}>")
    if c.get("origem") in ("ia", "foto"):
        props.append(f"<Iptc4xmpExt:DigitalSourceType>{IA if c['origem'] == 'ia' else FOTO}"
                     "</Iptc4xmpExt:DigitalSourceType>")
    xml = (
        '<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>'
        '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
        '<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/"'
        ' xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/" xmlns:exif="http://ns.adobe.com/exif/1.0/"'
        ' xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/"'
        ' xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/">'
        + "".join(props)
        + '</rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="w"?>'
    )
    return xml.encode("utf-8")


def montar_exif(c: dict) -> bytes:
    """TIFF little-endian com IFD0: descrição, autor, direitos e as tags XP* que o Windows mostra."""
    def utf16(s):
        return (s or "").encode("utf-16-le") + b"\x00\x00"

    def ascii_(s):
        # tags EXIF "ASCII" são 7 bits: sem acento (o texto completo, acentuado, vai no XMP e nas tags XP*)
        s = (s or "").replace("—", "-").replace("–", "-").replace("©", "(c)")
        return unicodedata.normalize("NFKD", s).encode("ascii", "ignore") + b"\x00"

    autores = c["autores"] if isinstance(c["autores"], list) else [c["autores"]]
    autores_txt = "; ".join(a for a in autores if a)
    palavras = "; ".join(dict.fromkeys(list(c["marcas"]) + termos_assunto(c["assunto"])))
    tags = sorted([
        (0x010E, 2, ascii_(c["titulo"])),        # ImageDescription
        (0x013B, 2, ascii_(autores_txt)),        # Artist
        (0x8298, 2, ascii_(c["direitos"])),      # Copyright
        (0x9C9B, 1, utf16(c["titulo"])),         # XPTitle      → Título
        (0x9C9C, 1, utf16(c["comentarios"])),    # XPComment    → Comentários
        (0x9C9D, 1, utf16(autores_txt)),         # XPAuthor     → Autores
        (0x9C9E, 1, utf16(palavras)),            # XPKeywords   → Marcas
        (0x9C9F, 1, utf16(c["assunto"])),        # XPSubject    → Assunto
    ])
    n = len(tags)
    dados_ini = 8 + 2 + n * 12 + 4
    entradas, dados = b"", b""
    for tag, tipo, valor in tags:
        if len(valor) <= 4:
            campo = valor.ljust(4, b"\x00")
        else:
            campo = struct.pack("<I", dados_ini + len(dados))
            dados += valor + (b"\x00" if len(valor) % 2 else b"")
        entradas += struct.pack("<HHI", tag, tipo, len(valor)) + campo
    return b"II*\x00" + struct.pack("<I", 8) + struct.pack("<H", n) + entradas + b"\x00\x00\x00\x00" + dados


# ----------------------------------------------------------------------------- gravação por formato

def _chunk_riff(fourcc: bytes, dados: bytes) -> bytes:
    return fourcc + struct.pack("<I", len(dados)) + dados + (b"\x00" if len(dados) % 2 else b"")


def gravar_webp(caminho: Path, xmp: bytes, exif: bytes) -> None:
    b = caminho.read_bytes()
    if b[:4] != b"RIFF" or b[8:12] != b"WEBP":
        raise ValueError("não é WebP válido")
    chunks, i = [], 12
    while i + 8 <= len(b):
        fourcc, tam = b[i:i + 4], struct.unpack("<I", b[i + 4:i + 8])[0]
        chunks.append([fourcc, b[i + 8:i + 8 + tam]])
        i += 8 + tam + (tam % 2)
    chunks = [ch for ch in chunks if ch[0] not in (b"EXIF", b"XMP ")]
    if chunks[0][0] != b"VP8X":
        w, h, alfa = _tamanho_webp_simples(chunks[0])
        vp8x = bytes([0x10 if alfa else 0, 0, 0, 0]) + (w - 1).to_bytes(3, "little") + (h - 1).to_bytes(3, "little")
        chunks.insert(0, [b"VP8X", vp8x])
    cab = bytearray(chunks[0][1])
    cab[0] |= 0x08 | 0x04  # tem EXIF e XMP
    chunks[0][1] = bytes(cab)
    chunks += [[b"EXIF", exif], [b"XMP ", xmp]]
    corpo = b"WEBP" + b"".join(_chunk_riff(f, d) for f, d in chunks)
    caminho.write_bytes(b"RIFF" + struct.pack("<I", len(corpo)) + corpo)


def _tamanho_webp_simples(chunk):
    fourcc, d = chunk
    if fourcc == b"VP8 ":
        w, h = struct.unpack("<HH", d[6:10])
        return w & 0x3FFF, h & 0x3FFF, False
    if fourcc == b"VP8L":
        bits = struct.unpack("<I", d[1:5])[0]
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1, bool((bits >> 28) & 1)
    raise ValueError(f"chunk WebP inesperado: {fourcc!r}")


def gravar_jpeg(caminho: Path, xmp: bytes, exif: bytes) -> None:
    b = caminho.read_bytes()
    if b[:2] != b"\xff\xd8":
        raise ValueError("não é JPEG válido")
    i, segs = 2, []
    while i < len(b) and b[i] == 0xFF and b[i + 1] not in (0xDA, 0xD9):
        marca, tam = b[i + 1], struct.unpack(">H", b[i + 2:i + 4])[0]
        segs.append((marca, b[i:i + 2 + tam]))
        i += 2 + tam
    resto = b[i:]
    xmp_cab = b"http://ns.adobe.com/xap/1.0/\x00"
    segs = [s for s in segs if not (s[0] == 0xE1 and (s[1][4:10] == b"Exif\x00\x00" or s[1][4:4 + len(xmp_cab)] == xmp_cab))]
    def app1(dados):
        return b"\xff\xe1" + struct.pack(">H", len(dados) + 2) + dados
    novos = [app1(b"Exif\x00\x00" + exif), app1(xmp_cab + xmp)]
    pos = 1 if segs and segs[0][0] == 0xE0 else 0  # depois do JFIF
    corpo = [s[1] for s in segs]
    caminho.write_bytes(b"\xff\xd8" + b"".join(corpo[:pos] + novos + corpo[pos:]) + resto)


def gravar_png(caminho: Path, xmp: bytes, exif: bytes) -> None:
    b = caminho.read_bytes()
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("não é PNG válido")
    i, chunks = 8, []
    while i < len(b):
        tam = struct.unpack(">I", b[i:i + 4])[0]
        tipo = b[i + 4:i + 8]
        chunks.append((tipo, b[i:i + 12 + tam]))
        i += 12 + tam
    def eh_xmp(t, raw):
        return t == b"iTXt" and raw[8:8 + 17] == b"XML:com.adobe.xmp"
    chunks = [c for c in chunks if c[0] != b"eXIf" and not eh_xmp(*c)]
    def novo(tipo, dados):
        return struct.pack(">I", len(dados)) + tipo + dados + struct.pack(">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF)
    extras = [novo(b"eXIf", exif), novo(b"iTXt", b"XML:com.adobe.xmp\x00\x00\x00\x00\x00" + xmp)]
    corpo = [c[1] for c in chunks]
    caminho.write_bytes(b[:8] + corpo[0] + b"".join(extras) + b"".join(corpo[1:]))


GRAVADORES = {".webp": gravar_webp, ".jpg": gravar_jpeg, ".jpeg": gravar_jpeg, ".png": gravar_png}


# ----------------------------------------------------------------------------- leitura (verificação)

def ler_xmp(caminho: Path) -> str:
    b = caminho.read_bytes()
    ini, fim = b.find(b"<x:xmpmeta"), b.find(b"</x:xmpmeta>")
    return b[ini:fim + 12].decode("utf-8", "replace") if ini >= 0 and fim > ini else ""


def campos_no_arquivo(caminho: Path) -> dict:
    x = ler_xmp(caminho)
    def pega(tag):
        m = re.search(rf"<{tag}>(.*?)</{tag}>", x, re.S)
        return re.sub(r"<[^>]+>", " ", m.group(1)).strip() if m else ""
    return {"titulo": pega("dc:title"), "comentarios": pega("dc:description"), "marcas": pega("dc:subject"),
            "autores": pega("dc:creator"), "direitos": pega("dc:rights"), "assunto": pega("dc:subject")}


class _Imgs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imgs = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            self.imgs.append(dict(attrs))


# ----------------------------------------------------------------------------- comandos

def cmd_preparar(public: Path, manifesto: Path) -> int:
    dados = carregar(manifesto)
    todos = imagens_do_site(public, dados.get("ignorar", []))
    cobertos = {r for e in dados["imagens"] for r in arquivos_da_entrada(e, todos)}
    novos = [r for r in todos if r not in cobertos]
    if not dados.get("padrao"):
        dados["padrao"] = {
            "autores": "[preencher: nome — profissão | registro | especialidade]",
            "direitos": "[preencher: © titular — marca]",
            "credito": "", "site_direitos": "", "cidade": "", "estado": "", "pais": "Brasil",
            "marcas_base": ["[preencher: nome do cliente]", "[preencher: cidade – UF]"],
        }
    for r in novos:
        dados["imagens"].append({
            "arquivos": [r], "origem": "foto",
            "titulo": "[preencher]", "assunto": "[preencher]", "marcas": [],
            "comentarios": "[preencher]", "alt": "[preencher]",
        })
    salvar(manifesto, dados)
    print(f"Manifesto: {manifesto}  ·  imagens no site: {len(todos)}  ·  novas entradas: {len(novos)}")
    for r in novos:
        print(f"  + {r}")
    return 0


def cmd_aplicar(public: Path, manifesto: Path) -> int:
    dados = carregar(manifesto)
    todos = imagens_do_site(public, dados.get("ignorar", []))
    gravados, erros = 0, 0
    for e in dados["imagens"]:
        if e.get("decorativa_sem_metadados"):
            continue
        c = resolver(e, dados.get("padrao", {}))
        faltam = [k for k in CAMPOS if not c.get(k)]
        pend = [k for k in CAMPOS if c.get(k) and PENDENTE.search(json.dumps(c[k], ensure_ascii=False))]
        alvo = arquivos_da_entrada(e, todos)
        if faltam or pend or not alvo:
            erros += 1
            print(f"  ✗ {e.get('arquivos')}: " + "; ".join(filter(None, [
                f"campos vazios {faltam}" if faltam else "", f"pendentes {pend}" if pend else "",
                "nenhum arquivo encontrado" if not alvo else ""])))
            continue
        xmp, exif = montar_xmp(c), montar_exif(c)
        for rel in alvo:
            p = public / rel
            gravar = GRAVADORES.get(p.suffix.lower())
            if not gravar:
                erros += 1
                print(f"  ✗ {rel}: formato {p.suffix} não gravado por este script (use WebP)")
                continue
            try:
                gravar(p, xmp, exif)
                gravados += 1
                print(f"  ✓ {rel}")
            except Exception as ex:  # noqa: BLE001
                erros += 1
                print(f"  ✗ {rel}: {ex}")
    print(f"Gravados: {gravados}  ·  com problema: {erros}")
    return 1 if erros else 0


def cmd_verificar(public: Path, manifesto: Path, html_dir) -> int:
    dados = carregar(manifesto)
    todos = imagens_do_site(public, dados.get("ignorar", []))
    entrada_de = {}
    for e in dados["imagens"]:
        for r in arquivos_da_entrada(e, todos):
            entrada_de[r] = e
    falhas = []
    for rel in todos:
        nome = Path(rel).name
        if not NOME_OK.match(nome):
            falhas.append(f"{rel}: nome fora do padrão (minúsculas, sem acento, palavras-com-hífen)")
        e = entrada_de.get(rel)
        if e is None:
            falhas.append(f"{rel}: sem entrada no manifesto ({manifesto.name})")
            continue
        if e.get("decorativa_sem_metadados"):
            continue
        if Path(rel).suffix.lower() == ".avif":
            falhas.append(f"{rel}: AVIF sem gravação de metadados neste processo (publique em WebP)")
            continue
        lido = campos_no_arquivo(public / rel)
        vazios = [k for k in ("titulo", "comentarios", "marcas", "autores", "direitos") if not lido[k]]
        if vazios:
            falhas.append(f"{rel}: metadados ausentes no arquivo {vazios} (rode `aplicar`)")
        elif PENDENTE.search(" ".join(lido.values())):
            falhas.append(f"{rel}: metadados com pendência [a confirmar]/[preencher]")
        if (not e.get("alt") and not e.get("decorativa")) or PENDENTE.search(e.get("alt", "")):
            falhas.append(f"{rel}: alt não definido no manifesto")
    if html_dir:
        # alt="" é válido para uso decorativo (miniatura que repete a foto principal, ícone dentro de botão com
        # texto). Reprova: <img> sem atributo alt, ou imagem de conteúdo que não tem alt descritivo em lugar nenhum.
        descrita, so_vazia = set(), {}
        for pagina in sorted(Path(html_dir).rglob("*.html")):
            p = _Imgs()
            p.feed(pagina.read_text(encoding="utf-8", errors="replace"))
            for img in p.imgs:
                src = (img.get("src") or "").split("?")[0]
                if src.startswith("data:"):
                    continue  # marcador vazio (ex.: lightbox antes de carregar a foto)
                e = entrada_de.get(src.lstrip("/"))
                chave = id(e) if e else src
                if "alt" not in img:
                    falhas.append(f"{pagina.relative_to(html_dir)}: <img src=\"{src}\"> sem atributo alt")
                elif img["alt"].strip():
                    descrita.add(chave)
                elif not (e and e.get("decorativa")):
                    so_vazia.setdefault(chave, f"{pagina.relative_to(html_dir)}: {src}")
        for chave, onde in so_vazia.items():
            if chave not in descrita:
                falhas.append(f"{onde} só aparece com alt vazio no site (descreva ou marque \"decorativa\": true)")
    print(f"Imagens verificadas: {len(todos)}")
    if falhas:
        print(f"REPROVADO — {len(falhas)} problema(s):")
        for f in falhas:
            print(f"  ✗ {f}")
        return 1
    print("APROVADO — todas as imagens com nome, metadados GEO e alt conforme o padrão.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("comando", choices=["preparar", "aplicar", "verificar"])
    ap.add_argument("--site", default="site")
    ap.add_argument("--manifesto")
    ap.add_argument("--public", help="pasta servida na raiz do site (padrão: <site>/public; site em HTML puro: --public .)")
    ap.add_argument("--html", help="pasta do build (ex.: site/dist) para conferir os alt no HTML")
    a = ap.parse_args()
    site = Path(a.site)
    manifesto = Path(a.manifesto) if a.manifesto else site / "imagens-geo.json"
    public = Path(a.public) if a.public else site / "public"
    if not public.is_dir():
        print(f"Pasta {public} não encontrada.")
        return 2
    if a.comando == "preparar":
        return cmd_preparar(public, manifesto)
    if a.comando == "aplicar":
        return cmd_aplicar(public, manifesto)
    return cmd_verificar(public, manifesto, a.html)


if __name__ == "__main__":
    sys.exit(main())
