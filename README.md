# PDTSP com Metaheurísticas

Implementação e comparação experimental de metaheurísticas aplicadas ao **Problema do Caixeiro Viajante com Coleta e Entrega (PDTSP)**.

O projeto utiliza duas abordagens principais:

- **Iterative Local Search (ILS)**
- **Biased Random-Key Genetic Algorithm (BRKGA)**

O trabalho foi desenvolvido para a disciplina de **Inteligência Artificial**.

## Sobre o projeto

O **Problema do Caixeiro Viajante com Coleta e Entrega (PDTSP)** é uma extensão do clássico Problema do Caixeiro Viajante.

O objetivo é encontrar uma rota de menor custo que percorra um conjunto de cidades respeitando restrições de coleta e entrega.

Para cada requisição existe um par:

```text
Coleta → Entrega
```

A cidade correspondente à coleta deve obrigatoriamente ser visitada antes de sua respectiva entrega.

O projeto utiliza metaheurísticas para procurar soluções de boa qualidade para esse problema de otimização combinatória.

## Modelagem do problema

A implementação considera:

- um conjunto de cidades;
- coordenadas geográficas para cada cidade;
- uma matriz de distâncias;
- restrições de precedência;
- uma rota representando a sequência de visitação;
- uma função objetivo baseada no custo total da rota.

A matriz de custos é construída utilizando a distância euclidiana entre as cidades.

Para cada relação de coleta e entrega:

```text
pickup → delivery
```

o nó de coleta deve aparecer antes do nó de entrega na rota.

## Metaheurísticas implementadas

Foram implementadas duas estratégias diferentes de otimização.

## Iterative Local Search — ILS

O **Iterative Local Search (ILS)** é uma metaheurística baseada na melhoria sucessiva de uma solução.

O algoritmo combina duas estratégias principais:

```text
Busca Local
    +
Perturbação
```

A busca local procura melhorar a solução atual, enquanto a perturbação permite explorar novas regiões do espaço de soluções.

### Inicialização

O algoritmo constrói inicialmente uma rota que respeita as relações de precedência.

Primeiro são inseridos os nós de coleta e posteriormente os nós de entrega.

Outros nós que não pertencem diretamente a esses grupos também são adicionados à rota.

### Hill Climbing

A busca local utiliza **Hill Climbing** com o operador de troca (`swap`).

Duas cidades da rota são selecionadas aleatoriamente:

```text
Antes:

A → B → C → D

Troca B ↔ D

A → D → C → B
```

A nova solução é avaliada.

Se possuir custo menor, a alteração é mantida.

Caso contrário, a troca é desfeita.

### Perturbação

Para evitar que o algoritmo permaneça preso em um ótimo local, são realizadas várias trocas aleatórias sobre a melhor solução encontrada.

Essa nova rota é utilizada como ponto de partida para uma nova busca local.

O processo pode ser representado como:

```text
Melhor solução atual
        ↓
   Perturbação
        ↓
    Nova região
        ↓
  Hill Climbing
        ↓
Melhor solução encontrada
```

## Biased Random-Key Genetic Algorithm — BRKGA

O **BRKGA** é uma metaheurística populacional baseada em algoritmos genéticos.

Em vez de representar diretamente uma rota, cada indivíduo é representado por um vetor de números reais aleatórios entre `0` e `1`.

Exemplo:

```text
[0.72, 0.15, 0.83, 0.31, 0.48]
```

Esses valores são chamados de **chaves aleatórias**.

## Decodificação

As chaves são ordenadas para determinar a sequência de cidades.

Exemplo:

```text
Chaves:

Cidade 0 → 0.72
Cidade 1 → 0.15
Cidade 2 → 0.83
Cidade 3 → 0.31
Cidade 4 → 0.48
```

Ordenando os valores:

```text
1 → 3 → 4 → 0 → 2
```

Essa sequência é utilizada como base para a construção da rota.

## Tratamento das restrições de precedência

Durante a decodificação, o algoritmo verifica se um nó de entrega aparece antes de sua respectiva coleta.

Caso isso aconteça, a entrega é temporariamente armazenada e inserida somente depois que sua coleta correspondente já estiver presente na rota.

