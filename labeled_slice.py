import pickle
import time
import copy
import os
import json

def find_opcode(string):
    ps = string.find(" ")
    return string[0:ps] if ps != -1 else string[0: len(string)]

def find_oprand(string):
    oprand = string.split(" ")
    oprand[0:len(oprand)-1] = oprand[1:len(oprand)]
    oprand.pop(len(oprand)-1)
    oprand = list(filter(None, oprand))
    return oprand[0] if len(oprand)>0 else None

def get_item(stack_item: dict):
    if(stack_item.get("1") is None):
        return stack_item.get("0")
    else: 
        return stack_item.get("1")

def get_value(stack_value: dict):
    return stack_value.get("value")

total_json = 0

id_cnt = 0
in_stack = 0

edges = list()
features = dict()
deleted_nodes = list()
draw_vis = list()
not_draw_vis = list()

def deal(asm_list: list, top: int, Stack: list, now_address, graph, start_cnt, if_draw):
        global id_cnt
        global edges
        global features
        global deleted_nodes
        global in_stack

        now_cnt = 0

        for asm in asm_list:

            if(now_cnt < start_cnt):
                now_cnt = now_cnt + 1
                continue
            
     #       time.sleep(0.5)
            now_opcode = find_opcode(asm)
            now_oprand = find_oprand(asm)

            if(if_draw == False):
                draw(now_address, asm_list, Stack, top, graph, now_opcode, now_cnt)

       #    print(now_opcode)
        #    print(now_oprand)
            if(now_opcode == "STOP"):
                break
            if(now_opcode == "ADD" or now_opcode == "EXP" or now_opcode == "SIGNEXTEND" or now_opcode == "MUL" or now_opcode == "SUB" or now_opcode == "DIV" or now_opcode == "SDIV" or now_opcode == "MOD" or now_opcode == "SMOD"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)

                value0 = int(value0, 16)
                value1 = int(value1, 16)
            
                top = top - 2
                tmp_str = "arith_res|" + tag0 + "|" + tag1
                if(tmp0.get("1") is None and tmp1.get("1") is None):
                    if(now_opcode == "ADD"):
                        Stack.append({"0":tmp_str, "value":str(hex(1))})
                    if(now_opcode == "EXP"):
                        Stack.append({"0":tmp_str, "value":str(hex(int(1)))})
                    if(now_opcode == "SIGNEXTEND" or now_opcode == "MUL"):
                        Stack.append({"0":tmp_str, "value":str(hex(int(1)))})
                    if(now_opcode == "SUB"):
                        Stack.append({"0":tmp_str, "value":str(hex(1))})
                    if(now_opcode == "DIV" or now_opcode == "SDIV"):
                        Stack.append({"0":tmp_str, "value":str(hex(int(1)))})
                    if(now_opcode == "MOD" or now_opcode == "SMOD"):
                        Stack.append({"0":tmp_str, "value":str(hex(1))})
                else:
                    if(tmp0.get("0") is None):
                        in_stack -= 1
                        edges.append([tmp0.get("id"), id_cnt])
                    if(tmp1.get("0") is None):
                        in_stack -= 1
                        edges.append([tmp1.get("id"), id_cnt])
                    features[str(id_cnt)] = tmp_str
                    if(now_opcode == "ADD"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    if(now_opcode == "EXP"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    if(now_opcode == "SIGNEXTEND" or now_opcode == "MUL"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    if(now_opcode == "SUB"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    if(now_opcode == "DIV" or now_opcode == "SDIV"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    if(now_opcode == "MOD" or now_opcode == "SMOD"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    in_stack += 1
                    id_cnt = id_cnt + 1
                top = top + 1
        
            if(now_opcode == "ADDMOD" or now_opcode == "MULMOD"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tmp2 = Stack.pop(top-3)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                tag2 = get_item(tmp2)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)
                value2 = get_value(tmp2)

                value0 = int(value0, 16)
                value1 = int(value1, 16)
                value2 = int(value2, 16)
                top = top - 3
                tmp_str = "arith_res|" + tag0 + "|" + tag1 + "|" + tag2
                if(tmp0.get("1") is None and tmp1.get("1") is None and tmp2.get("1") is None):
                    if(now_opcode == "ADDMOD"):     
                        Stack.append({"0":tmp_str, "value":str(hex(1))})
                    else:
                        Stack.append({"0":tmp_str, "value":str(hex(1))})
                else:
                    if(tmp0.get("0") is None):
                        in_stack -= 1
                        edges.append([tmp0.get("id"), id_cnt])
                    if(tmp1.get("0") is None):
                        in_stack -= 1
                        edges.append([tmp1.get("id"), id_cnt])
                    if(tmp2.get("0") is None):
                        in_stack -= 1
                        edges.append([tmp2.get("id"), id_cnt])
                    features[str(id_cnt)] = tmp_str
                    if(now_opcode == "ADDMOD"):     
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    else:
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    in_stack += 1
                    id_cnt = id_cnt + 1
                top = top + 1

            if(now_opcode == "LT" or now_opcode == "GT" or now_opcode == "SLT" or now_opcode == "SGT" or now_opcode == "EQ"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)

                top = top - 2
                tmp_str = "cmp_res|" + tag0 + "|" + tag1
                if(tmp0.get("1") is None and tmp1.get("1") is None):
                    
                    if(now_opcode == "LT" or now_opcode == "SLT"):
                        Stack.append({"0":tmp_str, "value": "0x1"})
                    if(now_opcode == "GT" or now_opcode == "SGT"):
                        Stack.append({"0":tmp_str, "value": "0x1"})
                    if(now_opcode == "EQ"):
                        Stack.append({"0":tmp_str, "value": "0x1"})
                else:
                    if(tmp0.get("0") is None):
                        in_stack -= 1
                        edges.append([tmp0.get("id"), id_cnt])
                    if(tmp1.get("0") is None):
                        in_stack -= 1
                        edges.append([tmp1.get("id"), id_cnt])
                    features[str(id_cnt)] = tmp_str

                    if(now_opcode == "LT" or now_opcode == "SLT"):
                        Stack.append({"1":tmp_str, "value": "0x1", "id":id_cnt})
                    if(now_opcode == "GT" or now_opcode == "SGT"):
                        Stack.append({"1":tmp_str, "value": "0x1", "id":id_cnt})
                    if(now_opcode == "EQ"):
                        Stack.append({"1":tmp_str, "value": "0x1", "id":id_cnt})
                    in_stack += 1
                    id_cnt = id_cnt + 1
                top = top + 1
            
            if(now_opcode == "ISZERO"):
                tmp0 = Stack.pop(top-1)
                tag0 = get_item(tmp0)
                value0 = get_value(tmp0)

                top = top - 1
                tmp_str = "cmp_res|" + tag0
                if(tmp0.get("1") is None):
                    Stack.append({"0":tmp_str, "value": "0x1"})
                else:
                    edges.append([tmp0.get("id"), id_cnt])
                    features[str(id_cnt)] = tmp_str
                    Stack.append({"1":tmp_str, "value": "0x1", "id":id_cnt})
                    id_cnt = id_cnt + 1
                top = top + 1

            if(now_opcode == "AND" or now_opcode == "OR" or now_opcode == "XOR" or now_opcode == "BYTE" or now_opcode == "SHL" or now_opcode == "SHR" or now_opcode == "SAR" or now_opcode == "SHA3"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)

                value0 = int(value0, 16)
                value1 = int(value1, 16)

                top = top - 2
                tmp_str = "bit_res|" + tag0 + "|" + tag1
                if(tmp0.get("1") is None and tmp1.get("1") is None):
                    if(now_opcode == "AND"):
                        Stack.append({"0":tmp_str, "value":str(hex(1))})
                    if(now_opcode == "OR"):
                        Stack.append({"0":tmp_str, "value":str(hex(1))})
                    if(now_opcode == "XOR"):
                        Stack.append({"0":tmp_str, "value":str(hex(1))})
                    if(now_opcode == "BYTE"):
                        Stack.append({"0":tmp_str, "value":str(hex(1))})
                    if(now_opcode == "SHL"):
                        Stack.append({"0":tmp_str, "value":str(hex(1))})
                    if(now_opcode == "SHR" or now_opcode == "SAR"):
                        Stack.append({"0":tmp_str, "value":str(hex(1))})
                    if(now_opcode == "SHA3"):
                        Stack.append({"0":tmp_str, "value": str(hex(1))})
                else:
                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        in_stack -= 1
                    features[str(id_cnt)] = tmp_str

                    if(now_opcode == "AND"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    if(now_opcode == "OR"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    if(now_opcode == "XOR"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    if(now_opcode == "BYTE"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    if(now_opcode == "SHL"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    if(now_opcode == "SHR" or now_opcode == "SAR"):
                        Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    if(now_opcode == "SHA3"):
                        Stack.append({"1":tmp_str, "value": str(hex(1)), "id":id_cnt})
                    in_stack += 1
                    id_cnt = id_cnt + 1
                top = top + 1

            if(now_opcode == "NOT"):
                tmp0 = Stack.pop(top-1)
                tag0 = get_item(tmp0)
                value0 = get_value(tmp0)

                value0 = int(value0, 16)

                top = top - 1
                tmp_str = "bit_res|" + tag0
                if(tmp0.get("1") is None):
                    Stack.append({"0":tmp_str, "value": str(hex(1))})
                else:
                    edges.append([tmp0.get("id"), id_cnt])
                    features[str(id_cnt)] = tmp_str
                    Stack.append({"1":tmp_str, "value": str(hex(1)), "id":id_cnt})
                    id_cnt = id_cnt + 1
                top = top + 1
            
            if(now_opcode == "ADDRESS" or now_opcode == "CODESIZE"):
                tmp_str = "adr_data"
                Stack.append({"0":tmp_str, "value":"0x1"})
                top = top + 1

            if(now_opcode == "BALANCE"):
                tmp0 = Stack.pop(top-1)
                tag0 = get_item(tmp0)
                value0 = get_value(tmp0)

                top = top - 1
                tmp_str = "adr_data|" + tag0
                if(tmp0.get("1") is None):
                    Stack.append({"0":tmp_str, "value": "0x1"})
                else:
                    edges.append([tmp0.get("id"), id_cnt])
                    features[str(id_cnt)] = tmp_str
                    Stack.append({"1":tmp_str, "value": "0x1", "id":id_cnt})
                    id_cnt = id_cnt + 1
                
                top = top + 1

            if(now_opcode == "ORIGIN" or now_opcode == "CALLER"):
                tmp_str = "tx_data"
                Stack.append({"0":tmp_str, "value": "0x1"})
                top = top + 1	
            
            if(now_opcode == "CALLVALUE"):
                tmp_str = "tx_data"
                Stack.append({"0":tmp_str, "value": "0x1"})
                top = top + 1	
            
            if(now_opcode == "CALLDATALOAD"):
                tmp0 = Stack.pop(top-1)
                tag0 = get_item(tmp0)
                value0 = get_value(tmp0)

                top = top - 1
                tmp_str = "calldata|" + tag0
                if(tmp0.get("1") is None):
                    Stack.append({"0":tmp_str, "value":str(hex(1))})
                else:
                    edges.append([tmp0.get("id"), id_cnt])
                    features[str(id_cnt)] = tmp_str
                    Stack.append({"1":tmp_str, "value":str(hex(1)), "id":id_cnt})
                    id_cnt = id_cnt + 1
                top = top + 1

            if(now_opcode == "CALLDATASIZE" or now_opcode == "CODESIZE"):
                tmp_str = "calldata"
                Stack.append({"0":tmp_str, "value":str(hex(1))})
                top = top + 1
            
            if(now_opcode == "CALLDATACOPY" or now_opcode == "CODECOPY"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tmp2 = Stack.pop(top-3)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                tag2 = get_item(tmp2)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)
                value2 = get_value(tmp2)

                value0 = int(value0, 16)
                value1 = int(value1, 16)
                value2 = int(value2, 16)

                top = top - 3

                tmp_str = "calldata|" + tag0 + "|" + tag1 + "|" + tag2

                if(tmp0.get("0") is None or tmp1.get("0") is None or tmp2.get("0") is None):
                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp2.get("0") is None):
                        edges.append([tmp2.get("id"), id_cnt])
                        in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    id_cnt = id_cnt + 1

            if(now_opcode == "GASPRICE"):
                tmp_str = "tx_data"
                Stack.append({"0":tmp_str, "value": "0x1"})
                top = top + 1
            
            if(now_opcode == "EXTCODECOPY"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tmp2 = Stack.pop(top-3)
                tmp3 = Stack.pop(top-4)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                tag2 = get_item(tmp2)
                tag3 = get_item(tmp3)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)
                value2 = get_value(tmp2)
                value3 = get_value(tmp3)
                
                value0 = int(value0, 16)
                value1 = int(value1, 16)
                value2 = int(value2, 16)
                value3 = int(value3, 16)

                top = top - 4
                tmp_str = "adr_data|" + tag0 + "|" + tag1 + "|" + tag2 + "|" + tag3

                if(tmp0.get("0") is None or tmp1.get("0") is None or tmp2.get("0") is None or tmp3.get("0") is None):
                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp2.get("0") is None):
                        edges.append([tmp2.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp3.get("0") is None):
                        edges.append([tmp3.get("id"), id_cnt])
                        in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    id_cnt = id_cnt + 1
            
            if(now_opcode == "RETURNDATASIZE"):
                tmp_str = "ret_data"
                Stack.append({"0":tmp_str, "value":str(hex(1))})
                top = top + 1

            if(now_opcode == "RETURNDATACOPY"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tmp2 = Stack.pop(top-3)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                tag2 = get_item(tmp2)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)
                value2 = get_value(tmp2)

                top = top - 3
                tmp_str = "ret_data|" + tag0 + "|" + tag1 + "|" + tag2
                if(tmp0.get("0") is None or tmp1.get("0") is None or tmp2.get("0") is None):
                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp2.get("0") is None):
                        edges.append([tmp2.get("id"), id_cnt])
                        in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    id_cnt = id_cnt + 1

            if(now_opcode == "EXTCODEHASH"):
                tmp0 = Stack.pop(top-1)
                tag0 = get_item(tmp0)
                value0 = get_value(tmp0)

                top = top - 1
                tmp_str = "adr_data|" + tag0
                if(tmp0.get("1") is None):
                    Stack.append({"0":tmp_str, "value": str(hex(1))})
                else:
                    edges.append([tmp0.get("id"), id_cnt])
                    features[str(id_cnt)] = tmp_str
                    Stack.append({"1":tmp_str, "value": str(hex(1)), "id":id_cnt})
                    id_cnt = id_cnt + 1
                top = top + 1
            
            if(now_opcode == "BLOCKHASH" or now_opcode == "COINBASE" or now_opcode == "TIMESTAMP" or now_opcode == "NUMBER" or now_opcode == "DIFFICULTY" or now_opcode == "GASLIMIT" or now_opcode == "CHAINID" or now_opcode == "SELFBALANCE" or now_opcode == "BASEFEE"):
                tmp_str = "blk_data"
                Stack.append({"0":tmp_str, "value": "0x1"})
                top = top + 1
            
            if(now_opcode == "POP"):
                tmp0 = Stack.pop(top-1)
                tag0 = get_item(tmp0)
                top = top - 1

                tmp_str = "literal|" + tag0

                if(tmp0.get("0") is None):
                    edges.append([tmp0.get("id"), id_cnt])
                    in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    id_cnt = id_cnt + 1
                

            if(now_opcode == "MLOAD"):
                tmp0 = Stack.pop(top-1)
                tag0 = get_item(tmp0)
                value0 = get_value(tmp0)

                value0 = int(value0, 16)
                top = top - 1
                tmp_str = "mem_data|" + tag0
                if(tmp0.get("1") is None):
                    Stack.append({"0":tmp_str, "value": "0x1"})
                else:
                    edges.append([tmp0.get("id"), id_cnt])
                    features[str(id_cnt)] = tmp_str
                    Stack.append({"1":tmp_str, "value": "0x1", "id":id_cnt})
                    id_cnt = id_cnt + 1
                top = top + 1
            
            if(now_opcode == "MSTORE"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)


                top = top - 2

                tmp_str = "mem_data|" + tag0 + tag1
                if(tmp0.get("0") is None or tmp1.get("0") is None):
                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    id_cnt = id_cnt + 1
                

            if(now_opcode == "MSTORE8"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)

                value1 = int(value1, 16)

                top = top - 2

                tmp_str = "mem_data|" + tag0 + tag1
                if(tmp0.get("0") is None or tmp1.get("0") is None):
                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    id_cnt = id_cnt + 1
            
            if(now_opcode == "SLOAD"):
                tmp0 = Stack.pop(top-1)
                tag0 = get_item(tmp0)
                value0 = get_value(tmp0)

                value0 = int(value0, 16)

                top = top - 1
                tmp_str = "sto_data|" + tag0
                if(tmp0.get("1") is None):
                    Stack.append({"0":tmp_str, "value": "0x1"})
                else:
                    edges.append([tmp0.get("id"), id_cnt])
                    features[str(id_cnt)] = tmp_str
                    Stack.append({"1":tmp_str, "value": "0x1", "id":id_cnt})
                    id_cnt = id_cnt + 1
                top = top + 1

            if(now_opcode == "SSTORE"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)

                top = top - 2
                tmp_str = "sto_data|" + tag0 + tag1
                if(tmp0.get("0") is None or tmp1.get("0") is None ):
                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    id_cnt = id_cnt + 1

            if(now_opcode == "PC"):
                Stack.append({"0": "pc", "value": "0x1"})
                top = top + 1
            
            if(now_opcode == "JUMP"):
                tmp0 = Stack.pop(top-1)
                tag0 = get_item(tmp0)
                value0 = get_value(tmp0)

                top = top - 1

                tmp_str = "jump|" + tag0
                if(tmp0.get("0") is None):
                    edges.append([tmp0.get("id"), id_cnt])
                    in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    id_cnt = id_cnt + 1
            
            if(now_opcode == "JUMPI"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)

                top = top - 2

                tmp_str = "jump|" + tag0 + tag1
                if(tmp0.get("0") is None or tmp1.get("0") is None):
                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    id_cnt = id_cnt + 1

                
            
            if(len(now_opcode)>4):
                if(now_opcode[0:4] == "PUSH"):
                    Stack.append({"0": "literal", "value": now_oprand})
                    top = top + 1
                if(now_opcode == "CONST"):
                    Stack.append({"0": "literal", "value": "0x1"})
                    top = top + 1
            
            if(len(now_opcode)>3):
                if(now_opcode[0:3] == "DUP"):
                    dup_num = now_opcode[3:len(now_opcode)+1]
                    dup_num = int(dup_num)
                    tmp0 = Stack[top-dup_num]
                    tag0 = get_item(tmp0)
                    value0 = get_value(tmp0)

                    tmp_str = tag0
                    if(tmp0.get("1") is None):
                        Stack.append({"0":tmp_str, "value": str(hex(1))})
                    else:
                        edges.append([tmp0.get("id"), id_cnt])
                        features[str(id_cnt)] = tmp_str
                        Stack.append({"1":tmp_str, "value": str(hex(1)), "id":id_cnt})
                        deleted_nodes.append(str(id_cnt))
                        deleted_nodes.append(" ")
                        in_stack += 1
                        id_cnt = id_cnt + 1
                    top = top + 1
            if(len(now_opcode)>4):
                if(now_opcode[0:4] == "SWAP"):
                    swap_num = now_opcode[4:len(now_opcode)+1]
                    swap_num = int(swap_num)
                    tmp0 = copy.deepcopy(Stack[top-swap_num-1])
                    tmp1 = copy.deepcopy(Stack[top-1])
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        features[str(id_cnt)] = get_item(tmp1)
                        deleted_nodes.append(str(id_cnt))
                        deleted_nodes.append(" ")

                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        features[str(id_cnt)] = get_item(tmp0)
                        deleted_nodes.append(str(id_cnt))
                        deleted_nodes.append(" ")
                    
                    Stack[top-swap_num-1] = tmp1
                    Stack[top-1] = tmp0

            if(len(now_opcode)>3):
                if(now_opcode[0:3] == "LOG"):
                    flag = 0
                    tmp_str = str()
                    log_num = now_opcode[3:len(now_opcode)+1]
                    log_num = int(log_num) + 2
                    for pop_num in range(0, log_num):
                        tmp_store = Stack.pop(top-1)
                        tmp_str = tmp_str + get_item(tmp_store)
                        top = top - 1

                        if(tmp_store.get("0") is None):
                            flag = 1
                            edges.append([tmp_store.get("id"), id_cnt])
                            in_stack -= 1
                    if(flag == 1):
                        tmp_str = "log|" + tmp_str
                        features[str(id_cnt)] = tmp_str
                        id_cnt = id_cnt + 1
            
            if(now_opcode == "CALL" or now_opcode == "CALLCODE"):
                tmp_str = "cal_ret"
                flag = 0
                for tmp_num in range(0,7):
                    tmp_store = Stack.pop(top - 1)
                    tag = get_item(tmp_store)
                    tmp_str = tmp_str + "|" + tag
                    top = top - 1
                    if(tmp_store.get("0") is None):
                        edges.append([tmp_store.get("id"), id_cnt])
                        in_stack -= 1
                        flag = 1
                if(flag == 0):
                    Stack.append({"0": tmp_str, "value": "0x1"})
                else:
                    features[str(id_cnt)] = tmp_str
                    Stack.append({"1": tmp_str, "value": "0x1", "id":id_cnt})
                    id_cnt = id_cnt + 1
                    in_stack += 1
                top = top + 1
            
            if(now_opcode == "DELEGATECALL" or now_opcode == "STATICCALL"):
                tmp_str = "cal_ret"
                flag = 0
                for tmp_num in range(0,6):
                    tmp_store = Stack.pop(top - 1)
                    tag = get_item(tmp_store)
                    tmp_str = tmp_str + "|" + tag
                    top = top - 1
                    if(tmp_store.get("0") is None):
                        edges.append([tmp_store.get("id"), id_cnt]) 
                        in_stack -= 1
                        flag = 1
                if(flag == 0):
                    Stack.append({"0": tmp_str, "value": "0x1"})
                else:
                    features[str(id_cnt)] = tmp_str
                    Stack.append({"1": tmp_str, "value": "0x1", "id":id_cnt})
                    id_cnt = id_cnt + 1
                    in_stack += 1
                top = top + 1
            
            if(now_opcode == "CREATE"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tmp2 = Stack.pop(top-3)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                tag2 = get_item(tmp2)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)
                value2 = get_value(tmp2)
                
                top = top - 3
                tmp_str = "literal|" + tag0 + "|" + tag1 + "|" + tag2
                if(tmp0.get("1") is None and tmp1.get("1") is None and tmp2.get("1") is None):
                    Stack.append({"0":tmp_str, "value": "0x1"})
                else:
                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp2.get("0") is None):
                        edges.append([tmp2.get("id"), id_cnt])
                        in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    Stack.append({"1":tmp_str, "value": "0x1", "id":id_cnt})
                    id_cnt = id_cnt + 1
                    in_stack += 1
                top = top + 1
            
            if(now_opcode == "CREATE2"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tmp2 = Stack.pop(top-3)
                tmp3 = Stack.pop(top-4)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                tag2 = get_item(tmp2)
                tag3 = get_item(tmp3)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)
                value2 = get_value(tmp2)
                value3 = get_value(tmp3)
                
                top = top - 4
                tmp_str = "literal|" + tag0 + "|" + tag1 + "|" + tag2 + "|" + tag3
                if(tmp0.get("1") is None and tmp1.get("1") is None and tmp2.get("1") is None and tmp3.get("1") is None):
                    Stack.append({"0":tmp_str, "value": "0x1"})
                else:
                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp2.get("0") is None):
                        edges.append([tmp2.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp3.get("0") is None):
                        edges.append([tmp3.get("id"), id_cnt])
                        in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    Stack.append({"1":tmp_str, "value": "0x1", "id":id_cnt})
                    in_stack += 1
                    id_cnt = id_cnt + 1
                top = top + 1
            
            if(now_opcode == "RETURN" or now_opcode == "REVERT"):
                tmp0 = Stack.pop(top-1)
                tmp1 = Stack.pop(top-2)
                tag0 = get_item(tmp0)
                tag1 = get_item(tmp1)
                value0 = get_value(tmp0)
                value1 = get_value(tmp1)

                top = top - 2
                tmp_str = "stop|" + tag0 + tag1
                if(tmp0.get("0") is None or tmp1.get("0") is None):
                    if(tmp0.get("0") is None):
                        edges.append([tmp0.get("id"), id_cnt])
                        in_stack -= 1
                    if(tmp1.get("0") is None):
                        edges.append([tmp1.get("id"), id_cnt])
                        in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    id_cnt = id_cnt + 1
            
            if(now_opcode == "SELFDESTRUCT"):
                tmp0 = Stack.pop(top-1)
                tag0 = get_item(tmp0)
                value0 = get_value(tmp0)
                
                top = top - 1

                tmp_str = "stop|" + tag0

                if(tmp0.get("0") is None):
                    edges.append([tmp0.get("id"), id_cnt])
                    in_stack -= 1
                    features[str(id_cnt)] = tmp_str
                    id_cnt = id_cnt + 1
                

            now_cnt = now_cnt + 1
            if(in_stack <= 0 and if_draw == True):
                return Stack, top
       #     print(if_draw)
    #      print(in_stack)
       #     print(Stack)
       #     print(top)
        return Stack, top

def dfs(now_address, now_bb, now_stack, top, graph, sta_cnt, i_draw):
        
    # print("----")
    # print(now_address)
        
    global in_stack
    global not_draw_vis
    global draw_vis

    if(i_draw == False):
        if(now_bb in not_draw_vis):
            return
        else:
            not_draw_vis.append(now_bb)
        
    if(i_draw == True):
        if(now_bb in draw_vis):
            return
        else:
            draw_vis.append(now_bb)

    if(in_stack <= 0 and i_draw == True):
        return

    nex_stack, top = deal(now_bb, top, now_stack, now_address, graph, sta_cnt, i_draw)

    if(graph.out_edges()._adjdict[now_address] is None):
        return

    for nex_address in graph.out_edges()._adjdict[now_address]:
     #   print(nex_address)
        tmp_stack = copy.deepcopy(nex_stack)
        dfs(nex_address, graph.nodes().get(nex_address)['asm'], tmp_stack, top, graph, 0, i_draw)
    return

def draw(now_address, now_bb, now_stack, top, graph, opc, s_cnt):

    if(opc in target):
    #    print(now_address)
     #   print(opc)
        global id_cnt
        global edges
        global features
        global deleted_nodes
        global in_stack
        global total_json
        global draw_vis

        id_cnt = 0
        edges = list()
        features = dict()
        deleted_nodes = list()
        draw_vis = list()
        in_stack = 0
        tmp_stack = copy.deepcopy(now_stack)

        if(opc == "CALLDATALOAD"):
            tmp0 = tmp_stack.pop(top-1)
            tag0 = get_item(tmp0)

            top = top - 1
            tmp_str = "calldata|" + tag0
            tmp_stack.append({"1":tmp_str, "value":str(hex(1)), "id": 0})
            in_stack += 1
            top = top + 1
            
        if(opc == "BLOCKHASH" or opc == "TIMESTAMP" or opc == "COINBASE" or opc == "NUMBER" or opc == "DIFFICULTY" or opc == "GASLIMIT"):
            tmp_str = "blk_data"
            tmp_stack.append({"1":tmp_str, "value": "0x1", "id": 0})
            in_stack += 1
            top = top + 1

        if(opc == "SLOAD"):
            tmp0 = tmp_stack.pop(top-1)
            tag0 = get_item(tmp0)

            top = top - 1
            tmp_str = "sto_data|" + tag0
            tmp_stack.append({"1":tmp_str, "value": "0x1", "id": 0})
            in_stack += 1
            top = top + 1
            
        if(opc == "CALLER" or opc == "CALLVALUE" or opc == "CALLDATASIZE"):
            tmp_str = "tx_data"
            tmp_stack.append({"1":tmp_str, "value": "0x1", "id": 0})
            in_stack += 1
            top = top + 1	
            
        if(opc == "CALL"):
            tmp_str = "cal_ret"
            for tmp_num in range(0,7):
                tmp_store = tmp_stack.pop(top - 1)
                tag = get_item(tmp_store)
                tmp_str = tmp_str + "|" + tag
                top = top - 1
                
            tmp_stack.append({"1": tmp_str, "value": "0x1", "id": 0})
            in_stack += 1
            top = top + 1
            
        id_cnt = 1
     #   print("True")
     #   print(opc)
    #   print(in_stack)
     #   print(tmp_stack)
     #   print(top)

        dfs(now_address, now_bb, tmp_stack, top, graph, s_cnt + 1, True)

        if(len(features) - len(deleted_nodes) > 10):
            my_slice = dict()
            my_slice["edges"] = edges
            my_slice["features"] = features
            with open("./dataset/" + str(total_json) + ".json", "w") as f:
                my_slice = json.dumps(my_slice)
                f.write(my_slice)
                f.write("\n")
                f.write("".join(deleted_nodes))
                f.close()
            total_json += 1
        draw_vis = list()

pkl_path = "pkl_list"
pkl_list = os.listdir(pkl_path)

cnt = 0

for pkl_name in pkl_list:
    cnt = cnt + 1
    print(cnt)
   # print(pkl_name)
  #  time.sleep(5)

    not_draw_vis = list()
    with open(os.path.join(pkl_path, pkl_name), "rb") as f:
        contract = pickle.load(f)

    asm = contract['asmcode']
    target = ["CALLDATALOAD", "CALLER", "CALLVALUE","CALLDATASIZE", "BLOCKHASH", "TIMESTAMP", "COINBASE", "NUMBER", "DIFFICULTY", "GASLIMIT", "SLOAD", "CALL"]


