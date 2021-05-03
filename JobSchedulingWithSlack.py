import random
import copy
import itertools


class Task:
    counter = 0

    def __init__(self, start, end, duration, slack) -> None:
        self.id = Task.counter
        Task.counter += 1

        self.start = start
        self.end = end
        self.duration = duration
        self.slack = slack


class Workspace:
    ALL_SORTING = [
        ('x.start', 'x.duration', 'x.end', 'x.slack'),  # 0
        ('x.start', 'x.duration', 'x.slack', 'x.end'),  # 1
        ('x.start', 'x.end', 'x.duration', 'x.slack'),  # 2
        ('x.start', 'x.end', 'x.slack', 'x.duration'),  # 3
        ('x.start', 'x.slack', 'x.duration', 'x.end'),  # 4
        ('x.start', 'x.slack', 'x.end', 'x.duration'),  # 5
        ('x.duration', 'x.start', 'x.end', 'x.slack'),  # 6
        ('x.duration', 'x.start', 'x.slack', 'x.end'),  # 7
        ('x.duration', 'x.end', 'x.start', 'x.slack'),  # 8
        ('x.duration', 'x.end', 'x.slack', 'x.start'),  # 9
        ('x.duration', 'x.slack', 'x.start', 'x.end'),  # 10
        ('x.duration', 'x.slack', 'x.end', 'x.start'),  # 11
        ('x.end', 'x.start', 'x.duration', 'x.slack'),  # 12
        ('x.end', 'x.start', 'x.slack', 'x.duration'),  # 13
        ('x.end', 'x.duration', 'x.start', 'x.slack'),  # 14
        ('x.end', 'x.duration', 'x.slack', 'x.start'),  # 15
        ('x.end', 'x.slack', 'x.start', 'x.duration'),  # 16
        ('x.end', 'x.slack', 'x.duration', 'x.start'),  # 17
        ('x.slack', 'x.start', 'x.duration', 'x.end'),  # 18
        ('x.slack', 'x.start', 'x.end', 'x.duration'),  # 19
        ('x.slack', 'x.duration', 'x.start', 'x.end'),  # 20
        ('x.slack', 'x.duration', 'x.end', 'x.start'),  # 21
        ('x.slack', 'x.end', 'x.start', 'x.duration'),  # 22
        ('x.slack', 'x.end', 'x.duration', 'x.start'),  # 23
        ('x.start', 'x.duration', 'x.end', '-x.slack'),  # 24
        ('x.start', 'x.duration', '-x.slack', 'x.end'),  # 25
        ('x.start', 'x.end', 'x.duration', '-x.slack'),  # 26
        ('x.start', 'x.end', '-x.slack', 'x.duration'),  # 27
        ('x.start', '-x.slack', 'x.duration', 'x.end'),  # 28
        ('x.start', '-x.slack', 'x.end', 'x.duration'),  # 29
        ('x.duration', 'x.start', 'x.end', '-x.slack'),  # 30
        ('x.duration', 'x.start', '-x.slack', 'x.end'),  # 31
        ('x.duration', 'x.end', 'x.start', '-x.slack'),  # 32
        ('x.duration', 'x.end', '-x.slack', 'x.start'),  # 33
        ('x.duration', '-x.slack', 'x.start', 'x.end'),  # 34
        ('x.duration', '-x.slack', 'x.end', 'x.start'),  # 35
        ('x.end', 'x.start', 'x.duration', '-x.slack'),  # 36
        ('x.end', 'x.start', '-x.slack', 'x.duration'),  # 37
        ('x.end', 'x.duration', 'x.start', '-x.slack'),  # 38
        ('x.end', 'x.duration', '-x.slack', 'x.start'),  # 39
        ('x.end', '-x.slack', 'x.start', 'x.duration'),  # 40
        ('x.end', '-x.slack', 'x.duration', 'x.start'),  # 41
        ('-x.slack', 'x.start', 'x.duration', 'x.end'),  # 42
        ('-x.slack', 'x.start', 'x.end', 'x.duration'),  # 43
        ('-x.slack', 'x.duration', 'x.start', 'x.end'),  # 44
        ('-x.slack', 'x.duration', 'x.end', 'x.start'),  # 45
        ('-x.slack', 'x.end', 'x.start', 'x.duration'),  # 46
        ('-x.slack', 'x.end', 'x.duration', 'x.start'),  # 47
        ('x.start', 'x.duration', '-x.end', 'x.slack'),  # 48
        ('x.start', 'x.duration', 'x.slack', '-x.end'),  # 49
        ('x.start', '-x.end', 'x.duration', 'x.slack'),  # 50
        ('x.start', '-x.end', 'x.slack', 'x.duration'),  # 51
        ('x.start', 'x.slack', 'x.duration', '-x.end'),  # 52
        ('x.start', 'x.slack', '-x.end', 'x.duration'),  # 53
        ('x.duration', 'x.start', '-x.end', 'x.slack'),  # 54
        ('x.duration', 'x.start', 'x.slack', '-x.end'),  # 55
        ('x.duration', '-x.end', 'x.start', 'x.slack'),  # 56
        ('x.duration', '-x.end', 'x.slack', 'x.start'),  # 57
        ('x.duration', 'x.slack', 'x.start', '-x.end'),  # 58
        ('x.duration', 'x.slack', '-x.end', 'x.start'),  # 59
        ('-x.end', 'x.start', 'x.duration', 'x.slack'),  # 60
        ('-x.end', 'x.start', 'x.slack', 'x.duration'),  # 61
        ('-x.end', 'x.duration', 'x.start', 'x.slack'),  # 62
        ('-x.end', 'x.duration', 'x.slack', 'x.start'),  # 63
        ('-x.end', 'x.slack', 'x.start', 'x.duration'),  # 64
        ('-x.end', 'x.slack', 'x.duration', 'x.start'),  # 65
        ('x.slack', 'x.start', 'x.duration', '-x.end'),  # 66
        ('x.slack', 'x.start', '-x.end', 'x.duration'),  # 67
        ('x.slack', 'x.duration', 'x.start', '-x.end'),  # 68
        ('x.slack', 'x.duration', '-x.end', 'x.start'),  # 69
        ('x.slack', '-x.end', 'x.start', 'x.duration'),  # 70
        ('x.slack', '-x.end', 'x.duration', 'x.start'),  # 71
        ('x.start', 'x.duration', '-x.end', '-x.slack'),  # 72
        ('x.start', 'x.duration', '-x.slack', '-x.end'),  # 73
        ('x.start', '-x.end', 'x.duration', '-x.slack'),  # 74
        ('x.start', '-x.end', '-x.slack', 'x.duration'),  # 75
        ('x.start', '-x.slack', 'x.duration', '-x.end'),  # 76
        ('x.start', '-x.slack', '-x.end', 'x.duration'),  # 77
        ('x.duration', 'x.start', '-x.end', '-x.slack'),  # 78
        ('x.duration', 'x.start', '-x.slack', '-x.end'),  # 79
        ('x.duration', '-x.end', 'x.start', '-x.slack'),  # 80
        ('x.duration', '-x.end', '-x.slack', 'x.start'),  # 81
        ('x.duration', '-x.slack', 'x.start', '-x.end'),  # 82
        ('x.duration', '-x.slack', '-x.end', 'x.start'),  # 83
        ('-x.end', 'x.start', 'x.duration', '-x.slack'),  # 84
        ('-x.end', 'x.start', '-x.slack', 'x.duration'),  # 85
        ('-x.end', 'x.duration', 'x.start', '-x.slack'),  # 86
        ('-x.end', 'x.duration', '-x.slack', 'x.start'),  # 87
        ('-x.end', '-x.slack', 'x.start', 'x.duration'),  # 88
        ('-x.end', '-x.slack', 'x.duration', 'x.start'),  # 89
        ('-x.slack', 'x.start', 'x.duration', '-x.end'),  # 90
        ('-x.slack', 'x.start', '-x.end', 'x.duration'),  # 91
        ('-x.slack', 'x.duration', 'x.start', '-x.end'),  # 92
        ('-x.slack', 'x.duration', '-x.end', 'x.start'),  # 93
        ('-x.slack', '-x.end', 'x.start', 'x.duration'),  # 94
        ('-x.slack', '-x.end', 'x.duration', 'x.start'),  # 95
        ('x.start', '-x.duration', 'x.end', 'x.slack'),  # 96
        ('x.start', '-x.duration', 'x.slack', 'x.end'),  # 97
        ('x.start', 'x.end', '-x.duration', 'x.slack'),  # 98
        ('x.start', 'x.end', 'x.slack', '-x.duration'),  # 99
        ('x.start', 'x.slack', '-x.duration', 'x.end'),  # 100
        ('x.start', 'x.slack', 'x.end', '-x.duration'),  # 101
        ('-x.duration', 'x.start', 'x.end', 'x.slack'),  # 102
        ('-x.duration', 'x.start', 'x.slack', 'x.end'),  # 103
        ('-x.duration', 'x.end', 'x.start', 'x.slack'),  # 104
        ('-x.duration', 'x.end', 'x.slack', 'x.start'),  # 105
        ('-x.duration', 'x.slack', 'x.start', 'x.end'),  # 106
        ('-x.duration', 'x.slack', 'x.end', 'x.start'),  # 107
        ('x.end', 'x.start', '-x.duration', 'x.slack'),  # 108
        ('x.end', 'x.start', 'x.slack', '-x.duration'),  # 109
        ('x.end', '-x.duration', 'x.start', 'x.slack'),  # 110
        ('x.end', '-x.duration', 'x.slack', 'x.start'),  # 111
        ('x.end', 'x.slack', 'x.start', '-x.duration'),  # 112
        ('x.end', 'x.slack', '-x.duration', 'x.start'),  # 113
        ('x.slack', 'x.start', '-x.duration', 'x.end'),  # 114
        ('x.slack', 'x.start', 'x.end', '-x.duration'),  # 115
        ('x.slack', '-x.duration', 'x.start', 'x.end'),  # 116
        ('x.slack', '-x.duration', 'x.end', 'x.start'),  # 117
        ('x.slack', 'x.end', 'x.start', '-x.duration'),  # 118
        ('x.slack', 'x.end', '-x.duration', 'x.start'),  # 119
        ('x.start', '-x.duration', 'x.end', '-x.slack'),  # 120
        ('x.start', '-x.duration', '-x.slack', 'x.end'),  # 121
        ('x.start', 'x.end', '-x.duration', '-x.slack'),  # 122
        ('x.start', 'x.end', '-x.slack', '-x.duration'),  # 123
        ('x.start', '-x.slack', '-x.duration', 'x.end'),  # 124
        ('x.start', '-x.slack', 'x.end', '-x.duration'),  # 125
        ('-x.duration', 'x.start', 'x.end', '-x.slack'),  # 126
        ('-x.duration', 'x.start', '-x.slack', 'x.end'),  # 127
        ('-x.duration', 'x.end', 'x.start', '-x.slack'),  # 128
        ('-x.duration', 'x.end', '-x.slack', 'x.start'),  # 129
        ('-x.duration', '-x.slack', 'x.start', 'x.end'),  # 130
        ('-x.duration', '-x.slack', 'x.end', 'x.start'),  # 131
        ('x.end', 'x.start', '-x.duration', '-x.slack'),  # 132
        ('x.end', 'x.start', '-x.slack', '-x.duration'),  # 133
        ('x.end', '-x.duration', 'x.start', '-x.slack'),  # 134
        ('x.end', '-x.duration', '-x.slack', 'x.start'),  # 135
        ('x.end', '-x.slack', 'x.start', '-x.duration'),  # 136
        ('x.end', '-x.slack', '-x.duration', 'x.start'),  # 137
        ('-x.slack', 'x.start', '-x.duration', 'x.end'),  # 138
        ('-x.slack', 'x.start', 'x.end', '-x.duration'),  # 139
        ('-x.slack', '-x.duration', 'x.start', 'x.end'),  # 140
        ('-x.slack', '-x.duration', 'x.end', 'x.start'),  # 141
        ('-x.slack', 'x.end', 'x.start', '-x.duration'),  # 142
        ('-x.slack', 'x.end', '-x.duration', 'x.start'),  # 143
        ('x.start', '-x.duration', '-x.end', 'x.slack'),  # 144
        ('x.start', '-x.duration', 'x.slack', '-x.end'),  # 145
        ('x.start', '-x.end', '-x.duration', 'x.slack'),  # 146
        ('x.start', '-x.end', 'x.slack', '-x.duration'),  # 147
        ('x.start', 'x.slack', '-x.duration', '-x.end'),  # 148
        ('x.start', 'x.slack', '-x.end', '-x.duration'),  # 149
        ('-x.duration', 'x.start', '-x.end', 'x.slack'),  # 150
        ('-x.duration', 'x.start', 'x.slack', '-x.end'),  # 151
        ('-x.duration', '-x.end', 'x.start', 'x.slack'),  # 152
        ('-x.duration', '-x.end', 'x.slack', 'x.start'),  # 153
        ('-x.duration', 'x.slack', 'x.start', '-x.end'),  # 154
        ('-x.duration', 'x.slack', '-x.end', 'x.start'),  # 155
        ('-x.end', 'x.start', '-x.duration', 'x.slack'),  # 156
        ('-x.end', 'x.start', 'x.slack', '-x.duration'),  # 157
        ('-x.end', '-x.duration', 'x.start', 'x.slack'),  # 158
        ('-x.end', '-x.duration', 'x.slack', 'x.start'),  # 159
        ('-x.end', 'x.slack', 'x.start', '-x.duration'),  # 160
        ('-x.end', 'x.slack', '-x.duration', 'x.start'),  # 161
        ('x.slack', 'x.start', '-x.duration', '-x.end'),  # 162
        ('x.slack', 'x.start', '-x.end', '-x.duration'),  # 163
        ('x.slack', '-x.duration', 'x.start', '-x.end'),  # 164
        ('x.slack', '-x.duration', '-x.end', 'x.start'),  # 165
        ('x.slack', '-x.end', 'x.start', '-x.duration'),  # 166
        ('x.slack', '-x.end', '-x.duration', 'x.start'),  # 167
        ('x.start', '-x.duration', '-x.end', '-x.slack'),  # 168
        ('x.start', '-x.duration', '-x.slack', '-x.end'),  # 169
        ('x.start', '-x.end', '-x.duration', '-x.slack'),  # 170
        ('x.start', '-x.end', '-x.slack', '-x.duration'),  # 171
        ('x.start', '-x.slack', '-x.duration', '-x.end'),  # 172
        ('x.start', '-x.slack', '-x.end', '-x.duration'),  # 173
        ('-x.duration', 'x.start', '-x.end', '-x.slack'),  # 174
        ('-x.duration', 'x.start', '-x.slack', '-x.end'),  # 175
        ('-x.duration', '-x.end', 'x.start', '-x.slack'),  # 176
        ('-x.duration', '-x.end', '-x.slack', 'x.start'),  # 177
        ('-x.duration', '-x.slack', 'x.start', '-x.end'),  # 178
        ('-x.duration', '-x.slack', '-x.end', 'x.start'),  # 179
        ('-x.end', 'x.start', '-x.duration', '-x.slack'),  # 180
        ('-x.end', 'x.start', '-x.slack', '-x.duration'),  # 181
        ('-x.end', '-x.duration', 'x.start', '-x.slack'),  # 182
        ('-x.end', '-x.duration', '-x.slack', 'x.start'),  # 183
        ('-x.end', '-x.slack', 'x.start', '-x.duration'),  # 184
        ('-x.end', '-x.slack', '-x.duration', 'x.start'),  # 185
        ('-x.slack', 'x.start', '-x.duration', '-x.end'),  # 186
        ('-x.slack', 'x.start', '-x.end', '-x.duration'),  # 187
        ('-x.slack', '-x.duration', 'x.start', '-x.end'),  # 188
        ('-x.slack', '-x.duration', '-x.end', 'x.start'),  # 189
        ('-x.slack', '-x.end', 'x.start', '-x.duration'),  # 190
        ('-x.slack', '-x.end', '-x.duration', 'x.start'),  # 191
        ('-x.start', 'x.duration', 'x.end', 'x.slack'),  # 192
        ('-x.start', 'x.duration', 'x.slack', 'x.end'),  # 193
        ('-x.start', 'x.end', 'x.duration', 'x.slack'),  # 194
        ('-x.start', 'x.end', 'x.slack', 'x.duration'),  # 195
        ('-x.start', 'x.slack', 'x.duration', 'x.end'),  # 196
        ('-x.start', 'x.slack', 'x.end', 'x.duration'),  # 197
        ('x.duration', '-x.start', 'x.end', 'x.slack'),  # 198
        ('x.duration', '-x.start', 'x.slack', 'x.end'),  # 199
        ('x.duration', 'x.end', '-x.start', 'x.slack'),  # 200
        ('x.duration', 'x.end', 'x.slack', '-x.start'),  # 201
        ('x.duration', 'x.slack', '-x.start', 'x.end'),  # 202
        ('x.duration', 'x.slack', 'x.end', '-x.start'),  # 203
        ('x.end', '-x.start', 'x.duration', 'x.slack'),  # 204
        ('x.end', '-x.start', 'x.slack', 'x.duration'),  # 205
        ('x.end', 'x.duration', '-x.start', 'x.slack'),  # 206
        ('x.end', 'x.duration', 'x.slack', '-x.start'),  # 207
        ('x.end', 'x.slack', '-x.start', 'x.duration'),  # 208
        ('x.end', 'x.slack', 'x.duration', '-x.start'),  # 209
        ('x.slack', '-x.start', 'x.duration', 'x.end'),  # 210
        ('x.slack', '-x.start', 'x.end', 'x.duration'),  # 211
        ('x.slack', 'x.duration', '-x.start', 'x.end'),  # 212
        ('x.slack', 'x.duration', 'x.end', '-x.start'),  # 213
        ('x.slack', 'x.end', '-x.start', 'x.duration'),  # 214
        ('x.slack', 'x.end', 'x.duration', '-x.start'),  # 215
        ('-x.start', 'x.duration', 'x.end', '-x.slack'),  # 216
        ('-x.start', 'x.duration', '-x.slack', 'x.end'),  # 217
        ('-x.start', 'x.end', 'x.duration', '-x.slack'),  # 218
        ('-x.start', 'x.end', '-x.slack', 'x.duration'),  # 219
        ('-x.start', '-x.slack', 'x.duration', 'x.end'),  # 220
        ('-x.start', '-x.slack', 'x.end', 'x.duration'),  # 221
        ('x.duration', '-x.start', 'x.end', '-x.slack'),  # 222
        ('x.duration', '-x.start', '-x.slack', 'x.end'),  # 223
        ('x.duration', 'x.end', '-x.start', '-x.slack'),  # 224
        ('x.duration', 'x.end', '-x.slack', '-x.start'),  # 225
        ('x.duration', '-x.slack', '-x.start', 'x.end'),  # 226
        ('x.duration', '-x.slack', 'x.end', '-x.start'),  # 227
        ('x.end', '-x.start', 'x.duration', '-x.slack'),  # 228
        ('x.end', '-x.start', '-x.slack', 'x.duration'),  # 229
        ('x.end', 'x.duration', '-x.start', '-x.slack'),  # 230
        ('x.end', 'x.duration', '-x.slack', '-x.start'),  # 231
        ('x.end', '-x.slack', '-x.start', 'x.duration'),  # 232
        ('x.end', '-x.slack', 'x.duration', '-x.start'),  # 233
        ('-x.slack', '-x.start', 'x.duration', 'x.end'),  # 234
        ('-x.slack', '-x.start', 'x.end', 'x.duration'),  # 235
        ('-x.slack', 'x.duration', '-x.start', 'x.end'),  # 236
        ('-x.slack', 'x.duration', 'x.end', '-x.start'),  # 237
        ('-x.slack', 'x.end', '-x.start', 'x.duration'),  # 238
        ('-x.slack', 'x.end', 'x.duration', '-x.start'),  # 239
        ('-x.start', 'x.duration', '-x.end', 'x.slack'),  # 240
        ('-x.start', 'x.duration', 'x.slack', '-x.end'),  # 241
        ('-x.start', '-x.end', 'x.duration', 'x.slack'),  # 242
        ('-x.start', '-x.end', 'x.slack', 'x.duration'),  # 243
        ('-x.start', 'x.slack', 'x.duration', '-x.end'),  # 244
        ('-x.start', 'x.slack', '-x.end', 'x.duration'),  # 245
        ('x.duration', '-x.start', '-x.end', 'x.slack'),  # 246
        ('x.duration', '-x.start', 'x.slack', '-x.end'),  # 247
        ('x.duration', '-x.end', '-x.start', 'x.slack'),  # 248
        ('x.duration', '-x.end', 'x.slack', '-x.start'),  # 249
        ('x.duration', 'x.slack', '-x.start', '-x.end'),  # 250
        ('x.duration', 'x.slack', '-x.end', '-x.start'),  # 251
        ('-x.end', '-x.start', 'x.duration', 'x.slack'),  # 252
        ('-x.end', '-x.start', 'x.slack', 'x.duration'),  # 253
        ('-x.end', 'x.duration', '-x.start', 'x.slack'),  # 254
        ('-x.end', 'x.duration', 'x.slack', '-x.start'),  # 255
        ('-x.end', 'x.slack', '-x.start', 'x.duration'),  # 256
        ('-x.end', 'x.slack', 'x.duration', '-x.start'),  # 257
        ('x.slack', '-x.start', 'x.duration', '-x.end'),  # 258
        ('x.slack', '-x.start', '-x.end', 'x.duration'),  # 259
        ('x.slack', 'x.duration', '-x.start', '-x.end'),  # 260
        ('x.slack', 'x.duration', '-x.end', '-x.start'),  # 261
        ('x.slack', '-x.end', '-x.start', 'x.duration'),  # 262
        ('x.slack', '-x.end', 'x.duration', '-x.start'),  # 263
        ('-x.start', 'x.duration', '-x.end', '-x.slack'),  # 264
        ('-x.start', 'x.duration', '-x.slack', '-x.end'),  # 265
        ('-x.start', '-x.end', 'x.duration', '-x.slack'),  # 266
        ('-x.start', '-x.end', '-x.slack', 'x.duration'),  # 267
        ('-x.start', '-x.slack', 'x.duration', '-x.end'),  # 268
        ('-x.start', '-x.slack', '-x.end', 'x.duration'),  # 269
        ('x.duration', '-x.start', '-x.end', '-x.slack'),  # 270
        ('x.duration', '-x.start', '-x.slack', '-x.end'),  # 271
        ('x.duration', '-x.end', '-x.start', '-x.slack'),  # 272
        ('x.duration', '-x.end', '-x.slack', '-x.start'),  # 273
        ('x.duration', '-x.slack', '-x.start', '-x.end'),  # 274
        ('x.duration', '-x.slack', '-x.end', '-x.start'),  # 275
        ('-x.end', '-x.start', 'x.duration', '-x.slack'),  # 276
        ('-x.end', '-x.start', '-x.slack', 'x.duration'),  # 277
        ('-x.end', 'x.duration', '-x.start', '-x.slack'),  # 278
        ('-x.end', 'x.duration', '-x.slack', '-x.start'),  # 279
        ('-x.end', '-x.slack', '-x.start', 'x.duration'),  # 280
        ('-x.end', '-x.slack', 'x.duration', '-x.start'),  # 281
        ('-x.slack', '-x.start', 'x.duration', '-x.end'),  # 282
        ('-x.slack', '-x.start', '-x.end', 'x.duration'),  # 283
        ('-x.slack', 'x.duration', '-x.start', '-x.end'),  # 284
        ('-x.slack', 'x.duration', '-x.end', '-x.start'),  # 285
        ('-x.slack', '-x.end', '-x.start', 'x.duration'),  # 286
        ('-x.slack', '-x.end', 'x.duration', '-x.start'),  # 287
        ('-x.start', '-x.duration', 'x.end', 'x.slack'),  # 288
        ('-x.start', '-x.duration', 'x.slack', 'x.end'),  # 289
        ('-x.start', 'x.end', '-x.duration', 'x.slack'),  # 290
        ('-x.start', 'x.end', 'x.slack', '-x.duration'),  # 291
        ('-x.start', 'x.slack', '-x.duration', 'x.end'),  # 292
        ('-x.start', 'x.slack', 'x.end', '-x.duration'),  # 293
        ('-x.duration', '-x.start', 'x.end', 'x.slack'),  # 294
        ('-x.duration', '-x.start', 'x.slack', 'x.end'),  # 295
        ('-x.duration', 'x.end', '-x.start', 'x.slack'),  # 296
        ('-x.duration', 'x.end', 'x.slack', '-x.start'),  # 297
        ('-x.duration', 'x.slack', '-x.start', 'x.end'),  # 298
        ('-x.duration', 'x.slack', 'x.end', '-x.start'),  # 299
        ('x.end', '-x.start', '-x.duration', 'x.slack'),  # 300
        ('x.end', '-x.start', 'x.slack', '-x.duration'),  # 301
        ('x.end', '-x.duration', '-x.start', 'x.slack'),  # 302
        ('x.end', '-x.duration', 'x.slack', '-x.start'),  # 303
        ('x.end', 'x.slack', '-x.start', '-x.duration'),  # 304
        ('x.end', 'x.slack', '-x.duration', '-x.start'),  # 305
        ('x.slack', '-x.start', '-x.duration', 'x.end'),  # 306
        ('x.slack', '-x.start', 'x.end', '-x.duration'),  # 307
        ('x.slack', '-x.duration', '-x.start', 'x.end'),  # 308
        ('x.slack', '-x.duration', 'x.end', '-x.start'),  # 309
        ('x.slack', 'x.end', '-x.start', '-x.duration'),  # 310
        ('x.slack', 'x.end', '-x.duration', '-x.start'),  # 311
        ('-x.start', '-x.duration', 'x.end', '-x.slack'),  # 312
        ('-x.start', '-x.duration', '-x.slack', 'x.end'),  # 313
        ('-x.start', 'x.end', '-x.duration', '-x.slack'),  # 314
        ('-x.start', 'x.end', '-x.slack', '-x.duration'),  # 315
        ('-x.start', '-x.slack', '-x.duration', 'x.end'),  # 316
        ('-x.start', '-x.slack', 'x.end', '-x.duration'),  # 317
        ('-x.duration', '-x.start', 'x.end', '-x.slack'),  # 318
        ('-x.duration', '-x.start', '-x.slack', 'x.end'),  # 319
        ('-x.duration', 'x.end', '-x.start', '-x.slack'),  # 320
        ('-x.duration', 'x.end', '-x.slack', '-x.start'),  # 321
        ('-x.duration', '-x.slack', '-x.start', 'x.end'),  # 322
        ('-x.duration', '-x.slack', 'x.end', '-x.start'),  # 323
        ('x.end', '-x.start', '-x.duration', '-x.slack'),  # 324
        ('x.end', '-x.start', '-x.slack', '-x.duration'),  # 325
        ('x.end', '-x.duration', '-x.start', '-x.slack'),  # 326
        ('x.end', '-x.duration', '-x.slack', '-x.start'),  # 327
        ('x.end', '-x.slack', '-x.start', '-x.duration'),  # 328
        ('x.end', '-x.slack', '-x.duration', '-x.start'),  # 329
        ('-x.slack', '-x.start', '-x.duration', 'x.end'),  # 330
        ('-x.slack', '-x.start', 'x.end', '-x.duration'),  # 331
        ('-x.slack', '-x.duration', '-x.start', 'x.end'),  # 332
        ('-x.slack', '-x.duration', 'x.end', '-x.start'),  # 333
        ('-x.slack', 'x.end', '-x.start', '-x.duration'),  # 334
        ('-x.slack', 'x.end', '-x.duration', '-x.start'),  # 335
        ('-x.start', '-x.duration', '-x.end', 'x.slack'),  # 336
        ('-x.start', '-x.duration', 'x.slack', '-x.end'),  # 337
        ('-x.start', '-x.end', '-x.duration', 'x.slack'),  # 338
        ('-x.start', '-x.end', 'x.slack', '-x.duration'),  # 339
        ('-x.start', 'x.slack', '-x.duration', '-x.end'),  # 340
        ('-x.start', 'x.slack', '-x.end', '-x.duration'),  # 341
        ('-x.duration', '-x.start', '-x.end', 'x.slack'),  # 342
        ('-x.duration', '-x.start', 'x.slack', '-x.end'),  # 343
        ('-x.duration', '-x.end', '-x.start', 'x.slack'),  # 344
        ('-x.duration', '-x.end', 'x.slack', '-x.start'),  # 345
        ('-x.duration', 'x.slack', '-x.start', '-x.end'),  # 346
        ('-x.duration', 'x.slack', '-x.end', '-x.start'),  # 347
        ('-x.end', '-x.start', '-x.duration', 'x.slack'),  # 348
        ('-x.end', '-x.start', 'x.slack', '-x.duration'),  # 349
        ('-x.end', '-x.duration', '-x.start', 'x.slack'),  # 350
        ('-x.end', '-x.duration', 'x.slack', '-x.start'),  # 351
        ('-x.end', 'x.slack', '-x.start', '-x.duration'),  # 352
        ('-x.end', 'x.slack', '-x.duration', '-x.start'),  # 353
        ('x.slack', '-x.start', '-x.duration', '-x.end'),  # 354
        ('x.slack', '-x.start', '-x.end', '-x.duration'),  # 355
        ('x.slack', '-x.duration', '-x.start', '-x.end'),  # 356
        ('x.slack', '-x.duration', '-x.end', '-x.start'),  # 357
        ('x.slack', '-x.end', '-x.start', '-x.duration'),  # 358
        ('x.slack', '-x.end', '-x.duration', '-x.start'),  # 359
        ('-x.start', '-x.duration', '-x.end', '-x.slack'),  # 360
        ('-x.start', '-x.duration', '-x.slack', '-x.end'),  # 361
        ('-x.start', '-x.end', '-x.duration', '-x.slack'),  # 362
        ('-x.start', '-x.end', '-x.slack', '-x.duration'),  # 363
        ('-x.start', '-x.slack', '-x.duration', '-x.end'),  # 364
        ('-x.start', '-x.slack', '-x.end', '-x.duration'),  # 365
        ('-x.duration', '-x.start', '-x.end', '-x.slack'),  # 366
        ('-x.duration', '-x.start', '-x.slack', '-x.end'),  # 367
        ('-x.duration', '-x.end', '-x.start', '-x.slack'),  # 368
        ('-x.duration', '-x.end', '-x.slack', '-x.start'),  # 369
        ('-x.duration', '-x.slack', '-x.start', '-x.end'),  # 370
        ('-x.duration', '-x.slack', '-x.end', '-x.start'),  # 371
        ('-x.end', '-x.start', '-x.duration', '-x.slack'),  # 372
        ('-x.end', '-x.start', '-x.slack', '-x.duration'),  # 373
        ('-x.end', '-x.duration', '-x.start', '-x.slack'),  # 374
        ('-x.end', '-x.duration', '-x.slack', '-x.start'),  # 375
        ('-x.end', '-x.slack', '-x.start', '-x.duration'),  # 376
        ('-x.end', '-x.slack', '-x.duration', '-x.start'),  # 377
        ('-x.slack', '-x.start', '-x.duration', '-x.end'),  # 378
        ('-x.slack', '-x.start', '-x.end', '-x.duration'),  # 379
        ('-x.slack', '-x.duration', '-x.start', '-x.end'),  # 380
        ('-x.slack', '-x.duration', '-x.end', '-x.start'),  # 381
        ('-x.slack', '-x.end', '-x.start', '-x.duration'),  # 382
        ('-x.slack', '-x.end', '-x.duration', '-x.start'),  # 383
    ]

    # noinspection PyDefaultArgument
    def __init__(self, tasks_list=[]) -> None:
        self.tasks_list = copy.deepcopy(tasks_list)
        self.workforce = Workforce()
        self.tasks_number = len(self.tasks_list)
        self.optimal_slack_combination = None
        self.minimum_employees_no = None

    def list_tasks(self) -> None:
        for task_no, task in enumerate(self.tasks_list):
            assert isinstance(task, Task)
            print(
                f'Task #{task_no}, ID: {task.id}, start: {task.start * 15}, end: {task.end * 15}, '
                f'duration: {task.duration * 15}, slack: {task.slack * 15}')

    def generate_random_tasks(self, total_time, tolerance_perc=10, mean_value=2, std_dev=3, step=1, min_duration=0,
                              max_duration=12, work_end_time=24) -> None:
        """Function generates random tasks list with sum of all tasks equal to total_time"""

        temp_task_list = []
        self.tasks_list = []
        number_of_tasks = total_time // mean_value

        while (sum(temp_task_list) < total_time * (100 - tolerance_perc) / 100) or (
                sum(temp_task_list) > total_time * (100 + tolerance_perc) / 100):

            temp_task_list = [int(random.gauss(mean_value, std_dev)) // step * step for _ in range(0, number_of_tasks)]
            temp_task_list = [y for y in temp_task_list if min_duration < y < max_duration]

            if sum(temp_task_list) != 0:
                number_of_tasks = int(number_of_tasks * total_time / sum(temp_task_list))
            else:
                number_of_tasks = 1

        for duration in temp_task_list:

            end = random.randrange(duration, work_end_time, step)
            if end - duration:
                # slack = random.randrange(0, min(end - duration, 3), step)
                slack = random.randrange(0, end - duration, step)
            else:
                slack = 0
            start = end - slack - duration

            self.tasks_list.append(Task(start, end, duration, slack))
        self.tasks_number = len(self.tasks_list)

    @staticmethod
    def lambda_function(x, sorting_type):
        """function returns one of all possible sorting combinations"""
        assert sorting_type in range(0, 384)

        POSITIVE_SORTING_COMBINATIONS = [
            (x.start, x.duration, x.end, x.slack),  # 0
            (x.start, x.duration, x.slack, x.end),  # 1
            (x.start, x.end, x.duration, x.slack),  # 2
            (x.start, x.end, x.slack, x.duration),  # 3
            (x.start, x.slack, x.duration, x.end),  # 4
            (x.start, x.slack, x.end, x.duration),  # 5
            (x.duration, x.start, x.end, x.slack),  # 6
            (x.duration, x.start, x.slack, x.end),  # 7
            (x.duration, x.end, x.start, x.slack),  # 8
            (x.duration, x.end, x.slack, x.start),  # 9
            (x.duration, x.slack, x.start, x.end),  # 10
            (x.duration, x.slack, x.end, x.start),  # 11
            (x.end, x.start, x.duration, x.slack),  # 12
            (x.end, x.start, x.slack, x.duration),  # 13
            (x.end, x.duration, x.start, x.slack),  # 14
            (x.end, x.duration, x.slack, x.start),  # 15
            (x.end, x.slack, x.start, x.duration),  # 16 - Best
            (x.end, x.slack, x.duration, x.start),  # 17
            (x.slack, x.start, x.duration, x.end),  # 18
            (x.slack, x.start, x.end, x.duration),  # 19
            (x.slack, x.duration, x.start, x.end),  # 20
            (x.slack, x.duration, x.end, x.start),  # 21
            (x.slack, x.end, x.start, x.duration),  # 22
            (x.slack, x.end, x.duration, x.start),  # 23
        ]
        ALL_SORTING_COMBINATIONS = [
            (x.start, x.duration, x.end, x.slack),  # 0
            (x.start, x.duration, x.slack, x.end),  # 1
            (x.start, x.end, x.duration, x.slack),  # 2
            (x.start, x.end, x.slack, x.duration),  # 3
            (x.start, x.slack, x.duration, x.end),  # 4
            (x.start, x.slack, x.end, x.duration),  # 5
            (x.duration, x.start, x.end, x.slack),  # 6
            (x.duration, x.start, x.slack, x.end),  # 7
            (x.duration, x.end, x.start, x.slack),  # 8
            (x.duration, x.end, x.slack, x.start),  # 9
            (x.duration, x.slack, x.start, x.end),  # 10
            (x.duration, x.slack, x.end, x.start),  # 11
            (x.end, x.start, x.duration, x.slack),  # 12
            (x.end, x.start, x.slack, x.duration),  # 13
            (x.end, x.duration, x.start, x.slack),  # 14
            (x.end, x.duration, x.slack, x.start),  # 15
            (x.end, x.slack, x.start, x.duration),  # 16
            (x.end, x.slack, x.duration, x.start),  # 17
            (x.slack, x.start, x.duration, x.end),  # 18
            (x.slack, x.start, x.end, x.duration),  # 19
            (x.slack, x.duration, x.start, x.end),  # 20
            (x.slack, x.duration, x.end, x.start),  # 21
            (x.slack, x.end, x.start, x.duration),  # 22
            (x.slack, x.end, x.duration, x.start),  # 23
            (x.start, x.duration, x.end, -x.slack),  # 24
            (x.start, x.duration, -x.slack, x.end),  # 25
            (x.start, x.end, x.duration, -x.slack),  # 26
            (x.start, x.end, -x.slack, x.duration),  # 27
            (x.start, -x.slack, x.duration, x.end),  # 28
            (x.start, -x.slack, x.end, x.duration),  # 29
            (x.duration, x.start, x.end, -x.slack),  # 30
            (x.duration, x.start, -x.slack, x.end),  # 31
            (x.duration, x.end, x.start, -x.slack),  # 32
            (x.duration, x.end, -x.slack, x.start),  # 33
            (x.duration, -x.slack, x.start, x.end),  # 34
            (x.duration, -x.slack, x.end, x.start),  # 35
            (x.end, x.start, x.duration, -x.slack),  # 36
            (x.end, x.start, -x.slack, x.duration),  # 37
            (x.end, x.duration, x.start, -x.slack),  # 38
            (x.end, x.duration, -x.slack, x.start),  # 39
            (x.end, -x.slack, x.start, x.duration),  # 40
            (x.end, -x.slack, x.duration, x.start),  # 41
            (-x.slack, x.start, x.duration, x.end),  # 42
            (-x.slack, x.start, x.end, x.duration),  # 43
            (-x.slack, x.duration, x.start, x.end),  # 44
            (-x.slack, x.duration, x.end, x.start),  # 45
            (-x.slack, x.end, x.start, x.duration),  # 46
            (-x.slack, x.end, x.duration, x.start),  # 47
            (x.start, x.duration, -x.end, x.slack),  # 48
            (x.start, x.duration, x.slack, -x.end),  # 49
            (x.start, -x.end, x.duration, x.slack),  # 50
            (x.start, -x.end, x.slack, x.duration),  # 51
            (x.start, x.slack, x.duration, -x.end),  # 52
            (x.start, x.slack, -x.end, x.duration),  # 53
            (x.duration, x.start, -x.end, x.slack),  # 54
            (x.duration, x.start, x.slack, -x.end),  # 55
            (x.duration, -x.end, x.start, x.slack),  # 56
            (x.duration, -x.end, x.slack, x.start),  # 57
            (x.duration, x.slack, x.start, -x.end),  # 58
            (x.duration, x.slack, -x.end, x.start),  # 59
            (-x.end, x.start, x.duration, x.slack),  # 60
            (-x.end, x.start, x.slack, x.duration),  # 61
            (-x.end, x.duration, x.start, x.slack),  # 62
            (-x.end, x.duration, x.slack, x.start),  # 63
            (-x.end, x.slack, x.start, x.duration),  # 64
            (-x.end, x.slack, x.duration, x.start),  # 65
            (x.slack, x.start, x.duration, -x.end),  # 66
            (x.slack, x.start, -x.end, x.duration),  # 67
            (x.slack, x.duration, x.start, -x.end),  # 68
            (x.slack, x.duration, -x.end, x.start),  # 69
            (x.slack, -x.end, x.start, x.duration),  # 70
            (x.slack, -x.end, x.duration, x.start),  # 71
            (x.start, x.duration, -x.end, -x.slack),  # 72
            (x.start, x.duration, -x.slack, -x.end),  # 73
            (x.start, -x.end, x.duration, -x.slack),  # 74
            (x.start, -x.end, -x.slack, x.duration),  # 75
            (x.start, -x.slack, x.duration, -x.end),  # 76
            (x.start, -x.slack, -x.end, x.duration),  # 77
            (x.duration, x.start, -x.end, -x.slack),  # 78
            (x.duration, x.start, -x.slack, -x.end),  # 79
            (x.duration, -x.end, x.start, -x.slack),  # 80
            (x.duration, -x.end, -x.slack, x.start),  # 81
            (x.duration, -x.slack, x.start, -x.end),  # 82
            (x.duration, -x.slack, -x.end, x.start),  # 83
            (-x.end, x.start, x.duration, -x.slack),  # 84
            (-x.end, x.start, -x.slack, x.duration),  # 85
            (-x.end, x.duration, x.start, -x.slack),  # 86
            (-x.end, x.duration, -x.slack, x.start),  # 87
            (-x.end, -x.slack, x.start, x.duration),  # 88
            (-x.end, -x.slack, x.duration, x.start),  # 89
            (-x.slack, x.start, x.duration, -x.end),  # 90
            (-x.slack, x.start, -x.end, x.duration),  # 91
            (-x.slack, x.duration, x.start, -x.end),  # 92
            (-x.slack, x.duration, -x.end, x.start),  # 93
            (-x.slack, -x.end, x.start, x.duration),  # 94
            (-x.slack, -x.end, x.duration, x.start),  # 95
            (x.start, -x.duration, x.end, x.slack),  # 96
            (x.start, -x.duration, x.slack, x.end),  # 97
            (x.start, x.end, -x.duration, x.slack),  # 98
            (x.start, x.end, x.slack, -x.duration),  # 99
            (x.start, x.slack, -x.duration, x.end),  # 100
            (x.start, x.slack, x.end, -x.duration),  # 101
            (-x.duration, x.start, x.end, x.slack),  # 102
            (-x.duration, x.start, x.slack, x.end),  # 103
            (-x.duration, x.end, x.start, x.slack),  # 104
            (-x.duration, x.end, x.slack, x.start),  # 105
            (-x.duration, x.slack, x.start, x.end),  # 106
            (-x.duration, x.slack, x.end, x.start),  # 107
            (x.end, x.start, -x.duration, x.slack),  # 108
            (x.end, x.start, x.slack, -x.duration),  # 109
            (x.end, -x.duration, x.start, x.slack),  # 110
            (x.end, -x.duration, x.slack, x.start),  # 111
            (x.end, x.slack, x.start, -x.duration),  # 112
            (x.end, x.slack, -x.duration, x.start),  # 113
            (x.slack, x.start, -x.duration, x.end),  # 114
            (x.slack, x.start, x.end, -x.duration),  # 115
            (x.slack, -x.duration, x.start, x.end),  # 116
            (x.slack, -x.duration, x.end, x.start),  # 117
            (x.slack, x.end, x.start, -x.duration),  # 118
            (x.slack, x.end, -x.duration, x.start),  # 119
            (x.start, -x.duration, x.end, -x.slack),  # 120
            (x.start, -x.duration, -x.slack, x.end),  # 121
            (x.start, x.end, -x.duration, -x.slack),  # 122
            (x.start, x.end, -x.slack, -x.duration),  # 123
            (x.start, -x.slack, -x.duration, x.end),  # 124
            (x.start, -x.slack, x.end, -x.duration),  # 125
            (-x.duration, x.start, x.end, -x.slack),  # 126
            (-x.duration, x.start, -x.slack, x.end),  # 127
            (-x.duration, x.end, x.start, -x.slack),  # 128
            (-x.duration, x.end, -x.slack, x.start),  # 129
            (-x.duration, -x.slack, x.start, x.end),  # 130
            (-x.duration, -x.slack, x.end, x.start),  # 131
            (x.end, x.start, -x.duration, -x.slack),  # 132
            (x.end, x.start, -x.slack, -x.duration),  # 133
            (x.end, -x.duration, x.start, -x.slack),  # 134
            (x.end, -x.duration, -x.slack, x.start),  # 135
            (x.end, -x.slack, x.start, -x.duration),  # 136
            (x.end, -x.slack, -x.duration, x.start),  # 137
            (-x.slack, x.start, -x.duration, x.end),  # 138
            (-x.slack, x.start, x.end, -x.duration),  # 139
            (-x.slack, -x.duration, x.start, x.end),  # 140
            (-x.slack, -x.duration, x.end, x.start),  # 141
            (-x.slack, x.end, x.start, -x.duration),  # 142
            (-x.slack, x.end, -x.duration, x.start),  # 143
            (x.start, -x.duration, -x.end, x.slack),  # 144
            (x.start, -x.duration, x.slack, -x.end),  # 145
            (x.start, -x.end, -x.duration, x.slack),  # 146
            (x.start, -x.end, x.slack, -x.duration),  # 147
            (x.start, x.slack, -x.duration, -x.end),  # 148
            (x.start, x.slack, -x.end, -x.duration),  # 149
            (-x.duration, x.start, -x.end, x.slack),  # 150
            (-x.duration, x.start, x.slack, -x.end),  # 151
            (-x.duration, -x.end, x.start, x.slack),  # 152
            (-x.duration, -x.end, x.slack, x.start),  # 153
            (-x.duration, x.slack, x.start, -x.end),  # 154
            (-x.duration, x.slack, -x.end, x.start),  # 155
            (-x.end, x.start, -x.duration, x.slack),  # 156
            (-x.end, x.start, x.slack, -x.duration),  # 157
            (-x.end, -x.duration, x.start, x.slack),  # 158
            (-x.end, -x.duration, x.slack, x.start),  # 159
            (-x.end, x.slack, x.start, -x.duration),  # 160
            (-x.end, x.slack, -x.duration, x.start),  # 161
            (x.slack, x.start, -x.duration, -x.end),  # 162
            (x.slack, x.start, -x.end, -x.duration),  # 163
            (x.slack, -x.duration, x.start, -x.end),  # 164
            (x.slack, -x.duration, -x.end, x.start),  # 165
            (x.slack, -x.end, x.start, -x.duration),  # 166
            (x.slack, -x.end, -x.duration, x.start),  # 167
            (x.start, -x.duration, -x.end, -x.slack),  # 168
            (x.start, -x.duration, -x.slack, -x.end),  # 169
            (x.start, -x.end, -x.duration, -x.slack),  # 170
            (x.start, -x.end, -x.slack, -x.duration),  # 171
            (x.start, -x.slack, -x.duration, -x.end),  # 172
            (x.start, -x.slack, -x.end, -x.duration),  # 173
            (-x.duration, x.start, -x.end, -x.slack),  # 174
            (-x.duration, x.start, -x.slack, -x.end),  # 175
            (-x.duration, -x.end, x.start, -x.slack),  # 176
            (-x.duration, -x.end, -x.slack, x.start),  # 177
            (-x.duration, -x.slack, x.start, -x.end),  # 178
            (-x.duration, -x.slack, -x.end, x.start),  # 179
            (-x.end, x.start, -x.duration, -x.slack),  # 180
            (-x.end, x.start, -x.slack, -x.duration),  # 181
            (-x.end, -x.duration, x.start, -x.slack),  # 182
            (-x.end, -x.duration, -x.slack, x.start),  # 183
            (-x.end, -x.slack, x.start, -x.duration),  # 184
            (-x.end, -x.slack, -x.duration, x.start),  # 185
            (-x.slack, x.start, -x.duration, -x.end),  # 186
            (-x.slack, x.start, -x.end, -x.duration),  # 187
            (-x.slack, -x.duration, x.start, -x.end),  # 188
            (-x.slack, -x.duration, -x.end, x.start),  # 189
            (-x.slack, -x.end, x.start, -x.duration),  # 190
            (-x.slack, -x.end, -x.duration, x.start),  # 191
            (-x.start, x.duration, x.end, x.slack),  # 192
            (-x.start, x.duration, x.slack, x.end),  # 193
            (-x.start, x.end, x.duration, x.slack),  # 194
            (-x.start, x.end, x.slack, x.duration),  # 195
            (-x.start, x.slack, x.duration, x.end),  # 196
            (-x.start, x.slack, x.end, x.duration),  # 197
            (x.duration, -x.start, x.end, x.slack),  # 198
            (x.duration, -x.start, x.slack, x.end),  # 199
            (x.duration, x.end, -x.start, x.slack),  # 200
            (x.duration, x.end, x.slack, -x.start),  # 201
            (x.duration, x.slack, -x.start, x.end),  # 202
            (x.duration, x.slack, x.end, -x.start),  # 203
            (x.end, -x.start, x.duration, x.slack),  # 204
            (x.end, -x.start, x.slack, x.duration),  # 205
            (x.end, x.duration, -x.start, x.slack),  # 206
            (x.end, x.duration, x.slack, -x.start),  # 207
            (x.end, x.slack, -x.start, x.duration),  # 208
            (x.end, x.slack, x.duration, -x.start),  # 209
            (x.slack, -x.start, x.duration, x.end),  # 210
            (x.slack, -x.start, x.end, x.duration),  # 211
            (x.slack, x.duration, -x.start, x.end),  # 212
            (x.slack, x.duration, x.end, -x.start),  # 213
            (x.slack, x.end, -x.start, x.duration),  # 214
            (x.slack, x.end, x.duration, -x.start),  # 215
            (-x.start, x.duration, x.end, -x.slack),  # 216
            (-x.start, x.duration, -x.slack, x.end),  # 217
            (-x.start, x.end, x.duration, -x.slack),  # 218
            (-x.start, x.end, -x.slack, x.duration),  # 219
            (-x.start, -x.slack, x.duration, x.end),  # 220
            (-x.start, -x.slack, x.end, x.duration),  # 221
            (x.duration, -x.start, x.end, -x.slack),  # 222
            (x.duration, -x.start, -x.slack, x.end),  # 223
            (x.duration, x.end, -x.start, -x.slack),  # 224
            (x.duration, x.end, -x.slack, -x.start),  # 225
            (x.duration, -x.slack, -x.start, x.end),  # 226
            (x.duration, -x.slack, x.end, -x.start),  # 227
            (x.end, -x.start, x.duration, -x.slack),  # 228
            (x.end, -x.start, -x.slack, x.duration),  # 229
            (x.end, x.duration, -x.start, -x.slack),  # 230
            (x.end, x.duration, -x.slack, -x.start),  # 231
            (x.end, -x.slack, -x.start, x.duration),  # 232
            (x.end, -x.slack, x.duration, -x.start),  # 233
            (-x.slack, -x.start, x.duration, x.end),  # 234
            (-x.slack, -x.start, x.end, x.duration),  # 235
            (-x.slack, x.duration, -x.start, x.end),  # 236
            (-x.slack, x.duration, x.end, -x.start),  # 237
            (-x.slack, x.end, -x.start, x.duration),  # 238
            (-x.slack, x.end, x.duration, -x.start),  # 239
            (-x.start, x.duration, -x.end, x.slack),  # 240
            (-x.start, x.duration, x.slack, -x.end),  # 241
            (-x.start, -x.end, x.duration, x.slack),  # 242
            (-x.start, -x.end, x.slack, x.duration),  # 243
            (-x.start, x.slack, x.duration, -x.end),  # 244
            (-x.start, x.slack, -x.end, x.duration),  # 245
            (x.duration, -x.start, -x.end, x.slack),  # 246
            (x.duration, -x.start, x.slack, -x.end),  # 247
            (x.duration, -x.end, -x.start, x.slack),  # 248
            (x.duration, -x.end, x.slack, -x.start),  # 249
            (x.duration, x.slack, -x.start, -x.end),  # 250
            (x.duration, x.slack, -x.end, -x.start),  # 251
            (-x.end, -x.start, x.duration, x.slack),  # 252
            (-x.end, -x.start, x.slack, x.duration),  # 253
            (-x.end, x.duration, -x.start, x.slack),  # 254
            (-x.end, x.duration, x.slack, -x.start),  # 255
            (-x.end, x.slack, -x.start, x.duration),  # 256
            (-x.end, x.slack, x.duration, -x.start),  # 257
            (x.slack, -x.start, x.duration, -x.end),  # 258
            (x.slack, -x.start, -x.end, x.duration),  # 259
            (x.slack, x.duration, -x.start, -x.end),  # 260
            (x.slack, x.duration, -x.end, -x.start),  # 261
            (x.slack, -x.end, -x.start, x.duration),  # 262
            (x.slack, -x.end, x.duration, -x.start),  # 263
            (-x.start, x.duration, -x.end, -x.slack),  # 264
            (-x.start, x.duration, -x.slack, -x.end),  # 265
            (-x.start, -x.end, x.duration, -x.slack),  # 266
            (-x.start, -x.end, -x.slack, x.duration),  # 267
            (-x.start, -x.slack, x.duration, -x.end),  # 268
            (-x.start, -x.slack, -x.end, x.duration),  # 269
            (x.duration, -x.start, -x.end, -x.slack),  # 270
            (x.duration, -x.start, -x.slack, -x.end),  # 271
            (x.duration, -x.end, -x.start, -x.slack),  # 272
            (x.duration, -x.end, -x.slack, -x.start),  # 273
            (x.duration, -x.slack, -x.start, -x.end),  # 274
            (x.duration, -x.slack, -x.end, -x.start),  # 275
            (-x.end, -x.start, x.duration, -x.slack),  # 276
            (-x.end, -x.start, -x.slack, x.duration),  # 277
            (-x.end, x.duration, -x.start, -x.slack),  # 278
            (-x.end, x.duration, -x.slack, -x.start),  # 279
            (-x.end, -x.slack, -x.start, x.duration),  # 280
            (-x.end, -x.slack, x.duration, -x.start),  # 281
            (-x.slack, -x.start, x.duration, -x.end),  # 282
            (-x.slack, -x.start, -x.end, x.duration),  # 283
            (-x.slack, x.duration, -x.start, -x.end),  # 284
            (-x.slack, x.duration, -x.end, -x.start),  # 285
            (-x.slack, -x.end, -x.start, x.duration),  # 286
            (-x.slack, -x.end, x.duration, -x.start),  # 287
            (-x.start, -x.duration, x.end, x.slack),  # 288
            (-x.start, -x.duration, x.slack, x.end),  # 289
            (-x.start, x.end, -x.duration, x.slack),  # 290
            (-x.start, x.end, x.slack, -x.duration),  # 291
            (-x.start, x.slack, -x.duration, x.end),  # 292
            (-x.start, x.slack, x.end, -x.duration),  # 293
            (-x.duration, -x.start, x.end, x.slack),  # 294
            (-x.duration, -x.start, x.slack, x.end),  # 295
            (-x.duration, x.end, -x.start, x.slack),  # 296
            (-x.duration, x.end, x.slack, -x.start),  # 297
            (-x.duration, x.slack, -x.start, x.end),  # 298
            (-x.duration, x.slack, x.end, -x.start),  # 299
            (x.end, -x.start, -x.duration, x.slack),  # 300
            (x.end, -x.start, x.slack, -x.duration),  # 301
            (x.end, -x.duration, -x.start, x.slack),  # 302
            (x.end, -x.duration, x.slack, -x.start),  # 303
            (x.end, x.slack, -x.start, -x.duration),  # 304
            (x.end, x.slack, -x.duration, -x.start),  # 305
            (x.slack, -x.start, -x.duration, x.end),  # 306
            (x.slack, -x.start, x.end, -x.duration),  # 307
            (x.slack, -x.duration, -x.start, x.end),  # 308
            (x.slack, -x.duration, x.end, -x.start),  # 309
            (x.slack, x.end, -x.start, -x.duration),  # 310
            (x.slack, x.end, -x.duration, -x.start),  # 311
            (-x.start, -x.duration, x.end, -x.slack),  # 312
            (-x.start, -x.duration, -x.slack, x.end),  # 313
            (-x.start, x.end, -x.duration, -x.slack),  # 314
            (-x.start, x.end, -x.slack, -x.duration),  # 315
            (-x.start, -x.slack, -x.duration, x.end),  # 316
            (-x.start, -x.slack, x.end, -x.duration),  # 317
            (-x.duration, -x.start, x.end, -x.slack),  # 318
            (-x.duration, -x.start, -x.slack, x.end),  # 319
            (-x.duration, x.end, -x.start, -x.slack),  # 320
            (-x.duration, x.end, -x.slack, -x.start),  # 321
            (-x.duration, -x.slack, -x.start, x.end),  # 322
            (-x.duration, -x.slack, x.end, -x.start),  # 323
            (x.end, -x.start, -x.duration, -x.slack),  # 324
            (x.end, -x.start, -x.slack, -x.duration),  # 325
            (x.end, -x.duration, -x.start, -x.slack),  # 326
            (x.end, -x.duration, -x.slack, -x.start),  # 327
            (x.end, -x.slack, -x.start, -x.duration),  # 328
            (x.end, -x.slack, -x.duration, -x.start),  # 329
            (-x.slack, -x.start, -x.duration, x.end),  # 330
            (-x.slack, -x.start, x.end, -x.duration),  # 331
            (-x.slack, -x.duration, -x.start, x.end),  # 332
            (-x.slack, -x.duration, x.end, -x.start),  # 333
            (-x.slack, x.end, -x.start, -x.duration),  # 334
            (-x.slack, x.end, -x.duration, -x.start),  # 335
            (-x.start, -x.duration, -x.end, x.slack),  # 336
            (-x.start, -x.duration, x.slack, -x.end),  # 337
            (-x.start, -x.end, -x.duration, x.slack),  # 338
            (-x.start, -x.end, x.slack, -x.duration),  # 339
            (-x.start, x.slack, -x.duration, -x.end),  # 340
            (-x.start, x.slack, -x.end, -x.duration),  # 341
            (-x.duration, -x.start, -x.end, x.slack),  # 342
            (-x.duration, -x.start, x.slack, -x.end),  # 343
            (-x.duration, -x.end, -x.start, x.slack),  # 344
            (-x.duration, -x.end, x.slack, -x.start),  # 345
            (-x.duration, x.slack, -x.start, -x.end),  # 346
            (-x.duration, x.slack, -x.end, -x.start),  # 347
            (-x.end, -x.start, -x.duration, x.slack),  # 348
            (-x.end, -x.start, x.slack, -x.duration),  # 349
            (-x.end, -x.duration, -x.start, x.slack),  # 350
            (-x.end, -x.duration, x.slack, -x.start),  # 351
            (-x.end, x.slack, -x.start, -x.duration),  # 352
            (-x.end, x.slack, -x.duration, -x.start),  # 353
            (x.slack, -x.start, -x.duration, -x.end),  # 354
            (x.slack, -x.start, -x.end, -x.duration),  # 355
            (x.slack, -x.duration, -x.start, -x.end),  # 356
            (x.slack, -x.duration, -x.end, -x.start),  # 357
            (x.slack, -x.end, -x.start, -x.duration),  # 358
            (x.slack, -x.end, -x.duration, -x.start),  # 359
            (-x.start, -x.duration, -x.end, -x.slack),  # 360
            (-x.start, -x.duration, -x.slack, -x.end),  # 361
            (-x.start, -x.end, -x.duration, -x.slack),  # 362
            (-x.start, -x.end, -x.slack, -x.duration),  # 363
            (-x.start, -x.slack, -x.duration, -x.end),  # 364
            (-x.start, -x.slack, -x.end, -x.duration),  # 365
            (-x.duration, -x.start, -x.end, -x.slack),  # 366
            (-x.duration, -x.start, -x.slack, -x.end),  # 367
            (-x.duration, -x.end, -x.start, -x.slack),  # 368
            (-x.duration, -x.end, -x.slack, -x.start),  # 369
            (-x.duration, -x.slack, -x.start, -x.end),  # 370
            (-x.duration, -x.slack, -x.end, -x.start),  # 371
            (-x.end, -x.start, -x.duration, -x.slack),  # 372
            (-x.end, -x.start, -x.slack, -x.duration),  # 373
            (-x.end, -x.duration, -x.start, -x.slack),  # 374
            (-x.end, -x.duration, -x.slack, -x.start),  # 375
            (-x.end, -x.slack, -x.start, -x.duration),  # 376
            (-x.end, -x.slack, -x.duration, -x.start),  # 377
            (-x.slack, -x.start, -x.duration, -x.end),  # 378
            (-x.slack, -x.start, -x.end, -x.duration),  # 379
            (-x.slack, -x.duration, -x.start, -x.end),  # 380
            (-x.slack, -x.duration, -x.end, -x.start),  # 381
            (-x.slack, -x.end, -x.start, -x.duration),  # 382
            (-x.slack, -x.end, -x.duration, -x.start),  # 383
        ]

        return ALL_SORTING_COMBINATIONS[sorting_type]

    def sort_tasks(self, sorting_type=16) -> None:
        """function sorts tasks list"""
        self.tasks_list = sorted(self.tasks_list, key=lambda x: Workspace.lambda_function(x, sorting_type))

    def best_sorting__simplified(self):
        """function returning best sorting method for given task list"""
        utilisation_per_sorting = {}

        for sorting_type in range(0, 384):
            self.sort_tasks(sorting_type)
            self.allocate_tasks__simplified()

            utilisation_per_sorting[sorting_type] = self.workforce.workforce_utilization()

        sorted_dict = sorted(utilisation_per_sorting.items(), key=lambda x: x[1])

        return sorted_dict[-1][0]

    def allocate_tasks__simplified(self) -> None:
        """Function uses simplified algorithm to allocate tasks among minimal number of employee
        Complexity of algorithm is O(n)
        Max number of iterations: number_of_tasks *average_slack* number of employees"""

        self.workforce.create_employees_list(1)

        for task in self.tasks_list:
            for employee in self.workforce.employees_list:
                if employee.assign_task(task):
                    break
            else:
                self.workforce.add_employee()
                self.workforce.employees_list[-1].assign_task(task)

    def allocate_tasks__simplified_with_defined_slack(self) -> None:
        """Function uses simplified algorithm to allocate tasks among minimal number of employee
        Complexity of algorithm is O(n)
        Max number of iterations: number_of_tasks * number of employees"""

        self.workforce.create_employees_list(self.minimum_employees_no)

        for task_no, task in enumerate(self.tasks_list):
            for employee in self.workforce.employees_list:
                if employee.assign_task_with_slack(task, self.optimal_slack_combination[task_no]):
                    break

    def allocate_tasks__complete(self, number_of_employees: int, print_text=False):
        """Function uses complete algorithm to allocate tasks among given number of employee,
        iterating through all possible options
        Complexity of algorithm is exponential 2^O(n)
        Max number of iterations: (avg_slack_options^number_of_tasks)*(employee^number_of_tasks)
        Returns True if succeeded, False if it didn't"""

        self.workforce.create_employees_list(number_of_employees)

        number_of_employees = len(self.workforce.employees_list)
        number_of_tasks = len(self.tasks_list)
        slack_list = []

        iteration = 0

        for tasks_index in range(number_of_tasks):
            if self.tasks_list[tasks_index].slack:
                slack_range = range(self.tasks_list[tasks_index].slack)
                slack_list.append(slack_range)
            else:
                slack_list.append([0])

        number_of_slack_options = len(list(itertools.product(*slack_list)))
        number_of_combinations = len(list(itertools.product(range(number_of_employees), repeat=number_of_tasks)))
        max_number_of_iterations = number_of_slack_options * number_of_combinations * number_of_tasks
        if print_text:
            print(
                f'#Combinations:{number_of_combinations}, #slack_options:{number_of_slack_options}, '
                f'#tasks:{number_of_tasks}, #employees:{number_of_employees}')
            print(f'Max iterations: {max_number_of_iterations}')

        for combination_no, combination in enumerate(
                iter(itertools.product(range(number_of_employees), repeat=number_of_tasks))):
            # (E1, E1, E1, E1, E2, E2, E2, E3) -> (1,1,1,1,2,2,2,3)

            self.workforce.reset_employees_tasks_list()

            for slack_combination_no, slack_combination in enumerate(iter(itertools.product(*slack_list))):

                for tasks_index, employee_no in enumerate(combination):
                    iteration += 1

                    employee = self.workforce.employees_list[employee_no]
                    task = self.tasks_list[tasks_index]
                    slack = slack_combination[tasks_index]

                    if employee.assign_task_with_slack(task, slack):
                        if tasks_index == len(combination) - 1:
                            if print_text:
                                print(f'Ultimate solution found after {iteration} iterations')
                            return True
                    else:
                        self.workforce.reset_employees_tasks_list()
                        break
        if print_text:
            print(f'No solutions founds after {iteration} iterations')
        return False

    def check_slacks_for_min_employees(self, print_text=False):
        """Function checks all slacks combination to establish minimum number of employees to allocate tasks and
        best slack combination"""

        number_of_tasks = len(self.tasks_list)
        total_tasks_time = sum([x.duration for x in self.tasks_list])
        min_employees = total_tasks_time // 24

        slack_list = []

        for tasks_index in range(number_of_tasks):
            if self.tasks_list[tasks_index].slack:
                slack_range = range(self.tasks_list[tasks_index].slack)
                slack_list.append(slack_range)
            else:
                slack_list.append([0])

            number_of_slack_options = 1
        for item in slack_list:
            number_of_slack_options *= len(item)

        print(f'#slack_options:{number_of_slack_options}')

        for slack_combination_no, slack_combination in enumerate(iter(itertools.product(*slack_list))):
            if print_text:
                print(f'#{slack_combination_no}, slack combination:{slack_combination}')

            all_tasks_time_slot = [0] * 24

            for task_index, task in enumerate(self.tasks_list):
                start = task.start + slack_combination[task_index]
                end = task.start + slack_combination[task_index] + task.duration

                for index in range(start, end):
                    all_tasks_time_slot[index] = all_tasks_time_slot[index] + 1

            number_of_employees = max(all_tasks_time_slot)

            if self.minimum_employees_no is None:
                self.minimum_employees_no = number_of_employees
                self.optimal_slack_combination = slack_combination

            elif self.minimum_employees_no > number_of_employees:
                self.minimum_employees_no = number_of_employees
                self.optimal_slack_combination = slack_combination

            if min_employees == number_of_employees:
                break

            if print_text:
                print(
                    f'All_tasks:{all_tasks_time_slot}, sum: {sum(all_tasks_time_slot)}, min_employees: {max(all_tasks_time_slot)} task_list_sum: {sum([x.duration for x in self.tasks_list])}')
                print(
                    f'Best employee no:{self.minimum_employees_no}, best slack combination:{self.optimal_slack_combination}')

    def optimize_no_of_employees_simplified_allocation(self, print_text=False):

        number_of_tasks = len(self.tasks_list)
        total_tasks_time = sum([x.duration for x in self.tasks_list])
        min_employees = total_tasks_time // 24

        slack_list = []

        for tasks_index in range(number_of_tasks):
            if self.tasks_list[tasks_index].slack:
                slack_range = range(self.tasks_list[tasks_index].slack)
                slack_list.append(slack_range)
            else:
                slack_list.append([0])

        print(f'{slack_list}')

        slack = 0
        all_tasks_time_slot = [0] * 24

        for task_index, task in enumerate(self.tasks_list):
            start = task.start + slack
            end = task.start + slack + task.duration

            for index in range(start, end):
                all_tasks_time_slot[index] = all_tasks_time_slot[index] + 1

        print(f'All tasks: {all_tasks_time_slot}')

        initial_max = max(all_tasks_time_slot)

        max_employees_time = [index for index, no in enumerate(all_tasks_time_slot) if no == initial_max]
        print(f'max employees times: {max_employees_time}')
        max_employees_tasks = []

        for task_index, task in enumerate(self.tasks_list):
            start = task.start
            end = task.start + task.duration

            for index in max_employees_time:
                if end >= index >= start and task_index not in max_employees_tasks:
                    max_employees_tasks.append(task_index)

        print(f'max employees tasks:{max_employees_tasks}')

        total_duration = 0
        slack_list_filtered = copy.deepcopy(slack_list)

        for task in max_employees_tasks:
            total_duration += self.tasks_list[task].duration
        else:
            slack_list_filtered[task] = [0]

        if total_duration // 24 == max(all_tasks_time_slot):
            return True

        for slack_combination_no, slack_combination in enumerate(iter(itertools.product(*slack_list_filtered))):
            # print(f'#{slack_combination_no}, combination:{slack_combination}')

            all_tasks_time_slot = [0] * 24

            for task_index, task in enumerate(self.tasks_list):
                slack = slack_combination[task_index]
                start = task.start + slack
                end = task.start + slack + task.duration

                for index in range(start, end):
                    all_tasks_time_slot[index] = all_tasks_time_slot[index] + 1
            if max(all_tasks_time_slot) < initial_max:
                print(f'All tasks: {all_tasks_time_slot} vs initial: {initial_max}')
                return True
        return False
        print(total_duration)


class Employee:
    counter = 0

    def __init__(self, tasks_list=[], time_list_size=24) -> None:
        self.id = Employee.counter
        self.time_list = [0 for _ in range(0, time_list_size)]
        Employee.counter += 1
        self.tasks_list = copy.deepcopy(tasks_list)

    def reset_tasks_list(self) -> None:

        self.time_list = [0 for _ in range(0, len(self.time_list))]
        self.tasks_list = []

    def assign_task(self, task):
        assert isinstance(task, Task)

        free_slots = (task.end - task.start) - sum(self.time_list[task.start:task.end])
        if free_slots >= task.duration:
            for slack in range(0, task.slack + 1):
                if sum(self.time_list[task.start + slack: task.start + slack + task.duration]) == 0:
                    self.time_list[task.start + slack: task.start + slack + task.duration] = [1] * task.duration
                    self.tasks_list.append(task.id)
                    return True
        return False

    def assign_task_no_slack(self, task, slack: int):
        assert isinstance(task, Task)

        if sum(self.time_list[task.start + slack: task.start + slack + task.duration]) == 0:
            self.time_list[task.start + slack: task.start + slack + task.duration] = [1] * task.duration
            self.tasks_list.append(task.id)
            return True
        return False

    def assign_task_with_slack(self, task, slack: int):
        assert isinstance(task, Task)

        if sum(self.time_list[task.start + slack: task.start + slack + task.duration]) == 0:
            self.time_list[task.start + slack: task.start + slack + task.duration] = [1] * task.duration
            self.tasks_list.append(task.id)
            return True
        return False


class Workforce:
    def __init__(self, employees_list=[]) -> None:
        self.employees_list = copy.deepcopy(employees_list)

    def create_employees_list(self, number_of_employees) -> None:
        self.employees_list = []
        for employee in range(0, number_of_employees):
            self.employees_list.append(Employee())

    def reset_employees_tasks_list(self) -> None:

        for employee in self.employees_list:
            employee.reset_tasks_list()

    def add_employee(self) -> None:
        self.employees_list.append(Employee())

    def list_employees(self) -> None:
        for employee_no, employee in enumerate(self.employees_list):
            assert isinstance(employee, Employee)
            print(
                f'Employee #{employee_no}, Id:{employee.id}, tasks list:{employee.tasks_list}, '
                f'utilization: {sum(employee.time_list) / len(employee.time_list) * 100:.0f}% time list:{employee.time_list}')

    def workforce_utilization(self):

        total_time_slots = []

        for slot in range(0, 24):
            time_slots = 0
            for employee in self.employees_list:
                time_slots += employee.time_list[slot]
            total_time_slots.append(time_slots)

        utilization = sum([sum(employee.time_list) for employee in self.employees_list]) / len(
            self.employees_list) / 24 * 100

        return utilization


