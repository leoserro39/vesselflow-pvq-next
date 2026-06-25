# Operational State Model

## Regra de liberação

O sistema não libera automaticamente campo crítico com revisão técnica/documental pendente.

## Rotas de decisão

- `AUTO_SYSTEM_RULE`
- `HUMAN_DATA_REVIEW`
- `NAVAL_CONSULTANT_REVIEW`
- `MQP_REVIEW`
- `MANAGEMENT_ARBITRATION`
- `BUSINESS_POLICY_DECISION`
- `STATE_ARBITRATION_REQUIRED`

## Status principais

- `READY_FOR_NOMINATION`
- `PRE_APT_WITH_TECHNICAL_REVIEW`
- `PRE_APT_WITH_DOCUMENT_REVIEW`
- `BLOCKED`
- `POLICY_DEPENDENT`
- `NOT_APPLICABLE`

## MADRE DE DEUS

Estado recomendado:

`PRE_APT_WITH_TECHNICAL_REVIEW`

Revisões controladas:
1. Open Conditions of Class = Sim
2. ITF Blue Card expiry = 06/17/2025
3. Mooring Arrangement Plan = ABS, requer validação semântica/evidencial
