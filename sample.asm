ADDI $zero, $s1,  4
ADDI $zero, $s2, 3
ADDI $zero, $s3, 2
ADDI $zero, $s4, 1

ADD $s1, $s2, $t0 //$t0 = $s1 + $s2
ADD $s3, $s4, $t1 //$t1 = $s3 + $s4
SUB $t0, $t1, $s0 //$s0 = $t0 - $t1

BEQ $s3, $s4, else
ADD $s1, $s2, $s0
jump end
else:
SUB $s1, $s2, $s0
end:

ADD $zero, $zero, $zero// not necessary
