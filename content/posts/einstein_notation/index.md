---
title: Einstein Notation
date: 2022-12-29
draft: false
summaryImage: "images/main.png"
keepImageRatio: true
---

# Introduction
This post is written with the intention of serving as an easy reminder of how Einstein notation works for me and perhaps others who might find it useful.
This is geared towards people (like myself) who want to ignore differential geometry and want to use it mainly as a simple way of expressing relatively simple computations (things like multiplying N matrices with N other matrices, perhaps summation over particular indices but not others, etc.).

First, a brief description of what Einstein notation is:
> "a notational convention that implies summation over a set of indexed terms in a formula, thus achieving brevity"  [[wikipedia]](#wiki)

Many operations like matrix multiplication, dot products, can all be thought up as "multiplying two terms from two objects and summing the multiplication up across some axes" and Einstein notation can be used to express it in a simple and compact way.

If you search up what this means you may get results like [wikipedia](#wiki) and [youtube videos](#youtube) that can be confusing as it tries to explain this in more general terms with respect to some concepts in differential geometry which may not apply to your use case. Most notably, they have superscripts and subscripts to distinguish between "tangent" and "cotangent" spaces. For our purposes, we can just imagine everything is a subscript that tell us which element to look at in a multidimensional array. To add complexity to the matter, many [blogposts](#blog1) you find will try to explain this with respect to the numpy function [einsum](#numpy) which is Numpy's implementation of taking an Einstein notation formula and executing it. However, there are some differences between numpy's implementation and how it is defined elsewhere (notably, *explicit* mode -- as noted in the numpy documentation -- has slightly different rules). For example, one main rule you will see for "classical" Einstein notation is that "an index can not repeat more than twice" -- this rule is not true for numpy explicit mode. 

This post will focus on defining a simple set of rules for which *numpy explicit mode* obeys. The reason for this is because I personally think it is easier to reason about and tools exist to parse this notation such as numpy einsum and tensorflow/pytorch einsum.

# Einstein Notation (numpy explicit mode) basics
The rules for *numpy explicit mode* evaluation of einstein notation is not documented well (in my opinion) from the [numpy website](#numpy). This section will try to detail my understanding of it (obtained through experimentation and consolidation of other explanations). If any part of this is wrong, please reach out to me so that I can correct my understanding.

At its core, einstein notation (numpy explicit mode) can describe operations of the following form:
$$ A_{\color{red} \text{free indices}} = \sum_{\color{blue} \text{summation indices}} B_{\color{green}\text{b indices}} * C_{\color{violet} \text{c indices}} * ... $$
We will call this equation the "Core Notation Equation" as we will be thinking of how to express operations in this form.

For example, matrix multiplication is:
$$ A_{\color{red}ik} = \sum_{\color{blue}j} B_{\color{green}ij} * C_{\color{violet}jk}$$

We define an output, \\( A \\), by noting how each element of it (\\( i, k \\)  for matrix multiplication case) is computed with respect to entries in \\( B, C, ...\\).
We will call \\( j \\) a "summation" index as it is summed across and \\( (i, k) \\)  as "free" indices to denote they are the indices that define what the output is and is "free" to vary over the output.
Note: this definition of "summation" and "free" indices is very close to the wikipedia definition, but we are using it to define numpy explicit mode rules. 
The notation for numpy einstein notation will be:

$$ {\color{green}\text{\<b indices\>}}\text{,} {\color{violet}\text{\<c indices\>}} \rightarrow {\color{red}\text{\<free indices\>}}$$

For example, matrix multiplication will be expressed as

$$ {\color{green}\text{ij}}\text{,} {\color{violet}\text{jk}} \rightarrow {\color{red}\text{ik}}$$

Note that the specific letters chosen to represent an index \\(i, j, k\\) are arbitrary but must be consistent in the expression, so an exactly equal expression for matrix multiplication can be


$$ {\color{green}\text{bc}}\text{,} {\color{violet}\text{ca}} \rightarrow {\color{red}\text{ba}}$$

Note: Numpy explicit mode happens when an arrow "->" is in the expression. If it is not, these rules do not apply. I would recommend always using numpy explicit mode.

Here are some basic rules to remember this notation:
- Free indices are explicitly defined after the arrow (->).
- Summation indices are defined implicitly by all indices that are not a free.
- Any time a summation index appears multiple times, the notation will multiply the values together and sum across those axes.
    - Thus, any axes addressed by the same index, say i, must have the same length.


# Einstein Notation Extra Information
This section contains some additional information that may be helpful. Again, this applies to numpy explicit mode evaluation.

If every index is free (every index to the left of "->" is also to the right of "->") then there is no summation indices to sum over.
This allows an expression like "ij->ji" to express transposition. In the "Core Notation Equation" we will get something like
$$ A_{ji} = B_{ij}$$ 
where the sum drops away because there are no summation indices.

Similarily, we can extract the diagonal of a matrix into a vector with an expression like "ii->i". The "Core Notation Equation" to think of is
$$ A_{i} = B_{ii} $$
where, again, the sum drops away because there are no summation indices.


If every index is summed over, then there will be no indices to the right of the "->". This indicates we are summing over all indices.
For example, an expression like "ij->" will simply sum up all the elements in the matrix. The "Core Notation Equation" here is
$$ A = \sum_{ij} B_ij  $$


One extra feature of numpy einstein notation is to indicate broadcasting via ellipsis. A "..." indicates all the remaining indices positionally.
For example, for an N dimensional array
- "i...": the "..." refers to the last (N-1) dimensions
- "ij...": the "..." refers to the last (N-2) dimensions
- "...i": the "..." refers to the first (N-1) dimensions
- "i...j": the "..." refers to the middle (N-2) dimensions

This is very useful when dealing with operations where the core operation is only happening in a few dimensions and every other dimension is more for "structure."
A common example is say to multiply a batch of data by a single matrix (useful for lots of neural networks) of size (N_in, N_out).

The expression "...ij,jk->...ik" will work for all of the following shapes for the data:
- (A, N_in) : which is just singular piece of data
- (B, A, N_in) : a batch of B data each of shape (A, N_in)
- (B_1, B_2, A, N_in): a batch of (B_1*B_2) data each of shape (A, N_in) where the batch is spread over a 2d grid.


# Examples

#### Matrix-Matrix Multiplication
Math expression: \\( A_{ik} = \sum_{j} B_{ij} * C_{jk} \\)

Einstein notation (numpy explicit mode): "ij,jk->ik"


#### Matrix Hadamard Multiplication
Math expression: \\( A_{ij} =  B_{ij} * C_{ij} \\)

Einstein notation (numpy explicit mode): "ij,ij->ij"


#### Matrix-Vector Multiplication
Math expression: \\( A_{ik} = \sum_{j} B_{ij} * C_{j} \\)

Einstein notation (numpy explicit mode): "ij,j->i"

#### Vector Dot Product
Math expression: \\( A = \sum_{i} B_{i} * C_{i} \\)

Einstein notation (numpy explicit mode): "i,i->"

#### Sum all elements in Matrix
Math expression: \\( A = \sum_{ij} B_{ij} \\)

Einstein notation (numpy explicit mode): "ij->"

#### Obtain the diagonal vector from a matrix
Math expression: \\( A_i =  B_{ii} \\)

Einstein notation (numpy explicit mode): "ii->i"

#### Matrix Trace
Math expression: \\( A =  \sum_{i} B_{ii} \\)

Einstein notation (numpy explicit mode): "ii->"

#### Matrix Transpose
Math expression: \\( A_{ji} = B_{ij} \\)

Einstein notation (numpy explicit mode): "ij->ji"

#### Batch Matrix Multiplication
I have a stack (size B) of matrices (each of size (N, M)) represented by a multidimensional array (B, N, M).
I have a second stack (size B) of matrices (each of size (M, K)) represented by a multidimensional array (B, M, K).
I want to compute an output stack (B, N, K) where the i'th matrix of shape (N, K) is computed from multiplying the i'th matrix in the first stack by the i'th matrix in the second stack.

Math expression: \\( A_{bnk} = \sum_{m} B_{bnm} * C_{bmk} \\)

Einstein notation (numpy explicit mode): "bnm,bmk->bnk"

# References

<a name="youtube" href="https://www.youtube.com/watch?v=CLrTj7D2fLM&ab_channel=FacultyofKhan" target="_blank">[Youtube Video] Einstein Summation Convention: an Introduction. Faculty of Khan.</a>

<a name="wiki" href="https://en.wikipedia.org/wiki/Einstein_notation" target="_blank">[Wikipedia] Einstein Notation.</a>

<a name="numpy" href="https://numpy.org/doc/stable/reference/generated/numpy.einsum.html" target="_blank">[Numpy] einsum documentation.</a>

<a name="blog1" href="https://rockt.github.io/2018/04/30/einsum" target="_blank">[Blog Post] EINSUM IS ALL YOU NEED - EINSTEIN SUMMATION IN DEEP LEARNING. TIM ROCKTÄSCHEL</a>






<script type="text/javascript">
    // set the pyodide files URL (packages.json, pyodide.asm.data etc)
    window.languagePluginUrl = 'https://cdn.jsdelivr.net/pyodide/v0.16.1/full/';
</script>
<script src="https://code.jquery.com/jquery-3.5.1.min.js"
integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" 
crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/ace.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/mode-python.min.js" integrity="sha512-2Ke4vMGrMfYRM55pT1aA5bw7Pl82Sc7K5Hg8XZYZu+EQrb0AO1mNYTagwZm+MFVAImYS9Mlnm73zcgc01wPXxA==" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.12/theme-monokai.min.js" integrity="sha512-S4i/WUGRs22+8rjUVu4kBjfNuBNp8GVsgcK2lbaFdws4q6TF3Nd00LxqnHhuxS9iVDfNcUh0h6OxFUMP5DBD+g==" crossorigin="anonymous"></script>


<script src="https://cdn.jsdelivr.net/pyodide/v0.16.1/full/pyodide.js"></script>

<script src="resources/script.js"></script>
<link rel="stylesheet" href="resources/style.css">


<!-- Math Jax -->
<script>
  MathJax = {
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      processEscapes: true,
    },
    svg: {
      fontCache: 'global'
    },
    loader: {load: ['[tex]/color', '[tex]/configMacros']},
    tex: {
      packages: {'[+]': ['color', 'configMacros']},
    },
    startup:{
       ready: () => {
         MathJax.startup.defaultReady();
         MathJax.startup.promise.then(() => {
           resize_mathjax();
         });
       }
    }
  };
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js">
</script>
