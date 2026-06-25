# Architecture

## Repositório novo

Recomendado: criar um repo novo, por exemplo:

`vesselflow-pvq-next`

## Camadas

1. **Nomination Core**
   - Campos objetivos para decisão de nomeação.
2. **Technical Evidence**
   - Evidências técnicas/documentais usadas pela consultora/MQP.
3. **Full Archive**
   - 392 campos preservados para auditoria/exportação.
4. **Operational State**
   - Respostas de estado por área e status final.

## Integração futura com repo atual

O repo atual deve consumir este pacote por:
- cópia controlada de contratos; ou
- submodule/package; ou
- router read-only importado depois de validação.

Nada deve ser migrado por `git add -A`.
