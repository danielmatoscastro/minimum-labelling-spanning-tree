
# Set of nodes
set V;

# Set of edges
set E dimen 2;

# Set of labels
set L;

# Set of edges with l as label
set EL {L} dimen 2;

param sizeV;

param sizeEL {L};

# 1 if l is in solution. 0 otherwise.
var y {L} binary;

# 1 if (i, j) is in solution. 0 otherwise.
var x {E} binary;

# flow variables
var f {E} >= 0;

minimize label_amount: sum {l in L} y[l];

s.t. r1 {j in V diff {0}}: 
    sum {i in V : (i,j) in E} x[i,j] = 1;

s.t. r2 {j in V diff {0}}: 
    (sum {i in V : (i,j) in E} f[i,j]) - (sum {i in V : (j,i) in E} f[j,i]) = 1;

s.t. r3_1 {(i, j) in E}: 
    x[i,j] <=  f[i,j];

s.t. r3_2 {(i, j) in E}: 
    f[i,j] <= (sizeV * x[i,j]);

s.t. r4 {l in L}: 
    sum {(i, j) in EL[l]} x[i,j] <= (min(sizeV-1, sizeEL[l]) * y[l]);

end;
