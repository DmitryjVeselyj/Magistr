from .utils import *
from .constants import *


class AESEncryptionHelper:
    def __init__(self, key):
        self._key = key

    def execute(self, input_bytes):
        state = self._create_state_matrix(input_bytes, nb)

        key_schedule = self._key_expansion(self._key)

        state = self._add_round_key(state, key_schedule)
        rnd = 0
        for rnd in range(1, nr):
            state = self._sub_bytes(state)
            state = self._shift_rows(state)
            state = self._mix_columns(state)
            state = self._add_round_key(state, key_schedule, rnd)

        state = self._sub_bytes(state)
        state = self._shift_rows(state)
        state = self._add_round_key(state, key_schedule, rnd + 1)

        return self._form_output(state)

    @staticmethod
    def _create_state_matrix(input_bytes, nb):
        state = [[] for j in range(4)]
        for r in range(4):
            for c in range(nb):
                state[r].append(input_bytes[r + 4 * c])

        return state

    @staticmethod
    def _key_expansion(key):

        key_symbols = [ord(symbol) for symbol in key]

        if len(key_symbols) < 4 * nk:
            for i in range(4 * nk - len(key_symbols)):
                key_symbols.append(0x01)

        key_schedule = [[] for i in range(4)]
        for r in range(4):
            for c in range(nk):
                key_schedule[r].append(key_symbols[r + 4 * c])

        for col in range(nk, nb * (nr + 1)):
            if col % nk == 0:
                tmp = [key_schedule[row][col - 1] for row in range(1, 4)]
                tmp.append(key_schedule[0][col - 1])

                for j in range(len(tmp)):
                    sbox_row = tmp[j] // 0x10
                    sbox_col = tmp[j] % 0x10
                    sbox_elem = sbox[16 * sbox_row + sbox_col]
                    tmp[j] = sbox_elem

                for row in range(4):
                    s = (key_schedule[row][col - 4]) ^ (tmp[row]) ^ (rcon[row][int(col / nk - 1)])
                    key_schedule[row].append(s)

            else:
                for row in range(4):
                    s = key_schedule[row][col - 4] ^ key_schedule[row][col - 1]
                    key_schedule[row].append(s)

        return key_schedule

    @staticmethod
    def _add_round_key(state, key_schedule, rnd=0):

        for col in range(nk):
            s0 = state[0][col] ^ key_schedule[0][nb * rnd + col]
            s1 = state[1][col] ^ key_schedule[1][nb * rnd + col]
            s2 = state[2][col] ^ key_schedule[2][nb * rnd + col]
            s3 = state[3][col] ^ key_schedule[3][nb * rnd + col]

            state[0][col] = s0
            state[1][col] = s1
            state[2][col] = s2
            state[3][col] = s3

        return state

    @staticmethod
    def _sub_bytes(state):
        box = sbox

        for i in range(len(state)):
            for j in range(len(state[i])):
                row = state[i][j] // 0x10
                col = state[i][j] % 0x10

                box_elem = box[16 * row + col]
                state[i][j] = box_elem

        return state

    @staticmethod
    def _shift_rows(state):
        for i in range(1, nb):
            state[i] = left_shift(state[i], i)

        return state

    @staticmethod
    def _mix_columns(state):
        for i in range(nb):
            s0 = mul_by_02(state[0][i]) ^ mul_by_03(state[1][i]) ^ state[2][i] ^ state[3][i]
            s1 = state[0][i] ^ mul_by_02(state[1][i]) ^ mul_by_03(state[2][i]) ^ state[3][i]
            s2 = state[0][i] ^ state[1][i] ^ mul_by_02(state[2][i]) ^ mul_by_03(state[3][i])
            s3 = mul_by_03(state[0][i]) ^ state[1][i] ^ state[2][i] ^ mul_by_02(state[3][i])

            state[0][i] = s0
            state[1][i] = s1
            state[2][i] = s2
            state[3][i] = s3

        return state

    @staticmethod
    def _form_output(state):
        output = [None] * (4 * nb)
        for r in range(4):
            for c in range(nb):
                output[r + 4 * c] = state[r][c]
        return output
