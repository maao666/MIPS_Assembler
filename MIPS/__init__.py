import json
import logging


class mips:
    addr_offset = 1
    label_addr = {}

    def __init__(self, base_address=0, reg_json="./_db/registers.json", format_json="./_db/inst_format.json", inst_json="./_db/inst.json"):
        with open(reg_json)as fp:
            self.reg = json.load(fp)
        with open(format_json)as fp:
            self.format = json.load(fp)
        with open(inst_json)as fp:
            self.inst = json.load(fp)
        self.base_address = base_address

    def _preprocess(self, text: str) -> list:
        text = text.splitlines()
        addr = self.base_address
        new = []
        for i in text:
            i = self._decommentize(i)
            if i.strip() == '':
                continue
            else:
                if i.find(':') >= 1:
                    # save the label
                    self.label_addr[i[:i.find(':')].strip(
                    ).upper()] = addr - 1  # fixed
                else:
                    new.append(i)
                    addr = addr + 1
        return new

    def _convert_reg(self, nickname: str) -> int:
        nickname = nickname.strip()
        if nickname.startswith(self.reg.get("prefix")):
            reg_num = self.reg.get("reg_name", {}).get(
                nickname[1:].lower(), -1)
            if reg_num == -1:
                logging.error("Invalid register name: {0}".format(nickname))
            return reg_num
        logging.error('Invalid register prefix: {0}'.format(nickname[0]))
        return -1

    def _convert_to_bin(self, src, digits: int) -> str:
        if isinstance(src, str):
            try:
                src = int(src)
            except Exception:
                logging.error('Cannot convert src to integer')
        if isinstance(src, int):
            if src < 0:
                # 2's comp
                return bin(src % (1 << digits))
            return bin(src)[2:].zfill(digits)
        logging.error('Unsupported src type')
        return ''

    def _decommentize(self, line: str, comment='''//''') -> str:
        pos = line.find(comment)
        if pos != -1:
            line = line[:pos]
        return line.strip()

    def _special_inst_handeler(self, l: list) -> list:
        if l[0].upper() == 'LW' or l[0].upper() == 'SW':
            base_reg = l[2][l[2].find('(')+1:l[2].find(')')]
            dest_reg = l[1]
            offset = l[2][:l[2].find('(')]
            return [l[0].upper(), base_reg, dest_reg, offset]
        return l

    def _replace_slot(self, src, addr, relative_addr: bool) -> int:
        # keep in mind that returning negative num is allowed here
        if isinstance(src, int) or (isinstance(src, str) and src.isdigit()):
            # no action required
            return int(src)
        if isinstance(src, str):
            if src.startswith(self.reg.get("prefix")):
                # Special case for register like $s0
                src = self._convert_reg(src)
            elif src.startswith('#'):
                # Special case for address like #2
                src = src[1:]
            elif src.startswith('0x'):
                # Special case for hexadecimal
                src = int(src, 0)
            else:
                # Replace a label
                prev = self.label_addr.get(src.strip().upper(), -1)
                if prev == -1:
                    logging.error('Undefined label: {}'.format(src))
                if relative_addr:
                    src = (prev - addr) * self.addr_offset
                else:
                    src = prev * self.addr_offset

                print(self.label_addr, src)
        else:
            logging.error("What the fuck is this type {}?".format(type(src)))
        return int(src)

    def _parse(self, line: str, addr: int, sep=' ', end='\n') -> str:
        line = self._decommentize(line)
        l = [i for i in line.replace(',', ' ').split(' ') if i]

        if len(l) < 2:
            logging.error("Invalid Instruction {}".format(line))
            return ''
        inst_dict = self.inst.get('inst', {}).get(l[0].upper())
        if inst_dict == None:
            logging.error("Unknown instruction {}".format(l[0].upper()))
            return end
        l = self._special_inst_handeler(l)
        binary = []
        inst_format = self.format.get('types', {}).get(inst_dict.get('format'))
        if inst_format == None:
            logging.error("Unknown instruction type {}".format(
                inst_dict.get('format')))
            return end
        index = 1
        for slot in inst_format:
            placeholder = list(slot.keys())[0]
            bit = list(slot.values())[0]
            if placeholder == 'op':
                binary.append(self._convert_to_bin(inst_dict.get(
                    'op', {}).get('dec'), bit))
                continue
            else:
                if inst_dict.get(placeholder, {}).get('enabled', False):
                    if index < len(l):
                        l[index] = self._replace_slot(
                            l[index], addr, inst_dict.get("relative_addr", False))
                    value = inst_dict.get(placeholder, {}).get('value', '-1')
                    if value == None:  # value from l
                        ph = self._convert_to_bin(l[index], bit)
                        index = index + 1
                    elif value == '-1' or value == -1:  # no value. say a reg
                        ph = self._convert_to_bin(l[index], bit)
                        index = index + 1
                    else:  # result should be value
                        ph = self._convert_to_bin(value, bit)
                    binary.append(ph)
        return sep.join(binary) + end

    def translate_line(self, assembly_code: str, human_readable=False) -> str:
        '''
        Translate a single line of assembly code to binary
        --------------------------------------------------
        Usage: `translate_line('BEQ $s3 $s1 #2')`

        `human_readable`: set True to add a space between slots to make it more readable

        '''
        return self._parse(assembly_code, addr=-1, sep=' ' if human_readable else '', end='')

    def assemble(self, filename: str, human_readable=False, with_src=True) -> str:
        '''
        Assemble a assembly file to binary
        --------------------------------------------------
        Usage: `assemble('./sample.asm')`

        `human_readable`: set True to add a space between slots to make it more readable
        `with_src`: set False to generate pure machine code

        '''
        bin_code = []
        with open(filename, 'r') as f:
            text = f.read()
        lines = self._preprocess(text)
        addr = self.base_address
        for i in lines:
            src = '    |    ' + i.strip() if with_src else ''
            bin_code.append(self._parse(i, addr=addr, end='',
                                        sep=' ' if human_readable else '') + src)
            addr += 1
        return '\n'.join(bin_code)
