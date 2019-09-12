from numpy import random as rnd

HANDS = ("グー","チョキ","パー")
WIN_PATTERN = {
    "グー" : "チョキ",
    "チョキ" : "パー",
    "パー" : "グー"
}

def user_select():
    ip = input_int(message=":", min=1, max=3) - 1

    return HANDS[ip]

def random_select():
    tmp_list = list(HANDS)
    rnd.shuffle(tmp_list)

    return(tmp_list[0])

def input_int(message, min, max):
    while True:
        ip_data = input(message)

        if ip_data.isdecimal():
            int_data = int(ip_data)
            if int_data in range(min, max+1):
                return int_data
            else:
                print("数値の範囲が不正です。")

        else:
            print("数値で入力してください。")

def main():
    print("\nじゃんけんをします。対応する数字を入力してください。")
    for num, hand in enumerate(HANDS,start=1):
        print(num, hand)

    janken_num = 10
    win = 0
    for _ in range(janken_num):
        flg = True
        while True:
            if flg:
                message = ("\nじゃんけん・・・","ぽん！")
            else:
                message = ("\nあーいこーで・・・","しょっ！")

            print(message[0])

            user_hand = user_select()
            pc_hand = random_select()

            print(message[1])

            print(f"(あなた){user_hand} : (PC){pc_hand}")

            if WIN_PATTERN[user_hand] == pc_hand:
                win += 1
                print("あなたのかち")
                break

            elif user_hand == pc_hand:
                flg = False

            else:
                print("あなたのまけ")
                break

    print(f"\n{'=' * 20}\n{win}勝{janken_num - win}敗\n")

main()
