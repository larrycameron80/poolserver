import struct
import binascii

import util
from transaction import Transaction


class CoinbaseTransaction(object):
    def __init__(self, block_template, generation_pubkey,
                 extranonce1, extranonce2):
        #BIP 0034
        coinbase_script = util.encode_height(block_template['height'])

        if 'coinbaseaux' in block_template:
            for i in block_template['coinbaseaux']:
                data = binascii.unhexlify(block_template['coinbaseaux'][i])
                coinbase_script += data
        if 'coinbaseflags' in block_template:
            data = binascii.unhexlify(block_template['coinbaseflags'])
            coinbase_script += data

        coinbase_script += extranonce1
        coinbase_script += extranonce2

        if 'coinbasevalue' in block_template:
            coinbase_value = block_template['coinbasevalue']
        else:
            tx = Transaction(block_template['coinbasetxn'])
            coinbase_value = tx.output[0]['value']

        output_script = '\x76\xa9\x14' + generation_pubkey + '\x88\xac'

        result = '\x01\x00\x00\x00'  # Version
        result += '\x01'  # In counter(1)
        result += '\x00' * 32  # Input(None)
        result += '\xff\xff\xff\xff'  # Input Index (None)
        result += util.encode_size(len(coinbase_script))
        result += coinbase_script
        result += '\xff\xff\xff\xff'  # Sequence
        result += '\x01'  # Out counter(1)
        result += struct.pack('<Q', coinbase_value)
        result += util.encode_size(len(output_script))
        result += output_script
        result += '\x00\x00\x00\x00'  # Lock time

        self.raw_tx = result

    def serialize(self):
        return {'data': binascii.hexlify(self.raw_tx)}
