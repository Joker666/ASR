class TextTransformBengali:
    """Maps characters to integers and vice versa"""

    def __init__(self):
        char_map_str = """
        ঀ 0
        ঁ 1
        ং 2
        ঃ 3
        অ 4
        আ 5
        ই 6
        ঈ 7
        উ 8
        ঊ 9
        ঋ 10
        ঌ 11
        এ 12
        ঐ 13
        ও 14
        ঔ 15
        ক 16
        খ 17
        গ 18
        ঘ 19
        ঙ 20
        চ 21
        ছ 22
        জ 23
        ঝ 24
        ঞ 25
        ট 26
        ঠ 27
        ড 28
        ঢ 29
        ণ 30
        ত 31
        থ 32
        দ 33
        ধ 34
        ন 35
        প 36
        ফ 37
        ব 38
        ভ 39
        ম 40
        য 41
        র 42
        ল 43
        শ 44
        ষ 45
        স 46
        হ 47
        ় 48
        ঽ 49
        া 50
        ি 51
        ী 52
        ু 53
        ূ 54
        ৃ 55
        ৄ 56
        ে 57
        ৈ 58
        ো 59
        ৌ 60
        ্ 61
        ৎ 62
        ৗ 63
        ড় 64
        ঢ় 65
        য় 66
        ৠ 67
        ০ 68
        ১ 69
        ২ 70
        ৩ 71
        ৪ 72
        ৫ 73
        ৬ 74
        ৭ 75
        ৮ 76
        ৯ 77
        ৱ 78
        ৲ 79
        ৴ 80
        । 81
        - 82
        ’ 83
        : 84
        , 85
        . 86
        ? 87
        ! 88
        ( 89
        ) 90
        ; 91
        ʼ 92
        ‘ 93
        a 94
        b 95
        c 96
        d 97
        e 98
        f 99
        g 100
        h 101
        i 102
        j 103
        k 104
        l 105
        m 106
        n 107
        o 108
        p 109
        q 110
        r 111
        s 112
        t 113
        u 114
        v 115
        w 116
        x 117
        y 118
        z 119
        1 120
        2 121
        3 122
        4 123
        5 124
        6 125
        7 126
        8 127
        9 128
        ' 129
        0 130
        <SPACE> 131
        """
        self.char_map = {}
        self.index_map = {}
        for line in char_map_str.strip().split('\n'):
            ch, index = line.split()
            self.char_map[ch] = int(index)
            self.index_map[int(index)] = ch
        self.index_map[131] = ' '

    def text_to_int(self, text):
        """ Use a character map and convert text to an integer sequence """
        int_sequence = []
        for c in text:
            ch = -1
            if c == ' ':
                ch = self.char_map['<SPACE>']
            else:
                if self.char_map.get(c) is not None:
                    ch = self.char_map[c]
            if ch > -1:
                int_sequence.append(ch)
        return int_sequence

    def int_to_text(self, labels):
        """ Use a character map and convert integer labels to an text sequence """
        string = []
        for i in labels:
            string.append(self.index_map[i])
        return ''.join(string).replace('<SPACE>', ' ')
