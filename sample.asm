ADDI $zero, $s1,  4
ADDI $zero, $s2, 3
ADDI $zero, $s3, 1
ADDI $zero, $s4, 2

BEQ $s3, $s4, else
ADD $s1, $s2, $s0
jump end
else:
SUB $s1, $s2, $s0
end:

ADD $zero, $zero, $zero// not necessary
