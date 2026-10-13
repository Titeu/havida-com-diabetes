# Exemplo preenchido — consultório de psicologia (Elaine Rosa)

> **Só exemplo.** Mostra o [padrão](padrao.md) aplicado a uma cliente real (psicologia, Alphaville – Barueri/SP).
> Original: [`exemplo-elaine-rosa.docx`](exemplo-elaine-rosa.docx). Em outro cliente, **nenhum** destes termos é
> reaproveitado: os dados vêm da ficha do novo cliente.

## Como o padrão ficou para esta cliente

**Objetivo:** fortalecer a identificação de Elaine Rosa, o contexto da psicologia baseada em evidências e a
relevância geográfica em Alphaville – Barueri/SP.

**filename:** `palavra-chave-contexto-alphaville-barueri-sp.webp`

**Referências institucionais e geográficas prioritárias (Marcas):**
- Elaine Rosa
- Psicologia Baseada em Evidências
- Análise do Comportamento
- Terapia de Aceitação e Compromisso (ACT)
- Psicologia clínica
- Alphaville – Barueri/SP
- Edifício Pravda (Alphaville) — referência geográfica padronizada; não apresentar como endereço do consultório
  sem confirmação.

**Autores:** `Elaine Rosa – Psicóloga | CRP [número profissional a confirmar] | Especialista em ACT`
(+ `Alphaville – Barueri/SP` quando pertinente). Não publicar o CRP sem confirmação; não atribuir a ela a autoria
de fotografia não confirmada.

**Direitos Autorais:** `© Elaine Rosa – Psicologia Baseada em Evidências` (só quando os direitos forem dela ou autorizados).

**Comentários:** contextualizar no campo da psicologia quando houver fundamento; relacionar à atuação de Elaine
Rosa só quando confirmado; incorporar Alphaville – Barueri/SP quando pertinente; nunca inventar elementos visuais,
serviços, especialidades, endereço ou informação clínica.

## Palavras-chave prioritárias desta cliente

| Grupo | Termos |
|---|---|
| Entidade profissional | Elaine Rosa · psicóloga · psicologia baseada em evidências · psicologia clínica |
| Abordagens | Análise do Comportamento · Terapia de Aceitação e Compromisso · ACT · saúde mental · psicoterapia |
| Públicos e contextos | adolescentes · adultos · casais · famílias · pessoas com doenças crônicas (só quando corresponder aos serviços oferecidos e ao contexto da imagem) |
| SEO local | psicóloga em Alphaville · psicologia em Alphaville · psicóloga em Barueri · psicoterapia em Alphaville · Alphaville – Barueri/SP · Edifício Pravda (Alphaville), como referência geográfica quando aplicável |

## Como fica no manifesto (`site/imagens-geo.json`)

```json
{
  "padrao": {
    "autores": "Elaine Rosa — Psicóloga | CRP [a confirmar] | Especialista em ACT",
    "direitos": "© Elaine Rosa — Psicologia Baseada em Evidências",
    "cidade": "Barueri", "estado": "SP", "pais": "Brasil",
    "marcas_base": ["Elaine Rosa", "Alphaville – Barueri/SP"]
  },
  "imagens": [
    {
      "arquivos": ["img/ambiente/consultorio-sala-atendimento-alphaville-barueri-sp.webp"],
      "origem": "foto",
      "titulo": "Sala de atendimento do consultório de psicologia de Elaine Rosa em Alphaville",
      "assunto": "consultório de psicologia; sala de psicoterapia; psicologia clínica; Alphaville – Barueri/SP",
      "marcas": ["Psicologia clínica", "Edifício Pravda (Alphaville)"],
      "comentarios": "Sala de atendimento com poltronas, luz natural e decoração neutra, preparada para sessões de psicoterapia individual e de casal. O ambiente reservado favorece o sigilo e o conforto do paciente. Consultório de Elaine Rosa, psicóloga clínica, em Alphaville – Barueri/SP.",
      "alt": "Sala de atendimento do consultório com duas poltronas e luz natural"
    }
  ]
}
```

Enquanto o CRP estiver `[a confirmar]`, o script **não grava** e o portão **reprova**: confirme o número ou
retire o registro do campo Autores.