Esse mecanismo ajuda a produzir soluções compatíveis com as restrições do PDTSP.

## Evolução da população

A cada geração, o BRKGA divide a população de acordo com a qualidade das soluções.

A nova população é formada através de três mecanismos.

### Elite

As melhores soluções são preservadas diretamente para a próxima geração.

Isso garante que boas soluções encontradas anteriormente não sejam perdidas.

### Mutantes

Novos indivíduos completamente aleatórios são criados.

Os mutantes aumentam a diversidade da população e ajudam o algoritmo a explorar novas regiões do espaço de busca.

### Crossover enviesado

Novos indivíduos também são produzidos através do cruzamento entre:

- um indivíduo da elite;
- um indivíduo não pertencente à elite.

Para cada gene, existe uma probabilidade maior de herdar o valor pertencente ao indivíduo elite.

Essa probabilidade é controlada pelo parâmetro:

```text
rho
```

## Estrutura genérica de otimização

Além das metaheurísticas, o projeto possui classes genéricas utilizadas para organizar a implementação.

### `Algorithm`

Classe base dos algoritmos de otimização.

Define o fluxo geral:

```text
initialize()
     ↓
 advance()
     ↓
Verificação do critério de parada
     ↓
 finalize()
```

### `Problem`

Classe base utilizada para representar um problema de otimização.

### `Solution`

Representa uma solução candidata.

Cada solução possui:

```text
value
cost
```

onde:

- `value` representa a solução;
- `cost` representa seu custo.

### `Termination`

Classe base responsável pelos critérios de parada dos algoritmos.

O projeto utiliza um critério baseado em um número máximo de iterações.

## Experimento Time-to-Target

Também foi implementado um experimento **Time-to-Target (TTT)** para comparar o comportamento das metaheurísticas.

O objetivo é medir quantas iterações cada algoritmo precisa para atingir determinado valor-alvo.

No experimento atual:

```text
Target: 24000
Execuções por algoritmo: 20
```

Para cada execução, é registrado o número de iterações necessário até que a solução alcance o custo definido.

Os resultados são utilizados para gerar uma curva de probabilidade acumulada.

O gráfico permite comparar a distribuição do número de iterações necessárias pelos algoritmos.

O arquivo gerado é:

```text
grafico_ttt.png
```

## Estrutura do projeto

```text
.
├── main.py
├── ttt_experiment.py
├── report.md
├── README.md
├── LICENSE
├── grafico_ttt.png
│
└── program/
    ├── core/
    │   ├── algorithm.py
    │   ├── problem.py
    │   ├── solution.py
    │   └── termination.py
    │
    ├── algorithims/
    │   ├── ils.py
    │   ├── brkga.py
    │   └── sa.py
    │
    ├── termination/
    │   └── maximum_iteration.py
    │
    ├── problems/
    │   └── ...
    │
    └── instances/
        └── ...
```

> A pasta `algorithims` aparece dessa forma porque este é o nome utilizado atualmente pelos imports do projeto.

## Comparação dos algoritmos

O arquivo principal executa uma comparação entre ILS e BRKGA utilizando a mesma instância do PDTSP.

Ao final são apresentados os melhores custos encontrados por cada algoritmo.

## Como executar

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/pdtsp-metaheuristicas.git
```

Entre na pasta:

```bash
cd pdtsp-metaheuristicas
```

Execute:

```bash
python main.py
```

## Experimento Time-to-Target

Para executar o experimento é necessário instalar:

```text
NumPy
Matplotlib
```

Instale as dependências:

```bash
pip install numpy matplotlib
```

Depois execute:

```bash
python ttt_experiment.py
```

Ao final será gerado o gráfico:

```text
grafico_ttt.png
```

## Tecnologias e conceitos utilizados

- Python
- Inteligência Artificial
- Otimização combinatória
- Metaheurísticas
- Iterative Local Search
- Hill Climbing
- BRKGA
- Algoritmos genéticos
- Random Keys
- Busca local
- Time-to-Target
- NumPy
- Matplotlib

## Autores

- Pietro Pires Bertato
- Miguel Lopes de Almeida
- João Lustosa Cordeiro

## Licença

Consulte o arquivo `LICENSE` para informações sobre a licença do projeto.
