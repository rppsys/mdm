# Estudos Gensim


Cada documento precisar ser um string. Ok

https://radimrehurek.com/gensim/auto_examples/core/run_core_concepts.html#sphx-glr-auto-examples-core-run-core-concepts-py


Modelos do Gensim:
sphx_glr_auto_examples_core_run_topics_and_transformations.py

# Decidir entre LSA e LDA

Latent Semantic Analysis (LSA):
O que é? O LSA é uma técnica de processamento de linguagem natural que analisa as relações entre um conjunto de documentos e os termos que eles contêm. Ele produz conceitos relacionados aos documentos e termos.
Como funciona? O LSA parte da hipótese distribucional, que assume que palavras com significados semelhantes ocorrerão em textos similares. Ele cria uma matriz de contagem de palavras por documento e usa a decomposição de valores singulares (SVD) para reduzir o número de linhas (termos) enquanto preserva a estrutura de similaridade entre colunas (documentos).
Aplicações: O LSA é usado em análise de tópicos, pontuação algorítmica de ensaios e análise de respostas construídas.
Vantagens: Alta confiabilidade e concordância com avaliadores humanos.
Desvantagens: Menos eficiente para grandes matrizes densas.
Exemplo: Descobrir temas comuns em conjuntos de documentos.
Latent Dirichlet Allocation (LDA):
O que é? O LDA é um modelo estatístico generativo para modelar tópicos extraídos automaticamente de corpora textuais.
Funcionamento: As observações (palavras) são agrupadas em documentos, e cada palavra é atribuída a um dos tópicos do documento. Cada documento contém um pequeno número de tópicos.
Aplicações: Descoberta de tópicos, classificação automática de documentos e análise de estruturas genéticas.
Vantagens: Flexibilidade, aplicável a diferentes domínios.
Desvantagens: Requer ajuste de hiperparâmetros.
Exemplo: Identificar tópicos em coleções de documentos.

## Penso em tentar com o LSA pra ver no que dá.
## Mas precisaria de um tutorial pra isso.

https://en.wikipedia.org/wiki/Latent_semantic_indexing

Então vou pegar os dados e escolher apenas as 2 maiores classes e aplicar LSI e ver aonde ele vai classificar cada um e ver se bate.

# 04/07/2024

Preciso gerar um arquivo texto onde cada linha é um documento.
















 


 



