import time
from lcd import LCD

lcd = LCD(2,0x27)
time0 = time.time()
f = open("babydaddy.lrc")
ch = f.readlines()


filtered = []
for lign in ch:
    if len(lign) > 9 and lign[0] == "[" and lign[3] == ":" and lign[6] == "." and lign[9] == "]":
        filtered.append(lign[:len(lign)-1])

def format_time(time0):
    total = time.time() - time0
    print(total)
    minutes = int(total // 60)
    seconds = int(total % 60)
    hundredths = int((total - int(total)) * 100)

    return f"[{minutes:02d}:{seconds:02d}.{hundredths:02d}]"

print(filtered)
i=0
while i < len(filtered):
    if format_time(time0) >= filtered[i][:10] :
        lcd.clear()
        current_time = filtered[i][1:9]

        if i < len(filtered) - 1:
            next_time = filtered[i + 1][1:9]

            cur_sec = int(current_time[:2]) * 60 + int(current_time[3:5]) + int(current_time[6:8]) / 100
            next_sec = int(next_time[:2]) * 60 + int(next_time[3:5]) + int(next_time[6:8]) / 100

            display_time = (next_sec - cur_sec) * 0.6
        else:
            display_time = 0
           
           
        lyric = filtered[i][10:]
        if lyric == "":
            i += 1
            continue   
        pages= lcd.message_align(lyric)
        
        print(filtered[i][10:])
        
        page_duration = display_time / len(pages)

        page_start = time.time()
        page_index = 0

        lcd.message(pages[0], 0)

        while page_index < len(pages):

            if time.time() - page_start >= page_duration:

                page_index += 1

                if page_index < len(pages):
                    if page_index%2 == 0:
                        lcd.clear()
                    lcd.message(pages[page_index], page_index % 2)
                    page_start = time.time()

        i = i+1


