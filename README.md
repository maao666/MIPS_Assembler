# MIPS Assembler

## Get Started

![Screen Shot](https://github.com/maao666/MIPS_Assembler/raw/master/Screen%20Shot.png)

To turn `.asm` file into machine code, simply do:

`python3 main.py ./sample.asm`

Of course parsing a single line is also supported.

## APIs

- `translate_line`:
        Translate a single line of assembly code to binary

        Usage: `translate_line('BEQ $s3 $s1 #2')`
    
        `human_readable`: set True to add a space between slots to make it more readable

- `assemble`:
        Assemble a assembly file to binary

        Usage: `assemble('./sample.asm')`
    
        `human_readable`: set True to add a space between slots to make it more readable
        `with_src`: set False to generate pure machine code

## Customization

The JSON format database makes it easy to create your own instruction sets.

To add your own instruction, edit `_db/inst.json` following the format of other instructions.

**Your star is always appreciated!**
