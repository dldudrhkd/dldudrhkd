word="sex"
word=word.upper()
word_show='_'*len(word)
tynum=0
ok_list=[]
no_list=[]
while True:
    ans=input().upper()
    result= word.find(ans)
    if result ==-1:
        print("오답")
        tynum += 1
    else:
        print("정답")
        ok_list.append(ans)
        for i in range(len(word)):
            if word[i] == ans:
                word_show = word_show[:i] + ans + word_show[i+1]
        print(word_show)
    if tynum ==7 : break
    if word_show.find("_")==-1:break