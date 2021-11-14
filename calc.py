import csv, ctypes as ct

csv.field_size_limit(int(ct.c_ulong(-1).value // 2))
with open("./asr_bengali/utt_spk_text.tsv") as file:
    tsv_file = csv.reader(file, delimiter="\t")
    cnt = 0
    for line in tsv_file:
        cnt = cnt + 1
    print(cnt)
