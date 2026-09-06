![](imagens/fig01.png)

# TRABALHO 1

**PARTE 1. EXPRESSÕES DE PERDAS EM SEMICONDUTORES DE POTÊNCIA**

**PARTE 2. PROJETO DE TRANSFORMADOR DE ALTA FREQUÊNCIA USANDO FERRITE DA THORNTON**

Equipe:

Fortaleza, 22 de agosto de 2026

---

## SUMÁRIO — PARTE 1


**1. DIODO DE POTÊNCIA**

- 1.1. Características Básicas
- 1.2. Princípio de Polarização
- 1.3. Perdas de Condução
- 1.4. Perdas de Comutação

**2. TIRISTOR E TRIAC DE POTÊNCIA**

- 2.1. Características Básicas
- 2.2. Princípio de Polarização
- 2.3. Perdas de Condução
- 2.4. Perdas de Comutação

**3. MOSFETs DE POTÊNCIA**

- 3.1. Características Básicas
- 3.2. Princípio de Polarização
- 3.3. Perdas de Condução
- 3.4. Perdas de Comutação

**4. IGBTs DE POTÊNCIA**

- 4.1. Características Básicas
- 4.2. Princípio de Polarização
- 4.3. Perdas de Condução
- 4.4. Perdas de Comutação

**5. REFERÊNCIAS**


## SUMÁRIO — PARTE 2

**1. ESPECIFICAÇÕES E CONSIDERAÇÕES**

**2. DIMENSIONAMENTO PASSO A PASSO**

**3. REFERÊNCIAS**

---

> **NOTA:** PESSOAL, O TEXTO DEVE SER EM PORTUGUÊS, EU FIZ O PRINT PARA COLOCAR COMO EXEMPLO. O TRABALHO DEVE SER FEITO DE MANEIRA QUE QUALQUER LEITOR POSSA ENTENDER PARA FAZER DIMENSIONAMENTO DE PERDAS EM SEMICONDUTORES.

---

# PARTE 1 — EXPRESSÕES DE PERDAS EM SEMICONDUTORES DE POTÊNCIA

## 1. DIODO DE POTÊNCIA

### 1.1. Características Básicas

Na Figura 1(a) e 1(b), são mostradas a estrutura física básica e o símbolo do diodo. Já na Figura 2 é mostrada a curva característica dele, onde foram discriminadas as três regiões de operação, sendo elas a correspondente aà polarização direta, polarização reversa e ruptura.

![](imagens/fig02.png) ![](imagens/fig03.png)

*Figura 1. (a) Estrutura básica, (b) símbolo do diodo.*

![](imagens/fig04.png)

*Figura 2. Curva característica do diodo.*

### 1.2. Princípio de Polarização

**Operação na regição direta:** Vd>VTO>0,7V, o potencial no terminal anodo é maior que no terminal catodo, o qual permite a circulação de corrente no sentido do anodo para o catodo.

**Operação na região reversa:** Vd<0V, o potencia no terminal catodo é maior que no terminal anodo,que permite a circulação de uma corrente reversa a ordem de uA, idealmente a corrente é consideradazero.

**Operação na região de ruptura:** a região é destrutiva para um diodo retificador. Somente o diodo ZENERopera nessa região dentro límites especificados em potência e tensão.

### 1.3. Perda de Condução

A perda de condução é obtida a partir a partir do modelo linear por partes [Boylestad]

![](imagens/fig05.png)

### 1.4. Perda de Comutação

En diodos se silício, a perda na entrada em condução é desprezível, somente há perda no bloqueio por causa da recuperação reversa da corrente no diodo. O valor do tempo de recuperação trr varia conforme o tipo de diodo.

![](imagens/fig06.png)

- Standard diodes (trr in microsecond range).
- Fast recovery diodes (trrin 200–500 ns).
- Ultra fast recovery diodes (trr ∼ 30–200 ns).
- Schottky diode (metal semiconductor junction –trr < 30 ns).

![](imagens/fig07.png)

## 2. TIRISTOR E TRIAC DE POTÊNCIA

*(seção ainda não desenvolvida no arquivo original)*
