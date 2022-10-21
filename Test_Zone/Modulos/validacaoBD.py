import dateutil.parser

# Dicionários
repeticao_RFID = {}
repeticao_SN = {}



def rec_validation(item, repeticao):
    # Imports
    from datetime import datetime
    from Modulos.class_erros import Error, SaveError
    from dateutil.parser import parse

    global error_chave

    print('Início da validação - Recebimento')

    error = Error()

    error_chave = 0
    error_PO = 0
    error_PN = 0
    error_RFID = 0
    error_SN = 0
    error_Date = 0
    error_ChaveRel = 0

    ### VALIDAÇÃO DA CHAVE DE NOTA FISCAL

    cell_range = item['ChaveNF_Entrada']
    if bool(cell_range) is False:
        error.empty()
        error_chave += 1
    try:
        cell_range = int(cell_range)
    except:
        error.chave()
        error_chave += 1
    finally:
        pass
    if len(cell_range) != 44:
        error.chave()
        error_chave += 1

    ### VALIDAÇÃO DO PEDIDO DE COMPRA (PO)

    cell_range = item['PedidoCompra']
    if bool(cell_range) is False:
        error_PO += 1
        error.empty()
    try:
        int_test = int(cell_range[1:])
    except:
        error.po()
        error_PO += 1
    finally:
        pass
    if 'K' in cell_range or 'k' in cell_range:
        if len(cell_range[1:]) > 5 or len(cell_range[1:]) < 5:
            error_PO += 1
            error.po()
    elif len(str(cell_range)) > 5 or len(str(cell_range)) < 5:
        error_PO += 1
        error.po()
    else:
        pass

    ### VALIDAÇÃO DO PART-NUMBER

    cell_range = item['PartNumber']
    if bool(cell_range) is False or cell_range is None:
        error.empty()
        error_PN += 1
    elif "!" in cell_range or \
            "@" in cell_range or \
            "$" in cell_range or \
            "%" in cell_range or \
            "&" in cell_range or \
            "*" in cell_range or \
            ")" in cell_range or \
            "'" in cell_range or \
            ":" in cell_range or \
            ";" in cell_range:
        error.part_number()
        error_PN += 1
    else:
        pass

    ### VALIDAÇÃO RFID DO PRODUTO

    cell_range = item['RFID_Produto']
    if bool(cell_range) is False:
        error.empty()
        error_RFID += 1
    elif len(cell_range) != 24:
        error.rfid()
        error_RFID += 1
    elif "E" != cell_range[0]:
        error.rfid()
        error_RFID += 1
    if repeticao.count(cell_range) > 1:
        error.rfid_repetido()
        error_RFID += 1
    else:
        pass

    ### VALIDAÇÃO DO SERIAL NUMBER

    cell_range = item['SerialNumber']
    if bool(cell_range) is False:
        error.empty()
        error_SN += 1
    if "!" in str(cell_range) or \
            "@" in str(cell_range) or \
            "$" in str(cell_range) or \
            "%" in str(cell_range) or \
            "&" in str(cell_range) or \
            "*" in str(cell_range) or \
            "(" in str(cell_range) or \
            ")" in str(cell_range) or \
            "'" in str(cell_range) or \
            ":" in str(cell_range) or \
            "/" in str(cell_range):
        error.serial_number()
        error_SN += 1
    if repeticao.count(cell_range) > 1:
        error.rfid_repetido()
        error_RFID += 1
    else:
        pass

    ### VALIDAÇÃO LOCAL

    ### VALIDAÇÃO DA DATA

    cell_range = item['DataEvidencia']

    try:
        parse(cell_range)
        data = parse(cell_range)
        if data.day <= 12:
            data = datetime.strptime(datetime.strftime(parse(cell_range), "%m/%d/%Y"), "%d/%m/%Y")
        if data > datetime.today():
            error.data_maior()
            error_Date += 1
        else:
            pass
    except Exception as erros:
        print(erros)
        error.data()
        error_Date += 1
    finally:
        pass

    ### CHAVE DE RELACIONAMENTO

    # Select na tabela Recebimento com base na data

    repeticao_RFID.clear()
    repeticao_SN.clear()

    if error_chave > 0 or error_PO > 0 or error_PN > 0 \
            or error_RFID > 0 or error_SN > 0 or error_Date > 0 or error_ChaveRel:
        return 'Erro nos dados'
    else:
        return 'Sucesso'