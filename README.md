# PVQ Next Operational State Bootstrap

Bootstrap limpo para criar o novo repositório do PVQ Next / Operational State.

Este pacote NÃO contém frontend, não altera `app.py`, não carrega storage runtime e não depende do repo contaminado.
Ele congela os contratos, modelos, evidências e amostra MADRE DE DEUS para iniciar backend read-only com segurança.

## Decisão de arquitetura

- O repo atual continua como fonte histórica e runtime legado.
- Este repo novo nasce como núcleo limpo de PVQ Next.
- Os 392 campos ficam preservados como `full archive`.
- O PVQ Next principal usa um `Nomination Core` objetivo.
- A liberação técnica é da consultora naval/MQP.
- Gerência só aprova exceção de negócio/risco, quando aplicável.

## Status MADRE DE DEUS

`PRE_APT_WITH_TECHNICAL_REVIEW`

Isto significa:
- pode seguir como candidato;
- não deve ser liberado automaticamente;
- exige liberação técnica/documental controlada.

## Validação rápida

```bash
python -m pvq_next.validate_contracts
```

## Próxima etapa

Criar endpoints GET read-only a partir dos contratos.
