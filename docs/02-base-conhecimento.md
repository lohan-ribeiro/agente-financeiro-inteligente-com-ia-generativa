# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Registra interações anteriores para fornecer contexto e acompanhar a evolução financeira do usuário ao longo do tempo. |
| `produtos_financeiros.json` | JSON | Informações sobre produtos financeiros, risco, liquidez, rentabilidade esperada e descrição. |
| `transacoes.csv` | CSV | Contém o histórico de receitas e despesas do usuário, utilizado para análise dos padrões de gastos e cálculo da saúde financeira. |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Não foram realizadas adaptações nos dados. O agente trabalha diretamente com as informações fornecidas pelo usuário nos formatos CSV ou JSON.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos da pasta data são carregados na inicialização da aplicação.

- transacoes.csv fornece o histórico financeiro do usuário.
- historico_atendimento.csv permite contextualizar conversas anteriores.
- investimentos.json é utilizado como base de conhecimento para explicar modalidades de investimento.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são consultados dinamicamente antes da geração da resposta.

O contexto enviado ao modelo inclui:

- informações financeiras do usuário;
- perfil de investidor;
- histórico relevante de atendimentos;
- informações sobre investimentos quando necessário.

As instruções de comportamento, segurança e limitações permanecem definidas no System Prompt, enquanto os dados são adicionados dinamicamente ao contexto da conversa.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Contexto do Usuário

Nome: João Silva

Receita Mensal
- Salário: R$ 5.500

Despesas
- Moradia: R$ 1.500
- Alimentação: R$ 850
- Transporte: R$ 400
- Lazer: R$ 600

Perfil do Investidor
- Conservador

Último Atendimento
- Objetivo: Criar uma reserva de emergência.
- Recomendação anterior: Reduzir gastos com lazer em 10%.

Base de Conhecimento (Investimentos)

Tesouro Selic
- Categoria: Renda Fixa
- Risco: Baixo
- Liquidez: Alta
- Indicado para: Perfil Conservador
- Descrição: Investimento de baixo risco frequentemente utilizado para reserva de emergência.

Instrução ao Agente

Analise a situação financeira do usuário utilizando exclusivamente os dados fornecidos, gere insights personalizados e explique conceitos financeiros de forma clara e educativa.
```
